import hashlib
import random

from flask import redirect, url_for, render_template, flash, request

from app import db
from app.models import Link, Page
from app.parser import bp
from app.parser.forms import StartParserForm
from app.parser.funcs import Funcs
from app.parser.dbase import ParserDB
from flask_login import current_user


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    links = Link.query.order_by(Link.created_at.desc()).paginate(page=page, per_page=10)
    next_link = url_for('parser.index', page=links.next_num) if links.has_next else None
    prev_link = url_for('parser.index', page=links.prev_num) if links.has_prev else None
    return render_template('parser/index.html', title='Список страниц', links=links.items, next_link=next_link, prev_link=prev_link)


@bp.route('/<int:page_id>')
def view(page_id):
    page_data = Page.query.get_or_404(page_id)
    return render_template('parser/view.html', title=page_data.title, page=page_data)


@bp.route('/edit/<int:link_id>', methods=['GET', 'POST'])
def edit(link_id):
    return render_template('parser/edit.html', title='Редактирование страницы')


@bp.route('/start', methods=['GET', 'POST'])
def start():
    form = StartParserForm()
    dbase = ParserDB()
    if form.validate_on_submit():
        if form.count.data>100:
            flash("Ссылка не должна быть более 100")
            return redirect(url_for("parser.start"))
        funcs = Funcs(form.start_link.data)
        iters_val = int(form.count.data)
        try:
            first_link = funcs.send_request()
        except ValueError:
            flash("Ошибка сервера")
            return redirect(url_for("parser.start"))
        else:

            links = funcs.start_kr()
            while iters_val != 0:
                ran = random.randint(0, len(links)-1)
                link_href = links[ran].attrs['href']
                link_md5h = hashlib.md5(link_href.encode('utf-8')).hexdigest()
                link_title = funcs.read_page(link_href)[0]
                if not dbase.search_link_by_hash(link_md5h):
                    lnk = Link(title=link_title, path=link_href, md5h=link_md5h)
                    lnk = Link(title=link_title, path=link_href, md5h=link_md5h, author=current_user)
                    db.session.add(lnk)
                    db.session.commit()
                    iters_val -= 1
                    links = funcs.start_kr(url_path=link_href)
                    continue
                else:

                    links = funcs.start_kr(url_path=link_href)
            flash("Успешно")
            return redirect(url_for("parser.index"))
    return render_template("parser/start.html", title="Запуск парсера", form=form)

@bp.route("/read_page/<int:link_id>")
def read_page(link_id):
    lnk = Link.query.get_or_404(link_id)
    try:
        funcs = Funcs()
        page_data = funcs.read_page(lnk.path)
        pg = Page(title=page_data[0], body=page_data[1], link_id=link_id)
    except:
        flash('Error')
    else:
        lnk.mark_parsed()
        db.session.add(pg)
        db.session.add(lnk)
        db.session.commit()
        flash('Ok')
    finally:
        return redirect(url_for('parser.index'))

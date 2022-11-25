from flask import render_template, redirect, url_for, flash, request
from app.news import bp
from app.news.forms import NewsCreateForm
from flask_login import current_user
from app.models import News
from app import db


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    news = News.query.order_by(News.timestamp.desc()).paginate(page=page, per_page=5)
    next_link = url_for('news.index', page=news.next_num) if news.has_next else None
    prev_link = url_for('news.index', page=news.prev_num) if news.has_prev else None
    return render_template('news/index.html', title='Новости', news=news.items,
                           next_link=next_link, prev_link=prev_link)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = NewsCreateForm()
    if form.validate_on_submit():
        post = News(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваша запись успешно создана!')
        return redirect(url_for('news.index'))
    return render_template('news/create.html', title='Создание записи', form=form)


@bp.route('/<int:id>')
def article(id):
    art = News.query.get(int(id))
    return render_template('news/article.html', title=art.title, art=art)

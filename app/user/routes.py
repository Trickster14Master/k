from flask import render_template, url_for, request
from app.user import bp

from app.models import User


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=5)
    next_link = url_for('news.index', page=users.next_num) if users.has_next else None
    prev_link = url_for('news.index', page=users.prev_num) if users.has_prev else None
    return render_template('user/index.html', title='Пользователи', users=users.items,
                           next_link=next_link, prev_link=prev_link)

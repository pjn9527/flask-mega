from flask import render_template
from app import db
from app.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    try:
        db.session.rollback()
    except InvalidRequestError:
        # 如果 session 已在 committed 状态，先清理旧 session
        db.session.remove()
    return render_template('errors/500.html'), 500
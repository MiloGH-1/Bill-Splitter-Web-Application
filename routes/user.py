from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register')
def register():
    return render_template('registrationpage.html')

@user_bp.route('/test')
def test():
    return render_template('dashboard.html')
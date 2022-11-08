try:
    from flask import Blueprint, render_template, redirect, url_for
    from flask import request
    from flask_login import login_required, current_user
except Exception as e:
    print(" Some pacakages are missing: {}".format(e))

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',current_user = current_user.__name)


if __name__ == '__main__':
    main.run(debug=True,host='0.0.0.0')

# Survey flask server file
from server import APP, LOGIN_MANAGER
from modules.head import *
from modules.LoginForm import LoginForm
from modules.Authenticate import Authenticate, UserClass, RestoreUser

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    return RestoreUser(user_id)

@APP.route('/', methods=['GET', 'POST'])
def survey_homepage():
    """ The function to render the homepage
    """
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        Authenticate(form.username.data, form.password.data)
        if current_user.get_role() == "student":
            return(redirect(url_for('student_homepage')))
        elif current_user.get_role() == "staff":
            return(redirect(url_for('staff_homepage')))

    return render_template('index.html', form=form)

@APP.route('/student')
@login_required
def student_homepage():
    if current_user.get_role() == "student":
        return render_template('student.html')
    else:
        return "gtfo, u aint cool like a student"

@APP.route('/staff')
@login_required
def staff_homepage():
    if current_user.get_role() == "staff":
        return render_template('staff.html')
    else:
        return "gtfo"

@APP.route('/logout')
@login_required
def logout():
    logout_user()
    return(redirect(url_for('survey_homepage')))
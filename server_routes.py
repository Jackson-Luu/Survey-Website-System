# Survey flask server file
from server import APP
from modules.head import *
from modules.LoginForm import LoginForm
from modules.CheckLogin import CheckCreds

@APP.route('/', methods=['GET', 'POST'])
def survey_homepage():
    """ The function to render the homepage
    """
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        role = CheckCreds(form.username.data, form.password.data)

    return render_template('index.html', form=form)

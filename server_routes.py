# Survey flask server file
from server import APP, LOGIN_MANAGER
from flask import session
from modules.head import *
from modules.LoginForm import LoginForm
from modules.Authenticate import Authenticate, RestoreUser
from modules.DatabaseManager import DBManager
from modules.QuestionsManager import ModifyForm, QuestionForm, read_questions, create_question
from modules.DataPacket import DataPacket

DBMANAGER_QU = DBManager('questions')
DBMANAGER_SU = DBManager('surveys')

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    return RestoreUser(user_id)

@APP.route('/', methods=['GET', 'POST'])
def survey_homepage():
    """ The function to render the homepage
    """
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        if Authenticate(form.username.data, form.password.data):
            if current_user.get_role() == 'student':
                return redirect(url_for('student_homepage'))
            elif current_user.get_role() == 'staff':
                return redirect(url_for('staff_homepage'))

    return render_template('index.html', form=form)

@APP.route('/student')
@login_required
def student_homepage():
    if current_user.get_role() == 'student':
        return render_template('student.html')
    else:
        return 'gtfo, u aint cool like a student'

@APP.route('/staff')
@login_required
def staff_homepage():
    if current_user.get_role() == 'staff':
        return render_template('staff.html')
    else:
        return 'gtfo'

@APP.route('/staff/questions', methods=['GET', 'POST'])
@login_required
def staff_questions():
    """ This function will run when the user goes to the url above """
    if current_user.get_role() == 'staff':
        form = QuestionForm(request.form)
        form_mod = ModifyForm(request.form)

        # Load up packet to read the information.
        # This should be after the form data but because we are being lazy with the
        # data id, we need to load it first.
        read_packet = DataPacket('1219', ['ID', 'TEXT', 'TYPE'])
        read_packet = DBMANAGER_QU.retrieve_data(read_packet)

        if form.add.data and form.validate():
            # If the form is needed to add data, use it to add data
            # Load up the packet and set it to store the data
            add_packet = DataPacket('1219', ['ID', 'TEXT', 'TYPE'])
            add_packet = create_question(add_packet, len(read_packet.retrieve_data()),
                                         form.question.data, form.questiontype.data)
            DBMANAGER_QU.add_data(add_packet)
            return redirect(url_for('staff_questions'))

        if form_mod.mod.data and form_mod.validate():
            # Here, we should modify the questions but this is extremely low
            # priority, do it later I guess.
            return redirect(url_for('staff_questions'))

        questions = read_questions(read_packet)

        return render_template('dashboard/dash-questions.html',
                               questions=questions, form=form, form_mod=form_mod)
    else:
        return 'gtfo'

@APP.route('/staff/questions/ajax-delete-questions', methods=['GET', 'POST'])
@login_required
def delete_question():
    """ Delete the questions """
    delete_packet = DataPacket('1219', ['ID'])

    # From the javascript an Ajax call will be made
    for questionids in request.json['questionids']:
        delete_packet.add_data(questionids)

    DBMANAGER_QU.remove_data(delete_packet)

    return redirect(url_for('staff_questions'))

@APP.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('survey_homepage'))

@APP.route('/staff/survey', methods=['GET', 'POST'])
@login_required
def staff_survey():
    return render_template('dashboard/dash-surveys.html')

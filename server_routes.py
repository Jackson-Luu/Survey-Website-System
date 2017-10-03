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

        add_packet = DataPacket('1219', ['ID', 'TEXT', 'TYPE'])
        read_packet = DataPacket('1219', ['ID', 'TEXT', 'TYPE'])
        read_packet = DBMANAGER_QU.retrieve_data(read_packet)

        if form.add.data and form.validate():
            add_packet = create_question(add_packet, DBMANAGER_QU.last_id(read_packet),
                                         form.question.data, form.questiontype.data)
            DBMANAGER_QU.add_data(add_packet)
            return redirect(url_for('staff_questions'))

        if form_mod.mod.data and form_mod.validate():
            add_packet = create_question(add_packet, form_mod.questionid.data,
                                         form_mod.modquestion.data, form_mod.modquestiontype.data)
            DBMANAGER_QU.modify_data(add_packet)
            return redirect(url_for('staff_questions'))

        questions = read_questions(read_packet)

        return render_template('dashboard/dash-questions.html',
                               questions=questions, form=form, form_mod=form_mod)
    else:
        return 'gtfo'

@APP.route('/staff/questions/ajax-delete-questions', methods=['GET', 'POST'])
@login_required
def delete_question():
    delete_packet = DataPacket('1219', ['ID'])

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
    render_template('dashboard/dash-surveys.html')

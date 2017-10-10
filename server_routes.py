# Survey flask server file
from server import APP, LOGIN_MANAGER
from flask import session
from modules.head import *
from modules.LoginForm import LoginForm
from modules.Authenticate import Authenticate, RestoreUser
from modules.DatabaseManager import DBManager
from modules.QuestionsManager import ModifyForm, QuestionForm, read_questions, create_question
from modules.DataPacket import DataPacket
from modules.SurveyManager import AddSurveyForm, create_survey, read_surveys

DBMANAGER = DBManager('user_information')
question_list = []

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
            elif current_user.get_role() == 'admin':
                return redirect(url_for('admin_homepage'))
            elif current_user.get_role() == 'staff':
                return redirect(url_for('staff_homepage'))

    return render_template('index.html', form=form)

@APP.route('/student')
@login_required
def student_homepage():
    
    """ This function will run when the user goes to the url above """
    if current_user.get_role() == 'student':
    
       
        #surveys = read_surveys(data_packet)    
        return render_template('student/dash-nav-student.html')
    else:
        return 'gtfo, u aint cool like a student'

@APP.route('/admin')
@login_required
def admin_homepage():
    if current_user.get_role() == 'admin':
        return render_template('admin.html')
    else:
        return 'gtfo'
        
@APP.route('/staff')
@login_required
def staff_homepage():
    if current_user.get_role() == 'staff':
        return render_template('staff.html')
    else:
        return 'gtfo, u aint cool like a staff'

@APP.route('/admin/questions', methods=['GET', 'POST'])
@login_required
def admin_questions():
    """ This function will run when the user goes to the url above """
    if current_user.get_role() == 'admin':
        form = QuestionForm(request.form)
        form_mod = ModifyForm(request.form)

        read_packet = DataPacket(current_user.get_id(), ['ID', 'TEXT', 'TYPE'], "_questions")
        read_packet = DBMANAGER.retrieve_data(read_packet)

        if form.add.data and form.validate():
            # If the form is needed to add data, use it to add data
            # Load up the packet and set it to store the data
            add_packet = DataPacket(current_user.get_id(), ['ID', 'TEXT', 'TYPE'], "_questions")
            add_packet = create_question(add_packet, DBMANAGER.last_id(read_packet),
                                         form.question.data, form.questiontype.data)
            DBMANAGER.add_data(add_packet)
            return redirect(url_for('admin_questions'))

        if form_mod.mod.data and form_mod.validate():
            add_packet = create_question(add_packet, form_mod.questionid.data,
                                         form_mod.modquestion.data, form_mod.modquestiontype.data)
            DBMANAGER.modify_data(add_packet)
            return redirect(url_for('admin_questions'))

        questions = read_questions(read_packet)

        return render_template('admin/dash-questions.html',
                               questions=questions, form=form, form_mod=form_mod)
    else:
        return 'gtfo'

@APP.route('/admin/survey', methods=['GET', 'POST'])
@login_required
def admin_survey():
    survey_form = AddSurveyForm(request.form)

    survey_packet = DataPacket(current_user.get_id(), ['ID', 'COURSE', 'QUESTIONS', 'STATE'], '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)
    surveys = read_surveys(survey_packet)

    if survey_form.survey_submit.data and survey_form.validate():
        add_packet = DataPacket(current_user.get_id(), ['ID', 'COURSE', 'QUESTIONS', 'STATE'], "_survey")
        add_packet = create_survey(add_packet, DBMANAGER.last_id(survey_packet), survey_form.survey_courses.data, question_list, "Review")
        DBMANAGER.add_data(add_packet)
        question_list.clear()
        return redirect(url_for('admin_survey'))

    # Display Question Pool
    read_packet = DataPacket(current_user.get_id(), ['ID', 'TEXT', 'TYPE', 'STATE'], "_questions")
    read_packet = DBMANAGER.retrieve_data(read_packet)
    questions = read_questions(read_packet)

    return render_template('admin/dash-surveys.html', survey_form=survey_form, questions=questions, surveys=surveys)

@APP.route('/admin/survey/ajax-delete-questions', methods=['GET', 'POST'])
@login_required
def add_survey():
    for questionids in request.json['questionids']:
        question_list.append(questionids)

@APP.route('/admin/questions/ajax-delete-questions', methods=['GET', 'POST'])
@login_required
def delete_question():
    """ Delete the questions """
    delete_packet = DataPacket(current_user.get_id(), ['ID'], "_questions")

    # From the javascript an Ajax call will be made
    for questionids in request.json['questionids']:
        delete_packet.add_data(questionids)

    DBMANAGER.remove_data(delete_packet)

    return redirect(url_for('admin_questions'))

@APP.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('survey_homepage'))
    
@APP.route('/staff/survey', methods=['GET', 'POST'])
@login_required
def staff_survey():
    survey_form = AddSurveyForm(request.form)

    if survey_form.survey_submit.data and survey_form.validate():
        s_name = survey_form.survey_name.data
        s_course = survey_form.survey_courses.data

        add_packet = DataPacket(current_user.get_id(), ['ID', 'NAME', 'COURSE', 'STATE'], '_survey')
        add_packet.add_data([DBMANAGER.last_id(add_packet), s_name, s_course])

        DBMANAGER.add_data(add_packet)
        return redirect(url_for('staff_survey'))

    survey_packet = DataPacket(current_user.get_id(), ['ID', 'NAME', 'COURSE', 'STATE'], '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)

    return render_template('staff/dash-surveys-staff.html', survey_form=survey_form)


@APP.route('/admin/survey/<id>', methods=['GET', 'POST'])
@login_required
def staff_mod_survey(id):
    survey_packet = DataPacket(current_user.get_id(), ['ID', 'NAME', 'COURSE', 'STATE'], '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)

    question_packet = DataPacket(current_user.get_id(), ['ID', 'TEXT', 'TYPE', 'STATE'], "_questions")
    question_packet = DBMANAGER.retrieve_data(question_packet)

    survey = ["", "", ""]

    for d in survey_packet.retrieve_data():
        if d[0] == id:
            survey[0] = d[1]
            survey[1] = d[2]
            break

    return render_template('admin/dash-survey-modify.html',
                           survey=survey, questions=question_packet.retrieve_data())
@APP.route('/staff/questions', methods=['GET', 'POST'])
@login_required
def staff_questions():
    """ This function will run when the user goes to the url above """
    if current_user.get_role() == 'staff':
        form = QuestionForm(request.form)
        form_mod = ModifyForm(request.form)

        read_packet = DataPacket(current_user.get_id(), ['ID', 'TEXT', 'TYPE'], "_questions")
        read_packet = DBMANAGER.retrieve_data(read_packet)

        if form.add.data and form.validate():
            # If the form is needed to add data, use it to add data
            # Load up the packet and set it to store the data
            add_packet = DataPacket(current_user.get_id(), ['ID', 'TEXT', 'TYPE'], "_questions")
            add_packet = create_question(add_packet, DBMANAGER.last_id(read_packet),
                                         form.question.data, form.questiontype.data)
            DBMANAGER.add_data(add_packet)
            return redirect(url_for('staff_questions'))

        if form_mod.mod.data and form_mod.validate():
            add_packet = create_question(add_packet, form_mod.questionid.data,
                                         form_mod.modquestion.data, form_mod.modquestiontype.data)
            DBMANAGER.modify_data(add_packet)
            return redirect(url_for('staff_questions'))

        questions = read_questions(read_packet)

        return render_template('staff/dash-questions-staff.html',
                               questions=questions, form=form, form_mod=form_mod)
    else:
        return 'gtfo'

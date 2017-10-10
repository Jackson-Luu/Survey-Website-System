# Survey flask server file
from server import APP, LOGIN_MANAGER
from flask import session
from modules.head import *
from modules.LoginForm import LoginForm
from modules.Authenticate import Authenticate, RestoreUser
from modules.DatabaseManager import DBManager
from modules.QuestionsManager import ModifyForm, QuestionForm, read_questions, create_question
from modules.DataPacket import DataPacket
from modules.SurveyManager import create_survey, read_surveys, get_course_list

DBMANAGER = DBManager('user_information')
SURVEY_COL_IDS = ['ID', 'COURSE', 'QUESTION_LIST', 'STATE']
QUESTION_COL_IDS = ['ID', 'TEXT', 'TYPE', 'STATE']
METRICS_COL_IDS = ['ID', 'SURVEY_ID', 'QUESTION', 'ANSWER']

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
        return render_template('unauth.html')

@APP.route('/admin')
@login_required
def admin_homepage():
    if current_user.get_role() == 'admin':
        return render_template('admin.html')
    else:
        return render_template('unauth.html')
        
@APP.route('/staff')
@login_required
def staff_homepage():
    if current_user.get_role() == 'staff':
        return render_template('staff.html')
    else:
        return render_template('unauth.html')

@APP.route('/admin/questions', methods=['GET', 'POST'])
@login_required
def admin_questions():
    """ This function will run when the user goes to the url above """
    if current_user.get_role() == 'admin':
        form = QuestionForm(request.form)
        form_mod = ModifyForm(request.form)

        read_packet = DataPacket(current_user.get_id(), QUESTION_COL_IDS, "_questions")
        read_packet = DBMANAGER.retrieve_data(read_packet)

        if form.add.data and form.validate():
            # If the form is needed to add data, use it to add data
            # Load up the packet and set it to store the data
            add_packet = DataPacket(current_user.get_id(), QUESTION_COL_IDS, "_questions")
            add_packet = create_question(add_packet, DBMANAGER.last_id(read_packet),
                                         form.question.data, form.questiontype.data, current_user.get_role())
            DBMANAGER.add_data(add_packet)
            return redirect(url_for('admin_questions'))

        if form_mod.mod.data and form_mod.validate():
            add_packet = create_question(add_packet, form_mod.questionid.data,
                                         form_mod.modquestion.data, form_mod.modquestiontype.data, current_user.get_role())
            DBMANAGER.modify_data(add_packet)
            return redirect(url_for('admin_questions'))

        questions = read_questions(read_packet)

        return render_template('admin/dash-questions.html',
                               questions=questions, form=form, form_mod=form_mod)
    else:
        return render_template('unauth.html')

@APP.route('/admin/survey', methods=['GET', 'POST'])
@login_required
def admin_survey():
    # Display Survey Pool
    survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)
    surveys = read_surveys(survey_packet)

    course_list = get_course_list()

    return render_template('admin/dash-surveys.html', surveys=surveys, course_list=course_list)

@APP.route('/admin/survey/<id>', methods=['GET', 'POST'])
@login_required
def admin_mod_survey(id):
    survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)

    question_packet = DataPacket(current_user.get_id(), ['ID', 'TEXT', 'TYPE', 'STATE'], "_questions")
    question_packet = DBMANAGER.retrieve_data(question_packet)

    questions = read_questions(question_packet)

    survey = ["", "", ""]

    for d in survey_packet.retrieve_data():
        if d[0] == id:
            survey[0] = d[0]
            survey[1] = d[1]
            break

    return render_template('admin/dash-survey-modify.html',
                           survey=survey, questions=questions)

@APP.route('/admin/survey/add-survey', methods=['GET', 'POST'])
@login_required
def add_survey():
    if request.method == "POST":
        survey_course = request.json["survey-course"]

        add_survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
        add_survey_packet = create_survey(add_survey_packet,
                                        DBMANAGER.last_id(add_survey_packet),
                                        survey_course,
                                        "",
                                        "Review")

        DBMANAGER.add_data(add_survey_packet)

    return "AJAX-PAGE"

@APP.route('/admin/survey/ajax-update-survey', methods=['GET', 'POST'])
@login_required
def mod_survey():
    if request.method == "POST":
        survey_id = request.json["survey_id"]
        survey_course = request.json["survey_course"]
        questions = request.json["question_ids"]

        mod_survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
        mod_survey_packet = create_survey(mod_survey_packet,
                                        survey_id,
                                        survey_course,
                                        questions,
                                        "Review")

        DBMANAGER.modify_data(mod_survey_packet)

    return "AJAX-PAGE"

@APP.route('/admin/questions/ajax-delete-questions', methods=['GET', 'POST'])
@login_required
def delete_question():
    """ Delete the questions """
    if request.method == "POST":
        delete_packet = DataPacket(current_user.get_id(), ['ID'], "_questions")

        # From the javascript an Ajax call will be made
        for questionids in request.json['questionids']:
            delete_packet.add_data(questionids)

        DBMANAGER.remove_data(delete_packet)

    return "AJAX-PAGE"

@APP.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('survey_homepage'))
    
@APP.route('/staff/survey', methods=['GET', 'POST'])
@login_required
def staff_survey():
    survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)

    return render_template('staff/dash-surveys-staff.html')

@APP.route('/staff/questions', methods=['GET', 'POST'])
@login_required
def staff_questions():
    """ This function will run when the user goes to the url above """
    if current_user.get_role() == 'staff':
        form = QuestionForm(request.form)
        form_mod = ModifyForm(request.form)

        read_packet = DataPacket(current_user.get_id(), QUESTION_COL_IDS, "_questions")
        read_packet = DBMANAGER.retrieve_data(read_packet)

        if form.add.data and form.validate():
            # If the form is needed to add data, use it to add data
            # Load up the packet and set it to store the data
            add_packet = DataPacket(current_user.get_id(), QUESTION_COL_IDS, "_questions")
            add_packet = create_question(add_packet, DBMANAGER.last_id(read_packet),
                                         form.question.data,
                                         form.questiontype.data,
                                         current_user.get_role())
            DBMANAGER.add_data(add_packet)
            return redirect(url_for('staff_questions'))

        if form_mod.mod.data and form_mod.validate():
            add_packet = create_question(add_packet, form_mod.questionid.data,
                                         form_mod.modquestion.data,
                                         form_mod.modquestiontype.data,
                                         current_user.get_role())
            DBMANAGER.modify_data(add_packet)
            return redirect(url_for('staff_questions'))

        questions = read_questions(read_packet)

        return render_template('staff/dash-questions-staff.html',
                               questions=questions, form=form, form_mod=form_mod)
    else:
        return render_template('unauth.html')

@APP.route('/1210-JSP/survey-id=<id>')
def show_survey(id):
    question_packet = DataPacket(current_user.get_id(), QUESTION_COL_IDS, "_questions")
    question_packet = DBMANAGER.retrieve_data(question_packet)

    survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)

    # Loop through the packet and find the right survey
    survey_info = ["", "", ""]
    for survey in survey_packet.retrieve_data():
        if survey[0] == id:
            survey_info = survey
            break
    
    question_ids = survey_info[2].split(',')
    display_info = []

    for question in question_packet.retrieve_data():
        for qid in question_ids:
            if qid == question[0]:
                display_info.append(question)

    return render_template('student/dash-student-survey.html', survey_id=id, display=display_info)

@APP.route('/1210-JSP/submit-survey', methods=['GET', 'POST'])
def submit_survey():
    if request.method == 'POST':
        answers = request.json['survey-answers']
        survey_id = request.json['survey-id']

        read_packet = DataPacket(current_user.get_id(), METRICS_COL_IDS, '_metrics')
        read_packet = DBMANAGER.retrieve_data(read_packet)

        metrics_packet = DataPacket(current_user.get_id(), METRICS_COL_IDS, '_metrics')

        unique_id = DBMANAGER.last_id(metrics_packet)
        for answer in answers:
            metrics_packet.add_data([unique_id,
                                     survey_id,
                                     answer[0],
                                     answer[1]])
            unique_id += 1
        DBMANAGER.add_data(metrics_packet)
    return "AJAX"

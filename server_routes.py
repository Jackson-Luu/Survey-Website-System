# Survey flask server file
from server import APP, LOGIN_MANAGER
from flask import session
from modules.head import *
from modules.LoginForm import LoginForm
from modules.Authenticate import Authenticate, RestoreUser
from modules.QuestionsManager import ModifyForm, QuestionForm, read_questions, create_question
from modules.SurveyManager import create_survey, read_surveys, get_course_list

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """ This function is called when you load the user """
    return RestoreUser(user_id)

@APP.route('/', methods=['GET', 'POST'])
def survey_homepage():
    """ The function to render the homepage
    """

    # If the user is already logged in, redirect as appropriate
    if "get_role" in dir(current_user):
        if current_user.get_role() == 'student':
            return redirect(url_for('student_homepage'))
        elif current_user.get_role() == 'admin':
            return redirect(url_for('admin_homepage'))
        elif current_user.get_role() == 'staff':
            return redirect(url_for('staff_homepage'))

    # If not, show the log in page
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
    """ Show the student homepage. Display available surveys. """
    if current_user.get_role() == 'student':
        survey_packet = DataPacket("admin", SURVEY_COL_IDS, '_survey')
        survey_packet = DBMANAGER.retrieve_data(survey_packet)
        
        courses = []
        results = []
        user_entry = DBMANAGER.find('*', "enrolments", "ID", int(current_user.get_id()))
        for entry in user_entry:
            if entry[2] != "YES":
                courses.append([entry[1]])
            results.append([entry[1]])
        surveys = read_surveys(survey_packet, False, courses)
        r_surveys = read_surveys(survey_packet, False, results)
        return render_template('student/dash-nav-student.html', surveys=surveys, results=r_surveys)
    else:
        return render_template('unauth.html')

@APP.route('/admin')
@login_required
def admin_homepage():
    """ Show the administrator home page """
    if current_user.get_role() == 'admin':
        return render_template('admin.html')
    else:
        return render_template('unauth.html')

@APP.route('/staff')
@login_required
def staff_homepage():
    """ Show the staff home page. Display available surveys."""
    if current_user.get_role() == 'staff':
        survey_packet = DataPacket("admin", SURVEY_COL_IDS, '_survey')
        survey_packet = DBMANAGER.retrieve_data(survey_packet)

        return render_template('staff.html', surveys=survey_packet.retrieve_data())
    else:
        return render_template('unauth.html')

@APP.route('/staff/survey/<id>', methods=["GET", "POST"])
@login_required
def staff_show_survey(id):
    """ Display selected survey for staff user to review.""" 
    question_packet = DataPacket("admin", QUESTION_COL_IDS, "_questions")
    question_packet = DBMANAGER.retrieve_data(question_packet)

    survey_packet = DataPacket("admin", SURVEY_COL_IDS, '_survey')
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

    if request.method == 'POST':
        if request.form['btn'] == 'approve':
            mod_survey_packet = DataPacket("admin", SURVEY_COL_IDS, '_survey')
            mod_survey_packet = create_survey(mod_survey_packet,
                                        survey[0],
                                        survey[1],
                                        survey[2],
                                        "Open")

            DBMANAGER.modify_data(mod_survey_packet, True)

            return redirect(url_for('staff_homepage'))

    return render_template('staff/dash-staff-survey.html', survey_id=id, display=display_info, survey_state=survey[3])

@APP.route('/staff/questions/ajax-add-questions', methods=['GET', 'POST'])
@login_required
def staff_add_question():
    """ Delete the questions """
    if request.method == "POST":
        question = request.json["question"]
        question_type = request.json["question_type"]

        add_packet = DataPacket("admin", QUESTION_COL_IDS, "_questions")
        add_packet.add_data([DBMANAGER.last_id(add_packet), question, question_type, "Optional"])

        DBMANAGER.add_data(add_packet)

    return "AJAX-PAGE"

@APP.route('/admin/questions', methods=['GET', 'POST'])
@login_required
def admin_questions():
    """ Displays the question pool to admin users. Allows them to add/modify/delete a question."""
    if current_user.get_role() == 'admin':
        form = QuestionForm(request.form)
        form_mod = ModifyForm(request.form)

        read_packet = DataPacket(current_user.get_id(), QUESTION_COL_IDS, "_questions")
        read_packet = DBMANAGER.retrieve_data(read_packet)

        if form.add.data and form.validate():
            # If the form is needed to add data, use it to add data
            # Load up the packet and set it to store the data
            add_packet = DataPacket(current_user.get_id(), QUESTION_COL_IDS, "_questions")
            add_packet = create_question(add_packet,
                                         DBMANAGER.last_id(read_packet),
                                         form.question.data,
                                         form.questiontype.data,
                                         form.questionstate.data)
            DBMANAGER.add_data(add_packet)
            return redirect(url_for('admin_questions'))

        if form_mod.mod.data and form_mod.validate():
            add_packet = create_question(add_packet,
                                         form_mod.questionid.data,
                                         form_mod.modquestion.data,
                                         form_mod.modquestiontype.data,
                                         form.mod.modquestionstate.data)
            DBMANAGER.modify_data(add_packet, True)
            return redirect(url_for('admin_questions'))

        questions = read_questions(read_packet)

        return render_template('admin/dash-questions.html',
                               questions=questions, form=form, form_mod=form_mod)
    else:
        return render_template('unauth.html')

@APP.route('/admin/survey', methods=['GET', 'POST'])
@login_required
def admin_survey():
    """ Show the survey management page to the admin """
    # Display Survey Pool
    survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)
    surveys = read_surveys(survey_packet, True, None)

    course_list = get_course_list()

    return render_template('admin/dash-surveys.html', surveys=surveys, course_list=course_list)

@APP.route('/admin/survey/ajax-close-survey', methods=['GET', 'POST'])
@login_required
def close_survey():
    """ Close a survey """
    if request.method == "POST":
        # From the javascript an Ajax call will be made
        survey_id = request.json['survey-id']
        
        survey = DBMANAGER.find('*', current_user.get_id() + '_survey', "ID", survey_id)

        survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
        survey_packet = create_survey(survey_packet, survey[0][0], survey[0][1], survey[0][2], "Closed")

        DBMANAGER.modify_data(survey_packet, True)
    return "AJAX-PAGE"

@APP.route('/admin/survey/<survey_id>', methods=['GET', 'POST'])
@login_required
def admin_mod_survey(survey_id):
    """ This URL will show the survey based on the id given to the URL """
    survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)

    question_packet = DataPacket(current_user.get_id(), QUESTION_COL_IDS, "_questions")
    question_packet = DBMANAGER.retrieve_data(question_packet)

    questions = read_questions(question_packet)

    survey = ["", "", ""]

    for d in survey_packet.retrieve_data():
        if d[0] == survey_id:
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
        #todo: remove metrics when survey is updated

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

        DBMANAGER.modify_data(mod_survey_packet, True)

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

@APP.route('/staff/questions', methods=['GET', 'POST'])
@login_required
def staff_questions():
    """ Displays the optional question pool to staff. """
    if current_user.get_role() == 'staff':
        read_packet = DataPacket("admin", QUESTION_COL_IDS, "_questions")
        read_packet = DBMANAGER.retrieve_data(read_packet)

        return render_template('staff/dash-questions-staff.html',
                               questions=read_packet.retrieve_data())
    else:
        return render_template('unauth.html')

@APP.route('/1210-JSP/survey-id=<id>', methods=['GET', 'POST'])
@login_required
def show_survey(id):
    """ Displays the survey form to students. """
    question_packet = DataPacket("admin", QUESTION_COL_IDS, "_questions")
    question_packet = DBMANAGER.retrieve_data(question_packet)

    survey_packet = DataPacket("admin", SURVEY_COL_IDS, '_survey')
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

    if request.method == 'POST':
        return redirect(url_for('student_homepage'))

    return render_template('student/dash-student-survey.html', survey_id=id, survey_course=survey_info[1], display=display_info)

@APP.route('/1210-JSP/submit-survey', methods=['GET', 'POST'])
@login_required
def submit_survey():
    """ This function runs upon a user submitting a survey. Updates database
        with survey responses. """
    if request.method == 'POST':
        answers = request.json['survey-answers']
        survey_course = request.json['survey-course']

        read_packet = DataPacket(survey_course, METRICS_COL_IDS, '_metrics')
        read_packet = DBMANAGER.retrieve_data(read_packet)

        metrics_packet = DataPacket(survey_course, METRICS_COL_IDS, '_metrics')

        unique_id = DBMANAGER.last_id(metrics_packet)
        for answer in answers:
            print(answer)
            metrics_packet.add_data([unique_id,
                                     answer[0],
                                     answer[2],
                                     answer[1]])
            unique_id += 1
        DBMANAGER.add_data(metrics_packet)

        #enrol_packet = DataPacket('enrolments', ENROL_COL_IDS)
        #enrol_packet.add_data([current_user.get_id(), survey_course, "YES"])

        #DBMANAGER.modify_data(enrol_packet, False)        
    return "AJAX"

@APP.route('/admin/metrics')
def admin_metrics():
    """ Displays admin metrics dashboard.  """

    # Display Survey Pool
    survey_packet = DataPacket(current_user.get_id(), SURVEY_COL_IDS, '_survey')
    survey_packet = DBMANAGER.retrieve_data(survey_packet)
    surveys = read_surveys(survey_packet, True, None)

    return render_template('admin/dash-metrics.html', surveys=surveys)

@APP.route('/metrics/<survey_course>')
@login_required
def survey_metrics(survey_course):
    """ Displays metrics page for all users. Always visible to admins. Visible
        to staff and students after survey closes. """
    results = DBMANAGER.sort_metrics(survey_course + '_metrics', 'QUESTION')
    results_list = []
    q_text = None;
    result_count = 0
    if results:
        for r in results:
            if r[3] == 'None':
                continue
            if int(r[2]) == QuestionType.TEXT.value:
                result_count += 1
                if r[1] != q_text:
                    results_list.append([r[1], r[2], []])
                results_list[-1][2].append(r[3])             
            elif int(r[2]) == QuestionType.BOOL.value:
                if r[1] != q_text:
                    results_list.append([r[1], r[2], [0]*2])
                if r[3] == 'TRUE':
                    results_list[-1][2][0] += 1  
                else:
                    results_list[-1][2][1] += 1 
            else:
                if r[1] != q_text:
                    results_list.append([r[1], r[2], [0]*6])
                results_list[-1][2][int(r[3]) - 1] += 1
            q_text = r[1]
    #reminder: fix headers later
    return render_template('metrics.html', results=results_list, course=survey_course, result_count=result_count)

# Survey flask server file
from server import APP, LOGIN_MANAGER
from flask import session
from modules.head import *
from modules.LoginForm import LoginForm
from modules.Authenticate import Authenticate, RestoreUser
from modules.QuestionsManager import DeleteQuestion, QuestionForm, ReadQuestions, AddQuestion

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
    if current_user.get_role() == 'staff':
        form = QuestionForm(request.form)
        questions = ReadQuestions()

        if request.method == 'POST' and form.validate():
            AddQuestion(form.question.data, form.questiontype.data)
            return redirect(url_for('staff_questions'))

        return render_template('dashboard/dash-questions.html', questions=questions, form = form)
    else:
        return 'gtfo'

@APP.route('/staff/questions/delete/<int:questionid>')
@login_required
def delete_question(questionid):
    questionid = int(questionid)
    DeleteQuestion(questionid)

    return redirect(url_for('staff_questions'))

@APP.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('survey_homepage'))

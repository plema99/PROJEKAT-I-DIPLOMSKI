import json
from jsonpickle import encode
from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from model.models import Question, QuestionSchema
from config import db


main = Blueprint("main", __name__) #kao kontroler da pravim, a dole cu akcije


@main.route("/")
def index():
    return render_template("startup.html")


@main.route("/create")
def create():
    db.create_all()
    return render_template("startup.html")

@main.route("/startQuiz",  methods=['POST'])
def startQuiz():

    if "category" not in request.form:
        error_msg = "Molimo vas odaberite oblast"
        return render_template("startup.html", errormsg=error_msg)

    category = request.form["category"]
    questions = Question.query.filter_by(category=category)
    schema = QuestionSchema(many=True)

    session["correctAnswers"] = 0
    session["questions"] = None
    session["questions"] = schema.dump(questions)
    question = session["questions"][0]
    answer_list = questions[0].get_answers()

    options = create_option_list(question)

    context = {
        "question": question,
        "options": options,
        "question_num": 0,
        "num_answ": len(answer_list)
    }
    session["counting"] = 0
    return render_template("question.html", **context)

def create_option_list(question):
    options = [question["option1"], question["option2"]]

    if (question["option3"] != None):
        options.append(question["option3"])
    if (question["option4"] != None):
        options.append(question["option4"])
    if (question["option5"] != None):
        options.append(question["option5"])
    if (question["option6"] != None):
        options.append(question["option6"])
    return options

@main.route("/explanation", methods=['GET', 'POST'])
def explanation():

    user_answers = request.form.getlist("answer")
    current_question = session["questions"][session["counting"]]
    question_object = Question.query.get(current_question["id"])
    answer_list = question_object.get_answers()

    user_answers_as_string = get_user_answers(user_answers, question_object)

    options = create_option_list(current_question)

    correct_answers = get_list_string(question_object)

    if user_answers == answer_list:
        session["correctAnswers"] += 1

    context = {
        "current_question": current_question,
        "explanation": question_object.explanation,
        "correct_answers": correct_answers,
        "options": options,
        "user_answers": user_answers_as_string
    }

    return render_template("explanation.html", **context)

def get_user_answers(user_answers, question_object):
    list = []
    if "0" in user_answers:
        list.append(question_object.option1)
    if "1" in user_answers:
        list.append(question_object.option2)
    if "2" in user_answers:
        list.append(question_object.option3)
    if "3" in user_answers:
        list.append(question_object.option4)
    if "4" in user_answers:
        list.append(question_object.option5)
    if "5" in user_answers:
        list.append(question_object.option6)

    return list

def get_list_string(question_object):
    answer_list = question_object.get_answers()
    list_answer_string = []
    if "0" in answer_list:
        list_answer_string.append(question_object.option1)
    if "1" in answer_list:
        list_answer_string.append(question_object.option2)
    if "2" in answer_list:
        list_answer_string.append(question_object.option3)
    if "3" in answer_list:
        list_answer_string.append(question_object.option4)
    if "4" in answer_list:
        list_answer_string.append(question_object.option5)
    if "5" in answer_list:
        list_answer_string.append(question_object.option6)

    return list_answer_string



@main.route("/nextQuestion", methods=['GET', 'POST'])
def nextQuestion():

    number_of_questions_answered = session["counting"] + 1
    if len(session["questions"]) == number_of_questions_answered:
        return redirect(url_for('main.endQuiz'))

    session["counting"] += 1
    current_question = session["questions"][session["counting"]]
    question_object = Question.query.get(current_question["id"])
    answer_list = question_object.get_answers()

    next_question = session["questions"][session["counting"]]

    options = create_option_list(next_question)

    context = {
        "question": next_question,
        "options": options,
        "question_num": session["counting"],
        "num_answ": len(answer_list)
    }

    return render_template("question.html", **context)

@main.route("/endQuiz", methods=['GET', 'POST'])
def endQuiz():
    score = session["correctAnswers"]
    numQuest = len(session["questions"])

    context = {
        "score": score,
        "numQuest": numQuest
    }
    return render_template("endQuiz.html", **context)

@main.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "GET":
        return render_template("adding.html")
    else:
        question_text = request.form["q_text"]
        category = request.form["category"]
        option1 = request.form["opt1"]
        option2 = request.form["opt2"]
        option3 = request.form["opt3"]
        option4 = request.form["opt4"]
        option5 = request.form["opt5"]
        option6 = request.form["opt6"]
        image = request.form["image"]

        answers = request.form.getlist("answer")

        question = Question(text=question_text, category=category)
        question.option1 = option1
        question.option2 = option2
        question.image = image
        question.explanation = request.form["explanation"]

        if(option3 != ""):
            question.option3 = option3
        if(option4 != ""):
            question.option4 = option4
        if(option5 != ""):
            question.option5 = option5
        if(option6 != ""):
            question.option6 = option6

        s = ",".join(answers)
        question.answers = s

        db.session.add(question)
        db.session.commit()
        return render_template("adding.html")





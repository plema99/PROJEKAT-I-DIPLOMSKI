import json
from jsonpickle import encode
from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from model.models import Question, QuestionSchema
from config import db


main = Blueprint("main", __name__) #kao kontroler da pravis, a dole cu akcije


@main.route("/")
def index():
    return render_template("startup.html")


@main.route("/create")
def create():
    db.create_all()
    return render_template("startup.html")


@main.route("/startQuiz",  methods=['POST'])
def startQuiz():
    category = request.form["category"]
    session["counting"] = 0

    questions = Question.query.filter_by(category=category)
    schema = QuestionSchema(many=True)

    session["questions"] = schema.dump(questions)
    question = session["questions"][0]

    options = create_option_list(question)

    context = {
        "question": question,
        "options": options
    }

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

@main.route("/nextQuestion", methods=['GET', 'POST'])
def nextQuestion():
    user_answers = request.form.getlist("answer")
    number_of_questions_answered = session["counting"] + 1
    if len(session["questions"]) == number_of_questions_answered:
        return redirect(url_for('main.endQuiz'))

    current_question = session["questions"][session["counting"]]
    session["correctAnswers"] = 0

    question_object = Question.query.get(current_question["id"])
    answer_list = question_object.get_answers()

    if user_answers == answer_list:
        session["correctAnswers"] += 1

    session["counting"] += 1

    question = session["questions"][session["counting"]]

    options = create_option_list(question)

    context = {
        "question": question,
        "options": options
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

        answers = request.form.getlist("answer")

        question = Question(text=question_text, category=category)
        question.option1 = option1
        question.option2 = option2

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






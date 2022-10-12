from config import db, ma
from marshmallow import fields  #za serijalizaciju ibjekata iz baze jer ce ti bacati error
#kako kako nije moguce da serijalizuje dobavljeni objekat
import json

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    explanation = db.Column(db.String(1000))
    category = db.Column(db.String(50))
    option1 = db.Column(db.String(50))
    option1 = db.Column(db.String(50))
    option2 = db.Column(db.String(50))
    option3 = db.Column(db.String(50))
    option4 = db.Column(db.String(50))
    option5 = db.Column(db.String(50))
    option6 = db.Column(db.String(50))
    answers = db.Column(db.String(50))
    image = db.Column(db.String(50), default = '')
    opt1com = db.Column(db.String(50))
    opt2com = db.Column(db.String(50))
    opt3com = db.Column(db.String(50))
    opt4com = db.Column(db.String(50))
    opt5com = db.Column(db.String(50))
    opt6com = db.Column(db.String(50))


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_answers(self):
        answer_list = self.answers
        answer_list = answer_list.split(",")
        return answer_list

    def get_optcomm(self):
        opt_com_list = [self.opt1com, self.opt2com, self.opt3com, self.opt4com, self.opt5com, self.opt6com]
        return opt_com_list


class QuestionSchema(ma.Schema):
    id = fields.Number()
    text = fields.Str()
    explanation = fields.Str()
    category = fields.Str()
    option1 = fields.Str()
    option1 = fields.Str()
    option2 = fields.Str()
    option3 = fields.Str()
    option4 = fields.Str()
    option5 = fields.Str()
    option6 = fields.Str()
    answers = fields.Str()
    image = fields.Str()
    opt1com = fields.Str()
    opt2com = fields.Str()
    opt3com = fields.Str()
    opt4com = fields.Str()
    opt5com = fields.Str()
    opt6com = fields.Str()

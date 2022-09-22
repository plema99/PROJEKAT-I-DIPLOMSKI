from flask import Flask
from config import Config, db
from model.models import Question
from routes import main
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "aon32c423c432v423v4"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)
app.register_blueprint(main)#dovlacim blueprint

if __name__ == '__main__':
    app.run()
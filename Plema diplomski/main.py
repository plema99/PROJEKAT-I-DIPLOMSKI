from flask import Flask
from config import Config, db
from model.models import Question
from routes import main

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "aon32c423c432v423v4"
db.init_app(app)
app.register_blueprint(main)#dovlacim blueprint

if __name__ == '__main__':
    app.run()
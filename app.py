from flask import Flask, render_template
from models import db, UserModel

app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hdp_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run('localhost', 9999, debug=True, use_reloader=True)
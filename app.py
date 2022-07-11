from flask import Flask, render_template, request
from models import db, UserModel

app = Flask(__name__)
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hdp_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/clean_data', methods=["POST"])
def clean_data():
    print(" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< WHAT THE HELL IS GOING ON HERE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    if request.method == "POST":
        data = request.get_json(force=True)
        csv_data = ''
       
        with open('./data.csv', 'w') as data_file:
            csv_data += ",".join(data[0].keys()) + '\n' # Headers in string format e.g. A, B, C, D, E, F 
            for row in data:
                csv_data += ",".join(row.values()) + '\n'
            
            data_file.write(csv_data)
    
        print(csv_data)
        return csv_data
    else:
        return "NOT SO GREAT"
if __name__ == "__main__":
    app.run('localhost', 9999, debug=True, use_reloader=True)
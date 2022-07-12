from flask import Flask, redirect, render_template, request
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from models import db, UserModel
import pandas as pd
import secrets
import joblib

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)
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

    if request.method == "POST":
        try:
            data = request.get_json(force=True)
            csv_data = ''
        
            with open('./data.csv', 'w') as data_file:
                for row in data:
                    csv_data += ",".join(row.values()) + '\n'
                
                data_file.write(csv_data)

            heart = pd.read_csv('./data.csv', names=data[0].keys())

            heart["ST depression"] = heart["ST depression"].astype("int64")
            
            min_max = MinMaxScaler()
            columns_to_scale = ['Age', 'BP', 'Cholesterol', 'Max HR', 'Thallium']
            heart[columns_to_scale ] = min_max.fit_transform(heart[columns_to_scale ])

            x = heart[['Age', 'BP', 'Cholesterol', 'Max HR', 'Thallium']]
            y = heart['Heart Disease']
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.30)
            
            data = {
                'headers' : ['Age', 'BP', 'Cholesterol', 'Max HR', 'Thallium', 'Heart Disease'],
                'clean_data' : (x.join(y)).to_dict('records'), 
                'train_data' : (x_train.join(y_train)).to_dict('records'),
                'test_data' : (x_test.join(y_test)).to_dict('records')
            }

            return {'message': 'Success', 'data': data, 'status': 200}
        except Exception as error:
            return {'message': 'Failed - Internal Server Error - {}'.format(error), 'status': 500}
    else:
        return {'message': 'Method not allowed, only POST method is supported', 'status': 404}

@app.route('/train_model', methods=["POST"])
def train_model():

    if request.method == "POST":
        try:
            data = request.get_json(force=True)
            train_data = pd.DataFrame(data['train_data'])
            test_data = pd.DataFrame(data['test_data'])
            x_train, y_train = train_data[['Age', 'BP', 'Cholesterol', 'Max HR', 'Thallium']] , train_data['Heart Disease']
            x_test, y_test= test_data[['Age', 'BP', 'Cholesterol', 'Max HR', 'Thallium']], test_data['Heart Disease']

            model = LogisticRegression()
            model.fit(x_train, y_train)
            y_pred = model.predict(x_test)

            joblib.dump(model, "model.pkl")

            return {
                'message': 'Logistic Regression, Training Successfull',
                'body': 'Model accuracy score: {}'.format(accuracy_score(y_test, y_pred)*100),
                'status': 200
                }

        except Exception as error:
            return {'message': 'Failed - Internal Server Error - {}'.format(error), 'status': 500}
    else:
        return {'message': 'Method not allowed, only POST method is supported', 'status': 404}


if __name__ == "__main__":
    app.run('localhost', 9999, debug=True, use_reloader=True)
  
import models
from dotenv import load_dotenv
import os
import sqlalchemy
import bcrypt
import jwt
import requests
from flask_cors import CORS
from flask import Flask, request


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

models.db.init_app(app)

def root():
    return { 'message': 'You hit the root route!' }
app.route('/', methods=["GET"])(root)

@app.route('/all',methods=['GET'])
def all_Train():
    try:
        response = request.get(f'DATABASE_URL=https://api.wmata.com/StationPrediction.svc/json/GetPrediction')
    except print(0):
        pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
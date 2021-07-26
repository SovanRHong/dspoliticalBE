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

weather_url="https://api.wmata.com/StationPrediction.svc/json/GetPrediction/"
api_key=os.environ.get('METRO_API_KEY')

def root():
    return { 'message': 'You hit the root route!' }
app.route('/', methods=["GET"])(root)

@app.route('/ALL',methods=['GET'])
def all_Train():
    try:
        response = requests.get(f'{weather_url}ALL',params={'format':'json','API_KEY':api_key})
        
        print(response.json())
        return{'message':'search successful',"trains_data":response.json()}
            
    except Exception as e:
        return{'message':'error request all train unsuccessful'},401

    finally:
        print('ALL trains routes is working')

@app.route('/<station_codes>',methods=['GET'])
def single_station(station_codes):
    try:
        response = requests.get(f'{weather_url}{station_codes}',params={'format':'json','API_KEY':api_key})

        print(response)
        if response:
            print(response.json())
            return{'message':'search successful',"station_data":response.json()}
        else:
            return{'message':'There are no trains at this station'}
      
    except Exception as e:
        return{'message':'error request  unsuccessful'},401
    
    finally:
        print('single station route is working')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
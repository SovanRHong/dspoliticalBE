import models
from dotenv import load_dotenv
import os
import requests
from flask_cors import CORS
from flask import Flask, request



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

models.db.init_app(app)

metro_url="https://api.wmata.com/StationPrediction.svc/json/GetPrediction/"
api_key=os.environ.get('METRO_API_KEY')

@app.route('/', methods=["GET"])
def root():
    return 'Hi Ben!'


@app.route('/ALL',methods=['GET'])
def all_Train():
    try:
        response = requests.get(f'{metro_url}ALL',params={'format':'json','API_KEY':api_key})
            # GET data from API

        print(response.json())
            # if response == success, EVAL and Print data 
        return{'message':'search successful',"trains_data":response.json()}
            # FORMAT message:
                #   response{status:ok,data:[]} 
                # SEND message to FE   
    except Exception as e:
        return{'message':'reached your allowed API limit'},429
            # if error:
            # response {error}
    

@app.route('/<station_codes>',methods=['GET'])
def single_station(station_codes):
    try:
        response = requests.get(f'{metro_url}{station_codes}',params={'format':'json','API_KEY':api_key})
            #GET data from API
        print(response)
            # if response == success, EVAL and Print data 
        if response:
            print(response.json())
            return{'message':'search successful',"station_data":response.json()}
               # FORMAT message:
                # response{status:ok,data:[]} 
                # SEND message to FE 
        else:
            return{'message':'There are no trains at this station',"station_data":{"Trains":[]}}
                 # FORMAT message:
                    # response{status:error,data:[]} 
                    # SEND message to FE 
    except Exception as e:
        return{'message':'error request unsuccessful'},401
        # if error:
            # response {error}
    
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


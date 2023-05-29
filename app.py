from flask import Flask,jsonify
# from flask_sqlalchemy import SQLAlchemy

api_key = ''

import openai


import phonenumbers
from phonenumbers import carrier, geocoder, timezone

openai.api_key = api_key

# list models
models = openai.Model.list()

import wikipedia

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = {'key': 'value'}
    # return data
    return jsonify(data)

@app.route("/api/wikipedia/<data>")
def cT(data):
    try:
        data = {'type':'wikipedia','value' : wikipedia.summary(data)}

        return jsonify(data)
    except:
        return jsonify({'type':'wikipedia','value':'No Result Found'})
    
@app.route("/api/chatGPT/<question>")
def chatGPT(question):

    try:

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])
# print the completion
    # print(completion.choices[0].message.content)
        data = {'type':'chatGPT', 'value': completion.choices[0].message.content }

        return jsonify(data)
    except:    
        data = {'type':'chatGPT', 'value': 'There is some error ! Can You Please Try Once Again...' }
        return jsonify(data)


@app.route("/api/createIMG/<que>")
def createIMG(que):

    try:

        data=[]
        img = openai.Image.create(prompt=que, n=4, size="512x512")
        for i in range(len(img.data)):
            data.append({'type':'createIMG', 'value': img.data[i].url})

        return jsonify(data)    
    except:    
        data = [{'type':'createIMG', 'value': 'There is some error ! Can You Please Try Once Again...' }]
        return jsonify(data)


@app.route("/api/phoneNumberDetails/<mob>")
def phoneNumber(mob):
        
    try:    
        mobileNo=phonenumbers.parse(mob)
        data = {'type':'phonenumber', 'Phone': mob,'timezone': timezone.time_zones_for_number(mobileNo), 'carrier':carrier.name_for_number(mobileNo,"en"), 'location':geocoder.description_for_number(mobileNo,"en"), 'Valid Mobile Number' : phonenumbers.is_valid_number(mobileNo),'Checking possibility of Number':phonenumbers.is_possible_number(mobileNo),'msg':'success'}
        return jsonify(data)

    except:
        data = {'type':'phonenumber', 'Phone': mob,'timezone': 'error', 'carrier':'error', 'location':'error', 'Valid Mobile Number' : 'error','Checking possibility of Number':'error', 'msg':'you should use number with countrycode'}

        return jsonify(data)






if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
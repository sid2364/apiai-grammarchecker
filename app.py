from flask import Flask
from flask import request
from flask import make_response

import json
import random

import AfterTheDeadlineHelper as ATD

app = Flask("apiai-grammarchecker")

replies_no_error = ["There seems to be no problem with this!", \
		"I think this is perfectly alright!", \
		"I don't think there is any problem with what you have there!", \
		"It's all correct!"]

@app.route("/")
def home():
	return "Hello Heroku!"

@app.route("/webhook", methods=["POST"])
def webhook():
	req = request.get_json() # removed str

	wrong_sentence = getWrongSentence(req)
	response = getResponse(wrong_sentence)
	
	r = {"speech": response, "displayText": response}
	r = make_response(json.dumps(r))
	r.headers['Content-Type'] = 'application/json'
	return r

def getWrongSentence(request):
	result = request.get("result")
	parameters = result.get("parameters")
	wrong_sentence = parameters.get("wrong-sentence")
	return wrong_sentence

def getResponse(wrong_sentence):
	response = ATD.checkDocument(wrong_sentence)
	if response.errorCount == 0:
		return replies_no_error[random.randint(0, len(replies_no_errors)-1]

	for e in range(response.errorCount):
		urltext = response.getURLText(e)
		if urltext is not None and urltext != 0:
			return urltext
	correct_rand = random.randint(0, response.errorCount-1)
	reply = "There seems to be a problem with '"+response.getErrorString(correct_rand)+"'. "
	reply += "Did you mean '"+("' or '".join(response.getSuggestions(correct_rand)))+"'?"
	return reply


if __name__ == "__main__":
	app.run()

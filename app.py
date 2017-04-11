from flask import Flask
from flask import request
from flask import make_response

import json
import ast

import AfterTheDeadlineHelper as ATD

app = Flask("apiai-grammarchecker")

sentence = "What is problem with sentense?" # Incorrect grammar and spelling

@app.route("/")
def home():
	return "Hello Heroku!"

@app.route("/webhook", methods=["POST"])
def webhook():
	req = request.get_json() # removed str

	wrong_sentence = getWrongSentence(req)

	print(wrong_sentence)
	print(req)
	response = "Testing"
	r = {"speech": response}
	r = make_response(json.dumps(r))
	r.headers['Content-Type'] = 'application/json'
	return r

def getWrongSentence(request):
	result = request.get("result")
	parameters = result.get("parameters")
	wrong_sentence = parameters.get("wrong-sentence")
	return wrong_sentence

if __name__ == "__main__":
	app.run()

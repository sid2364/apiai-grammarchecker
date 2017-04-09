from flask import Flask
import AfterTheDeadlineHelper as ATD

app = Flask("apiai-grammarchecker")

sentence = "What is problem with sentense?"

@app.route("/webhook")
def webhook():
	text = "Checking for sentence: " + sentence
	response = ATD.checkDocument(sentence)
	# print response.errorCount
	for error in range(response.errorCount):
		text += "<br>Error #" + str(error + 1)
		text += "<br>String: " + response.getErrorString(error)
		text += "<br>Precontext: " + response.getPrecontext(error)
		text += "<br>Type: " + response.getType(error)
		text += "<br>Suggestions: " + ", ".join(response.getSuggestions(error))
		text += "<br>Description: " + response.getDescription(error)
		if response.getURLText(error) is not None:
			text += "<br>URL: " + response.getURLText(error)
		text += "<br>"
	return text

if __name__ == "__main__":
	app.run()

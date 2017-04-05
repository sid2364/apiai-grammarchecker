"""
After The Deadline Helper Module

Author: Siddharth Sahay
"""

from bs4 import BeautifulSoup
import urllib
import requests
import xml.etree.ElementTree

# After The Deadline API
_key = 'apiai-grammarchecker'
atd_api_service = 'https://service.afterthedeadline.com/'
check_document_f = 'checkDocument'

# XML tags for the response from ATD
string_response = 'string'
option_response = 'option'
precontext_response = 'precontext'
type_response = 'type'
suggestions_response = 'suggestions'
description_response = 'description'
error_response = 'error'
url_response = 'url'


class Response:
	'''
	Attributes:
		info, dictionary containing the entire XML response.
		errorCount, number of errors in the text given as input.
		xmlTree, the XML tree from ATD.
	'''
	def __init__(self, doc):
		self.info = {}
		self.errorCount = 0
		self.xmlTree = xml.etree.ElementTree.fromstring(doc)
		for error in self.xmlTree.findall(error_response):
			key_t = error.tag + str(self.errorCount)
			error_d = {}
			for child in error:
				if child.tag == suggestions_response:
					suggestion_d = {}
					option_i = 1
					for option in child:
						suggestion_d[option.tag + str(option_i)] = option.text
						option_i += 1
					error_d[child.tag] = suggestion_d
					continue
				error_d[child.tag] = child.text
			self.info[key_t] = error_d
			self.errorCount += 1
	
	def getErrorString(self, errorNumber):
		return self.info[error_response + str(errorNumber)][string_response]
	
	def getPrecontext(self, errorNumber):
		return self.info[error_response + str(errorNumber)][precontext_response]
	
	def getType(self, errorNumber):
		return self.info[error_response + str(errorNumber)][type_response]
	
	def getDescription(self, errorNumber):
		return self.info[error_response + str(errorNumber)][description_response]
	'''
	Returns:
		List of suggestions for error.
	'''
	def getSuggestions(self, errorNumber):
		suggestions = []
		s = self.info[error_response + str(errorNumber)][suggestions_response]
		for option in s:
			suggestions.append(s[option])
		return suggestions

	'''
	Returns:
		None, if URL is not found in the reponse from ATD.
		0, if service is temporarily unavailable.
		Insight into error, if service is up, as a string.
	'''
	def getURLText(self, errorNumber):
		try:
			text = requests.get(
				self.info[error_response + str(errorNumber)][url_response]).text
			soup = BeautifulSoup(text, "lxml")
			if soup.p is None and soup.title.text is not None:
				return 0
			return soup.p.text
		except KeyError:
			return None


def checkDocument(text, key=None):
	if key is None:
		key = _key

	params = urllib.urlencode({
		'key': key,
		'data': text
	})

	return Response(requests.get(
		atd_api_service + check_document_f + "?" + params).text)

'''
response = checkDocument('What are problem with sentense?')
print(response.getErrorString(2))
print(response.getSuggestions(2))
print(response.getURLText(2))
print(response.getURLText(1))
'''

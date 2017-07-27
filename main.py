#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import sys
import jinja2
import json
import logging
import webapp2
import urllib2
import codecs
from wordnik import *
from random import randint
from google.appengine.ext import ndb


apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'f0261de6207a638a679085cc16b08c782598f242708775355'
client = swagger.ApiClient(apiKey, apiUrl)

#Darrell's Key = '6089226ee40a95fbb230a04f01406ab804d9b51cebc36272c'

wordApi = WordApi.WordApi(client)
wordsApi = WordsApi.WordsApi(client)

#response = Request("http://api.wordnik.com:80/v4/words.json/randomWord?hasDictionaryDef=true&minCorpusCount=0&maxCorpusCount=-1&minDictionaryCount=2&maxDictionaryCount=-1&minLength=3&maxLength=-1&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5")


env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class User(ndb.Model):
    ID = ndb.StringProperty();
    nickname = ndb.StringProperty();

class WrongWord(ndb.Model):
    word = ndb.StringProperty()
    definition = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    definitionOfDisplayedWord = None
    main_var = None
    randomWords = None
    displayedWord = None
    incorrectWord = None
    score = 0
    def get(self):
        template = env.get_template('templates/index.html')
        MainHandler.randomWords = wordsApi.getRandomWords(hasDictionaryDef = True,
                                            includePartOfSpeech = 'noun',
                                            excludePartOfSpeech = 'proper-noun-plural',
                                            minLength = 3,
                                            maxLength = -1,
                                            minDictionaryCount = 1,
                                            maxDictionaryCount = -1,
                                            minCorpusCount = 0,
                                            maxCorpusCount = -1,
                                            limit = 4)
        i = randint(0, 3)
        array = []
        for randomword in MainHandler.randomWords:
          definitions = wordApi.getDefinitions(randomword.word,
                                             sourceDictionaries = 'all',
                                             limit = 1)
          array.append(definitions[0].text)
        #wordrandom = randomWords[i].text
        MainHandler.definitionOfDisplayedWord = array[i]
        MainHandler.displayedWord = MainHandler.randomWords[i].word

        main_var = {'word': MainHandler.randomWords[i].word,
                    'def1': array[0],
                    'def2': array[1],
                    'def3': array[2],
                    'def4': array[3],
                    'score': MainHandler.score}

        self.response.out.write(template.render(main_var))

    def post(self):
        userIDToken = self.request.get("ID")
        nickName = self.request.get("nick")
        self.sendUser(userIDToken, nickName)
        selectionToCompare = self.request.get("option")
        if not selectionToCompare:
            self.processAnswer()
            return
        if selectionToCompare == MainHandler.definitionOfDisplayedWord.strip():
            response = "True"
        else:
            response = "False"

        return_data = {"answer": response}
        self.response.write(json.dumps(return_data))

    def sendUser(self, token, name):
        print token
        print name
        user = User(ID = token, nickname = name)
        user.put()

    def processAnswer(self):
        checkAnswer = self.request.get("selection")
        if checkAnswer == "True":
            MainHandler.score += 1
        else:
            MainHandler.incorrectWord = MainHandler.displayedWord
            wrongword = WrongWord(word = MainHandler.incorrectWord, definition = MainHandler.definitionOfDisplayedWord)
            key = wrongword.put()

        newscore = {"newscore": MainHandler.score}
        self.response.write(json.dumps(newscore))



class WrongHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/saved.html')
        self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/wrong', WrongHandler)
], debug=True)

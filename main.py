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

wordApi = WordApi.WordApi(client)
wordsApi = WordsApi.WordsApi(client)

env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class WrongWord(ndb.Model):
    words = ndb.StringProperty(repeated = True)


class WrongDef(ndb.Model):
    definitions = ndb.StringProperty(repeated = True)

class User(ndb.Model):
    IDs = ndb.StringProperty();
    nickname = ndb.StringProperty();

class MainHandler(webapp2.RequestHandler):
    definitionOfDisplayedWord = None
    main_var = None
    randomWords = None
    displayedWord = None
    incorrectWord = None
    score = 0
    key = None
    scoreKeep = []
    def get(self):
        template = env.get_template('templates/index.html')
        MainHandler.randomWords = wordsApi.getRandomWords(hasDictionaryDef = True,
                                            includePartOfSpeech = 'noun',
                                            excludePartOfSpeech = 'noun-plural',
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
        selectionToCompare = self.request.get("option")
        userIDToken = self.request.get("IDs")
        nickName = self.request.get("nick")

        if selectionToCompare:
            if selectionToCompare.strip() == MainHandler.definitionOfDisplayedWord:
                response = "True"
            else:
                response = "False"
            return_data = {"answer": response}
            self.response.write(json.dumps(return_data))

        elif not selectionToCompare:
            if not userIDToken or nickName:
                self.processAnswer()
            else:
                self.sendUser(userIDToken, nickName)

    def sendUser(self, token, name):
        print token
        print name
        userQuery = User.query(User.IDs == token) #Finds All ID's of same token
        testIDs = userQuery.fetch() #Puts them in a list
        print len(testIDs) #Find the length of the list
        if len(testIDs) > 0 : #Make sure theres only one element of this ID in a list
            return #Returns if there is more than one
        else: #Otherwise, send the info to the server
            user = User(IDs = token, nickname = name)
            user.put()
            print token

    def processAnswer(self):
        checkAnswer = self.request.get("selection")
        print checkAnswer
        if checkAnswer == "True":
            MainHandler.score += 1
            MainHandler.scoreKeep.append(MainHandler.score)
            newscore = {"newscore": MainHandler.score,
                        "scorekeep": MainHandler.scoreKeep}
            self.response.write(json.dumps(newscore))
        elif checkAnswer == "False":
            MainHandler.score += 0
            MainHandler.scoreKeep.append(MainHandler.score)
            newscore = {"newscore": MainHandler.score,
                        "scorekeep": MainHandler.scoreKeep}
            self.response.write(json.dumps(newscore))
            self.wordsAsHTML(MainHandler.displayedWord)
            self.definitionsAsHTML(MainHandler.definitionOfDisplayedWord)

    def wordsAsHTML(self, new_word):
        words_query = WrongWord.query()
        word_data = words_query.get()
        if word_data == None:
            if new_word == None:
                return
            else:
                word_list = [ new_word ]
                word_data = WrongWord(words = word_list)
                word_data.put()
        else:
            if new_word != None:
                word_data.words.append(new_word)
                word_data.put()

    def definitionsAsHTML(self, new_definition):
        definitions_query = WrongDef.query()
        definition_data = definitions_query.get()
        if definition_data == None:
            if new_definition == None:
                return
            else:
                definitions_list = [ new_definition ]
                definition_data = WrongDef(definitions = definitions_list)
                definition_data.put()
        else:
            if new_definition != None:
                definition_data.definitions.append(new_definition)
                definition_data.put()

class WrongHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/wrong.html')
        self.response.out.write(template.render())

    def post(self):
        words_query = WrongWord.query()
        word_data = words_query.get()
        define_query = WrongDef.query()
        define_data = define_query.get()
        somePostFromJS = self.request.get("getresponse")

        if word_data == None and define_data == None:
            self.response.out.write("No words to display.")
        else:
            if somePostFromJS == "True":
                incorrectVar = {"incorrectword": word_data.words,
                                "incorrectdef": define_data.definitions}
                self.response.write(json.dumps(incorrectVar))
            else:
                return False

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/wrong', WrongHandler)
], debug=True)

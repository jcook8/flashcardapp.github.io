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
from wordnik import *
from random import randint


apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'f0261de6207a638a679085cc16b08c782598f242708775355'
client = swagger.ApiClient(apiKey, apiUrl)

#Darrell's Key = '6089226ee40a95fbb230a04f01406ab804d9b51cebc36272c'

wordApi = WordApi.WordApi(client)
wordsApi = WordsApi.WordsApi(client)

#response = Request("http://api.wordnik.com:80/v4/words.json/randomWord?hasDictionaryDef=true&minCorpusCount=0&maxCorpusCount=-1&minDictionaryCount=2&maxDictionaryCount=-1&minLength=3&maxLength=-1&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5")


env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/index.html')
        randomWords = wordsApi.getRandomWords(hasDictionaryDef = True,
                                            minLength = 3,
                                            maxLength = 5,
                                            minDictionaryCount = 1,
                                            maxDictionaryCount = -1,
                                            minCorpusCount = 0,
                                            maxCorpusCount = -1,
                                            limit = 4)
        i = randint(0, 3)
        array = []
        for randomword in randomWords:
          randomDef = wordApi.getDefinitions(randomword.word,
                                             sourceDictionaries = 'all',
                                             limit = 1)
          array.append(randomDef[0].text)
        mainvar = {'word': randomWords[i].word,
                    'def1': array[0],
                    'def2': array[1],
                    'def3': array[2],
                    'def4': array[3]}
        self.response.out.write(template.render(mainvar))

class SavedHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/saved.html')
        self.response.out.write(template.render())

class TestHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/saved.html')
        randomWord = wordsApi.getRandomWord(hasDictionaryDef = True,
                                            minLength = 3,
                                            maxLength = 5,
                                            minDictionaryCount = 1,
                                            maxDictionaryCount = -1,
                                            minCorpusCount = 0,
                                            maxCorpusCount = -1)
        definitions = wordApi.getDefinitions(randomWord.word,
                                           sourceDictionaries = 'all',
                                           limit = 1)
        self.response.out.write(randomWord.word + ": " + definitions[0].text)
         # i = 0
        #randomDef = wordApi.getDefinitions(randomWords[1].text, limit = 1)
        #  i += 1
        #main_var = {"word": } #, "def1": randomDef[1].text}

class Test2Handler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/index.html')
        randomWords = wordsApi.getRandomWords(hasDictionaryDef = True,
                                            minLength = 3,
                                            maxLength = 5,
                                            minDictionaryCount = 1,
                                            maxDictionaryCount = -1,
                                            minCorpusCount = 0,
                                            maxCorpusCount = -1,
                                            limit = 4)
        i = randint(0, 3)
        array = []
        for randomword in randomWords:
          randomDef = wordApi.getDefinitions(randomword.word,
                                             sourceDictionaries = 'all',
                                             limit = 1)
          array.append(randomDef[0].text)
        mainvar = {'word': randomWords[i].word,
                    'def1': array[0],
                    'def2': array[1],
                    'def3': array[2],
                    'def4': array[3]}
        self.response.out.write(json.dumps(mainvar))
        self.response.out.write(template.render(mainvar))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/saved', SavedHandler),
    ('/testing', TestHandler),
    ('/testing2', Test2Handler)
], debug=True)

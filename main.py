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
import webapp2
import os
import sys
import jinja2
from wordnik import *

apiUrl = 'http://api.wordnik.com/v4'
apiKey = '6089226ee40a95fbb230a04f01406ab804d9b51cebc36272c'
client = swagger.ApiClient(apiKey, apiUrl)

wordApi = WordApi.WordApi(client)
example = wordApi.getTopExample('irony')

env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/index.html')
        self.response.out.write(template.render())
    print example.text

class SavedHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/saved.html')
        self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/saved', SavedHandler)
], debug=True)

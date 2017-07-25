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

env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/index.html')
        self.response.out.write(template.render())

class SavedHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/saved.html')
        self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/saved', SavedHandler)
], debug=True)



word = { "status": 200, "offset": 0, "limit": 1, "count": 1,  "total": 1,
  "url": "/v2/dictionaries/ldoce5/entries?headword=hypochondriac&limit=1",
  "results": [{"datasets": ["ldoce5","dictionary"],"headword": "hypochondriac", "id": "cqAFNmnynQ","part_of_speech": "noun","pronunciations": [{"audio": [{"lang": "British English","type": "pronunciation","url": "/v2/dictionaries/assets/ldoce/gb_pron/hypochondriac0205.mp3" }],
  "ipa": "ˌhaɪpəˈkɒndriæk"}, { "audio": [{ "lang": "American English", "type": "pronunciation", "url": "/v2/dictionaries/assets/ldoce/us_pron/hypochondriac.mp3" }], "ipa": "-ˈkɑːn-", "lang": "American English" }],
  "senses": [{ "definition": ["someone who always worries about their health and thinks they may be ill, even when they are really not ill"] }], "url": "/v2/dictionaries/entries/cqAFNmnynQ" }]}

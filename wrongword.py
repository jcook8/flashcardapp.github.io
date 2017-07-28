from google.appengine.ext import ndb

class WrongWords:
    def wordsAsHTML(self, new_word):
        words_query = WrongWord.query()
        word_data = words_query.get()
        if word_data == None:
            if new_word == None:
                return "<p>No incorrect words yet</p>"
            else:
                word_list = [ new_word ]
                word_data = WrongWord(words = word_list)
                word_data.put()
                return "<p>" + new_word + "</p>"
        else:
            if new_word != None:
                word_data.words.append(new_word)
            html_string = ""
            for word in word_data.words:
                html_string += "<p>" + word + "</p>"
            if new_word != None:
                word_data.put()
            return html_string

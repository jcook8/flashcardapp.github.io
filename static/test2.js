var randomWords = $.getJSON('http://api.wordnik.com:80/v4/words.json/randomWords?hasDictionaryDef=true&minCorpusCount=0&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=3&maxLength=-1&limit=4&api_key=f0261de6207a638a679085cc16b08c782598f242708775355', function(data){
    console.log(data)
    for (var i = 0; i < (data).length; i++){
      console.log(data[i].word)
      $('test-p').appendTo("<span>" + data[i].word + "</span>");
    }
});

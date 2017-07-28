$(document).ready( function(){

  $.post("/wrong", {"getresponse": "True"}, function(data){
      parsedterms = JSON.parse(data)
      printOutEachWord(parsedterms.incorrectword);
      getDefinitionOnClick(parsedterms.incorrectword, parsedterms.incorrectdef);
    });
});

function detectIfIncorrectWordsExistOnPage (){
  if ( $('div.incorrect-word-listing').length){
    $('#wrong-words-page-header').text("You Got These Words Wrong lol");
  } else {
    $('#wrong-words-page-header').text("No Incorrect Words to Display");
  }
}

detectIfIncorrectWordsExistOnPage();

function printOutEachWord(words){
  for (var i = 0; i < words.length; i++){
    currentWord = words[i]
    $('<div class = "incorrect-word-listing"><span class = "incorrect-word">' + currentWord + "</span></div>").appendTo('#wrong-words-list-container');
    detectIfIncorrectWordsExistOnPage();
  }
}

function getDefinitionOnClick(word, definitions){
  $('.incorrect-word-listing').click( function(){
     var i = $('.incorrect-word-listing').index(this);
     currentDef = definitions[i]
     currentWord = word[i]
     $('#myModal').css("display", "flex");
     $('#modal-word').text(currentWord);
     $('#modal-def').text(currentDef);
     $('.incorrect-word-listing').css("pointer-events", "none");
  });
}

$('.close').click( function(){
  $('#myModal').css("display", "none");
  $('.incorrect-word-listing').css("pointer-events", "auto");
});

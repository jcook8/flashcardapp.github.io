$('.dropdown-content').hide();
$('.dropdown-menu').click( function (){ $('.dropdown-content').slideToggle(300)}).mouseenter( function (){ $(this).fadeTo(100, 1.0)}).mouseleave( function (){ $(this).fadeTo(200, 0.78)});
$('.le-settings').hide();
$('#settings-menu').click( function (){ $('.le-settings').slideToggle(400) });

function sendText(optiontext) {
  console.log(optiontext);
  $.post("/", {"option": optiontext}, function(data) {
    declareWhetherAnswerIsCorrectOrNotThenAddNextButton(JSON.parse(data).answer)
  });
}

function declareWhetherAnswerIsCorrectOrNotThenAddNextButton(responseFromPyFile){
    console.log(responseFromPyFile);
    console.log(lastClicked);
    correctness = null;
    if (responseFromPyFile == "True") {
        $('#' + lastClicked).addClass('correctOption').find('li').css("border-color", "white");
        correctness = "True"
        console.log(correctness)
    } else if (responseFromPyFile == "False"){
        $('#' + lastClicked).addClass('incorrectOption').find('li').css("border-color", "white");
        correctness = "False"
        console.log(correctness)
    }
    $.post("/", {"selection": correctness}, function(data) {
        console.log(data);
        $('#scoreNum').text(JSON.parse(data).newscore);
        window.location = "/";
    });
}
var lastClicked;
function sendOptionA(){
  sendText( $('#option-one').text());
}

function sendOptionB(){
  sendText( $('#option-two').text());
}

function sendOptionC(){
  sendText( $('#option-three').text());
}

function sendOptionD(){
  sendText( $('#option-four').text());
}

function setupHandlersWhenYouChooseAnAnswer(){
  $('#optionA').click( function(){
    lastClicked = $(this).attr('id');
    sendOptionA();
  });
  $('#optionB').click( function(){
    lastClicked = $(this).attr('id');
    sendOptionB();
  });
  $('#optionC').click( function(){
    lastClicked = $(this).attr('id');
    sendOptionC();
  });
  $('#optionD').click( function(){
    lastClicked = $(this).attr('id');
    sendOptionD();
  });
}

$(document).ready(setupHandlersWhenYouChooseAnAnswer);

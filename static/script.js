$('.dropdown-content').hide();
$('.dropdown-menu').click( function (){ $('.dropdown-content').slideToggle(300)}).mouseenter( function (){ $(this).fadeTo(100, 1.0)}).mouseleave( function (){ $(this).fadeTo(200, 0.78)});

function sendText(optiontext) {
  console.log(optiontext);
  $.post("/", {"option": optiontext}, function(data) {
    declareWhetherAnswerIsCorrectOrNotThenAddNextButton(JSON.parse(data).answer)
  });
}
$('#next').hide()
$('#redo-wrong').hide()
function declareWhetherAnswerIsCorrectOrNotThenAddNextButton(responseFromPyFile){

    console.log(responseFromPyFile);
    console.log(lastClicked);
    correctness = null;
    if (responseFromPyFile == "True") {
      $('#' + lastClicked).addClass('correctOption').find('li').css("border-color", "white");
        $('#' + lastClicked).addClass('correctOption').find('li').css("border-color", "white");
        correctness = "True"
        console.log(correctness)
    } else if (responseFromPyFile == "False"){
        $('#' + lastClicked).addClass('incorrectOption').find('li').css("border-color", "white");
        correctness = "False"
        console.log(correctness)
    }
    $.post("/", {"selection": correctness}, function(data) {
        parsedscore = JSON.parse(data)
        console.log(parsedscore.scorekeep);
        console.log(parsedscore.newscore);
        $('#scoreNum').text(JSON.parse(data).newscore);
        testNumberOfNexts(parsedscore.scorekeep, parsedscore.newscore, 5);
    });
    $('.options-container').css("pointer-events", "none");
    $('#nextButtonPlaceholder').hide()
    $('#next').show()
    $('#next').click( function (){
        window.location.assign("/");
    });
}

function defineTheTwoButtonsAndShowThem (){
  $('#redo-wrong').fadeIn(300);
  $('#redo').click( function(){
    window.location.assign("/");
    $.post("/", {"reset": "Reset"}, function(data){
        console.log(JSON.parse(data).newscore)
    });
  });
  $('#wrong').click( function(){
    window.location.assign("/wrong");
  });
}

function testNumberOfNexts(scoreKeep, score, numRounds){
  if (scoreKeep == numRounds){
    $('#next').hide()
    setTimeout( function (){
      $('#for-show-and-hide').hide()
      $('#word').text("Your score was " + score + " out of " + numRounds + ".").css("font-size", "4vw")},
      2000);
    setTimeout( function(){
      defineTheTwoButtonsAndShowThem()
    }, 3000);
  }
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
  $('#signOut').hide();
}

$(document).ready(setupHandlersWhenYouChooseAnAnswer);

function onSignIn(googleUser) {
  console.log(googleUser);
  var profile = googleUser.getBasicProfile();
  var id_token = profile.getId();
  console.log(id_token);
  var nickname = "cheese";
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  $.post("/", {"IDs": id_token, "nick": nickname}, function(data){
     console.log(data);
  });
}
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
  $('#signOut').hide();
  $('#my-signin2').show();
  $.post("/", {"userSignedOut": "True"}, function(data){
      console.log(data);
  });
}

function onSuccess(googleUser) {
  console.log('Logged in as: ' + googleUser.getBasicProfile().getName());
  onSignIn(googleUser);
  $('#my-signin2').hide();
  $('#signOut').show()
}
function onFailure(error) {
  console.log(error);
}
function renderButton() {
  gapi.signin2.render('my-signin2', {
    'scope': 'profile email',
    'width': 150,
    'height': 60,
    'longtitle': false,
    'theme': 'light',
    'onsuccess': onSuccess,
    'onfailure': onFailure
  });
}

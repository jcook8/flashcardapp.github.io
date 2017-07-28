$('.dropdown-content').hide();
$('.dropdown-menu').click( function (){ $('.dropdown-content').slideToggle(300)}).mouseenter( function (){ $(this).fadeTo(100, 1.0)}).mouseleave( function (){ $(this).fadeTo(200, 0.78)});

function sendText(optiontext) {
  console.log(optiontext);
  $.post("/", {"option": optiontext}, function(data) {
    declareWhetherAnswerIsCorrectOrNotThenAddNextButton(JSON.parse(data).answer)
  });
}
$('#next').hide()
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
        console.log(data);
        $('#scoreNum').text(JSON.parse(data).newscore);
    });
    $('.options-container').css("pointer-events", "none");
    $('#nextButtonPlaceholder').hide()
    $('#next').show()
    $('#next').click( function (){
      window.location.assign("/")
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

$('#signOut').hide();

function showSignOutButton(){
    $('#signOut').show();
}

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
}
function onSuccess(googleUser) {
  console.log('Logged in as: ' + googleUser.getBasicProfile().getName());
  onSignIn(googleUser);
  $('#my-signin2').hide();
  showSignOutButton();
}
function onFailure(error) {
  console.log(error);
}
function renderButton() {
  gapi.signin2.render('my-signin2', {
    'scope': 'profile email',
    'width': 150,
    'height': 54,
    'longtitle': false,
    'theme': 'light',
    'onsuccess': onSuccess,
    'onfailure': onFailure
  });
}

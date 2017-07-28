$('.dropdown-content').hide();
$('.dropdown-menu').click( function (){ $('.dropdown-content').slideToggle(300)}).mouseenter( function (){ $(this).fadeTo(100, 1.0)}).mouseleave( function (){ $(this).fadeTo(200, 0.78)});

$.post("/wrong", {"getresponse": "True"}, function(data){
    someFunction(JSON.parse(data).incorrect)
});

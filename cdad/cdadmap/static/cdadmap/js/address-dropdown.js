/**
 * popup.js: controls the showing, hiding and content in the popup from the bottom
 * Author: NiJeL
 */


$( document ).ready(function() {					

	$("#topBarSelection li a").click(function(){
		// remove all chosen classes
		$(this).parents('ul').find(".menu-item").removeClass("chosen");
		// add chosen class to this menu item
		$(this).parent().addClass("chosen");
		var selText = $(this).text();
		$(this).parents('.dropdown').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
	});

});
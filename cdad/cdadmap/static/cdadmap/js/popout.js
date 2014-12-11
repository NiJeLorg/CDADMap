/**
 * popout.js: controls the showing, hiding and content in the popout
 * Author: NiJeL
 */


$( document ).ready(function() {
					
	$( ".settings" ).click(function() {		

		// populate banner				
		$( "#banner-text" ).html("SETTINGS");
		
		// ensure the correct content is showing
		$( "#popout-settings-content" ).show();
		$( "#popout-info-content" ).hide();
		$( "#popout-filters-content" ).hide();
		$( "#popout-about-content" ).hide();
		
		if ($( ".popout-banner" ).hasClass( "popout-banner-open" ) && $( ".settings" ).hasClass( "active" ) == false) {
			// don't toggle classes
		} else {
			$( ".popout-banner" ).toggleClass("popout-banner-open");		
			$( ".popout-content" ).toggleClass("popout-content-open");								
		}
		
		// set actives for next click
		$( ".settings" ).toggleClass("active");
		$( ".info" ).removeClass("active");
		$( ".filters" ).removeClass("active");
		$( ".about" ).removeClass("active");
		
		// create scrollbars
		$( "#popout-settings-content" ).perfectScrollbar({
			suppressScrollX: true,
			includePadding: true
		});
		
		// show yellow bar if scrollbar isn't on
		if ($( "#popout-settings-content" ).hasClass( "ps-active-y" )) {
			$( ".right-bar-color" ).hide();
		} else {
			$( ".right-bar-color" ).show();			
		}
		
				
	});
	
	$( ".info" ).click(function() {		
		
		// populate banner				
		$( "#banner-text" ).html("INFO");

		// ensure the correct content is showing
		$( "#popout-info-content" ).show();
		$( "#popout-settings-content" ).hide();
		$( "#popout-filters-content" ).hide();
		$( "#popout-about-content" ).hide();
		
		if ($( ".popout-banner" ).hasClass( "popout-banner-open" ) && $( ".info" ).hasClass( "active" ) == false) {
			// don't toggle classes
		} else {
			$( ".popout-banner" ).toggleClass("popout-banner-open");		
			$( ".popout-content" ).toggleClass("popout-content-open");								
		}		
		
		// set actives for next click
		$( ".info" ).toggleClass("active");
		$( ".settings" ).removeClass("active");
		$( ".filters" ).removeClass("active");
		$( ".about" ).removeClass("active");
		
		// create scrollbars
		$( "#popout-info-content" ).perfectScrollbar({
			suppressScrollX: true,
			includePadding: true
		});
		
		// show yellow bar if scrollbar isn't on
		if ($( "#popout-info-content" ).hasClass( "ps-active-y" )) {
			$( ".right-bar-color" ).hide();
		} else {
			$( ".right-bar-color" ).show();			
		}
		
	});
	
	$( ".filters" ).click(function() {		
		
		// populate banner				
		$( "#banner-text" ).html("FILTERS");

		// ensure the correct content is showing
		$( "#popout-filters-content" ).show();
		$( "#popout-info-content" ).hide();
		$( "#popout-settings-content" ).hide();
		$( "#popout-about-content" ).hide();
		
		if ($( ".popout-banner" ).hasClass( "popout-banner-open" ) && $( ".filters" ).hasClass( "active" ) == false) {
			// don't toggle classes
		} else {
			$( ".popout-banner" ).toggleClass("popout-banner-open");		
			$( ".popout-content" ).toggleClass("popout-content-open");								
		}				

		// set actives for next click
		$( ".filters" ).toggleClass("active");
		$( ".info" ).removeClass("active");
		$( ".settings" ).removeClass("active");
		$( ".about" ).removeClass("active");
		
		// create scrollbars
		$( "#popout-filters-content" ).perfectScrollbar({
			suppressScrollX: true,
			includePadding: true
		});
		
		// show yellow bar if scrollbar isn't on
		if ($( "#popout-filters-content" ).hasClass( "ps-active-y" )) {
			$( ".right-bar-color" ).hide();
		} else {
			$( ".right-bar-color" ).show();			
		}
				
	});
	
	$( ".about" ).click(function() {

		// populate banner				
		$( "#banner-text" ).html("ABOUT");

		// ensure the correct content is showing
		$( "#popout-about-content" ).show();
		$( "#popout-info-content" ).hide();
		$( "#popout-filters-content" ).hide();
		$( "#popout-settings-content" ).hide();
		
		if ($( ".popout-banner" ).hasClass( "popout-banner-open" ) && $( ".about" ).hasClass( "active" ) == false) {
			// don't toggle classes
		} else {
			$( ".popout-banner" ).toggleClass("popout-banner-open");		
			$( ".popout-content" ).toggleClass("popout-content-open");								
		}

		// set actives for next click
		$( ".about" ).toggleClass("active");
		$( ".info" ).removeClass("active");
		$( ".filters" ).removeClass("active");
		$( ".settings" ).removeClass("active");
		
		// create scrollbars
		$( "#popout-about-content" ).perfectScrollbar({
			suppressScrollX: true,
			includePadding: true
		});
		
		// show yellow bar if scrollbar isn't on
		if ($( "#popout-about-content" ).hasClass( "ps-active-y" )) {
			$( ".right-bar-color" ).hide();
		} else {
			$( ".right-bar-color" ).show();			
		}
				
	});
	
	
});
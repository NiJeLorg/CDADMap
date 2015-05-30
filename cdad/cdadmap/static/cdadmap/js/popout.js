/**
 * popout.js: controls the showing, hiding and content in the popout
 * Author: NiJeL
 */


function CDADMapPopout() {

	// ensure all menu's content is hidden on page load
	$( "#popout-settings-content" ).hide();
	$( "#popout-info-content" ).hide();
	$( "#popout-filters-content" ).hide();
	$( "#popout-about-content" ).hide();
	
	// clear all fliters if clicked
	$( "#clearFilters" ).click(function() {	
		$( "input:checked" ).attr("checked", false);
		CDADMapPopout.onFilterChange();
	});
	

					
	$( ".settings" ).click(function() {		

		// populate banner				
		$( "#banner-text" ).html("SETTINGS");
		
		// remove info content if any
		$( "#popout-info-content" ).html('');
		
		// ensure the correct content is showing
		$( "#popout-settings-content" ).toggle();
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

		// set class for popup box at the bottom for scrolling
		CDADMapPopout.checkPopoutOpen();
				
	});
	
	$( ".info" ).click(function() {

		// do nothing if there is no content 
		if ($( "#popout-info-content" ).html().length > 0) {
			// populate banner				
			$( "#banner-text" ).html("INFO");

			// ensure the correct content is showing
			$( "#popout-info-content" ).toggle();
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

			CDADMapPopout.checkPopoutOpen();

		}
		
	});
	
	$( ".filters" ).click(function() {		
		
		// populate banner				
		$( "#banner-text" ).html("FILTERS");
		
		// remove info content if any
		$( "#popout-info-content" ).html('');

		// ensure the correct content is showing
		$( "#popout-filters-content" ).toggle();
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

		CDADMapPopout.checkPopoutOpen();
				
	});
	
	$( ".about" ).click(function() {

		// populate banner				
		$( "#banner-text" ).html("ABOUT");
		
		// remove info content if any
		$( "#popout-info-content" ).html('');

		// ensure the correct content is showing
		$( "#popout-about-content" ).toggle();
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

		CDADMapPopout.checkPopoutOpen();
				
	});
	
	// map background button group
	// ensure the map buttion is active on page load
	$( "#CartoDBLayer" ).addClass('active');
	
	$( "#CartoDBLayer" ).click(function() {
		if (!$( "#CartoDBLayer" ).hasClass( "active" )) {
			$( "#CartoDBLayer").addClass('active');
			$( "#osmTileSat" ).removeClass('active');
			$( "#osmTileMap" ).removeClass('active');
			CDADMap.switchMaps('CartoDBLayer');			
		}
	});

	$( "#osmTileSat" ).click(function() {
		if (!$( "#osmTileSat" ).hasClass( "active" )) {
			$( "#osmTileSat" ).addClass('active');
			$( "#CartoDBLayer" ).removeClass('active');
			$( "#osmTileMap" ).removeClass('active');
			CDADMap.switchMaps('osmTileSat');			
		}
	});

	$( "#osmTileMap" ).click(function() {
		if (!$( "#osmTileMap" ).hasClass( "active" )) {
			$( "#osmTileMap" ).addClass('active');
			$( "#CartoDBLayer" ).removeClass('active');
			$( "#osmTileSat" ).removeClass('active');
			CDADMap.switchMaps('osmTileMap');			
		}
	});
	
	
	// toggle off and on map background layers in settings
	$( "#DetroitBoundary" ).click(function() {
		if ($( "#DetroitBoundary" ).hasClass( "toggle-off" )) {
			$( "#DetroitBoundary" ).removeClass('toggle-off');
			$( "#DetroitBoundary" ).addClass('toggle-on');
			CDADMap.loadLayerFor('DetroitBoundary');			
		} else {
			$( "#DetroitBoundary" ).removeClass('toggle-on');			
			$( "#DetroitBoundary" ).addClass('toggle-off');
			CDADMap.removeLayerFor('DetroitBoundary');
		}
	});

	$( "#CouncilDistrictBoundaries" ).click(function() {
		if ($( "#CouncilDistrictBoundaries" ).hasClass( "toggle-off" )) {
			$( "#CouncilDistrictBoundaries" ).removeClass('toggle-off');
			$( "#CouncilDistrictBoundaries" ).addClass('toggle-on');
			CDADMap.loadLayerFor('CouncilDistrictBoundaries');			
		} else {
			$( "#CouncilDistrictBoundaries" ).removeClass('toggle-on');			
			$( "#CouncilDistrictBoundaries" ).addClass('toggle-off');
			CDADMap.removeLayerFor('CouncilDistrictBoundaries');
		}
	});
	
	$( "#NeighborhoodBoundaries" ).click(function() {
		if ($( "#NeighborhoodBoundaries" ).hasClass( "toggle-off" )) {
			$( "#NeighborhoodBoundaries" ).removeClass('toggle-off');
			$( "#NeighborhoodBoundaries" ).addClass('toggle-on');
			CDADMap.loadLayerFor('NeighborhoodBoundaries');			
		} else {
			$( "#NeighborhoodBoundaries" ).removeClass('toggle-on');			
			$( "#NeighborhoodBoundaries" ).addClass('toggle-off');
			CDADMap.removeLayerFor('NeighborhoodBoundaries');
		}
	});
	
	$( "#ZipCodeBoundaries" ).click(function() {
		if ($( "#ZipCodeBoundaries" ).hasClass( "toggle-off" )) {
			$( "#ZipCodeBoundaries" ).removeClass('toggle-off');
			$( "#ZipCodeBoundaries" ).addClass('toggle-on');
			CDADMap.loadLayerFor('ZipCodeBoundaries');			
		} else {
			$( "#ZipCodeBoundaries" ).removeClass('toggle-on');			
			$( "#ZipCodeBoundaries" ).addClass('toggle-off');
			CDADMap.removeLayerFor('ZipCodeBoundaries');
		}
	});

	$( "#CDOBC" ).click(function() {
		if ($( "#CDOBC" ).hasClass( "toggle-off" )) {
			$( "#CDOBC" ).removeClass('toggle-off');
			$( "#CDOBC" ).addClass('toggle-on');
			CDADMap.loadLayerFor('CDOBC');			
		} else {
			$( "#CDOBC" ).removeClass('toggle-on');			
			$( "#CDOBC" ).addClass('toggle-off');
			CDADMap.removeLayerFor('CDOBC');
		}
	});
	

	// set up listeners to detect changes in checkbox toggling for filtering data
	// add event listeners to run functions on change
	$("#accordion").on("change", function(e){
		CDADMapPopout.onFilterChange();
	});

}	

CDADMapPopout.checkPopoutOpen = function () {
	if ($( ".popout-banner" ).hasClass( "popout-banner-open" )) {
		$("#popup-wrapper").css("right", "442px");
	} else {
		$("#popup-wrapper").css("right", "140px");
	}		
}	

CDADMapPopout.onFilterChange = function (){
	//get keyword
	var keyword = '';
	if ($("#liKeyword").hasClass("chosen")) {
		// get value
		keyword = $('.leaflet-control-geocoder-form input').val();	
	} 

	var Organization_Description_Choices = [];
	var Service_Area_Choices = [];
	var organization_structured_Choices = [];
	var Activities_Services_Choices = [];
	var Service_Population_Choices = [];
	var Languages_Choices = [];
	var cdadmebership = [];

	// select all checked and iterate through each checked value and bin into categories
	$( "input:checked" ).each(function() {				
		if ($( this ).attr('class') === "Organization_Description_Choices") {
			Organization_Description_Choices.push($( this ).attr('value'));
		}
		if ($( this ).attr('class') === "Service_Area_Choices") {
			Service_Area_Choices.push($( this ).attr('value'));
		}
		if ($( this ).attr('class') === "organization_structured_Choices") {
			organization_structured_Choices.push($( this ).attr('value'));
		}
		if ($( this ).attr('class') === "Activities_Services_Choices") {
			Activities_Services_Choices.push($( this ).attr('value'));
		}
		if ($( this ).attr('class') === "Service_Population_Choices") {
			Service_Population_Choices.push($( this ).attr('value'));
		}
		if ($( this ).attr('class') === "Languages_Choices") {
			Languages_Choices.push($( this ).attr('value'));
		}
		if ($( this ).attr('class') === "cdadmebership") {
			cdadmebership.push($( this ).attr('value'));
		}

	});

	// create comma delimited strings
	Organization_Description_Choices_String = Organization_Description_Choices.join("|");
	Service_Area_Choices_String = Service_Area_Choices.join("|");
	organization_structured_Choices_String = organization_structured_Choices.join("|");
	Activities_Services_Choices_String = Activities_Services_Choices.join("|");
	Service_Population_Choices_String = Service_Population_Choices.join("|");
	Languages_Choices_String = Languages_Choices.join("|");
	cdadmebership_String = cdadmebership.join("|");

    //reload map data
    CDADMapPopout.loadData(Organization_Description_Choices, Service_Area_Choices, organization_structured_Choices, Activities_Services_Choices, Service_Population_Choices, Languages_Choices, cdadmebership, Organization_Description_Choices_String, Service_Area_Choices_String, organization_structured_Choices_String, Activities_Services_Choices_String, Service_Population_Choices_String, Languages_Choices_String, cdadmebership_String, keyword);

}

	// ajax call to server to reload data when filters are chosen
CDADMapPopout.loadData = function (Organization_Description_Choices, Service_Area_Choices, organization_structured_Choices, Activities_Services_Choices, Service_Population_Choices, Languages_Choices, cdadmebership, Organization_Description_Choices_String, Service_Area_Choices_String, organization_structured_Choices_String, Activities_Services_Choices_String, Service_Population_Choices_String, Languages_Choices_String, cdadmebership_String, keyword){
    $.ajax({
        type: 'GET',
        url:  'filter/?Organization_Description_Choices=' + Organization_Description_Choices_String + '&Service_Area_Choices=' + Service_Area_Choices_String + '&organization_structured_Choices=' + organization_structured_Choices_String + '&Activities_Services_Choices=' + Activities_Services_Choices_String + '&Service_Population_Choices=' + Service_Population_Choices_String + '&Languages_Choices=' + Languages_Choices_String + '&cdadmebership=' + cdadmebership_String + '&keyword=' + keyword + '&template=locations',
        success: function(data){
        	//console.log(data);
        	// remove locations from map
        	CDADMap.clearLocationsLayers();
        	// parse new incoming geojson
        	var geoJSON = $.parseJSON( data );
        	// rebuild the geoJSON files with new data
			CDADMap.loadFilteredLocations(geoJSON);

			// remove polygons from cdad block groups layer
        	CDADMap.clearCDOBGLayer();

        	// load only ploygons that match the filtered dataset
        	CDADMap.loadFilteredCDOBGLayer(geoJSON);

        }
    });

	// second ajax call to reload the popup data when filters are chosen
    $.ajax({
        type: 'GET',
        url:  'filter/?Organization_Description_Choices=' + Organization_Description_Choices_String + '&Service_Area_Choices=' + Service_Area_Choices_String + '&organization_structured_Choices=' + organization_structured_Choices_String + '&Activities_Services_Choices=' + Activities_Services_Choices_String + '&Service_Population_Choices=' + Service_Population_Choices_String + '&Languages_Choices=' + Languages_Choices_String + '&cdadmebership=' + cdadmebership_String + '&keyword=' + keyword + '&template=popup',
        success: function(data){
        	// remove data in popup content
        	$("#popup-wrapper").html('');
        	// add new data to popup content
			$("#popup-wrapper").html(data);

			CDADMapPopout.setFiltersInPopup(Organization_Description_Choices, Service_Area_Choices, organization_structured_Choices, Activities_Services_Choices, Service_Population_Choices, Languages_Choices, cdadmebership, keyword);

			// open list below the map
			if ($( ".popup-wrapper" ).hasClass( "popup-wrapper-open" )) {
				// don't toggle classes
			} else {
				$( ".popup-wrapper" ).toggleClass("popup-wrapper-open");			
			}

        }
    });

	// third ajax call to reload the modals
    $.ajax({
        type: 'GET',
        url:  'filter/?Organization_Description_Choices=' + Organization_Description_Choices_String + '&Service_Area_Choices=' + Service_Area_Choices_String + '&organization_structured_Choices=' + organization_structured_Choices_String + '&Activities_Services_Choices=' + Activities_Services_Choices_String + '&Service_Population_Choices=' + Service_Population_Choices_String + '&Languages_Choices=' + Languages_Choices_String + '&cdadmebership=' + cdadmebership_String + '&keyword=' + keyword + '&template=modals',
        success: function(data){
        	// remove data in popup content
        	$("#modal-wrapper").html('');
        	// add new data to popup content
			$("#modal-wrapper").html(data);

        }
    });

	
}

CDADMapPopout.setFiltersInPopup = function(Organization_Description_Choices, Service_Area_Choices, organization_structured_Choices, Activities_Services_Choices, Service_Population_Choices, Languages_Choices, cdadmebership, keyword){
	if ((Organization_Description_Choices.length > 0) || (Service_Area_Choices.length > 0) || (organization_structured_Choices.length > 0) || (Activities_Services_Choices.length > 0) || (Service_Population_Choices.length > 0) || (Languages_Choices.length > 0) || (cdadmebership.length > 0)) {
		$("#popup-filters").append('<span class="popup-filters">Filters applied: </span>');
	}


	// set filters labels in the popup window for each filter selected
	$.each(Organization_Description_Choices, function( index, value ) {
		$("#popup-filters").append('<span class="label label-filter label-orgtype">' + value + '</span>');
	});
	$.each(Service_Area_Choices, function( index, value ) {
		$("#popup-filters").append('<span class="label label-filter label-servicearea">' + value + '</span>');
	});
	$.each(organization_structured_Choices, function( index, value ) {
		$("#popup-filters").append('<span class="label label-filter label-orgstructure">' + value + '</span>');
	});
	$.each(Activities_Services_Choices, function( index, value ) {
		$("#popup-filters").append('<span class="label label-filter label-activityservice">' + value + '</span>');
	});
	$.each(Service_Population_Choices, function( index, value ) {
		$("#popup-filters").append('<span class="label label-filter label-servicepop">' + value + '</span>');
	});
	$.each(Languages_Choices, function( index, value ) {
		$("#popup-filters").append('<span class="label label-filter label-language">' + value + '</span>');
	});
	$.each(cdadmebership, function( index, value ) {
		if (value == 'Yes') {
			$("#popup-filters").append('<span class="label label-filter label-cdadmebership">CDAD Members</span>');
		} else {
			$("#popup-filters").append('<span class="label label-filter label-cdadmebership">Not CDAD Members</span>');

		}
	});

}
	

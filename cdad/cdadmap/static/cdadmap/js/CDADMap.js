/* 
* Functions to create the main CDAD Map
*/

// initialize map
function CDADMap() {
	
    //where detroit is 42.377410, -83.093719
    this.map = new L.Map('map', {
		minZoom:10,
		maxZoom:17,
    	center: [42.307410, -83.043719],
   	 	zoom: 11,
	});
	
	// add CartoDB tiles
	this.CartoDBLayer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',{
	  attribution: 'Map Data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> Contributors, Map Tiles &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
	});
	
	// define areial tiles for future use
	this.osmTileSat = L.tileLayer('http://otile4.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg', {
	    attribution: '&copy; <a href="http://developer.mapquest.com/web/products/open/map">MapQuest Open Aerial</a>'
	});
	
	// define Mapquest tiles for future use
	this.osmTileMap = L.tileLayer('http://otile4.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg', {
	    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors; Map Tiles &copy;  <a href="http://developer.mapquest.com/web/products/open/map">MapQuest</a>'
	});

	this.map.attributionControl.setPosition('bottomleft');
	
	// add cartoDB tiles to start
	this.map.addLayer(this.CartoDBLayer);
	
	//load geocoder control
	this.map.addControl(L.Control.geocoder({collapsed: false, placeholder:'', geocoder:new L.Control.Geocoder.Google(GEOCODER_API_KEY)}));
	
	//load scale bars
	this.map.addControl(L.control.scale());
	
    // enable events
    this.map.doubleClickZoom.enable();
    this.map.scrollWheelZoom.enable();
	
	// create empty container for locations
	this.LOCATIONS = null;
	
	// empty containers for other layers 
	this.DETLAYER = null;
	this.CDBLAYER = null;
	this.NBLAYER = null;
	this.ZCBLAYER = null;
	this.CDOBCLAYER = null;
	this.CDOBCLAYER_geojsons = null;
	
	// marker cluster options
	clusterLocations = L.markerClusterGroup({ 
		showCoverageOnHover: false, 
		maxClusterRadius: 40
	});
	
	// popup container to catch on hover popups	
	this.popup = new L.Popup({ 
		autoPan: false, 
		maxWidth: 300,
		minWidth: 100, 
		minHeight: 30,
		closeButton:true 
	});


}


// map switcher
CDADMap.switchMaps = function (id){
	
	// remove all basemap layers if they exist
	if (MY_MAP.map.hasLayer(MY_MAP.CartoDBLayer)) {
		MY_MAP.map.removeLayer(MY_MAP.CartoDBLayer);
	}

	if (MY_MAP.map.hasLayer(MY_MAP.osmTileSat)) {
		MY_MAP.map.removeLayer(MY_MAP.osmTileSat);
	}

	if (MY_MAP.map.hasLayer(MY_MAP.osmTileMap)) {
		MY_MAP.map.removeLayer(MY_MAP.osmTileMap);
	}
	
	if (id == 'CartoDBLayer') {
		MY_MAP.map.addLayer(MY_MAP.CartoDBLayer);
	} else if (id == 'osmTileSat') {
		MY_MAP.map.addLayer(MY_MAP.osmTileSat);
	} else if (id == 'osmTileMap') {
		MY_MAP.map.addLayer(MY_MAP.osmTileMap);		
	}
	
			
}



CDADMap.onEachFeature_CDBLAYER = function(feature,layer){	
	var highlight = {
	    weight: 4,
	    opacity: 1
	};
	var noHighlight = {
        weight: 2,
        opacity: 0.75
	};

	layer.bindLabel(CDADMap.CouncilDistrictNames(feature.id), { direction:'auto' });
	
    //add on hover -- same on hover and mousemove for each layer
    layer.on('mouseover', function(ev) {
		//highlight polygon
		layer.setStyle(highlight);			
    });
	
	
    layer.on('mouseout', function(ev) {
		//remove highlight for polygon
		layer.setStyle(noHighlight);
		
    });	

	
}

CDADMap.onEachFeature_NBLAYER = function(feature,layer){	
	var highlight = {
	    weight: 4,
	    opacity: 1
	};
	var noHighlight = {
        weight: 2,
        opacity: 0.75
	};

	layer.bindLabel(feature.id, { direction:'auto' });

	
    //add on hover -- same on hover and mousemove for each layer
    layer.on('mouseover', function(ev) {
		//highlight polygon
		layer.setStyle(highlight);				
    });
	
    layer.on('mouseout', function(ev) {
		//remove highlight for polygon
		layer.setStyle(noHighlight);
    });	
		
}


CDADMap.onEachFeature_ZCBLAYER = function(feature,layer){	
	var highlight = {
	    weight: 4,
	    opacity: 1
	};
	var noHighlight = {
        weight: 2,
        opacity: 0.75
	};

	layer.bindLabel(feature.id, { direction:'auto' });
	// set so labels are not hidden

    //add on hover -- same on hover and mousemove for each layer
    layer.on('mouseover', function(ev) {		
		//highlight polygon
		layer.setStyle(highlight);				
    });
	
	
    layer.on('mouseout', function(ev) {
		//remove highlight for polygon
		layer.setStyle(noHighlight);		
    });	
	
}

CDADMap.onEachFeature_CDOBCLAYER = function(feature,layer){	
	var highlight = {
	    weight: 4,
	    opacity: 1
	};
	var noHighlight = {
        weight: 2,
        opacity: 0.75
	};

	layer.bindLabel(feature.properties.OrgName, { direction:'auto' });
	
    //add on hover -- same on hover and mousemove for each layer
    layer.on('mouseover', function(ev) {		
		//highlight polygon
		layer.setStyle(highlight);
    });
	
    layer.on('mouseout', function(ev) {
		//remove highlight for polygon
		layer.setStyle(noHighlight);
		layer.bringToBack();
		CDADMap.sendLayersToBack();	
    });	

	// ajax to bind data on click to the feature
	$.ajax({
		type: "GET",
		url: "/getlocationdataforcdobclayer/?Organization_Name="+ feature.properties.OrgName,
		success: function(data){
			// bind in the items on click
			if (data) {
				var result = $.grep(locations.features, function(e){ return e.properties.Organization_Name == data.Organization_Name; });
				data.counterId = result[0].properties.counterId;
				if (data.Address2) {
					data.Address2 = '<br />' + data.Address2;
				} else {
					data.Address2 = '';
				}

				layer.on("click",function(ev){
					CDADMap.sidebar(data);	
				});
			} 
        }
	});


	
}


CDADMap.loadLayers = function (){
	// load topoJSON data
	// path to data defined in index.html django template

	// define layer styles and oneachfeature popup styling
	MY_MAP.DETLAYER_style = L.geoJson(null, {
	    style: CDADMap.getStyleColorFor_DETLAYER,
	});

	MY_MAP.CDBLAYER_style = L.geoJson(null, {
	    style: CDADMap.getStyleColorFor_CDBLAYER,
		onEachFeature: CDADMap.onEachFeature_CDBLAYER
	});

	MY_MAP.NBLAYER_style = L.geoJson(null, {
	    style: CDADMap.getStyleColorFor_NBLAYER,
		onEachFeature: CDADMap.onEachFeature_NBLAYER
	});

	MY_MAP.ZCBLAYER_style = L.geoJson(null, {
	    style: CDADMap.getStyleColorFor_ZCBLAYER,
		onEachFeature: CDADMap.onEachFeature_ZCBLAYER
	});
			
	// load layers
	MY_MAP.DETLAYER = omnivore.topojson(detlayer, null, MY_MAP.DETLAYER_style);
	MY_MAP.CDBLAYER = omnivore.topojson(cdblayer, null, MY_MAP.CDBLAYER_style);
	MY_MAP.NBLAYER = omnivore.topojson(nblayer, null, MY_MAP.NBLAYER_style);
	MY_MAP.ZCBLAYER = omnivore.topojson(zcblayer, null, MY_MAP.ZCBLAYER_style);

	// create a feature group layer for all of the service area polygons
	MY_MAP.CDOBCLAYER = L.featureGroup();

	// for loop to open, parse and add each layer to the feature group set above
	for (var i = staticGeoJSON.length - 1; i >= 0; i--) {
		$.ajax({
			type: "GET",
			url: "/getjsonformap/"+ staticGeoJSON[i] +"/",
			success: function(data){
				// load the draw tools
				if (data) {
					var geojson = JSON.parse(data);

					var saGeoJSON = L.geoJson(geojson, {
				        style: CDADMap.getStyleColorFor_CDOBCLAYER,
				        onEachFeature: CDADMap.onEachFeature_CDOBCLAYER
				    });

				    // add to the feature group
					MY_MAP.CDOBCLAYER.addLayer(saGeoJSON);

				} 
	        }
		});
	
	};
		
}


CDADMap.getStyleColorFor_DETLAYER = function (feature){
    return {
        weight: 5,
        opacity: 1,
        color: '#252525',
        fillOpacity: 0
    }
}

CDADMap.getStyleColorFor_CDBLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: CDADMap.CouncilDistrictColors(feature.id),
        fillOpacity: 0.25,
        fill: CDADMap.CouncilDistrictColors(feature.id)
    }
}

CDADMap.getStyleColorFor_NBLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: '#7fc97f',
        fillOpacity: 0.25,
        fill: '#7fc97f'
    }
}

CDADMap.getStyleColorFor_ZCBLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: '#beaed4',
        fillOpacity: 0.25,
        fill: '#beaed4'
    }
}

CDADMap.getStyleColorFor_CDOBCLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: '#e8c51d',
        fillOpacity: 0.5,
        fill: '#e8c51d'
    }
}

CDADMap.CouncilDistrictColors = function (d){
    return d == "D1" ? '#dbec3b' :
           d == "D2" ? '#73a40a' :
           d == "D3" ? '#ffab00' :
           d == "D4" ? '#004da9' :
           d == "D5" ? '#d41711' :
           d == "D6" ? '#68e3ff' :
           d == "D7" ? '#790398' :
                    '#000';	
}

CDADMap.CouncilDistrictNames = function (d){
    return d == "D1" ? 'District 1' :
           d == "D2" ? 'District 2' :
           d == "D3" ? 'District 3' :
           d == "D4" ? 'District 4' :
           d == "D5" ? 'District 5' :
           d == "D6" ? 'District 6' :
           d == "D7" ? 'District 7' :
                    '';	
}


CDADMap.onEachFeatureFor_LOCATIONS = function(feature, layer){

	if (feature.properties.Address2) {
		feature.properties.Address2 = '<br />' + feature.properties.Address2;
	} else {
		feature.properties.Address2 = '';
	}

	if (feature.properties.Address) {
		var address = '<br />' + feature.properties.Address + ' ' + feature.properties.Address2 + '<br />' + feature.properties.City + ', ' + feature.properties.State + ' ' + feature.properties.ZipCode;
	} else {
		var address = '';
	}

	layer.bindLabel('<strong>' + feature.properties.Organization_Name + '</strong>' + address, { direction:'auto', offset:[20,-30] });
		
	// add on click popups for locations -- open ino sidebar and populate with data
	layer.on("click",function(ev){
		CDADMap.sidebar(feature.properties);	
	});
	
}


CDADMap.sidebar = function(data){

	// close all open popups
	MY_MAP.map.closePopup();
	
	// set up data for popout
	var commaSpace = /,\s/ig;
	var pipeSpace = /\|\s/ig;

	var openBracket = /\[/gi;
	var closeBracket = /\]/gi;
	var u_list = /u&#39;/gi;
	var quote_list = /&#39;/gi;

	// activities available at this location
	var activityString = data.Activity;
	if (typeof activityString === 'object') {
		var activityArray = activityString;
	} else {
		var activityArray = activityString.split(',');
	}
	var activityArrayLength = activityArray.length;
	for (var i = 0; i < activityArrayLength; i++) {
		// strip away the Python list stuff
		activityArray[i] = activityArray[i].replace(openBracket,'').replace(closeBracket,'').replace(u_list,'').replace(quote_list,'').trim()

		// wrap each item in labels
		if (activityArray[i] !== "undefined" && activityArray[i] && activityArray[i] !== "Other") {
			activityArray[i] = '<span class="label label-filter label-activity">' + activityArray[i] + '</span>';
		} else {
			activityArray[i] = '';
		}
	}
	// add other to Org Dec list
	if (data.Activity_Other) {
		// truncate string
		var length = 50;
		if (data.Activity_Other.length > length) {
			data.Activity_Other = data.Activity_Other.substring(0,length);
			data.Activity_Other = data.Activity_Other + '...';
		} 
		data.Activity_Other = '<span class="label label-filter label-activity">' + data.Activity_Other + '</span>';
		activityArray.push(data.Activity_Other);
	}

	// create list
	var activityList = activityArray.join(' ');

	
	// activities avialable at this location 
	var activities_ServicesString = data.Activities_Services;
	var activities_ServicesArray = activities_ServicesString.split(',');
	var activities_ServicesArrayLength = activities_ServicesArray.length;
	for (var i = 0; i < activities_ServicesArrayLength; i++) {
		// strip away the Python list stuff
		activities_ServicesArray[i] = activities_ServicesArray[i].replace(openBracket,'').replace(closeBracket,'').replace(u_list,'').replace(quote_list,'').trim()

		// wrap each item in labels
		if (activities_ServicesArray[i] !== "undefined" && activities_ServicesArray[i]) {
			activities_ServicesArray[i] = '<span class="label label-filter label-activityservice">' + activities_ServicesArray[i] + '</span>';
		} else {
			activities_ServicesArray[i] = '';
		}
	}
	var activities_ServicesList = activities_ServicesArray.join(' ');

	// organization type
	var Organization_DescriptionString = data.Organization_Description;
	var Organization_DescriptionArray = Organization_DescriptionString.split(',');
	var Organization_DescriptionArrayLength = Organization_DescriptionArray.length;
	for (var i = 0; i < Organization_DescriptionArrayLength; i++) {
		// strip away the Python list stuff
		Organization_DescriptionArray[i] = Organization_DescriptionArray[i].replace(openBracket,'').replace(closeBracket,'').replace(u_list,'').replace(quote_list,'').trim()
		
		// wrap each item in labels
		if (Organization_DescriptionArray[i] !== "undefined" && Organization_DescriptionArray[i] && Organization_DescriptionArray[i] !== "Other") {
			Organization_DescriptionArray[i] = '<span class="label label-filter label-orgtype">' + Organization_DescriptionArray[i].replace(pipeSpace, ', ') + '</span>';
		} else {
			Organization_DescriptionArray[i] = '';
		}
	}
	// add other to Org Dec list
	if (data.Organization_Description_Other) {
		// truncate string
		var length = 50;
		if (data.Organization_Description_Other.length > length) {
			data.Organization_Description_Other = data.Organization_Description_Other.substring(0,length);
			data.Organization_Description_Other = data.Organization_Description_Other + '...';
		} 
		data.Organization_Description_Other = '<span class="label label-filter label-orgtype">' + data.Organization_Description_Other + '</span>';
		Organization_DescriptionArray.push(data.Organization_Description_Other);
	}

	// create list
	var Organization_DescriptionList = Organization_DescriptionArray.join(' ');

	if (typeof data.Social_website !== 'undefined' && data.Social_website) {
		var website = "<p class='info-content'><span class='glyphicon glyphicon-link'></span> <a href='" + data.Social_website + "' target=\"_blank\">" + data.Social_website + "</a></p>";
	} else {
		var website = '';
	}

	if (typeof data.Phone !== 'undefined' && data.Phone) {
		var phone = "<p class='info-content'><span class='glyphicon glyphicon-phone'></span> " + data.Phone + "</p>";
	} else {
		var phone = '';
	}

	// facebook link
	if (typeof data.Social_facebook !== 'undefined' && data.Social_facebook) {
		var fbwebsite = "<a href='" + data.Social_facebook + "' target=\"_blank\"><span class='facebook-logo'></span></a>";
	} else {
		var fbwebsite = '';
	}

	// twitter link
	if (typeof data.Social_Twitter !== 'undefined' && data.Social_Twitter) {
		var twwebsite = "<a href='" + data.Social_Twitter + "' target=\"_blank\"><span class='twitter-logo'></span></a>";
	} else {
		var twwebsite = '';
	}

	// youtube link
	if (typeof data.youtube !== 'undefined' && data.youtube) {
		var youtube = "<a href='" + data.youtube + "' target=\"_blank\"><span class='youtube-logo'></span></a>";
	} else {
		var youtube = '';
	}

	// instagram link
	if (typeof data.instagram !== 'undefined' && data.instagram) {
		var instagram = "<a href='" + data.instagram + "' target=\"_blank\"><span class='instagram-logo'></span></a>";
	} else {
		var instagram = '';
	}

	// nextdoor link
	if (typeof data.nextdoor !== 'undefined' && data.nextdoor) {
		var nextdoor = "<a href='" + data.nextdoor + "' target=\"_blank\"><span class='nextdoor-logo'></span></a>";
	} else {
		var nextdoor = '';
	}

	// if an org has an acronym, add it
	if (data.Organizaton_Acronym) {
		var acronym = " (" + data.Organizaton_Acronym + ") ";
	} else {
		var acronym = "";
	}

	// if a logo is present, print it here
	if (!data.Organization_Logo_Image || data.Organization_Logo_Image == '/media/') {
		var logo = '';
	} else {
		var logo = "<img src='" + data.Organization_Logo_Image + "' class='img-responsive margin10topbottom'/> "
	}

	// google maps link for address
	var gmapslink = "<a href='https://www.google.com/maps/place/" + data.Address + "+" + data.City + "+" + data.State + "+" + data.ZipCode + "' target='_blank'>";

	if (data.Address) {
		var address = "<p class='info-content'><span class='glyphicon glyphicon-map-marker'></span> " + gmapslink + data.Address + " " + data.Address2 + "<br />" + data.City + ", " + data.State + " " + data.ZipCode + "</a></p>";
	} else {
		var address = '';
	}
	
	// update sidebar content based on click
	$( "#popout-info-content" ).html("<div class='info-title-bar text-capitalize'>" + data.Organization_Name + acronym + "</div>"+ logo +"<div class='info-content-titles'>ORGANIZATIONAL CONTACT</div>" + address + "<p class='info-content'><span class='glyphicon glyphicon-envelope'></span> <a href='mailto:" + data.Email + "'>" + data.Email + "</a></p>" + phone + website + "<p class='info-content'>" + twwebsite + fbwebsite + youtube + instagram + nextdoor + "</p><div class='info-content-titles'>ORGANIZATION TYPE</div><p class='info-content'>" + Organization_DescriptionList + "</p><div class='info-content-titles'>ACTIVITES & SERVICES AT THIS LOCATION</div><p class='info-content'>" + activityList + "</p><div class='info-content-titles'>SERVICES THIS ORGANIZATION PROVIDES</div><p class='info-content'>" + activities_ServicesList + "</p><button type='button' class='btn btn-default btn-block' data-toggle='modal' data-target='#orgModal' data-local='#orgCarousel' id='slideTo" + data.counterId + "'><span class='pull-left'>VIEW FULL PROFILE</span><span class='glyphicon glyphicon-fullscreen pull-right' aria-hidden='true'></span></button>");
			
	var slideToIdlocation = '#slideTo' + parseInt(data.counterId);
	$(slideToIdlocation).click(function() {
		// show carousel in modal
		$( "#orgCarousel" ).show();

		// rotate carousel
		$( "#orgCarousel" ).carousel(parseInt(data.counterId));
		
		setTimeout(function() {
			
			maps[data.counterId].map.invalidateSize();

		}, 200);
		
	});
			
	// populate banner				
	$( "#banner-text" ).html("INFO");

	// ensure the correct content is showing
	$( "#popout-info-content" ).show();
	$( "#popout-settings-content" ).hide();
	$( "#popout-filters-content" ).hide();
	$( "#popout-about-content" ).hide();
	
	if ($( ".popout-banner" ).hasClass( "popout-banner-open" )) {
		// don't toggle classes
	} else {
		$( ".popout-banner" ).toggleClass("popout-banner-open");		
		$( ".popout-content" ).toggleClass("popout-content-open");								
	}		
	
	// set actives for next click
	$( ".info" ).addClass("active");
	$( ".settings" ).removeClass("active");
	$( ".filters" ).removeClass("active");
	$( ".about" ).removeClass("active");

	// set up modal for having this org selected
	$( "#titleOrgName" ).html(data.Organization_Name + acronym);

	CDADMapPopout.checkPopoutOpen();

	
	// create scrollbars
	$( "#popout-info-content" ).perfectScrollbar({
		suppressScrollX: true,
		includePadding: true
	});			
					
	$( "#popout-info-content" ).perfectScrollbar('update');

	// show yellow bar if scrollbar isn't on
	if ($( "#popout-info-content .ps-scrollbar-y-rail .ps-scrollbar-y" ).css( "height" ) == "0px") {
		$( ".right-bar-color" ).show();
	} else {
		$( ".right-bar-color" ).hide();			
	}


}


CDADMap.prototype.loadLocations = function(){
					
	this.LOCATIONS = null;

	// define layer styles and oneachfeature popup styling
	this.LOCATIONS = L.geoJson(locations, {
		pointToLayer: CDADMap.getStyleFor_LOCATIONS,
		onEachFeature: CDADMap.onEachFeatureFor_LOCATIONS
	});
	
	
	// add media to cluster library
	clusterLocations.addLayer(this.LOCATIONS);
	
}

CDADMap.getStyleFor_LOCATIONS = function(feature, latlng){
	var locationIcon = L.icon({
	    iconUrl: feature.properties.iconUrl,
	    iconSize: [24, 32],
		iconAnchor: [12, 30], 
	});

	return L.marker(latlng, {icon: locationIcon, riseOnHover: true});
	
}


CDADMap.loadFilteredLocations = function(data){
	
	MY_MAP.LOCATIONS.addData(data);
	// add media to cluster library
	clusterLocations.addLayer(MY_MAP.LOCATIONS);

}

CDADMap.loadFilteredCDOBGLayer = function(){
	
	// for loop to open, parse and add each layer to the feature group set above
	for (var i = staticGeoJSON.length - 1; i >= 0; i--) {
		$.ajax({
			type: "GET",
			url: "/getjsonformap/"+ staticGeoJSON[i] +"/",
			success: function(data){
				// load the draw tools
				if (data) {
					var geojson = JSON.parse(data);

					var saGeoJSON = L.geoJson(geojson, {
				        style: CDADMap.getStyleColorFor_CDOBCLAYER,
				        onEachFeature: CDADMap.onEachFeature_CDOBCLAYER
				    });

				    // add to the feature group
					MY_MAP.CDOBCLAYER.addLayer(saGeoJSON);

				} 
	        }
		});
	
	};


}



CDADMap.loadLayerFor = function(layerId){
	
    if(layerId == "DetroitBoundary"){
		MY_MAP.DETLAYER.addTo(MY_MAP.map).bringToBack();
	}	

    if(layerId == "CouncilDistrictBoundaries"){
		MY_MAP.CDBLAYER.addTo(MY_MAP.map).bringToFront();
		if (MY_MAP.map.hasLayer(MY_MAP.NBLAYER)) {
			MY_MAP.NBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.ZCBLAYER)) {
			MY_MAP.ZCBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.CDOBCLAYER)) {
			MY_MAP.CDOBCLAYER.bringToFront();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.DETLAYER)) {
			MY_MAP.DETLAYER.bringToBack();
		}
	}	

    if(layerId == "NeighborhoodBoundaries"){
		MY_MAP.NBLAYER.addTo(MY_MAP.map).bringToFront();
		if (MY_MAP.map.hasLayer(MY_MAP.CDBLAYER)) {
			MY_MAP.CDBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.ZCBLAYER)) {
			MY_MAP.ZCBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.CDOBCLAYER)) {
			MY_MAP.CDOBCLAYER.bringToFront();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.DETLAYER)) {
			MY_MAP.DETLAYER.bringToBack();
		}
	}	

    if(layerId == "ZipCodeBoundaries"){
		MY_MAP.ZCBLAYER.addTo(MY_MAP.map).bringToFront();
		if (MY_MAP.map.hasLayer(MY_MAP.NBLAYER)) {
			MY_MAP.NBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.CDBLAYER)) {
			MY_MAP.CDBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.CDOBCLAYER)) {
			MY_MAP.CDOBCLAYER.bringToFront();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.DETLAYER)) {
			MY_MAP.DETLAYER.bringToBack();
		}
	}	

    if(layerId == "CDOBC"){
		MY_MAP.CDOBCLAYER.addTo(MY_MAP.map).bringToFront();
		if (MY_MAP.map.hasLayer(MY_MAP.NBLAYER)) {
			MY_MAP.NBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.ZCBLAYER)) {
			MY_MAP.ZCBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.CDBLAYER)) {
			MY_MAP.CDBLAYER.bringToBack();
		}
		if (MY_MAP.map.hasLayer(MY_MAP.DETLAYER)) {
			MY_MAP.DETLAYER.bringToBack();
		}
	}

	MY_MAP.LOCATIONS.bringToFront();


}

CDADMap.sendLayersToBack = function(){
	if (MY_MAP.map.hasLayer(MY_MAP.NBLAYER)) {
		MY_MAP.NBLAYER.bringToBack();
	}
	if (MY_MAP.map.hasLayer(MY_MAP.ZCBLAYER)) {
		MY_MAP.ZCBLAYER.bringToBack();
	}
	if (MY_MAP.map.hasLayer(MY_MAP.CDBLAYER)) {
		MY_MAP.CDBLAYER.bringToBack();
	}	
	if (MY_MAP.map.hasLayer(MY_MAP.DETLAYER)) {
		MY_MAP.DETLAYER.bringToBack();
	}
}


CDADMap.prototype.showLocationsOnPageLoad = function(){
	
	// set on mouseover interaction for cluster group
	clusterLocations.on('clustermouseover', function (ev) {
		// only have on mouseover work if popup2 isn't open
		if (!MY_MAP.popup._isOpen) {
			// close all popups first
			MY_MAP.map.closePopup();
		}
	});

	clusterLocations.addTo(this.map);
	
}


CDADMap.removeLayerFor = function(layerId){
	// remove all popups first
	MY_MAP.map.closePopup();
	// then remove layer
	if (layerId == 'DetroitBoundary') {
		MY_MAP.map.removeLayer( MY_MAP.DETLAYER ); 		
	}

	if (layerId == 'CouncilDistrictBoundaries') {
		MY_MAP.map.removeLayer( MY_MAP.CDBLAYER ); 		
	}

	if (layerId == 'NeighborhoodBoundaries') {
		MY_MAP.map.removeLayer( MY_MAP.NBLAYER ); 		
	}

	if (layerId == 'ZipCodeBoundaries') {
		MY_MAP.map.removeLayer( MY_MAP.ZCBLAYER ); 		
	}

	if (layerId == 'CDOBC') {
		MY_MAP.map.removeLayer( MY_MAP.CDOBCLAYER ); 		
	}

	if (MY_MAP.map.hasLayer(MY_MAP.DETLAYER)) {
		MY_MAP.DETLAYER.bringToBack();
	}


	
}

CDADMap.removeLocationsLayers = function(){
	// remove all popups first
	MY_MAP.map.closePopup();
	// then remove media layers
	MY_MAP.map.removeLayer(clusterLocations); 

}

CDADMap.clearLocationsLayers = function(){
	// clear data out of clusterer when users select filters
	MY_MAP.LOCATIONS.clearLayers();	
	clusterLocations.clearLayers();	
	
}

CDADMap.clearCDOBGLayer = function(){
	// clear data out of CDOBG layer when user selects filter
	MY_MAP.CDOBCLAYER.clearLayers();		
	
}
	
	

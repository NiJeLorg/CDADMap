/* 
* Functions to create the main CDAD Map
*/

// initialize map
function CDADMap() {
	
    //where detroit is 42.377410, -83.093719
    this.map = new L.Map('map', {
		minZoom:10,
		maxZoom:17,
    	center: [42.377410, -83.043719],
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
	
	// add cartoDB tiles to start
	this.map.addLayer(this.CartoDBLayer);
	
	//load geocoder control
	this.map.addControl(L.Control.geocoder({collapsed: false, placeholder:'', geocoder:new L.Control.Geocoder.Google()}));
	
	//load scale bars
	this.map.addControl(L.control.scale());
	
    // enable events
    this.map.doubleClickZoom.enable();
    this.map.scrollWheelZoom.enable();
	
	// create empty container for locations
	this.LOCATIONS = null;
	
	// empty containers for ohter layers 
	this.CDBLAYER = null;
	this.NBLAYER = null;
	this.ZCBLAYER = null;
	this.CDOBCLAYER = null;
	
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
	
    //add on hover -- same on hover and mousemove for each layer
    layer.on('mouseover', function(ev) {
		
		//highlight polygon
		layer.setStyle(highlight);		
		
    });
	
	
    layer.on('mouseout', function(ev) {
		//remove highlight for polygon
		layer.setStyle(noHighlight);
		
    });	
	
	// add on click popups for each layer -- these will be different
	layer.on("click",function(ev){
		// close all open popups
		MY_MAP.map.closePopup();
		
		// bind popup with data to the feature
		MY_MAP.popup.setLatLng(MY_MAP.map.layerPointToLatLng(ev.layerPoint));
		MY_MAP.popup.setContent('<div class="rollover-tooltip">City Council District: '+ feature.id + '</div>');
		MY_MAP.popup.openOn(MY_MAP.map);
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
	
    //add on hover -- same on hover and mousemove for each layer
    layer.on('mouseover', function(ev) {
		
		//highlight polygon
		layer.setStyle(highlight);		
		
    });
	
	
    layer.on('mouseout', function(ev) {
		//remove highlight for polygon
		layer.setStyle(noHighlight);
		
    });	
	
	// add on click popups for each layer -- these will be different
	layer.on("click",function(ev){
		// close all open popups
		MY_MAP.map.closePopup();
		
		// bind popup with data to the feature
		MY_MAP.popup.setLatLng(MY_MAP.map.layerPointToLatLng(ev.layerPoint));
		MY_MAP.popup.setContent('<div class="rollover-tooltip">Neighborhood Name: '+ feature.id + '</div>');
		MY_MAP.popup.openOn(MY_MAP.map);
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
	
    //add on hover -- same on hover and mousemove for each layer
    layer.on('mouseover', function(ev) {
		
		//highlight polygon
		layer.setStyle(highlight);		
		
    });
	
	
    layer.on('mouseout', function(ev) {
		//remove highlight for polygon
		layer.setStyle(noHighlight);
		
    });	
	
	// add on click popups for each layer -- these will be different
	layer.on("click",function(ev){
		// close all open popups
		MY_MAP.map.closePopup();
		
		// bind popup with data to the feature
		MY_MAP.popup.setLatLng(MY_MAP.map.layerPointToLatLng(ev.layerPoint));
		MY_MAP.popup.setContent('<div class="rollover-tooltip">Zip Code: '+ feature.id + '</div>');
		MY_MAP.popup.openOn(MY_MAP.map);
	});
	
}


CDADMap.prototype.loadLayers = function (){
    var self = this;
		
	// load topoJSON data
	// path to data defined in index.html django template

	// define layer styles and oneachfeature popup styling
	this.CDBLAYER_style = L.geoJson(null, {
	    style: CDADMap.getStyleColorFor_CDBLAYER,
		onEachFeature: CDADMap.onEachFeature_CDBLAYER
	});

	this.NBLAYER_style = L.geoJson(null, {
	    style: CDADMap.getStyleColorFor_NBLAYER,
		onEachFeature: CDADMap.onEachFeature_NBLAYER
	});

	this.ZCBLAYER_style = L.geoJson(null, {
	    style: CDADMap.getStyleColorFor_ZCBLAYER,
		onEachFeature: CDADMap.onEachFeature_ZCBLAYER
	});
			
	// load layers
	this.CDBLAYER = omnivore.topojson(cdblayer, null, this.CDBLAYER_style);
	this.NBLAYER = omnivore.topojson(nblayer, null, this.NBLAYER_style);
	this.ZCBLAYER = omnivore.topojson(zcblayer, null, this.ZCBLAYER_style);
			
}

CDADMap.getStyleColorFor_CDBLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: '#595959',
        fillOpacity: 0
    }
}

CDADMap.getStyleColorFor_NBLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: '#e8826d',
        fillOpacity: 0
    }
}

CDADMap.getStyleColorFor_ZCBLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: '#e8c51d',
        fillOpacity: 0
    }
}


CDADMap.onEachFeatureFor_LOCATIONS = function(feature, layer){
		
	// add on click popups for locations -- open ino sidebar and populate with data
	layer.on("click",function(ev){
		// close all open popups
		MY_MAP.map.closePopup();
		
		// set up data for popout
		var commaSpace = /,\s/ig;
		var pipeSpace = /\|\s/ig;
		var activityString = feature.properties.Activity.replace(commaSpace, '| ');
		var activityArray = activityString.split(',');
		var activityList = activityArray.join('; ');
		activityList.replace(pipeSpace, ', ');
		
		var activities_ServicesString = feature.properties.Activities_Services.replace(commaSpace, '| ');
		var activities_ServicesArray = activities_ServicesString.split(',');
		var activities_ServicesArrayLength = activities_ServicesArray.length;
		for (var i = 0; i < activities_ServicesArrayLength; i++) {
			// wrap each item in labels
			activities_ServicesArray[i] = '<span class="label label-activity">' + activities_ServicesArray[i].replace(pipeSpace, ', ') + '</span>';
		}
		var activities_ServicesList = activities_ServicesArray.join(' ');
		
		var url = feature.properties.Social_website.replace('http://', '');
		var printurl = url.replace(/\/$/, "");
		url = 'http://' + url;
		
		
		
		// update sidebar content based on click
		$( "#popout-info-content" ).html("<div class='info-title-bar text-capitalize'>" + feature.properties.Organization_Name + "</div><div class='info-content-titles'>OFFICE ADDRESS</div><p class='info-content'>" + feature.properties.Address + " " + feature.properties.Address2 + "<br>" + feature.properties.City + ", " + feature.properties.State + " " + feature.properties.ZipCode + "</p><div class='info-content-titles'>DESCRIPTION</div><p class='info-content'>" + feature.properties.Organization_Description + "</p><div class='info-content-titles'>PRIMARY FOCUS AREAS</div><p class='info-content'>" + activityList + "</p><div class='info-content-titles'>SERVICES</div><p class='info-content'>" + activities_ServicesList + "</p><div class='info-content-titles'>CONTACT</div><p class='info-content'>" + feature.properties.Tel + "<br><a href='mailto:" + feature.properties.Email + "'>" + feature.properties.Email + "</a></p><div class='info-content-titles'>WEBSITE</div><p class='info-content'><a href='" + url + "'>" + printurl + "</a></p><br><button type='button' class='btn btn-default btn-block' data-toggle='modal' data-target='#orgModal' data-local='#orgCarousel' id='slideTo" + feature.properties.idlocation + "'><span class='pull-left'>VIEW FULL PROFILE</span><span class='glyphicon glyphicon-fullscreen pull-right' aria-hidden='true'></span></button>");
				
		var slideToIdlocation = '#slideTo' + parseInt(feature.properties.idlocation);
		var modalItemId = '#modalItem' + parseInt(feature.properties.idlocation);
		$(slideToIdlocation).click(function() {
			// rotate carousel
			$( "#orgCarousel" ).carousel(parseInt(feature.properties.counterId));
			
			setTimeout(function() {
				
				maps[feature.properties.idlocation].map.invalidateSize();
				
				// update modal title
				if ($( modalItemId ).hasClass('active')) {
					$( "#titleOrgName" ).html(feature.properties.Organization_Name);						
				}
				
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
		
		// set up modal for having this org selected
		$( "#titleOrgName" ).html(feature.properties.Organization_Name);
		
		

	});
	
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

	return L.marker(latlng, {icon: locationIcon});
	
}


CDADMap.loadFilteredLocations = function(data){
	
	MY_MAP.SAMPLE_POINT.addData(data);
	// add media to cluster library
	clusterLocations.addLayer(MY_MAP.SAMPLE_POINT);

}



CDADMap.loadLayerFor = function(layerId){
	
    if(layerId == "CouncilDistrictBoundaries"){
		MY_MAP.CDBLAYER.addTo(MY_MAP.map).bringToBack();
	}	

    if(layerId == "NeighborhoodBoundaries"){
		MY_MAP.NBLAYER.addTo(MY_MAP.map).bringToBack();
	}	

    if(layerId == "ZipCodeBoundaries"){
		MY_MAP.ZCBLAYER.addTo(MY_MAP.map).bringToBack();
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

CDADMap.loadLocationsLayerFor = function(layerId){
	// add layer requested based on ID
	if (layerId == "LOC1") {
		LOC1 = MY_MAP.LOC1_PAWN_SHOPS.addTo(MY_MAP.map).bringToFront();
	}
	if (layerId == "LOC2") {
		LOC2 = MY_MAP.LOC2_CHECK_CASHING.addTo(MY_MAP.map).bringToFront();
	}
	if (layerId == "LOC3") {
		LOC3 = MY_MAP.LOC3_WIRE_TRANSFER.addTo(MY_MAP.map).bringToFront();
	}
	if (layerId == "LOC4") {
		LOC4 = MY_MAP.LOC4_BANKS.addTo(MY_MAP.map).bringToFront();
	}
	if (layerId == "LOC5") {
		LOC5 = MY_MAP.LOC5_MCDONALDS.addTo(MY_MAP.map).bringToFront();
	}
	if (layerId == "LOC6") {
		// load subway lines and stops together
		LOC7 = MY_MAP.LOC7_SUBWAY_STATIONS.addTo(MY_MAP.map).bringToFront();
		LOC6 = MY_MAP.LOC6_SUBWAY_LINES.addTo(MY_MAP.map).bringToFront();
	}
	
}

CDADMap.loadMediaLayers = function(){
		
	// set on mouseover interaction for cluster group
	clusterLocations.on('clustermouseover', function (ev) {
		// only have on mouseover work if popup2 isn't open
		if (!MY_MAP.popup2._isOpen) {
			// close all popups first
			MY_MAP.map.closePopup();
		}
	});

	MY_MAP.map.addLayer(clusterLocations);
	
}

CDADMap.removeLayerFor = function(layerId){
	// remove all popups first
	MY_MAP.map.closePopup();
	// then remove layer
	if (layerId == 'CouncilDistrictBoundaries') {
		MY_MAP.map.removeLayer( MY_MAP.CDBLAYER ); 		
	}

	if (layerId == 'NeighborhoodBoundaries') {
		MY_MAP.map.removeLayer( MY_MAP.NBLAYER ); 		
	}

	if (layerId == 'ZipCodeBoundaries') {
		MY_MAP.map.removeLayer( MY_MAP.ZCBLAYER ); 		
	}
	
}

CDADMap.removeLocationsLayers = function(){
	// remove all popups first
	MY_MAP.map.closePopup();
	// then remove media layers
	MY_MAP.map.removeLayer(clusterLocations); 

}

CDADMap.clearLocationsLayers = function(){
	// clear data out of cluserMedia when users search by tag
	MY_MAP.SAMPLE_POINT.clearLayers();	
	clusterLocations.clearLayers();	
	
}
	
	

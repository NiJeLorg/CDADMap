/* 
* Functions to create a generic City Digits map 
*/

function CDADMap() {
	
    //where detroit is 42.377410, -83.093719
    this.map = new L.Map('map', {
		minZoom:10,
		maxZoom:17,
    	center: [42.377410, -83.093719],
   	 	zoom: 12,
	});
	
	// add CartoDB tiles
	var CartoDBLayer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',{
	  attribution: 'Map Data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> Contributors, Map Tiles &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
	});
	
	this.map.addLayer(CartoDBLayer);
	
		
    //load logo in lower left corner
    //$("#citydigits-charts").attr({'class':'citydigits-charts'});


	//load geocoder control
	this.map.addControl(L.Control.geocoder({collapsed: false, placeholder:'', }));
	
	//load scale bars
	this.map.addControl(L.control.scale());
	
    // enable events
    this.map.doubleClickZoom.enable();
    this.map.scrollWheelZoom.enable();
	
	// placeholder for points
	this.SAMPLE_POINT = null;
	
	// placeholder for layers
	this.SAMPLE_LAYER = null;
	
	clusterLocations = L.markerClusterGroup();
	
	// popup container to catch on hover popups	
	this.popup = new L.Popup({ 
		maxWidth: 300,
		minWidth: 200, 
		minHeight: 30, 
	});
	
}


CDADMap.onEachFeature_SAMPLE_LAYER = function(feature,layer){	
	var highlight = {
	    weight: 3,
	    opacity: 1
	};
	var noHighlight = {
        weight: 1,
        opacity: .1
	};
	
    //add on hover -- same on hover and mousemove for each layer
    layer.on('mouseover', function(ev) {
		// only have on mouseover work if popup2 isn't open
		
    	MY_MAP.popup.setLatLng(MY_MAP.map.layerPointToLatLng(ev.layerPoint));
		MY_MAP.popup.setContent('<div class="rollover-tooltip">'+feature.properties.Name + '</div>');
	
		//display popup
        if (!MY_MAP.popup._isOpen && ($.inArray(feature.properties.Name,open_tooltips)<0)){
            MY_MAP.popup.openOn(MY_MAP.map);
        }else{
            MY_MAP.map.closePopup();
        }			
		
		//highlight polygon
		layer.setStyle(highlight);		
		
    });
		
    layer.on('mousemove', function(ev) {
		
        //get lat/long
        if(($.inArray(feature.properties.Name,open_tooltips)<0)){
			MY_MAP.popup.setLatLng(MY_MAP.map.layerPointToLatLng(ev.layerPoint));
			MY_MAP.popup.setContent('<div class="rollover-tooltip">'+feature.properties.Name + '</div>');
    	}

        //display popup
		if (!MY_MAP.popup._isOpen && ($.inArray(feature.properties.Name,open_tooltips)<0)){
			MY_MAP.popup.openOn(MY_MAP.map);
		}			

    });
	
    layer.on('mouseout', function(ev) {
		//remove highlight for polygon
		layer.setStyle(noHighlight);		
    });	
	
	
}

CDADMap.prototype.loadLayers = function (){
    var self = this;
		
	// load topoJSON data
	// path to data defined in index.html django template

	// define layer styles and oneachfeature popup styling
	this.SAMPLE_LAYER_style = L.geoJson(null, {
	    style: CDADMap.getStyleColorFor_SAMPLE_LAYER,
		onEachFeature: CDADMap.onEachFeature_SAMPLE_LAYER
	});
			
	// load layers
	this.SAMPLE_LAYER = omnivore.topojson(neighborhoods, null, this.MAP1_POP_POVERTY_style);
			
}

CDADMap.getStyleColorFor_SAMPLE_LAYER = function (feature){
    try{
        var value = feature.properties.PovertyPer;
        var fillColor = null;
        if(value >= 0 && value <=0.1){
			fillColor = "#a5f3fa";
        }
        if(value >0.1 && value <=0.15){
            fillColor = "#83E8F9";
        }
        if(value >0.15 && value<=0.2){
        	fillColor = "#62def8";
        }
        if(value > 0.2 && value <=0.3){
        	fillColor = "#0bb6ec";
        }
        if(value > 0.3 && value <=0.4) { 
			fillColor = "#178def";
        }
        if(value > 0.4) { 
			fillColor = "#254aeb";
        }
    }catch (e){

    }finally{
        return {
	        weight: 1,
	        opacity: .1,
	        color: 'white',
	        fillOpacity: 0.75,
	        fillColor: fillColor
        }
    }
}




CDADMap.onEachFeatureFor_SAMPLE_POINT = function(feature, layer){

    // on hover close the other popups
    layer.on('mouseover', function(ev) {
		MY_MAP.map.closePopup();
    });
		
	// add on click popups for each layer -- these will be different
	layer.on("click",function(ev){
		// close all open popups
		MY_MAP.map.closePopup();
		
		var lat = feature.geometry.coordinates[1];
		var lng = feature.geometry.coordinates[0];
		
		// set latlng variable
		var latlng = L.latLng(lat, lng);
		// bind popup with data to the feature
		MY_MAP.popup2.setLatLng(latlng);

		var header = '<div class="map-popup"><a href="/cashcity/media/image/' + feature.properties.id + '/" style="text-decoration:none; color:inherit"><h4 class="text-left">' + feature.properties.section + '</h4>';
		var mediaBox = '<div style="height: 280px; width: 280px; margin: auto; overflow: hidden;"><img src="' + feature.properties.image + '"></div>';
		var title = '<div style="margin-top: 5px"><p class="text-left">' + feature.properties.name + '</p></div></a>';
		var footer = '</div>';
				
		var popupContent = header + mediaBox + title + footer;
		
		MY_MAP.popup2.setContent(popupContent);
		MY_MAP.popup2.openOn(MY_MAP.map);
	});
	
}

CDADMap.prototype.loadLocations = function(){
				
	this.SAMPLE_POINT = null;

	// define layer styles and oneachfeature popup styling
	this.SAMPLE_POINT = L.geoJson(locationsJSON, {
		pointToLayer: CDADMap.getStyleFor_SAMPLE_POINT,
		onEachFeature: CDADMap.onEachFeatureFor_SAMPLE_POINT
	});
	
	
	// add media to cluster library
	clusterLocations.addLayer(this.SAMPLE_POINT);
	
}

CDADMap.getStyleFor_SAMPLE_POINT = function(feature, latlng){
	var locationIcon = L.icon({
	    iconUrl: feature.properties.iconUrl,
	    iconSize: [42, 50],
		iconAnchor: [17, 38], 
	});

	return L.marker(latlng, {icon: locationIcon});
	
}


CDADMap.loadFilteredLocations = function(data){
	
	MY_MAP.SAMPLE_POINT.addData(data);
	// add media to cluster library
	clusterLocations.addLayer(MY_MAP.SAMPLE_POINT);

}



CDADMap.loadLayerFor = function(layerId){
	
    if(layerId == "MAP1"){
        mainLayer = MY_MAP.SAMPLE_LAYER;
		mainLayer.addTo(MY_MAP.map).bringToBack();
	 }	

}

CDADMap.prototype.showLocationsOnPageLoad = function(){
	
	// add points to map			
	LOC1 = this.LOC1_PAWN_SHOPS.addTo(this.map);
	LOC2 = this.LOC2_CHECK_CASHING.addTo(this.map);
	LOC3 = this.LOC3_WIRE_TRANSFER.addTo(this.map);
	
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
	MY_MAP.map.removeLayer( layerId ); 
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
	
	

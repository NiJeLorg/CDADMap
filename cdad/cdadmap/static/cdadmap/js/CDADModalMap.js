/* 
* Functions to create the mini modal maps
*/

// initialize map
function CDADModalMap(mapid, lat, lon) {
	
	//console.log(mapid);
	
    //where detroit is 42.377410, -83.093719
    this.map = new L.Map(mapid, {
		dragging: false,
		minZoom: 16,
		maxZoom: 16,
		zoomControl: false,
		attributionControl: false,
    	center: [lat,lon],
   	 	zoom: 16,
	});
	
	// add CartoDB tiles
	this.CartoDBLayer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png');

	
	// add cartoDB tiles to start
	this.map.addLayer(this.CartoDBLayer);
				
	// create empty container for locations
	this.LOCATION = null;
	
	// define layer styles and oneachfeature popup styling
	this.LOCATION = L.geoJson(locations, {
		pointToLayer: CDADModalMap.getStyleFor_LOCATION,
		onEachFeature: CDADModalMap.onEachFeatureFor_LOCATION
	});
	
	this.map.addLayer(this.LOCATION);
		
}

CDADModalMap.onEachFeatureFor_LOCATION = function(feature, layer){
	
}

CDADModalMap.getStyleFor_LOCATION = function(feature, latlng){
	var locationIcon = L.icon({
	    iconUrl: feature.properties.iconUrl,
	    iconSize: [24, 32],
		iconAnchor: [12, 30], 
	});

	return L.marker(latlng, {icon: locationIcon});
	
}


/* 
* Functions to create the mini modal maps
*/

// initialize map
function CDADModalMap(mapid, lat, lon, zoom) {
	
	//console.log(mapid);
	
    //where detroit is 42.377410, -83.093719
    this.map = new L.Map(mapid, {
		dragging: false,
		minZoom: 8,
		maxZoom: 16,
		zoomControl: false,
		attributionControl: false,
    	center: [lat,lon],
   	 	zoom: zoom,
	});
	
	// add CartoDB tiles
	this.CartoDBLayer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png');

	// add cartoDB tiles to start
	this.map.addLayer(this.CartoDBLayer);
				
	// create empty container for locations
	this.LOCATION = null;

	// create and empty container for detroit city boundary
	this.DETLAYER = null;
	
	if (zoom == 16) {
		// define layer styles and oneachfeature popup styling
		this.LOCATION = L.geoJson(locations, {
			pointToLayer: CDADModalMap.getStyleFor_LOCATION,
		});
		
		this.map.addLayer(this.LOCATION);
	} else {
		this.DETLAYER_style = L.geoJson(null, {
		    style: CDADModalMap.getStyleColorFor_DETLAYER,
		}).addTo(this.map);

		this.DETLAYER = omnivore.topojson(detlayer, null, this.DETLAYER_style);

	}
		
}


CDADModalMap.getStyleFor_LOCATION = function(feature, latlng){
	var locationIcon = L.icon({
	    iconUrl: feature.properties.iconUrl,
	    iconSize: [24, 32],
		iconAnchor: [12, 30], 
	});

	return L.marker(latlng, {icon: locationIcon});
	
}

CDADModalMap.getStyleColorFor_DETLAYER = function (feature){
    return {
        weight: 2,
        opacity: 1,
        color: '#252525',
        fillOpacity: 0
    }
}



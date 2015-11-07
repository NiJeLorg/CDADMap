/* 
* Functions to create the mini modal maps
*/

// initialize map
function CDADModalMap(mapid, lat, lon, zoom, surveyid, type) {
	
	//console.log(mapid);
	
    //where detroit is 42.377410, -83.093719
    this.map = new L.Map(mapid, {
		minZoom: 8,
		maxZoom: 16,
		attributionControl: false,
	});
	
	// add CartoDB tiles
	this.CartoDBLayer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png');

	// add cartoDB tiles to start
	this.map.addLayer(this.CartoDBLayer);
				
	// create empty container for locations
	this.LOCATION = null;

	// create and empty container for detroit city boundary
	this.DETLAYER = null;
	this.CDOBCLAYER = null;

	if (type == 'locationAndSA') {
		// add location
		CDADModalMap.add_LOCATION(this);

		// add SA
		CDADModalMap.add_SA(this, surveyid);
		
	} else if (type == 'SA') {
		// add SA
		CDADModalMap.add_SA(this, surveyid);

	} else if (type == 'location') {
		// add location
		CDADModalMap.add_LOCATION(this);

		// set center and zoom
		this.map.setView([lat,lon], zoom);

		bounds = this.map.getBounds();

	} else {
		this.DETLAYER_style = L.geoJson(null, {
		    style: CDADModalMap.getStyleColorFor_DETLAYER,
		}).addTo(this.map);

		this.DETLAYER = omnivore.topojson(detlayer, null, this.DETLAYER_style);

		// set center and zoom
		this.map.setView([lat,lon], zoom);

		bounds = this.map.getBounds();

	}
		
}

CDADModalMap.add_LOCATION = function(sel) {
	// define layer styles and oneachfeature popup styling
	sel.LOCATION = L.geoJson(locations, {
		pointToLayer: CDADModalMap.getStyleFor_LOCATION,
	});
	
	sel.map.addLayer(sel.LOCATION);
}

CDADModalMap.add_SA = function(sel, surveyid) {
	$.ajax({
		type: "GET",
		url: "/getjsonformap/"+ surveyid +"/",
		success: function(data){
			// load the draw tools
			if (data) {
				var geojson = JSON.parse(data);

				sel.CDOBCLAYER = L.geoJson(geojson, {
			        style: CDADModalMap.getStyleColorFor_CDOBCLAYER,
			    });
			    sel.map.addLayer(sel.CDOBCLAYER);

			    // fit map to bounds of layer
				bounds = sel.CDOBCLAYER.getBounds();
				sel.map.fitBounds(bounds);

			} 
        }
	});
}


CDADModalMap.getStyleFor_LOCATION = function(feature, latlng){
	var locationIcon = L.icon({
	    iconUrl: feature.properties.iconUrl,
	    iconSize: [24, 32],
		iconAnchor: [12, 30], 
	});

	return L.marker(latlng, {icon: locationIcon});
	
}

CDADModalMap.getStyleColorFor_CDOBCLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: '#e8c51d',
        fillOpacity: 0.5,
        fill: '#e8c51d'
    }
}

CDADModalMap.getStyleColorFor_DETLAYER = function (feature){
    return {
        weight: 2,
        opacity: 1,
        color: '#252525',
        fillOpacity: 0
    }
}



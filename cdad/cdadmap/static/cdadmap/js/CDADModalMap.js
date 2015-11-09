/* 
* Functions to create the mini modal maps
*/

// initialize map
function CDADModalMap(mapid, lat, lon, zoom, surveyid, type, numid) {
	
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
		CDADModalMap.add_LOCATION(this, numid);

		// add SA
		CDADModalMap.add_SA(this, surveyid, numid);
		
	} else if (type == 'SA') {
		// add SA
		CDADModalMap.add_SA(this, surveyid, numid);

	} else if (type == 'location') {
		// add location
		CDADModalMap.add_LOCATION(this, numid);

		// set center and zoom
		this.map.setView([lat,lon], zoom);

		bounds[numid] = this.map.getBounds();

	} else {
		this.DETLAYER_style = L.geoJson(null, {
		    style: CDADModalMap.getStyleColorFor_DETLAYER,
		}).addTo(this.map);

		this.DETLAYER = omnivore.topojson(detlayer, null, this.DETLAYER_style);

		// set center and zoom
		this.map.setView([lat,lon], zoom);

		//var southWest = L.latLng(42.257746, -83.295593);
		//var northEast = L.latLng(42.489061, -82.853394);
		//bounds[numid] = L.latLngBounds(southWest, northEast);
		console.log(this.map.getZoom());

		bounds[numid] = this.map.getBounds();


	}
		
}

CDADModalMap.add_LOCATION = function(sel, numid) {
	// define layer styles and oneachfeature popup styling
	sel.LOCATION = L.geoJson(locations, {
		pointToLayer: CDADModalMap.getStyleFor_LOCATION,
		filter: function(feature, layer) {
			if (feature.properties.counterId == numid) {
				return true;
			} else {
				return false;
			}
	    }
	});
	
	sel.map.addLayer(sel.LOCATION);
}

CDADModalMap.add_SA = function(sel, surveyid, numid) {
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
				bounds[numid] = sel.CDOBCLAYER.getBounds();
				sel.map.fitBounds(bounds[numid]);

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



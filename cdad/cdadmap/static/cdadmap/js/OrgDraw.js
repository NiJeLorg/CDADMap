/* 
* Functions to create the main DNAinfo Crime Map
*/

// initialize map
function OrgDraw() {
	// set zoom and center for this map
	this.center = [42.377410, -83.043719];
    this.zoom = 11;

    this.map = new L.Map('map', {
		minZoom:11,
    	center: this.center,
   	 	zoom: this.zoom
	});

	// add CartoDB tiles
	this.CartoDBLayer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',{
	  attribution: 'Map Data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> Contributors, Map Tiles &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
	});

	// add cartoDB tiles to start
	this.map.addLayer(this.CartoDBLayer);

	//load geocoder control
	this.map.addControl(L.Control.geocoder({placeholder:'Address Search', geocoder:new L.Control.Geocoder.Google()}));

		
	//load scale bars
	this.map.addControl(L.control.scale());
	
    // enable events
    this.map.doubleClickZoom.enable();
    this.map.scrollWheelZoom.enable();
	
	// empty containers for layers 
	this.CDBLAYER = null;
	this.DRAWNGEOJSON = null;
	this.MapDissolve = null;

}

OrgDraw.prototype.getMapDissolve = function (){ 
	var thismap = this;
	$.ajax({
		type: "GET",
		url: "/getjsonformap/"+ id +"/",
		success: function(data){
			// load the draw tools
			if (data) {
				thismap.MapDissolve = JSON.parse(data);
			} else {
				thismap.MapDissolve = null;
			}
			OrgDraw.loadDrawTools(thismap);
        }
	});

}

OrgDraw.loadDrawTools = function (thismap){ 

	// initiate drawing tools
	// if MapDissolve has a geojson already, pass that to leaflet draw for editing
	if (thismap.MapDissolve) {
		thismap.FEATURELAYER = L.geoJson(thismap.MapDissolve, {style: {color: '#000'}});
		// show save and clear buttons if editing existing polygons
		$('#imFinished').removeClass('hidden');
	   	$('#startOver').removeClass('hidden');

	} else {
		thismap.FEATURELAYER = new L.FeatureGroup();
	}
	thismap.map.addLayer(thismap.FEATURELAYER);

	// Initialise the draw control and pass it the FeatureGroup of editable layers
	thismap.drawControl = new L.Control.Draw({
		draw: {
			polyline: false,
			rectangle: false,
			circle: false,
			marker: false,
			polygon: {
				repeatMode: true,
				guidelineDistance: 10,
				metric: false,
				shapeOptions: {
		            color: '#000'
		        }
			},
		},
	    edit: {
	        featureGroup: thismap.FEATURELAYER,
	    },
	});
	thismap.map.addControl(thismap.drawControl);

	thismap.map.on('draw:created', function (e) {
		thismap.FEATURELAYER.addLayer(e.layer);

	   	// add finished start over buttons
	   	$('#imFinished').removeClass('hidden');
	   	$('#startOver').removeClass('hidden');

	});

}



OrgDraw.startOver = function () {
	// remove buttons
	$('#imFinished').addClass('hidden');
	$('#startOver').addClass('hidden');

	// remove drawn layer from map
	MY_MAP.FEATURELAYER.clearLayers();

	// reset map to original zoom and center
	MY_MAP.map.setView(MY_MAP.center, MY_MAP.zoom);

}


OrgDraw.imFinished = function () {
	// ajax call to save the geojson
	MY_MAP.DRAWNGEOJSON = MY_MAP.FEATURELAYER.toGeoJSON();
	var geojson = MY_MAP.DRAWNGEOJSON;
	// add OrgName feature property
	geojson.properties.OrgName = OrgName
	var url = '/survey7save/'+ id + '/';
	var csrftoken = $.cookie('csrftoken');

	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});

	$.post( url, {'geojson': JSON.stringify(geojson)}, function(data){  
		window.location.href = '/survey8/'+ id + '/';
	}, "json");

}


OrgDraw.onEachFeature_CDBLAYER = function(feature,layer){	
	var highlight = {
	    weight: 4,
	    opacity: 1
	};
	var noHighlight = {
        weight: 2,
        opacity: 0.75
	};

	layer.bindLabel(OrgDraw.CouncilDistrictNames(feature.id), { direction:'auto' });
	
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


OrgDraw.prototype.loadCouncilDistricts = function (){
	var thismap = this;
	d3.json(cdblayer, function(data) {
		polyTopojson = topojson.feature(data, data.objects.DETROIT_CITY_COUNCIL_DISTRICT_BOUNDARIES4326).features;
		drawPolys();
	});

	function drawPolys() {
		thismap.CDBLAYER = L.geoJson(polyTopojson, {
		    style: OrgDraw.getStyleFor_CDBLAYER,
			onEachFeature: OrgDraw.onEachFeature_CDBLAYER,
		});
		thismap.map.addLayer(thismap.CDBLAYER);
	}

}

OrgDraw.getStyleFor_CDBLAYER = function (feature){
    return {
        weight: 2,
        opacity: 0.75,
        color: OrgDraw.CouncilDistrictColors(feature.id),
        fillOpacity: 0.25,
        fill: OrgDraw.CouncilDistrictColors(feature.id)
    }
}


OrgDraw.CouncilDistrictColors = function (d){
    return d == "D1" ? '#dbec3b' :
           d == "D2" ? '#73a40a' :
           d == "D3" ? '#ffab00' :
           d == "D4" ? '#004da9' :
           d == "D5" ? '#d41711' :
           d == "D6" ? '#68e3ff' :
           d == "D7" ? '#790398' :
                    '#000';	
}

OrgDraw.CouncilDistrictNames = function (d){
    return d == "D1" ? 'District 1' :
           d == "D2" ? 'District 2' :
           d == "D3" ? 'District 3' :
           d == "D4" ? 'District 4' :
           d == "D5" ? 'District 5' :
           d == "D6" ? 'District 6' :
           d == "D7" ? 'District 7' :
                    '';	
}



	

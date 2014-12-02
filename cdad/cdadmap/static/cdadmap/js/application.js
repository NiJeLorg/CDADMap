/**
 * Application.js: Sets global JS variables and initializes CDAD map
 * Author: NiJeL
 */

/*
  On DOM load handlers
 */
var map_popups = [];
var mainLayer = null;
var SAMPLE_POINT = null;
var SAMPLE_LAYER = null;
var clusterLocations = null;
var MY_MAP = null;


$().ready(new function(){
	
    //get screen measurements
    var myMap = new CDADMap();
    //myMap.loadMarkers();
    MY_MAP = myMap;	
		
});

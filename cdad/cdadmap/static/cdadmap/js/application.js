/**
 * Application.js: Sets global JS variables and initializes CDAD map
 * Author: NiJeL
 */

/*
  On DOM load handlers
 */
var map_popups = [];
var mainLayer = null;
var LOCATIONS = null;
var SAMPLE_LAYER = null;
var clusterLocations = null;
var MY_MAP = null;


$().ready(new function(){
	
    //get screen measurements
    var myMap = new CDADMap();
    myMap.loadLocations();
	myMap.showLocationsOnPageLoad();
    MY_MAP = myMap;	
		
});

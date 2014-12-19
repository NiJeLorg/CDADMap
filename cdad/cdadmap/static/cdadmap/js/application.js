/**
 * Application.js: Sets global JS variables and initializes CDAD map
 * Author: NiJeL
 */

/*
  On DOM load handlers
 */
var map_popups = [];
var open_tooltips = [];
var mainLayer = null;
var LOCATIONS = null;
var CDBLAYER = null;
var NBLAYER = null;
var ZCBLAYER = null;
var CDOBCLAYER = null;
var clusterLocations = null;
var MY_MAP = null;


$().ready(new function(){
	
    var myMap = new CDADMap();
    myMap.loadLocations();
    myMap.loadLayers();
	myMap.showLocationsOnPageLoad();
    MY_MAP = myMap;	
		
});

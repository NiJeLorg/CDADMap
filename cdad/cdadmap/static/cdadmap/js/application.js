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
var DETLAYER = null;
var CDBLAYER = null;
var NBLAYER = null;
var ZCBLAYER = null;
var CDOBCLAYER = null;
var clusterLocations = null;
var MY_MAP = null;


$().ready(new function(){
	
    var myMap = new CDADMap();
    myMap.loadLocations();
	myMap.showLocationsOnPageLoad();
    MY_MAP = myMap;	
    var myPopout = new CDADMapPopout();

    // load layers after map and popout are loaded to speed things up a bit
    CDADMap.loadLayers();

    // initialize all page tooltips
    $('[data-toggle="tooltip"]').tooltip();

		
});

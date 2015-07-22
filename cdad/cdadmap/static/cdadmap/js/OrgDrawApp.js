/**
 * nycfireworks2015citywideapp.js: Sets global JS variables and initializes DNAinfo fireworks 2015 citywide app
 * Author: NiJeL
 */

/*
  On DOM load handlers
 */
var CDBLAYER = null;
var FEATURELAYER = null;
var DRAWNGEOJSON = null;
var MY_MAP = null;

$().ready(new function(){
    var myMap = new OrgDraw();
    myMap.loadCouncilDistricts();
    myMap.getMapDissolve();
    MY_MAP = myMap;
});

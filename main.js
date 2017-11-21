/*jslint browser: true*/
/*global Tangram, gui */

(function () {
    'use strict';

    var locations = {
        'New York': [40.70531887544228, -74.00976419448853, 16],
    };

    var map_start_location = locations['New York'];

    /*** URL parsing ***/

    // leaflet-style URL hash pattern:
    // #[zoom],[lat],[lng]
    var url_hash = window.location.hash.slice(1, window.location.hash.length).split('/');

    if (url_hash.length == 3) {
        map_start_location = [url_hash[1],url_hash[2], url_hash[0]];
        // convert from strings
        map_start_location = map_start_location.map(Number);
    }

    var query = splitQueryParams();
    // { language: 'en', this: 'no'}

    function splitQueryParams () {
       var str = window.location.search;

       var kvArray = str.slice(1).split('&');
       // ['language=en', 'this=no']

       var obj = {};

       for (var i = 0, j=kvArray.length; i<j; i++) {
           var value = kvArray[i].split('=');
           var k = window.decodeURIComponent(value[0]);
           var v = window.decodeURIComponent(value[1]);

           obj[k] = v;
       }

       return obj;
    }


    /*** Map ***/

    var map = L.map('map',
        {'keyboardZoomOffset': .05}
    );


    var layer = Tangram.leafletLayer({
        scene: 'scene.yaml',
        attribution: '<a href="https://mapzen.com/tangram" target="_blank">Tangram</a> | &copy; OSM contributors | <a href="https://mapzen.com/" target="_blank">Mapzen</a>'
    });

    window.layer = layer;
    var scene = layer.scene;
    window.scene = scene;
    window.map = map;

    map.setView(map_start_location.slice(0, 2), map_start_location[2]);

    var hash = new L.Hash(map);
    
    // Resize map to window
    function resizeMap() {
        document.getElementById('map').style.width = window.innerWidth + 'px';
        document.getElementById('map').style.height = window.innerHeight + 'px';
        map.invalidateSize(false);
    }

    window.addEventListener('resize', resizeMap);
    resizeMap();

    // Create dat GUI
    var gui;
    function addGUI () {
        gui.domElement.parentNode.style.zIndex = 400; // make sure GUI is on top of map
        window.gui = gui;

        gui.OSM_ID = '3954665';
        gui.add(gui, 'OSM_ID').name("OSM ID");

        gui.API_KEY = query.api_key || 'mapzen-XXXXXX';

        gui.add(gui, 'API_KEY').name("API KEY");

        gui.ZOOM = '14';
        gui.add(gui, 'ZOOM');

        // gui.format = 'terrain-tif';
        gui.format = 'list';
        gui.add(gui, 'format', ['list', 'vbo', 'vector', 'terrain-png', 'terrain-tif']);

        gui.GRABLAND = function() {
            console.log('grabbin');
            landgrab(gui.OSM_ID, gui.ZOOM, gui.format, gui.API_KEY)
        };
        gui.add(gui, 'GRABLAND');

    }



    window.addEventListener('load', function () {
        // Scene initialized
        layer.addTo(map);

        gui = new dat.GUI({ autoPlace: true, hideable: true, width: 300 });
        addGUI();

        // landgrab(209879879874648, "0-3, 1, 12", "list")
        // landgrab(204648, "0-3, 1, 12", "list")
        // landgrab(3954665, 16, "list")
        // landgrab(3954665, 15)
        // landgrab(3954665, 16, "list")
        // landgrab(3954665, 10, 'vbo')
        // landgrab(3954665, 10, 'vector')
        // landgrab(3954665, 10, 'terrain')
    });


}());

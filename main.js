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

    window.addEventListener('load', function () {
        // Scene initialized
        layer.addTo(map);
        // landgrab(209879879874648, "0-3, 1, 12", "list")
        // landgrab(204648, "0-3, 1, 12", "list")
        // landgrab(3954665, 16, "list")
        // landgrab(3954665, 15)
        // landgrab(3954665, 16, "list")
        // landgrab(3954665, 14, 'vbo')
        landgrab(3954665, 10, 'vector')
    });


}());

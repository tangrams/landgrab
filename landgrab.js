var tile_size = 256;
var half_circumference_meters = 20037508.342789244;
var xmlroot;

function range(start, end) {
  return Array.apply(0, Array(end - start))
    .map(function (element, index) { 
      return index + start;
  });
}

function dedupe(b) {
	a = [];
	b.forEach(function(value){
	  if (a.indexOf(value)==-1) a.push(value);
	});
	return a;
}

function getHttp (url, callback) {
    var request = new XMLHttpRequest();
    var method = 'GET';

    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var response = request.responseText;

            var error = null;
            callback(error, response);
        } else if (request.readyState === 4 && request.status === 404) {
            var error = 'nope';
            callback(error, response);
        }
    };
    request.open(method, url, true);
    request.send();
}

// Convert lat-lng to mercator meters
function latLngToMeters( coords ) {
    y = parseFloat(coords['y']);
    x = parseFloat(coords['x']);
    // Latitude
    y = Math.log(Math.tan(y*Math.PI/360 + Math.PI/4)) / Math.PI;
    y *= half_circumference_meters;

    // Longitude
    x *= half_circumference_meters / 180;

    return {"x": x, "y": y};
}

// convert from tile-space coords to meters, depending on zoom
function tile_to_meters(zoom) {
    return 40075016.68557849 / Math.pow(2, zoom);
}

// Given a point in mercator meters and a zoom level
// return the tile X/Y/Z that the point lies in
function tileForMeters(coords, zoom) {
    y = parseFloat(coords['y']);
    x = parseFloat(coords['x']);
    return {
        "x": Math.floor((x + half_circumference_meters) / (half_circumference_meters * 2 / Math.pow(2, zoom))),
        "y": Math.floor((-y + half_circumference_meters) / (half_circumference_meters * 2 / Math.pow(2, zoom))),
        "z": zoom
    }
}

// Convert tile location to mercator meters - multiply by pixels per tile,
// then by meters per pixel, adjust for map origin
function metersForTile(tile) {
    return {
        "x": tile['x'] * half_circumference_meters * 2 / Math.pow(2, tile.z) - half_circumference_meters,
        "y": -(tile['y'] * half_circumference_meters * 2 / Math.pow(2, tile.z) - half_circumference_meters)
    }
}

function landgrab(OSMID, zoomarg, listonly) {

	console.log('OSMID:', OSMID, 'zoomarg:', zoomarg, 'listonly:', listonly);
	if (arguments.length < 3) {
	    console.log("At least 2 arguments needed - please enter an OSM ID and zoom level.")
	    return false;
	}

    zoom = [];
    console.log('zoomarg:', zoomarg)
    console.log('String(zoomarg):', String(zoomarg))
    console.log('String(zoomarg).split(","):', String(zoomarg).split(','))
    zoomarg = String(zoomarg).replace(/\s+/g, '');
    String(zoomarg).split(',').forEach(function(part) {
        if (part.indexOf('-') > -1) {
            split = part.split('-')
            a = parseInt(split[0]);
            b = parseInt(split[1]);
            zoom.push.apply(zoom, range(a, b + 1))
        } else {
            a = parseInt(part);
            zoom.push(a);
        }
	});
	zoom = dedupe(zoom);

	// try to download the node's xml from OSM
	// this is ugly
    INFILE = 'http://www.openstreetmap.org/api/0.6/relation/'+OSMID+'/full';
    console.log("Downloading", INFILE);
    getHttp(INFILE, function(err, res){
        if (err) {
	        INFILE = 'http://www.openstreetmap.org/api/0.6/way/'+OSMID+'/full'
		    console.log("Downloading", INFILE);
		    getHttp(INFILE, function(err, res){
		        if (err) {
	                INFILE = 'http://www.openstreetmap.org/api/0.6/node/'+OSMID
				    console.log("Downloading", INFILE);
				    getHttp(INFILE, function(err, res){
				        if (err) {
			    	        console.error(err);
				        } else {
				        	parseFile(res);
				        }
				    });
		        } else {
		        	parseFile(res);
		        }
	    	});
        } else {
        	parseFile(res);
        }
    });
}

function parseFile(res) {	
    parser = new DOMParser();
    response = parser.parseFromString(res, "text/xml");

    console.log('xml:')
    console.log(response)

    xmlroot = response.documentElement;
    console.log('xmlroot:', xmlroot)
    console.log('xmlroot children:', xmlroot.children)
    // console.log('xmlroot[0]:', xmlroot)

	//
	// PROCESSING points
	//

    console.log("Processing:")
    // var response = JSON.parse(res);

    points = [];
	for (n in xmlroot.children) {
		node = xmlroot.children[n];
	    if (node.tagName == "node") {
	        lat = parseFloat(node.getAttribute("lat"));
	        lon = parseFloat(node.getAttribute("lon"));
	        console.log('lat:', lat, 'lon:', lon)
	        points.push({'y':lat, 'x':lon});
	    }
	}
	console.log('points:', points);

	//
	// GET TILES for all zoom levels
	//
	for (z in zoom) {
	    getTiles(points,zoom[z]);
	}

}

function getTiles(points,zoom) {
	var tiles = [];

    for (p in points) {
    	point = points[p];
        tiles.push(tileForMeters(latLngToMeters({'x':point['x'],'y':point['y']}), zoom))
    }

var r = Array.from(new Set(tiles))
    // tiles = dedupe(tiles);
    // tiles = tiles.filter(function (v, i, a) { return a.indexOf (v) == i }); // dedupe array

	
	    // var o = {}, i, l = tiles.length, r = [];
	    // for(i=0; i<l;i+=1) o[tiles[i]] = tiles[i];
	    // for(i in o) r.push(o[i]);

console.log('r?', JSON.stringify(r));
    console.log('length:', r.length);


    // console.log('tiles:', JSON.stringify(tiles));
    // console.log('length:', tiles.length);

}
// landgrab(209879879874648, "0-3, 1, 12", 1)
// landgrab(204648, "0-3, 1, 12", 1)
landgrab(3954665, 16, 1)



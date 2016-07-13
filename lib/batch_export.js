
// batch_export.js
// batch tile export from Tangram -
// prepares tiles for conversion by vbo-export
//
// TODO:
// take in a selection of tiles from landgrab and pass files/data directly to vbo-export
//

window.exportVBO = function (callback) {

console.log("Beginning VBO export");

var mytiles = [
{'x': 19300, 'y': 24626.0, 'z': 16},
 {'x': 19297, 'y': 24636.0, 'z': 16},
 {'x': 19303.0, 'y': 24625, 'z': 16},
 {'x': 19308.0, 'y': 24608, 'z': 16},
 {'x': 19298.0, 'y': 24631, 'z': 16},
 {'x': 19300, 'y': 24639.0, 'z': 16},
 {'x': 19308.0, 'y': 24609.0, 'z': 16},
 {'x': 19296.0, 'y': 24627.0, 'z': 16},
 {'x': 19305, 'y': 24626.0, 'z': 16},
 {'x': 19293.0, 'y': 24641.0, 'z': 16},
 {'x': 19306, 'y': 24617.0, 'z': 16},
 {'x': 19308.0, 'y': 24617.0, 'z': 16},
 {'x': 19312.0, 'y': 24603.0, 'z': 16},
 {'x': 19300.0, 'y': 24628, 'z': 16},
 {'x': 19300.0, 'y': 24621.0, 'z': 16},
 {'x': 19302.0, 'y': 24618, 'z': 16},
 {'x': 19308.0, 'y': 24611.0, 'z': 16},
 {'x': 19309.0, 'y': 24603.0, 'z': 16},
 {'x': 19301.0, 'y': 24626, 'z': 16},
 {'x': 19310.0, 'y': 24600.0, 'z': 16},
 {'x': 19311.0, 'y': 24605.0, 'z': 16},
 {'x': 19307.0, 'y': 24606.0, 'z': 16},
 {'x': 19301.0, 'y': 24635.0, 'z': 16},
 {'x': 19304.0, 'y': 24629.0, 'z': 16},
 {'x': 19306.0, 'y': 24620, 'z': 16},
 {'x': 19297.0, 'y': 24634, 'z': 16},
 {'x': 19294.0, 'y': 24635.0, 'z': 16},
 {'x': 19299, 'y': 24639.0, 'z': 16},
 {'x': 19306.0, 'y': 24609.0, 'z': 16},
 {'x': 19306.0, 'y': 24626.0, 'z': 16},
 {'x': 19308.0, 'y': 24603.0, 'z': 16},
 {'x': 19307.0, 'y': 24612, 'z': 16},
 {'x': 19304.0, 'y': 24616, 'z': 16},
 {'x': 19309.0, 'y': 24617.0, 'z': 16},
 {'x': 19298.0, 'y': 24637, 'z': 16},
 {'x': 19309.0, 'y': 24616, 'z': 16},
 {'x': 19300.0, 'y': 24633, 'z': 16},
 {'x': 19296.0, 'y': 24637, 'z': 16},
 {'x': 19308.0, 'y': 24620.0, 'z': 16},
 {'x': 19299, 'y': 24632.0, 'z': 16},
 {'x': 19309.0, 'y': 24609.0, 'z': 16},
 {'x': 19304.0, 'y': 24615, 'z': 16},
 {'x': 19300.0, 'y': 24624, 'z': 16},
 {'x': 19309.0, 'y': 24606, 'z': 16},
 {'x': 19301.0, 'y': 24639.0, 'z': 16},
 {'x': 19304.0, 'y': 24614.0, 'z': 16},
 {'x': 19299, 'y': 24628.0, 'z': 16},
 {'x': 19296, 'y': 24632.0, 'z': 16},
 {'x': 19307.0, 'y': 24622.0, 'z': 16},
 {'x': 19300.0, 'y': 24640.0, 'z': 16},
 {'x': 19310.0, 'y': 24607.0, 'z': 16},
 {'x': 19312.0, 'y': 24602.0, 'z': 16},
 {'x': 19303.0, 'y': 24621, 'z': 16},
 {'x': 19309.0, 'y': 24614, 'z': 16},
 {'x': 19302.0, 'y': 24628, 'z': 16},
 {'x': 19294.0, 'y': 24633.0, 'z': 16},
 {'x': 19298.0, 'y': 24634, 'z': 16},
 {'x': 19307.0, 'y': 24604.0, 'z': 16},
 {'x': 19303.0, 'y': 24630.0, 'z': 16},
 {'x': 19303.0, 'y': 24628, 'z': 16},
 {'x': 19300.0, 'y': 24627, 'z': 16},
 {'x': 19305.0, 'y': 24619, 'z': 16},
 {'x': 19295, 'y': 24641.0, 'z': 16},
 {'x': 19305.0, 'y': 24611.0, 'z': 16},
 {'x': 19298.0, 'y': 24633, 'z': 16},
 {'x': 19302, 'y': 24622.0, 'z': 16},
 {'x': 19295, 'y': 24640.0, 'z': 16},
 {'x': 19301.0, 'y': 24628, 'z': 16},
 {'x': 19298, 'y': 24630.0, 'z': 16},
 {'x': 19307.0, 'y': 24610, 'z': 16},
 {'x': 19309.0, 'y': 24608.0, 'z': 16},
 {'x': 19295.0, 'y': 24632.0, 'z': 16},
 {'x': 19309.0, 'y': 24601.0, 'z': 16},
 {'x': 19301.0, 'y': 24636.0, 'z': 16},
 {'x': 19306.0, 'y': 24606.0, 'z': 16},
 {'x': 19306.0, 'y': 24618, 'z': 16},
 {'x': 19300.0, 'y': 24634, 'z': 16},
 {'x': 19307.0, 'y': 24618, 'z': 16},
 {'x': 19303, 'y': 24617.0, 'z': 16},
 {'x': 19303.0, 'y': 24615.0, 'z': 16},
 {'x': 19301.0, 'y': 24618.0, 'z': 16},
 {'x': 19304.0, 'y': 24624, 'z': 16},
 {'x': 19298.0, 'y': 24623.0, 'z': 16},
 {'x': 19298.0, 'y': 24640.0, 'z': 16},
 {'x': 19302, 'y': 24629.0, 'z': 16},
 {'x': 19293.0, 'y': 24643.0, 'z': 16},
 {'x': 19303.0, 'y': 24624, 'z': 16},
 {'x': 19302.0, 'y': 24632.0, 'z': 16},
 {'x': 19296, 'y': 24635.0, 'z': 16},
 {'x': 19301.0, 'y': 24623, 'z': 16},
 {'x': 19304, 'y': 24617.0, 'z': 16},
 {'x': 19310.0, 'y': 24604.0, 'z': 16},
 {'x': 19309.0, 'y': 24612, 'z': 16},
 {'x': 19299, 'y': 24629.0, 'z': 16},
 {'x': 19308.0, 'y': 24607, 'z': 16},
 {'x': 19301.0, 'y': 24620, 'z': 16},
 {'x': 19296.0, 'y': 24633, 'z': 16},
 {'x': 19302.0, 'y': 24621, 'z': 16},
 {'x': 19302.0, 'y': 24631.0, 'z': 16},
 {'x': 19308.0, 'y': 24615.0, 'z': 16},
 {'x': 19306.0, 'y': 24624.0, 'z': 16},
 {'x': 19305, 'y': 24620.0, 'z': 16},
 {'x': 19305, 'y': 24615.0, 'z': 16},
 {'x': 19297.0, 'y': 24641.0, 'z': 16},
 {'x': 19300.0, 'y': 24625, 'z': 16},
 {'x': 19307, 'y': 24609.0, 'z': 16},
 {'x': 19307.0, 'y': 24624.0, 'z': 16},
 {'x': 19307.0, 'y': 24614, 'z': 16},
 {'x': 19308.0, 'y': 24618, 'z': 16},
 {'x': 19295.0, 'y': 24631.0, 'z': 16},
 {'x': 19298, 'y': 24639.0, 'z': 16},
 {'x': 19301.0, 'y': 24627, 'z': 16},
 {'x': 19299, 'y': 24626.0, 'z': 16},
 {'x': 19305.0, 'y': 24614, 'z': 16},
 {'x': 19297.0, 'y': 24625.0, 'z': 16},
 {'x': 19304.0, 'y': 24621, 'z': 16},
 {'x': 19307.0, 'y': 24625.0, 'z': 16},
 {'x': 19293.0, 'y': 24638.0, 'z': 16},
 {'x': 19300.0, 'y': 24623, 'z': 16},
 {'x': 19305, 'y': 24617.0, 'z': 16},
 {'x': 19303.0, 'y': 24618, 'z': 16},
 {'x': 19304.0, 'y': 24627, 'z': 16},
 {'x': 19310.0, 'y': 24602, 'z': 16},
 {'x': 19306.0, 'y': 24623.0, 'z': 16},
 {'x': 19301.0, 'y': 24624, 'z': 16},
 {'x': 19296.0, 'y': 24628.0, 'z': 16},
 {'x': 19296.0, 'y': 24642.0, 'z': 16},
 {'x': 19305.0, 'y': 24616, 'z': 16},
 {'x': 19299, 'y': 24631.0, 'z': 16},
 {'x': 19298.0, 'y': 24625.0, 'z': 16},
 {'x': 19312.0, 'y': 24604.0, 'z': 16},
 {'x': 19297, 'y': 24630.0, 'z': 16},
 {'x': 19308.0, 'y': 24605, 'z': 16},
 {'x': 19299, 'y': 24640.0, 'z': 16},
 {'x': 19295.0, 'y': 24642.0, 'z': 16},
 {'x': 19307.0, 'y': 24619, 'z': 16},
 {'x': 19298, 'y': 24635.0, 'z': 16},
 {'x': 19298.0, 'y': 24624.0, 'z': 16},
 {'x': 19301.0, 'y': 24632.0, 'z': 16},
 {'x': 19298, 'y': 24626.0, 'z': 16},
 {'x': 19293.0, 'y': 24642.0, 'z': 16},
 {'x': 19303, 'y': 24620.0, 'z': 16},
 {'x': 19300, 'y': 24635.0, 'z': 16},
 {'x': 19310.0, 'y': 24601.0, 'z': 16},
 {'x': 19303.0, 'y': 24629.0, 'z': 16},
 {'x': 19312.0, 'y': 24601.0, 'z': 16},
 {'x': 19304.0, 'y': 24612.0, 'z': 16},
 {'x': 19309.0, 'y': 24613, 'z': 16},
 {'x': 19304.0, 'y': 24626, 'z': 16},
 {'x': 19294.0, 'y': 24634.0, 'z': 16},
 {'x': 19305.0, 'y': 24613, 'z': 16},
 {'x': 19301.0, 'y': 24629, 'z': 16},
 {'x': 19305.0, 'y': 24627.0, 'z': 16},
 {'x': 19311, 'y': 24603.0, 'z': 16},
 {'x': 19299, 'y': 24630.0, 'z': 16},
 {'x': 19299, 'y': 24637.0, 'z': 16},
 {'x': 19302.0, 'y': 24624, 'z': 16},
 {'x': 19301.0, 'y': 24637.0, 'z': 16},
 {'x': 19300.0, 'y': 24637, 'z': 16},
 {'x': 19298.0, 'y': 24632, 'z': 16},
 {'x': 19306.0, 'y': 24625.0, 'z': 16},
 {'x': 19309.0, 'y': 24618.0, 'z': 16},
 {'x': 19298, 'y': 24629.0, 'z': 16},
 {'x': 19308.0, 'y': 24602.0, 'z': 16},
 {'x': 19308.0, 'y': 24619, 'z': 16},
 {'x': 19299.0, 'y': 24621.0, 'z': 16},
 {'x': 19309.0, 'y': 24610, 'z': 16},
 {'x': 19296.0, 'y': 24634, 'z': 16},
 {'x': 19299, 'y': 24634.0, 'z': 16},
 {'x': 19303.0, 'y': 24627, 'z': 16},
 {'x': 19306.0, 'y': 24615, 'z': 16},
 {'x': 19299, 'y': 24624.0, 'z': 16},
 {'x': 19300.0, 'y': 24619.0, 'z': 16},
 {'x': 19302.0, 'y': 24623, 'z': 16},
 {'x': 19306.0, 'y': 24613, 'z': 16},
 {'x': 19295.0, 'y': 24637, 'z': 16},
 {'x': 19307, 'y': 24617.0, 'z': 16},
 {'x': 19297.0, 'y': 24637, 'z': 16},
 {'x': 19301.0, 'y': 24619.0, 'z': 16},
 {'x': 19309, 'y': 24605.0, 'z': 16},
 {'x': 19300, 'y': 24622.0, 'z': 16},
 {'x': 19303, 'y': 24622.0, 'z': 16},
 {'x': 19311.0, 'y': 24602, 'z': 16},
 {'x': 19309.0, 'y': 24611, 'z': 16},
 {'x': 19306.0, 'y': 24610.0, 'z': 16},
 {'x': 19299, 'y': 24627.0, 'z': 16},
 {'x': 19304.0, 'y': 24625, 'z': 16},
 {'x': 19305.0, 'y': 24610.0, 'z': 16},
 {'x': 19296, 'y': 24630.0, 'z': 16},
 {'x': 19305.0, 'y': 24628.0, 'z': 16},
 {'x': 19297, 'y': 24631.0, 'z': 16},
 {'x': 19301.0, 'y': 24634.0, 'z': 16},
 {'x': 19300.0, 'y': 24638, 'z': 16},
 {'x': 19301.0, 'y': 24621, 'z': 16},
 {'x': 19308.0, 'y': 24613.0, 'z': 16},
 {'x': 19307, 'y': 24620.0, 'z': 16},
 {'x': 19306.0, 'y': 24612, 'z': 16},
 {'x': 19300.0, 'y': 24630, 'z': 16},
 {'x': 19293.0, 'y': 24639.0, 'z': 16},
 {'x': 19302.0, 'y': 24619, 'z': 16},
 {'x': 19301.0, 'y': 24630, 'z': 16},
 {'x': 19305.0, 'y': 24612.0, 'z': 16},
 {'x': 19311.0, 'y': 24601.0, 'z': 16},
 {'x': 19305, 'y': 24622.0, 'z': 16},
 {'x': 19301.0, 'y': 24622, 'z': 16},
 {'x': 19308.0, 'y': 24612.0, 'z': 16},
 {'x': 19297.0, 'y': 24626.0, 'z': 16},
 {'x': 19294.0, 'y': 24636.0, 'z': 16},
 {'x': 19309.0, 'y': 24604, 'z': 16},
 {'x': 19307.0, 'y': 24621, 'z': 16},
 {'x': 19306.0, 'y': 24608.0, 'z': 16},
 {'x': 19295.0, 'y': 24638, 'z': 16},
 {'x': 19294.0, 'y': 24642.0, 'z': 16},
 {'x': 19299.0, 'y': 24633, 'z': 16},
 {'x': 19293.0, 'y': 24640.0, 'z': 16},
 {'x': 19310.0, 'y': 24606.0, 'z': 16},
 {'x': 19295.0, 'y': 24630.0, 'z': 16},
 {'x': 19299.0, 'y': 24641.0, 'z': 16},
 {'x': 19296.0, 'y': 24641.0, 'z': 16},
 {'x': 19308.0, 'y': 24610.0, 'z': 16},
 {'x': 19301.0, 'y': 24640.0, 'z': 16},
 {'x': 19309.0, 'y': 24619.0, 'z': 16},
 {'x': 19309.0, 'y': 24602.0, 'z': 16},
 {'x': 19303.0, 'y': 24631.0, 'z': 16},
 {'x': 19311.0, 'y': 24604.0, 'z': 16},
 {'x': 19301.0, 'y': 24617.0, 'z': 16},
 {'x': 19294.0, 'y': 24638.0, 'z': 16},
 {'x': 19296, 'y': 24636.0, 'z': 16},
 {'x': 19309.0, 'y': 24620.0, 'z': 16},
 {'x': 19301.0, 'y': 24638.0, 'z': 16},
 {'x': 19301.0, 'y': 24625, 'z': 16},
 {'x': 19309.0, 'y': 24600.0, 'z': 16},
 {'x': 19306.0, 'y': 24619, 'z': 16},
 {'x': 19299.0, 'y': 24623.0, 'z': 16},
 {'x': 19297.0, 'y': 24633, 'z': 16},
 {'x': 19301.0, 'y': 24633.0, 'z': 16},
 {'x': 19299.0, 'y': 24638, 'z': 16},
 {'x': 19307.0, 'y': 24613, 'z': 16},
 {'x': 19298.0, 'y': 24627, 'z': 16},
 {'x': 19294, 'y': 24641.0, 'z': 16},
 {'x': 19310.0, 'y': 24605.0, 'z': 16},
 {'x': 19307.0, 'y': 24605.0, 'z': 16},
 {'x': 19298, 'y': 24636.0, 'z': 16},
 {'x': 19296.0, 'y': 24629.0, 'z': 16},
 {'x': 19308.0, 'y': 24604.0, 'z': 16},
 {'x': 19308.0, 'y': 24621.0, 'z': 16},
 {'x': 19307.0, 'y': 24623.0, 'z': 16},
 {'x': 19302.0, 'y': 24625, 'z': 16},
 {'x': 19299, 'y': 24636.0, 'z': 16},
 {'x': 19297, 'y': 24640.0, 'z': 16},
 {'x': 19310, 'y': 24603.0, 'z': 16},
 {'x': 19297, 'y': 24635.0, 'z': 16},
 {'x': 19294, 'y': 24639.0, 'z': 16},
 {'x': 19299, 'y': 24635.0, 'z': 16},
 {'x': 19295, 'y': 24636.0, 'z': 16},
 {'x': 19306.0, 'y': 24622, 'z': 16},
 {'x': 19294, 'y': 24640.0, 'z': 16},
 {'x': 19299.0, 'y': 24622.0, 'z': 16},
 {'x': 19296.0, 'y': 24626.0, 'z': 16},
 {'x': 19303.0, 'y': 24614.0, 'z': 16},
 {'x': 19306.0, 'y': 24614, 'z': 16},
 {'x': 19307.0, 'y': 24608, 'z': 16},
 {'x': 19295.0, 'y': 24634, 'z': 16},
 {'x': 19297, 'y': 24632.0, 'z': 16},
 {'x': 19300.0, 'y': 24620.0, 'z': 16},
 {'x': 19305, 'y': 24623.0, 'z': 16},
 {'x': 19307.0, 'y': 24615, 'z': 16},
 {'x': 19297, 'y': 24639.0, 'z': 16},
 {'x': 19297, 'y': 24629.0, 'z': 16},
 {'x': 19307.0, 'y': 24616, 'z': 16},
 {'x': 19307.0, 'y': 24607, 'z': 16},
 {'x': 19297.0, 'y': 24638, 'z': 16},
 {'x': 19295.0, 'y': 24633.0, 'z': 16},
 {'x': 19305, 'y': 24625.0, 'z': 16},
 {'x': 19306.0, 'y': 24621, 'z': 16},
 {'x': 19300.0, 'y': 24636, 'z': 16},
 {'x': 19306.0, 'y': 24607.0, 'z': 16},
 {'x': 19305, 'y': 24624.0, 'z': 16},
 {'x': 19294.0, 'y': 24632.0, 'z': 16},
 {'x': 19304.0, 'y': 24619, 'z': 16},
 {'x': 19302, 'y': 24626.0, 'z': 16},
 {'x': 19303, 'y': 24626.0, 'z': 16},
 {'x': 19304.0, 'y': 24613.0, 'z': 16},
 {'x': 19295.0, 'y': 24628.0, 'z': 16},
 {'x': 19309.0, 'y': 24615, 'z': 16},
 {'x': 19302.0, 'y': 24627, 'z': 16},
 {'x': 19297.0, 'y': 24628, 'z': 16},
 {'x': 19304.0, 'y': 24622, 'z': 16},
 {'x': 19295, 'y': 24639.0, 'z': 16},
 {'x': 19300.0, 'y': 24631, 'z': 16},
 {'x': 19309.0, 'y': 24607.0, 'z': 16},
 {'x': 19313.0, 'y': 24602.0, 'z': 16},
 {'x': 19304.0, 'y': 24618, 'z': 16},
 {'x': 19299, 'y': 24625.0, 'z': 16},
 {'x': 19296, 'y': 24640.0, 'z': 16},
 {'x': 19308.0, 'y': 24614.0, 'z': 16},
 {'x': 19303.0, 'y': 24623, 'z': 16},
 {'x': 19294.0, 'y': 24643.0, 'z': 16},
 {'x': 19297.0, 'y': 24627.0, 'z': 16},
 {'x': 19296, 'y': 24639.0, 'z': 16},
 {'x': 19306.0, 'y': 24616, 'z': 16},
 {'x': 19307, 'y': 24611.0, 'z': 16},
 {'x': 19302, 'y': 24620.0, 'z': 16},
 {'x': 19304.0, 'y': 24623, 'z': 16},
 {'x': 19304.0, 'y': 24628.0, 'z': 16},
 {'x': 19301.0, 'y': 24631, 'z': 16},
 {'x': 19295.0, 'y': 24643.0, 'z': 16},
 {'x': 19294.0, 'y': 24637.0, 'z': 16},
 {'x': 19300.0, 'y': 24632, 'z': 16},
 {'x': 19300, 'y': 24629.0, 'z': 16},
 {'x': 19295, 'y': 24635.0, 'z': 16},
 {'x': 19308.0, 'y': 24616.0, 'z': 16},
 {'x': 19298.0, 'y': 24628, 'z': 16},
 {'x': 19302.0, 'y': 24617.0, 'z': 16},
 {'x': 19296, 'y': 24631.0, 'z': 16},
 {'x': 19303.0, 'y': 24619, 'z': 16},
 {'x': 19304.0, 'y': 24620, 'z': 16},
 {'x': 19294.0, 'y': 24631.0, 'z': 16},
 {'x': 19308.0, 'y': 24606, 'z': 16},
 {'x': 19306, 'y': 24611.0, 'z': 16},
 {'x': 19298.0, 'y': 24638, 'z': 16},
 {'x': 19298.0, 'y': 24641.0, 'z': 16},
 {'x': 19302, 'y': 24630.0, 'z': 16},
 {'x': 19296.0, 'y': 24638, 'z': 16},
 {'x': 19302.0, 'y': 24616.0, 'z': 16},
 {'x': 19305.0, 'y': 24618, 'z': 16},
 {'x': 19295.0, 'y': 24629.0, 'z': 16},
 {'x': 19305.0, 'y': 24621, 'z': 16},
 {'x': 19303.0, 'y': 24616, 'z': 16},
 {'x': 19308.0, 'y': 24622.0, 'z': 16}

];

var num = mytiles.length;
console.log("Loading", num, "tiles");

// find tile range, for offset calculation
min = {x: Infinity, y: Infinity};
max = {x:-Infinity, y: -Infinity};
for (t in mytiles) {
  mt = mytiles[t];

  min.x = Math.min(min.x, mt.x);
  min.y = Math.min(min.y, mt.y);
  max.x = Math.max(max.x, mt.x);
  max.y = Math.max(max.y, mt.y);
}

// prepare a list of vbos
vbos = [];
vbosProcessed = 0;

function waitForVerts(callback, coords, offset, name) {
  var coords = coords;
  var name = name;
  setTimeout(function () {
    // todo: determine which of these are necessary
    // also todo: trigger this based on a loadCoordinates callback instead
    if (typeof scene.tile_manager.tiles[coords] != "undefined") {
      if ( scene.tile_manager.tiles[coords].loaded != false) {
        if ( Object.keys(scene.tile_manager.tiles[coords].meshes).length != 0) {
          // if (typeof scene.tile_manager.tiles[coords].meshes.polygons != "undefined" || typeof scene.tile_manager.tiles[coords].meshes.lines != "undefined") {
          //   if (typeof scene.tile_manager.tiles[coords].meshes.polygons.vertex_data != "undefined" || typeof scene.tile_manager.tiles[coords].meshes.lines.vertex_data != "undefined") {
          //       callback(coords, offset, name);
          //       return;
          //   }
          // }
          callback(coords, offset, name);
          return;

        } else {
          // no verts in this tile to convert
          console.log('no verts in', coords);
          callback(coords, offset, name);
          return;
        }
      }
    }
    // if not ready, wait a sec and try again
    waitForVerts(callback, coords, offset, name);
  }, 1000);
}

function waitForWorkers(callback) {
  setTimeout(function () {
    // check for workers
    if (typeof scene.workers != "undefined") {
      // check that the workers are registered in the scene
      if (typeof scene.workers[scene.next_worker] != "undefined") {
        // check that the scene is instantiated and ready to go
        if (typeof scene.center_meters != "undefined") {
          callback();
          return;
        }
      }
    }
    // if not ready, wait a sec and try again
    waitForWorkers(callback);
  }, 1000);
}

function waitForScene(callback) {
  setTimeout(function () {
    if (scene.initialized) {
        callback();
        return;
    }
    // if not ready, wait a sec and try again
    waitForScene(callback);
  }, 250);
}

function waitForVBOs(callback) {
  setTimeout(function () {
    if (vbosProcessed == mytiles.length) {
        callback();
        return;
    }
    // if not ready, wait a sec and try again
    waitForVBOs(callback);
  }, 1000);
}

function loadTiles() {
  for (t in mytiles) {
    // console.log("loading", mytiles[t]);
    scene.tile_manager.loadCoordinate(mytiles[t]);
  }
  console.log("%d tiles loaded", mytiles.length);
}

function tile_to_meters(zoom) {
    return 40075016.68557849 / Math.pow(2, zoom)
}

function processTiles() {
  for (t in mytiles) {
    mt = mytiles[t];
    if (Object.keys(scene.config.sources).length > 1) {
      console.error("This scene has data from multiple sources:", Object.keys(scene.config.sources), "Only scenes with a single source are supported for export.");
      return false;
    }
    source = Object.keys(scene.config.sources)
    coords = source+"/"+mt.z+"/"+mt.x+"/"+mt.y+"/"+mt.z;
    name = mt.x+"-"+mt.y+"-"+mt.z;

    // calculate offset relative to the extents of the tile batch -
    // the top-left tile is 0,0 - one tile over is 1,0 - one tile down is 0,1
    // this will lay the tiles out in space correctly relative to each other
    var offset = {x: mt.x - min.x, y: mt.y - min.y};
    // multiply the offset by the local tile coordinate range for vertex position offset
    offset.x *= 4096;
    offset.y *= 4096;

    // wait for tile to load, then process it
    waitForVerts(processVerts, coords, offset, name);
  }
}

// todo: get zoom from mytiles or scene
zoom = 16;
maximum_range = 4096; // tile-space coordinate maximum
conversion_factor = tile_to_meters(zoom) / maximum_range;

function processVerts(coords, offset, name) {
  console.log("Processing tile", vbosProcessed + 1, "of", mytiles.length, "-", (((vbosProcessed + 1)/mytiles.length)*100).toFixed(2), "%");

  meshes = scene.tile_manager.tiles[coords].meshes;
  allverts = "";
  for (m in meshes) {
    mesh = meshes[m];
    if (typeof(mesh) != "undefined") { // check for empty tiles
      verts = [];
      vbo = new Int16Array(mesh.vertex_data.buffer);
      var stride = mesh.vertex_layout.stride / Int16Array.BYTES_PER_ELEMENT;
      var count = mesh.vertex_count;

      // use count instead of vbo.length - the vbo is size before population, and resized in chunks as needed, and might have old tile data in it from the last tile the worker worked on
      for (var i=0; i < count; i++) {
        // for every [stride] elements, copy the first three elements x, y, and z, adding the offset to the x and y to lay all the tiles out in the same world space - use the conversion factor so the z is to the same scale as the x & y
        verts[i] = [(vbo[i*stride] += offset.x) * conversion_factor, (vbo[i*stride+1] -= offset.y) * conversion_factor, vbo[i*stride+2]];
      }

      // multiply each entry by master scaling factor
      var masterScale = .17;
      for (var i=0; i < verts.length; i++) {
        for (var j=0; j < 3; j++) {
          verts[i][j] *= masterScale;
        }
      }

      // convert each entry into a string
      for (var i=0; i < verts.length; i++) {
          verts[i] = verts[i].join(' ');
      }
      // make it one long string
      verts = verts.join('\n');

      // add mesh verts to master tile verts list
      allverts = allverts + "\n" + verts;
    }
  }
  if (allverts.length > 0) {
    // add it to file list for zipping
    vbos.push({name: name, verts: allverts});
  }
  // } else {
  //   console.log('empty tile, skipping', coords);
  // }
  vbosProcessed++;
}

// zip with zip.js
function zipBlobs() {
  filenames = [];
  zip.workerScriptsPath = "/lib/";

  if (vbos.length == 0) { console.log("No files to zip!\nDone!"); return; }
  console.log('zipping %d files...', vbos.length);
  zip.createWriter(new zip.BlobWriter("application/zip"), function(writer) {
    console.log("Creating zip...");
    var f = 0;
    function nextFile(f) {
      fblob = new Blob([vbos[f].verts], { type: "text/plain" });
      // check for existing filename
      filename = vbos[f].name+".vbo";
      if (filenames.indexOf(filename) == -1) { // if file doesn't already exist:
        filenames.push(filename);
        writer.add(filename, new zip.BlobReader(fblob), function() {
          // callback
          f++;
          if (f < vbos.length) {
            nextFile(f);
          } else close();
        });
      } else {
        console.log(filename, "is a duplicate, skipping");
        f++;
        if (f < vbos.length) {
          nextFile(f);
        } else close();
      }
    }
    function close() {
        // close the writer
      writer.close(function(blob) {
        // save with FileSaver.js
        saveAs(blob, "example.zip");
        console.log("Done!");
        });
    }
    nextFile(f);
  }, onerror);
}

waitForWorkers(loadTiles);

waitForScene(processTiles);

waitForVBOs(zipBlobs);

}
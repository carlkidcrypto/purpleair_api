/**
 * PurpleAir API - Node.js bindings
 * 
 * JavaScript wrapper for the C++ PurpleAir API implementation
 */

// Load the native addon
const purpleairapi_base = require('./build/Release/purpleairapi_base.node');

// Export the classes
module.exports = {
    PurpleAirReadAPI: purpleairapi_base.PurpleAirReadAPI,
    PurpleAirWriteAPI: purpleairapi_base.PurpleAirWriteAPI,
    PurpleAirLocalAPI: purpleairapi_base.PurpleAirLocalAPI,
    PurpleAirAPIError: purpleairapi_base.PurpleAirAPIError
};

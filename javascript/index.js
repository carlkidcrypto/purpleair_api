/**
 * PurpleAir API - Node.js bindings
 * 
 * JavaScript wrapper for the C++ PurpleAir API implementation
 */

// Load the native addon
const purpleairapi_base = require('./build/Release/purpleairapi_base.node');

class PurpleAirLocalAPI extends purpleairapi_base.PurpleAirLocalAPI {
    constructor(ipv4_address_list) {
        if (Array.isArray(ipv4_address_list)) {
            const vec = new purpleairapi_base._string_vector();
            for (const ip of ipv4_address_list) {
                vec.add(String(ip));
            }
            super(vec);
        } else if (ipv4_address_list) {
            super(ipv4_address_list);
        } else {
            super();
        }
    }
}

// Export the classes
module.exports = {
    PurpleAirReadAPI: purpleairapi_base.PurpleAirReadAPI,
    PurpleAirWriteAPI: purpleairapi_base.PurpleAirWriteAPI,
    PurpleAirLocalAPI: PurpleAirLocalAPI,
    PurpleAirAPIError: purpleairapi_base.PurpleAirAPIError,
    StringMap: purpleairapi_base.StringMap,
    StringVector: purpleairapi_base._string_vector
};

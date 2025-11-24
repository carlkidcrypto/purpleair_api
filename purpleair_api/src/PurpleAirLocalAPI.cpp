#include "PurpleAirLocalAPI.hpp"
#include "PurpleAirAPIHelpers.hpp"
#include "PurpleAirAPIError.hpp"

namespace PurpleAirAPI {

PurpleAirLocalAPI::PurpleAirLocalAPI(const std::vector<std::string>& ipv4_address_list)
    : _ipv4_address_list(ipv4_address_list) {
}

std::string PurpleAirLocalAPI::request_local_sensor_data() {
    if (_ipv4_address_list.empty()) {
        throw PurpleAirAPIError("No IPv4 addresses provided for local API");
    }

    // Request data from the first IPv4 address
    // In the future, this could be extended to query all addresses and combine results
    std::string request_url = "http://" + _ipv4_address_list[0] + "/json";
    
    return send_url_get_request(request_url);
}

} // namespace PurpleAirAPI

#include "PurpleAirWriteAPI.hpp"
#include "PurpleAirAPIHelpers.hpp"

namespace PurpleAirAPI {

PurpleAirWriteAPI::PurpleAirWriteAPI(const std::string& api_write_key)
    : _your_api_write_key(api_write_key),
      _base_api_v1_request_string("https://api.purpleair.com/v1/") {
}

std::string PurpleAirWriteAPI::post_create_member(int sensor_index) {
    std::string request_url = _base_api_v1_request_string + "members";
    
    // Create JSON payload
    std::string post_data = "{\"sensor_index\": " + std::to_string(sensor_index) + "}";
    
    return send_url_post_request(request_url, _your_api_write_key, post_data);
}

std::string PurpleAirWriteAPI::delete_member(int member_id) {
    std::string request_url = _base_api_v1_request_string + "members/" + std::to_string(member_id);
    
    return send_url_delete_request(request_url, _your_api_write_key);
}

} // namespace PurpleAirAPI

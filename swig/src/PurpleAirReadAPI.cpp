#include "PurpleAirReadAPI.h"
#include "PurpleAirAPIHelpers.h"
#include <sstream>

namespace PurpleAirAPI {

PurpleAirReadAPI::PurpleAirReadAPI(const std::string& api_read_key)
    : _your_api_read_key(api_read_key),
      _base_api_v1_request_string("https://api.purpleair.com/v1/") {
}

std::string PurpleAirReadAPI::request_sensor_data(
    int sensor_index,
    const std::string& read_key,
    const std::string& fields
) {
    std::string request_url = _base_api_v1_request_string + "sensors/" + std::to_string(sensor_index);
    
    std::map<std::string, std::string> optional_parameters_dict;
    if (!read_key.empty()) {
        optional_parameters_dict["read_key"] = read_key;
    }
    if (!fields.empty()) {
        optional_parameters_dict["fields"] = fields;
    }

    std::string first_optional_parameter_separator = "?";
    return send_url_get_request(
        request_url,
        _your_api_read_key,
        first_optional_parameter_separator,
        optional_parameters_dict
    );
}

std::string PurpleAirReadAPI::request_multiple_sensors_data(
    const std::string& fields,
    const std::string& location_type,
    const std::string& read_keys,
    const std::string& show_only,
    const std::string& modified_since,
    int max_age,
    const std::string& nwlng,
    const std::string& nwlat,
    const std::string& selng,
    const std::string& selat
) {
    std::string request_url = _base_api_v1_request_string + "sensors";
    
    std::map<std::string, std::string> optional_parameters_dict;
    optional_parameters_dict["fields"] = fields;
    
    if (!location_type.empty()) {
        optional_parameters_dict["location_type"] = location_type;
    }
    if (!read_keys.empty()) {
        optional_parameters_dict["read_keys"] = read_keys;
    }
    if (!show_only.empty()) {
        optional_parameters_dict["show_only"] = show_only;
    }
    if (!modified_since.empty()) {
        optional_parameters_dict["modified_since"] = modified_since;
    }
    if (max_age > 0) {
        optional_parameters_dict["max_age"] = std::to_string(max_age);
    }
    if (!nwlng.empty()) {
        optional_parameters_dict["nwlng"] = nwlng;
    }
    if (!nwlat.empty()) {
        optional_parameters_dict["nwlat"] = nwlat;
    }
    if (!selng.empty()) {
        optional_parameters_dict["selng"] = selng;
    }
    if (!selat.empty()) {
        optional_parameters_dict["selat"] = selat;
    }

    std::string first_optional_parameter_separator = "?";
    return send_url_get_request(
        request_url,
        _your_api_read_key,
        first_optional_parameter_separator,
        optional_parameters_dict
    );
}

std::string PurpleAirReadAPI::request_sensor_history(
    int sensor_index,
    const std::string& read_key,
    int start_timestamp,
    int end_timestamp,
    int average,
    const std::string& fields
) {
    std::string request_url = _base_api_v1_request_string + "sensors/" + 
                              std::to_string(sensor_index) + "/history";
    
    std::map<std::string, std::string> optional_parameters_dict;
    optional_parameters_dict["start_timestamp"] = std::to_string(start_timestamp);
    optional_parameters_dict["end_timestamp"] = std::to_string(end_timestamp);
    
    if (!read_key.empty()) {
        optional_parameters_dict["read_key"] = read_key;
    }
    if (average > 0) {
        optional_parameters_dict["average"] = std::to_string(average);
    }
    if (!fields.empty()) {
        optional_parameters_dict["fields"] = fields;
    }

    std::string first_optional_parameter_separator = "?";
    return send_url_get_request(
        request_url,
        _your_api_read_key,
        first_optional_parameter_separator,
        optional_parameters_dict
    );
}

} // namespace PurpleAirAPI

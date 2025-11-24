#include "PurpleAirAPI.hpp"
#include "PurpleAirAPIHelpers.hpp"
#include "PurpleAirAPIError.hpp"
#include <iostream>

namespace PurpleAirAPI {

PurpleAirAPI::PurpleAirAPI(
    const std::string& your_api_read_key,
    const std::string& your_api_write_key,
    const std::string& your_ipv4_address
) : PurpleAirReadAPI(your_api_read_key),
    PurpleAirWriteAPI(your_api_write_key),
    PurpleAirLocalAPI(your_ipv4_address.empty() ? std::vector<std::string>() : std::vector<std::string>{your_ipv4_address}) {
    
    // We cannot have all three parameters be empty
    if (your_api_read_key.empty() && your_api_write_key.empty() && your_ipv4_address.empty()) {
        throw PurpleAirAPIError(
            "Ensure that the right combination of parameters have been provided! "
            "`your_api_read_key` or `your_api_write_key` for external internet requests. Or "
            "just `your_ipv4_address` for local network requests"
        );
    }

    bool retval_api_read_key = false;
    bool retval_api_write_key = false;

    if (!your_api_read_key.empty()) {
        retval_api_read_key = _check_an_api_key(your_api_read_key);
    }

    if (!your_api_write_key.empty()) {
        retval_api_write_key = _check_an_api_key(your_api_write_key);
    }

    if (retval_api_read_key) {
        if (_api_key_types[your_api_read_key] == "READ") {
            std::cout << "PurpleAirAPI: Successfully authenticated read key" << std::endl;
        } else {
            throw PurpleAirAPIError("Ensure 'your_api_read_key' is a read key.");
        }
    }

    if (retval_api_write_key) {
        if (_api_key_types[your_api_write_key] == "WRITE") {
            std::cout << "PurpleAirAPI: Successfully authenticated write key" << std::endl;
        } else {
            throw PurpleAirAPIError("Ensure 'your_api_write_key' is a write key");
        }
    }

    debug_log("_api_versions contains " + std::to_string(_api_versions.size()) + " key(s)");
    debug_log("_api_keys_last_checked contains " + std::to_string(_api_keys_last_checked.size()) + " key(s)");
    debug_log("_api_key_types contains " + std::to_string(_api_key_types.size()) + " key(s)");
    debug_log(your_ipv4_address);
}

bool PurpleAirAPI::_check_an_api_key(const std::string& api_key_to_check) {
    std::string request_url = "https://api.purpleair.com/v1/keys";
    std::string response = send_url_get_request(request_url, api_key_to_check);
    
    // Simple JSON parsing - in production, use a proper JSON library
    // For now, we'll do basic string parsing
    size_t api_version_pos = response.find("\"api_version\"");
    size_t time_stamp_pos = response.find("\"time_stamp\"");
    size_t api_key_type_pos = response.find("\"api_key_type\"");
    
    if (api_version_pos != std::string::npos) {
        size_t start = response.find(":", api_version_pos) + 1;
        size_t end = response.find(",", start);
        if (end == std::string::npos) end = response.find("}", start);
        std::string value = response.substr(start, end - start);
        // Remove quotes and whitespace
        value.erase(std::remove(value.begin(), value.end(), '"'), value.end());
        value.erase(std::remove(value.begin(), value.end(), ' '), value.end());
        _api_versions[api_key_to_check] = value;
    }
    
    if (time_stamp_pos != std::string::npos) {
        size_t start = response.find(":", time_stamp_pos) + 1;
        size_t end = response.find(",", start);
        if (end == std::string::npos) end = response.find("}", start);
        std::string value = response.substr(start, end - start);
        value.erase(std::remove(value.begin(), value.end(), '"'), value.end());
        value.erase(std::remove(value.begin(), value.end(), ' '), value.end());
        _api_keys_last_checked[api_key_to_check] = value;
    }
    
    if (api_key_type_pos != std::string::npos) {
        size_t start = response.find(":", api_key_type_pos) + 1;
        size_t end = response.find(",", start);
        if (end == std::string::npos) end = response.find("}", start);
        std::string value = response.substr(start, end - start);
        value.erase(std::remove(value.begin(), value.end(), '"'), value.end());
        value.erase(std::remove(value.begin(), value.end(), ' '), value.end());
        _api_key_types[api_key_to_check] = value;
    }
    
    return true;
}

std::map<std::string, std::string> PurpleAirAPI::get_api_versions() const {
    return _api_versions;
}

std::map<std::string, std::string> PurpleAirAPI::get_api_key_last_checked() const {
    return _api_keys_last_checked;
}

std::map<std::string, std::string> PurpleAirAPI::get_api_key_type() const {
    return _api_key_types;
}

} // namespace PurpleAirAPI

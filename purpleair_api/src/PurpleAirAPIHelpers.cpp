#include "PurpleAirAPIHelpers.hpp"
#include "PurpleAirAPIError.hpp"
#include <curl/curl.h>
#include <iostream>
#include <sstream>
#include <algorithm>

namespace PurpleAirAPI {

// Debug flag
static bool PRINT_DEBUG_MSGS = false;

// Success HTTP status codes
static const std::vector<int> SUCCESS_CODE_LIST = {200, 201};

// Error HTTP status codes
static const std::vector<int> ERROR_CODES_LIST = {
    400, 403, 404, 429, 500, 502, 503, 504
};

// Callback function for curl to write data
static size_t write_callback(void* contents, size_t size, size_t nmemb, std::string* userp) {
    size_t total_size = size * nmemb;
    userp->append((char*)contents, total_size);
    return total_size;
}

void debug_log(const std::string& msg) {
    if (PRINT_DEBUG_MSGS) {
        std::cerr << "\033[1;31m" << msg << "\x1b[0m" << std::endl;
    }
}

bool verify_request_status_codes(int status_code) {
    if (std::find(SUCCESS_CODE_LIST.begin(), SUCCESS_CODE_LIST.end(), status_code) != SUCCESS_CODE_LIST.end()) {
        return true;
    } else if (std::find(ERROR_CODES_LIST.begin(), ERROR_CODES_LIST.end(), status_code) != ERROR_CODES_LIST.end()) {
        return false;
    } else {
        throw PurpleAirAPIError("Unknown status code - " + std::to_string(status_code) + "!");
    }
}

std::string convert_text_to_json(const std::string& text) {
    if (!text.empty()) {
        debug_log("convert_text_to_json - text: " + text);
    }
    return text;
}

std::string send_url_get_request(
    const std::string& request_url,
    const std::string& api_key_to_use,
    const std::string& first_optional_parameter_separator,
    const std::map<std::string, std::string>& optional_parameters_dict
) {
    CURL* curl;
    CURLcode res;
    std::string response_string;
    std::string full_url = request_url;

    // Build URL with optional parameters
    if (!first_optional_parameter_separator.empty() && !optional_parameters_dict.empty()) {
        full_url += first_optional_parameter_separator;
        bool first = true;
        for (const auto& param : optional_parameters_dict) {
            if (!param.second.empty()) {
                if (!first) {
                    full_url += "&";
                }
                // URL-encode parameter values to handle special characters
                char* encoded_value = curl_easy_escape(nullptr, param.second.c_str(), param.second.length());
                if (encoded_value) {
                    full_url += param.first + "=" + std::string(encoded_value);
                    curl_free(encoded_value);
                } else {
                    full_url += param.first + "=" + param.second;
                }
                first = false;
            }
        }
    }

    debug_log("Request URL: " + full_url);

    curl = curl_easy_init();
    if (curl) {
        struct curl_slist* headers = nullptr;
        
        // Add API key header if provided
        if (!api_key_to_use.empty()) {
            std::string auth_header = "X-API-Key: " + api_key_to_use;
            headers = curl_slist_append(headers, auth_header.c_str());
        }

        curl_easy_setopt(curl, CURLOPT_URL, full_url.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 30L);

        res = curl_easy_perform(curl);

        long response_code;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);

        if (headers) {
            curl_slist_free_all(headers);
        }
        curl_easy_cleanup(curl);

        if (res != CURLE_OK) {
            throw PurpleAirAPIError("CURL error: " + std::string(curl_easy_strerror(res)));
        }

        if (!verify_request_status_codes(response_code)) {
            throw PurpleAirAPIError("HTTP error code: " + std::to_string(response_code) + ", Response: " + response_string);
        }

        return response_string;
    } else {
        throw PurpleAirAPIError("Failed to initialize CURL");
    }
}

std::string send_url_post_request(
    const std::string& request_url,
    const std::string& api_key_to_use,
    const std::string& post_data
) {
    CURL* curl;
    CURLcode res;
    std::string response_string;

    debug_log("POST Request URL: " + request_url);
    debug_log("POST Data: " + post_data);

    curl = curl_easy_init();
    if (curl) {
        struct curl_slist* headers = nullptr;
        
        // Add headers
        if (!api_key_to_use.empty()) {
            std::string auth_header = "X-API-Key: " + api_key_to_use;
            headers = curl_slist_append(headers, auth_header.c_str());
        }
        headers = curl_slist_append(headers, "Content-Type: application/json");

        curl_easy_setopt(curl, CURLOPT_URL, request_url.c_str());
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 30L);

        res = curl_easy_perform(curl);

        long response_code;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);

        if (headers) {
            curl_slist_free_all(headers);
        }
        curl_easy_cleanup(curl);

        if (res != CURLE_OK) {
            throw PurpleAirAPIError("CURL error: " + std::string(curl_easy_strerror(res)));
        }

        if (!verify_request_status_codes(response_code)) {
            throw PurpleAirAPIError("HTTP error code: " + std::to_string(response_code) + ", Response: " + response_string);
        }

        return response_string;
    } else {
        throw PurpleAirAPIError("Failed to initialize CURL");
    }
}

std::string send_url_delete_request(
    const std::string& request_url,
    const std::string& api_key_to_use
) {
    CURL* curl;
    CURLcode res;
    std::string response_string;

    debug_log("DELETE Request URL: " + request_url);

    curl = curl_easy_init();
    if (curl) {
        struct curl_slist* headers = nullptr;
        
        // Add API key header
        if (!api_key_to_use.empty()) {
            std::string auth_header = "X-API-Key: " + api_key_to_use;
            headers = curl_slist_append(headers, auth_header.c_str());
        }

        curl_easy_setopt(curl, CURLOPT_URL, request_url.c_str());
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 30L);

        res = curl_easy_perform(curl);

        long response_code;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);

        if (headers) {
            curl_slist_free_all(headers);
        }
        curl_easy_cleanup(curl);

        if (res != CURLE_OK) {
            throw PurpleAirAPIError("CURL error: " + std::string(curl_easy_strerror(res)));
        }

        if (!verify_request_status_codes(response_code)) {
            throw PurpleAirAPIError("HTTP error code: " + std::to_string(response_code) + ", Response: " + response_string);
        }

        return response_string;
    } else {
        throw PurpleAirAPIError("Failed to initialize CURL");
    }
}

} // namespace PurpleAirAPI

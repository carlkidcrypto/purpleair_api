#ifndef PURPLEAIR_API_HELPERS_HPP
#define PURPLEAIR_API_HELPERS_HPP

#include <string>
#include <map>
#include <vector>

namespace PurpleAirAPI {

/**
 * @brief Print debug messages if debugging is enabled
 * @param msg Debug message to print
 */
void debug_log(const std::string& msg);

/**
 * @brief Verify HTTP status code
 * @param status_code HTTP status code to verify
 * @return true if status code indicates success, false otherwise
 */
bool verify_request_status_codes(int status_code);

/**
 * @brief Convert text to JSON string (simplified for C++)
 * @param text Text to convert
 * @return std::string JSON string
 */
std::string convert_text_to_json(const std::string& text);

/**
 * @brief Send GET request to URL
 * @param request_url URL to send request to
 * @param api_key_to_use API key for authentication
 * @param first_optional_parameter_separator First parameter separator (e.g., "?")
 * @param optional_parameters_dict Optional parameters to include in URL
 * @return std::string Response as JSON string
 */
std::string send_url_get_request(
    const std::string& request_url,
    const std::string& api_key_to_use = "",
    const std::string& first_optional_parameter_separator = "",
    const std::map<std::string, std::string>& optional_parameters_dict = std::map<std::string, std::string>()
);

/**
 * @brief Send POST request to URL
 * @param request_url URL to send request to
 * @param api_key_to_use API key for authentication
 * @param post_data JSON data to send in POST body
 * @return std::string Response as JSON string
 */
std::string send_url_post_request(
    const std::string& request_url,
    const std::string& api_key_to_use,
    const std::string& post_data
);

/**
 * @brief Send DELETE request to URL
 * @param request_url URL to send request to
 * @param api_key_to_use API key for authentication
 * @return std::string Response as JSON string
 */
std::string send_url_delete_request(
    const std::string& request_url,
    const std::string& api_key_to_use
);

} // namespace PurpleAirAPI

#endif // PURPLEAIR_API_HELPERS_HPP

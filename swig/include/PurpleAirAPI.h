#ifndef PURPLEAIR_API_H
#define PURPLEAIR_API_H

#include "PurpleAirReadAPI.h"
#include "PurpleAirWriteAPI.h"
#include "PurpleAirLocalAPI.h"
#include <string>
#include <map>

namespace PurpleAirAPI {

/**
 * @brief Main PurpleAir API class that combines Read, Write, and Local APIs
 */
class PurpleAirAPI : public PurpleAirReadAPI, public PurpleAirWriteAPI, public PurpleAirLocalAPI {
private:
    std::map<std::string, std::string> _api_versions;
    std::map<std::string, std::string> _api_keys_last_checked;
    std::map<std::string, std::string> _api_key_types;

    /**
     * @brief Check if an API key is valid
     * @param api_key_to_check API key to validate
     * @return bool True if valid
     */
    bool _check_an_api_key(const std::string& api_key_to_check);

public:
    /**
     * @brief Construct a new PurpleAirAPI object
     * @param your_api_read_key Optional API read key
     * @param your_api_write_key Optional API write key
     * @param your_ipv4_address Optional IPv4 address for local API
     */
    PurpleAirAPI(
        const std::string& your_api_read_key = "",
        const std::string& your_api_write_key = "",
        const std::string& your_ipv4_address = ""
    );

    /**
     * @brief Get API versions
     * @return std::map<std::string, std::string> API versions map
     */
    std::map<std::string, std::string> get_api_versions() const;

    /**
     * @brief Get API key last checked timestamps
     * @return std::map<std::string, std::string> Last checked timestamps map
     */
    std::map<std::string, std::string> get_api_key_last_checked() const;

    /**
     * @brief Get API key types
     * @return std::map<std::string, std::string> API key types map
     */
    std::map<std::string, std::string> get_api_key_type() const;

    virtual ~PurpleAirAPI() = default;
};

} // namespace PurpleAirAPI

#endif // PURPLEAIR_API_H

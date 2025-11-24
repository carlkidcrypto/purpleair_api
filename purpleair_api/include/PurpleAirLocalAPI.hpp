#ifndef PURPLEAIR_LOCAL_API_HPP
#define PURPLEAIR_LOCAL_API_HPP

#include <string>
#include <vector>

namespace PurpleAirAPI {

/**
 * @brief Class for handling PurpleAir Local API requests
 */
class PurpleAirLocalAPI {
protected:
    std::vector<std::string> _ipv4_address_list;

public:
    /**
     * @brief Construct a new PurpleAirLocalAPI object
     * @param ipv4_address_list List of IPv4 addresses
     */
    explicit PurpleAirLocalAPI(const std::vector<std::string>& ipv4_address_list = std::vector<std::string>());

    /**
     * @brief Request local sensor data
     * @return std::string Local sensor data as JSON string
     */
    std::string request_local_sensor_data();

    virtual ~PurpleAirLocalAPI() = default;
};

} // namespace PurpleAirAPI

#endif // PURPLEAIR_LOCAL_API_HPP

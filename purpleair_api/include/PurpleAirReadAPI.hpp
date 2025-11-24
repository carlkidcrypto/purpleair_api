#ifndef PURPLEAIR_READ_API_HPP
#define PURPLEAIR_READ_API_HPP

#include <string>

namespace PurpleAirAPI {

/**
 * @brief Class for handling PurpleAir Read API requests
 */
class PurpleAirReadAPI {
protected:
    std::string _your_api_read_key;
    std::string _base_api_v1_request_string;

public:
    /**
     * @brief Construct a new PurpleAirReadAPI object
     * @param api_read_key API read key
     */
    explicit PurpleAirReadAPI(const std::string& api_read_key = "");

    /**
     * @brief Request sensor data for a single sensor
     * @param sensor_index Sensor index
     * @param read_key Optional read key for private sensors
     * @param fields Optional fields to include
     * @return std::string Sensor data as JSON string
     */
    std::string request_sensor_data(
        int sensor_index,
        const std::string& read_key = "",
        const std::string& fields = ""
    );

    /**
     * @brief Request data from multiple sensors
     * @param fields Fields to include
     * @param location_type Optional location type filter
     * @param read_keys Optional read keys for private sensors
     * @param show_only Optional show only filter
     * @param modified_since Optional modified since filter
     * @param max_age Optional max age filter
     * @param nwlng Optional northwest longitude
     * @param nwlat Optional northwest latitude
     * @param selng Optional southeast longitude
     * @param selat Optional southeast latitude
     * @return std::string Multiple sensors data as JSON string
     */
    std::string request_multiple_sensors_data(
        const std::string& fields,
        const std::string& location_type = "",
        const std::string& read_keys = "",
        const std::string& show_only = "",
        const std::string& modified_since = "",
        int max_age = 0,
        const std::string& nwlng = "",
        const std::string& nwlat = "",
        const std::string& selng = "",
        const std::string& selat = ""
    );

    /**
     * @brief Request sensor history data
     * @param sensor_index Sensor index
     * @param read_key Optional read key for private sensors
     * @param start_timestamp Start timestamp
     * @param end_timestamp End timestamp
     * @param average Optional average period
     * @param fields Optional fields to include
     * @return std::string Sensor history data as JSON string
     */
    std::string request_sensor_history(
        int sensor_index,
        const std::string& read_key,
        int start_timestamp,
        int end_timestamp,
        int average = 0,
        const std::string& fields = ""
    );

    virtual ~PurpleAirReadAPI() = default;
};

} // namespace PurpleAirAPI

#endif // PURPLEAIR_READ_API_HPP

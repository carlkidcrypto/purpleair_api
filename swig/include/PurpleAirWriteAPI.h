#ifndef PURPLEAIR_WRITE_API_H
#define PURPLEAIR_WRITE_API_H

#include <string>

namespace PurpleAirAPI {

/**
 * @brief Class for handling PurpleAir Write API requests
 */
class PurpleAirWriteAPI {
protected:
    std::string _your_api_write_key;
    std::string _base_api_v1_request_string;

public:
    /**
     * @brief Construct a new PurpleAirWriteAPI object
     * @param api_write_key API write key
     */
    explicit PurpleAirWriteAPI(const std::string& api_write_key = "");

    /**
     * @brief Create a new member
     * @param sensor_index Sensor index
     * @return std::string Response data as JSON string
     */
    std::string post_create_member(int sensor_index);

    /**
     * @brief Delete a member
     * @param member_id Member ID to delete
     * @return std::string Response data as JSON string
     */
    std::string delete_member(int member_id);

    virtual ~PurpleAirWriteAPI() = default;
};

} // namespace PurpleAirAPI

#endif // PURPLEAIR_WRITE_API_H

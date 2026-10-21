#ifndef PURPLEAIR_API_ERROR_H
#define PURPLEAIR_API_ERROR_H

#include <exception>
#include <string>

namespace PurpleAirAPI {

/**
 * @brief Custom exception class for PurpleAir API errors
 */
class PurpleAirAPIError : public std::exception {
private:
    std::string message;

public:
    /**
     * @brief Construct a new PurpleAirAPIError object
     * @param msg Error message
     */
    explicit PurpleAirAPIError(const std::string& msg) : message(msg) {}

    /**
     * @brief Get the error message
     * @return const char* Error message
     */
    virtual const char* what() const noexcept override {
        return message.c_str();
    }

    /**
     * @brief Get the error message as string
     * @return std::string Error message
     */
    std::string get_message() const {
        return message;
    }
};

} // namespace PurpleAirAPI

#endif // PURPLEAIR_API_ERROR_H

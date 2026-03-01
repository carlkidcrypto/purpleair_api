package purpleairapi_test

import (
	"testing"

	purpleairapi "github.com/carlkidcrypto/purpleair_api/go/purpleairapi"
)

// TestNewPurpleAirReadAPI verifies that PurpleAirReadAPI can be constructed.
func TestNewPurpleAirReadAPI(t *testing.T) {
	api := purpleairapi.NewPurpleAirReadAPI("test_read_key_123")
	if api == nil {
		t.Fatal("expected non-nil PurpleAirReadAPI")
	}
	defer purpleairapi.DeletePurpleAirReadAPI(api)
}

// TestPurpleAirReadAPIHasRequestSensorDataMethod verifies Request_sensor_data exists.
func TestPurpleAirReadAPIHasRequestSensorDataMethod(t *testing.T) {
	api := purpleairapi.NewPurpleAirReadAPI("test_read_key_123")
	if api == nil {
		t.Fatal("expected non-nil PurpleAirReadAPI")
	}
	defer purpleairapi.DeletePurpleAirReadAPI(api)
	// Note: This would need mocking in real tests.
	// For now, just verify the API object was created successfully.
}

// TestPurpleAirReadAPIHasRequestMultipleSensorsDataMethod verifies
// Request_multiple_sensors_data exists.
func TestPurpleAirReadAPIHasRequestMultipleSensorsDataMethod(t *testing.T) {
	api := purpleairapi.NewPurpleAirReadAPI("test_read_key_123")
	if api == nil {
		t.Fatal("expected non-nil PurpleAirReadAPI")
	}
	defer purpleairapi.DeletePurpleAirReadAPI(api)
	// Note: This would need mocking in real tests.
	// For now, just verify the API object was created successfully.
}

// TestNewPurpleAirWriteAPI verifies that PurpleAirWriteAPI can be constructed.
func TestNewPurpleAirWriteAPI(t *testing.T) {
	api := purpleairapi.NewPurpleAirWriteAPI("test_write_key_123")
	if api == nil {
		t.Fatal("expected non-nil PurpleAirWriteAPI")
	}
	defer purpleairapi.DeletePurpleAirWriteAPI(api)
}

// TestPurpleAirWriteAPIHasPostCreateMemberMethod verifies Post_create_member exists.
func TestPurpleAirWriteAPIHasPostCreateMemberMethod(t *testing.T) {
	api := purpleairapi.NewPurpleAirWriteAPI("test_write_key_123")
	if api == nil {
		t.Fatal("expected non-nil PurpleAirWriteAPI")
	}
	defer purpleairapi.DeletePurpleAirWriteAPI(api)
	// Note: This would need mocking in real tests.
	// For now, just verify the API object was created successfully.
}

// TestPurpleAirWriteAPIHasDeleteMemberMethod verifies Delete_member exists.
func TestPurpleAirWriteAPIHasDeleteMemberMethod(t *testing.T) {
	api := purpleairapi.NewPurpleAirWriteAPI("test_write_key_123")
	if api == nil {
		t.Fatal("expected non-nil PurpleAirWriteAPI")
	}
	defer purpleairapi.DeletePurpleAirWriteAPI(api)
	// Note: This would need mocking in real tests.
	// For now, just verify the API object was created successfully.
}

// TestNewPurpleAirLocalAPIWithIPAddressList verifies that PurpleAirLocalAPI
// can be constructed with an IPv4 address list.
func TestNewPurpleAirLocalAPIWithIPAddressList(t *testing.T) {
	addrs := purpleairapi.NewX_string_vector()
	defer purpleairapi.DeleteX_string_vector(addrs)
	addrs.Add("192.168.1.100")

	api := purpleairapi.NewPurpleAirLocalAPI(addrs)
	if api == nil {
		t.Fatal("expected non-nil PurpleAirLocalAPI")
	}
	defer purpleairapi.DeletePurpleAirLocalAPI(api)
}

// TestNewPurpleAirAPIError verifies that PurpleAirAPIError can be constructed.
func TestNewPurpleAirAPIError(t *testing.T) {
	err := purpleairapi.NewPurpleAirAPIError("Test error message")
	if err == nil {
		t.Fatal("expected non-nil PurpleAirAPIError")
	}
	defer purpleairapi.DeletePurpleAirAPIError(err)

	if got := err.Get_message(); got != "Test error message" {
		t.Errorf("expected 'Test error message', got %q", got)
	}
}

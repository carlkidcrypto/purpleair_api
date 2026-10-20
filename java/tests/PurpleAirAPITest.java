/**
 * PurpleAir API Tests - Java
 * 
 * Verifies construction and invocation of SWIG Java bindings.
 */

import com.purpleair.api.*;

public class PurpleAirAPITest {
    public static void main(String[] args) {
        System.out.println("Running PurpleAir API Java Tests...");
        int testsRun = 0;

        // Test 1: PurpleAirReadAPI
        PurpleAirReadAPI readApi = new PurpleAirReadAPI("test_read_key_123");
        if (readApi == null) {
            throw new AssertionError("Failed to create PurpleAirReadAPI");
        }
        testsRun++;
        System.out.println("PASS: PurpleAirReadAPI creation");

        // Test 2: PurpleAirWriteAPI
        PurpleAirWriteAPI writeApi = new PurpleAirWriteAPI("test_write_key_123");
        if (writeApi == null) {
            throw new AssertionError("Failed to create PurpleAirWriteAPI");
        }
        testsRun++;
        System.out.println("PASS: PurpleAirWriteAPI creation");

        // Test 3: StringVector and PurpleAirLocalAPI
        StringVector addrs = new StringVector();
        addrs.add("192.168.1.100");
        if (addrs.size() != 1 || !addrs.get(0).equals("192.168.1.100")) {
            throw new AssertionError("StringVector operations failed");
        }
        PurpleAirLocalAPI localApi = new PurpleAirLocalAPI(addrs);
        if (localApi == null) {
            throw new AssertionError("Failed to create PurpleAirLocalAPI");
        }
        testsRun++;
        System.out.println("PASS: PurpleAirLocalAPI with StringVector");

        // Test 4: PurpleAirAPIError
        PurpleAirAPIError err = new PurpleAirAPIError("Test Java Error Message");
        if (err == null || !err.get_message().equals("Test Java Error Message")) {
            throw new AssertionError("PurpleAirAPIError message mismatch: " + (err == null ? "null" : err.get_message()));
        }
        testsRun++;
        System.out.println("PASS: PurpleAirAPIError message verification");

        // Test 5: StringMap
        StringMap map = new StringMap();
        map.put("key1", "val1");
        if (!map.containsKey("key1") || !map.get("key1").equals("val1")) {
            throw new AssertionError("StringMap operations failed");
        }
        testsRun++;
        System.out.println("PASS: StringMap operations");

        // Test 6: Empty IPv4 address list throws exception
        try {
            StringVector emptyAddrs = new StringVector();
            PurpleAirLocalAPI emptyApi = new PurpleAirLocalAPI(emptyAddrs);
            emptyApi.request_local_sensor_data();
            throw new AssertionError("Expected exception was not thrown for empty IP list");
        } catch (RuntimeException expected) {
            testsRun++;
            System.out.println("PASS: PurpleAirLocalAPI empty IP list throws exception");
        }

        System.out.println("All " + testsRun + " Java tests passed successfully!");
    }
}

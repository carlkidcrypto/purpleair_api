/**
 * PurpleAir API Tests - JavaScript
 * Migrated from Python unit tests
 */

describe('PurpleAirAPI', () => {
    const { PurpleAirReadAPI, PurpleAirWriteAPI, PurpleAirLocalAPI, PurpleAirAPIError } = require('../index');

    describe('PurpleAirReadAPI', () => {
        test('should create PurpleAirReadAPI with valid read key', () => {
            const api = new PurpleAirReadAPI('test_read_key_123');
            expect(api).toBeDefined();
        });

        test('should request sensor data', () => {
            const api = new PurpleAirReadAPI('test_read_key_123');
            // Note: This would need mocking in real tests
            // For now, we just verify the method exists
            expect(typeof api.request_sensor_data).toBe('function');
        });

        test('should request multiple sensors data', () => {
            const api = new PurpleAirReadAPI('test_read_key_123');
            expect(typeof api.request_multiple_sensors_data).toBe('function');
        });

        test('should request sensor history', () => {
            const api = new PurpleAirReadAPI('test_read_key_123');
            expect(typeof api.request_sensor_history).toBe('function');
        });
    });

    describe('PurpleAirWriteAPI', () => {
        test('should create PurpleAirWriteAPI with valid write key', () => {
            const api = new PurpleAirWriteAPI('test_write_key_123');
            expect(api).toBeDefined();
        });

        test('should have post_create_member method', () => {
            const api = new PurpleAirWriteAPI('test_write_key_123');
            expect(typeof api.post_create_member).toBe('function');
        });

        test('should have delete_member method', () => {
            const api = new PurpleAirWriteAPI('test_write_key_123');
            expect(typeof api.delete_member).toBe('function');
        });
    });

    describe('PurpleAirLocalAPI', () => {
        test('should create PurpleAirLocalAPI with IP address list', () => {
            const api = new PurpleAirLocalAPI(['192.168.1.100']);
            expect(api).toBeDefined();
        });

        test('should have request_local_sensor_data method', () => {
            const api = new PurpleAirLocalAPI(['192.168.1.100']);
            expect(typeof api.request_local_sensor_data).toBe('function');
        });

        test('should throw error with empty IP list', () => {
            const api = new PurpleAirLocalAPI([]);
            expect(() => {
                api.request_local_sensor_data();
            }).toThrow();
        });
    });

    describe('PurpleAirAPIError', () => {
        test('should create custom error', () => {
            const error = new PurpleAirAPIError('Test error message');
            expect(error).toBeDefined();
            expect(error.get_message()).toBe('Test error message');
        });
    });
});

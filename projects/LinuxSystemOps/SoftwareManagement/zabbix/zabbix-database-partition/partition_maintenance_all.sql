DELIMITER $$
CREATE PROCEDURE `partition_maintenance_all`(SCHEMA_NAME VARCHAR(32))
BEGIN
                CALL partition_maintenance(SCHEMA_NAME, 'history', 7, 24, 14);
                CALL partition_maintenance(SCHEMA_NAME, 'history_log', 7, 24, 14);
                CALL partition_maintenance(SCHEMA_NAME, 'history_str', 7, 24, 14);
                CALL partition_maintenance(SCHEMA_NAME, 'history_text', 7, 24, 14);
                CALL partition_maintenance(SCHEMA_NAME, 'history_uint', 7, 24, 14);
                CALL partition_maintenance(SCHEMA_NAME, 'trends', 365, 24, 14);
                CALL partition_maintenance(SCHEMA_NAME, 'trends_uint', 365, 24, 14);
END$$
DELIMITER ;
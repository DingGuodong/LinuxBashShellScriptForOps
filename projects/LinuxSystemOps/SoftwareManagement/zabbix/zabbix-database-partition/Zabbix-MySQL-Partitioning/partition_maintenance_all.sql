USE zabbix;

DROP PROCEDURE IF EXISTS partition_maintenance_all;

DELIMITER $$
CREATE PROCEDURE `partition_maintenance_all`(SCHEMA_NAME VARCHAR(32))
BEGIN
    CALL partition_maintenance(SCHEMA_NAME, 'history', 'MONTH', 1, 12, 365);
    CALL partition_maintenance(SCHEMA_NAME, 'history_log', 'MONTH', 1, 12, 365);
    CALL partition_maintenance(SCHEMA_NAME, 'history_str', 'MONTH', 1, 12, 365);
    CALL partition_maintenance(SCHEMA_NAME, 'history_text', 'MONTH', 1, 12, 365);
    CALL partition_maintenance(SCHEMA_NAME, 'history_uint', 'MONTH', 1, 12, 365);
    CALL partition_maintenance(SCHEMA_NAME, 'trends', 'MONTH', 1, 12, 3650);
    CALL partition_maintenance(SCHEMA_NAME, 'trends_uint', 'MONTH', 1, 12, 3650);
END$$
DELIMITER ;

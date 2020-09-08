USE zabbix;

DROP PROCEDURE IF EXISTS partition_delete;

DELIMITER $$
CREATE PROCEDURE `partition_delete`(_SCHEMA_NAME VARCHAR(64), _TABLE_NAME VARCHAR(64), _KEEP_DATA_AFTER_TS INT)
BEGIN
    /*
       _SCHEMA_NAME = The DB schema in which to make changes
       _TABLE_NAME = The table with partitions to potentially delete
       _KEEP_DATA_AFTER_TS = Delete any partitions whose VALUES-LESS-THAN is less than or equal to _KEEP_DATA_AFTER_TS
    */

    DECLARE _OLD_PARTITION_NAME VARCHAR(64);
    DECLARE _PARTITIONS_TO_DELETE TEXT DEFAULT "";
    DECLARE __DONE INT DEFAULT FALSE;

    /*
       Get a list of all the partitions whose VALUES-LESS-THAN is less than or equal to _KEEP_DATA_AFTER_TS.
    */
    DECLARE __MY_CURSOR CURSOR FOR
        SELECT partition_name
        FROM information_schema.partitions
        WHERE table_schema = _SCHEMA_NAME
          AND table_name = _TABLE_NAME
          AND PARTITION_DESCRIPTION <> 'MAXVALUE'
          AND CAST(PARTITION_DESCRIPTION AS UNSIGNED) <= _KEEP_DATA_AFTER_TS;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET __DONE = TRUE;

    /*
       Start looping through all the partitions that are too old.
    */
    OPEN __MY_CURSOR;
    read_loop:
    LOOP
        FETCH __MY_CURSOR INTO _OLD_PARTITION_NAME;
        IF __DONE THEN
            LEAVE read_loop;
        END IF;
        SET _PARTITIONS_TO_DELETE = IF(_PARTITIONS_TO_DELETE = "", _OLD_PARTITION_NAME,
                                       CONCAT(_PARTITIONS_TO_DELETE, ", ", _OLD_PARTITION_NAME));
    END LOOP;

    IF _PARTITIONS_TO_DELETE <> "" THEN
        /*
           1. Build the SQL to drop all the partitions that are too old.
           2. Run the SQL to drop the partitions.
           3. Print out the table partitions that were deleted.
        */
        SET @delete_partition_sql =
                CONCAT("ALTER TABLE ", _SCHEMA_NAME, ".", _TABLE_NAME, " DROP PARTITION ", _PARTITIONS_TO_DELETE, ";");
        PREPARE __STMT FROM @delete_partition_sql;
        EXECUTE __STMT;
        DEALLOCATE PREPARE __STMT;

        SELECT CONCAT(_SCHEMA_NAME, ".", _TABLE_NAME) AS `table`, _PARTITIONS_TO_DELETE AS `partitions_deleted`;
    ELSE
        /*
           No partition has been deleted, so print out "N/A" (Not Applicable) to indicate that no change has been made.
        */
        SELECT CONCAT(_SCHEMA_NAME, ".", _TABLE_NAME) AS `table`, "N/A" AS `partitions_deleted`;
    END IF;

END$$
DELIMITER ;

USE zabbix;

DROP PROCEDURE IF EXISTS partition_verify;

DELIMITER $$
CREATE PROCEDURE `partition_verify`(_SCHEMA_NAME VARCHAR(64), _TABLE_NAME VARCHAR(64), _INTERVAL_TYPE VARCHAR(10),
                                    _INTERVAL_VALUE INT)
main:
BEGIN

    DECLARE _NOW_DT DATETIME;
    DECLARE _INTERVALSECS INT;
    DECLARE _EXP_CUR_START_TS INT;
    DECLARE _EXP_CUR_LESS_THAN_TS INT;
    DECLARE _MONTH_FIRST_DAY_DT DATETIME;
    DECLARE _EXP_CUR_START_DT DATETIME;
    DECLARE _EXP_CUR_LESS_THAN_DT DATETIME;
    DECLARE _PARTITION_NAME VARCHAR(16);
    DECLARE __RET_ROWS INT;

    SET _NOW_DT = NOW();

    /*
     * Check if any partitions exist for the given _SCHEMA_NAME._TABLE_NAME.
     */
    SELECT COUNT(1)
    INTO __RET_ROWS
    FROM information_schema.PARTITIONS
    WHERE TABLE_SCHEMA = _SCHEMA_NAME
      AND TABLE_NAME = _TABLE_NAME
      AND PARTITION_NAME IS NULL;

    /*
     * If partitions do not exist, go ahead and partition the table.
     */
    IF __RET_ROWS = 1 THEN

        # intervals with a fixed length
        IF _INTERVAL_TYPE IN ('HOUR', 'DAY') THEN

            CASE _INTERVAL_TYPE
                WHEN 'HOUR' THEN # We make the beginning of this hour as the start point of the current interval.
                SET _INTERVALSECS = _INTERVAL_VALUE * 3600;
                SET _EXP_CUR_START_TS = UNIX_TIMESTAMP(DATE_FORMAT(_NOW_DT, '%Y-%m-%d %H:00:00'));
                WHEN 'DAY' THEN # We make the beginning of today as the start point of the current interval.
                SET _INTERVALSECS = _INTERVAL_VALUE * 86400;
                SET _EXP_CUR_START_TS = UNIX_TIMESTAMP(DATE_FORMAT(_NOW_DT, '%Y-%m-%d 00:00:00'));
                END CASE;

            SET _EXP_CUR_LESS_THAN_TS = _EXP_CUR_START_TS + _INTERVALSECS;

            # intervals with a variable length
        ELSEIF _INTERVAL_TYPE = 'MONTH' THEN

            CASE _INTERVAL_TYPE
                WHEN 'MONTH' THEN # We make the first day of this month as the start point of the current interval.
                SET _MONTH_FIRST_DAY_DT = DATE_FORMAT(_NOW_DT, '%Y-%m-01 00:00:00');
                SET _EXP_CUR_START_DT = _MONTH_FIRST_DAY_DT;
                END CASE;

            SET _EXP_CUR_LESS_THAN_TS = UNIX_TIMESTAMP(DATE_ADD(_EXP_CUR_START_DT, INTERVAL _INTERVAL_VALUE MONTH));

        ELSE
            SELECT 'Invalid interval type specified.' AS Error;
            LEAVE main;
        END IF;

        -- Change the table into a partitioned one with a MAXVALUE partition.
        SET _EXP_CUR_LESS_THAN_DT = FROM_UNIXTIME(_EXP_CUR_LESS_THAN_TS);
        SET _PARTITION_NAME = DATE_FORMAT(_EXP_CUR_LESS_THAN_DT, 'bf%Y%m%d%H%i%s');

        -- Create the partitioning query.
        SET @partitioning_sql = CONCAT("ALTER TABLE ", _SCHEMA_NAME, ".", _TABLE_NAME, " PARTITION BY RANGE(`clock`)");
        SET @partitioning_sql =
                CONCAT(@partitioning_sql, '(PARTITION ', _PARTITION_NAME, ' VALUES LESS THAN (', _EXP_CUR_LESS_THAN_TS,
                       '), ');
        SET @partitioning_sql = CONCAT(@partitioning_sql, 'PARTITION bf99991231235959 VALUES LESS THAN MAXVALUE);');

        -- Run the partitioning query.
        PREPARE __STMT FROM @partitioning_sql;
        EXECUTE __STMT;
        DEALLOCATE PREPARE __STMT;

        SELECT CONCAT(_SCHEMA_NAME, ".", _TABLE_NAME)        AS `table`,
               CONCAT(_PARTITION_NAME, ", bf99991231235959") AS `partitions_created`;

    END IF;

END$$
DELIMITER ;

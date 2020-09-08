USE zabbix;

DROP PROCEDURE IF EXISTS partition_create;

DELIMITER $$
CREATE PROCEDURE `partition_create`(_SCHEMA_NAME varchar(64), _TABLE_NAME varchar(64), _INTERVAL_TYPE VARCHAR(10),
                                    _INTERVAL_VALUE INT, _INTERVALS INT)
main:
BEGIN

    DECLARE _CUR_MAX_LESS_THAN INT;
    DECLARE _NOW_DT DATETIME;
    DECLARE _NOW_TS INT;
    DECLARE _INTERVALSECS INT;
    DECLARE _EXP_FIRST_START_TS INT;
    DECLARE _EXP_MAX_LESS_THAN INT;
    DECLARE _MONTH_FIRST_DAY_DT DATETIME;
    DECLARE _EXP_FIRST_START_DT DATETIME;
    DECLARE _NEW_PARTITION_NAME VARCHAR(16);
    DECLARE _PARTITIONS_TO_CREATE TEXT DEFAULT "";
    DECLARE _MONTH_OFFSET INT;
    DECLARE __RET_ROWS INT;
    DECLARE __LESS_THAN_TS INT;
    DECLARE __LESS_THAN_DT DATETIME;
    DECLARE __INTERVAL INT;

    # You can create 50 partitions at most.
    IF _INTERVALS > 50 THEN SET _INTERVALS = 50; END IF;

    # See if the bf99991231235959 partition exists.
    SELECT COUNT(1)
    INTO __RET_ROWS
    FROM information_schema.PARTITIONS
    WHERE TABLE_SCHEMA = _SCHEMA_NAME
      AND TABLE_NAME = _TABLE_NAME
      AND PARTITION_NAME = 'bf99991231235959';

    IF __RET_ROWS <> 1 THEN
        SELECT 'No bf99991231235959 partition exists.' AS Error;
        LEAVE main;
    END IF;

    # Get the current max 'VALUES LESS THAN' of existing partitions except 'MAXVALUE'.  
    SELECT MAX(PARTITION_DESCRIPTION)
    INTO _CUR_MAX_LESS_THAN
    FROM information_schema.PARTITIONS
    WHERE TABLE_SCHEMA = _SCHEMA_NAME
      AND TABLE_NAME = _TABLE_NAME
      AND PARTITION_DESCRIPTION <> 'MAXVALUE';

    SET _NOW_DT = NOW();
    SET _NOW_TS = UNIX_TIMESTAMP(_NOW_DT);

    # intervals with a fixed length
    IF _INTERVAL_TYPE IN ('HOUR', 'DAY') THEN

        CASE _INTERVAL_TYPE
            WHEN 'HOUR' THEN SET _INTERVALSECS = _INTERVAL_VALUE * 3600;

                             IF _CUR_MAX_LESS_THAN IS NULL OR FROM_UNIXTIME(_CUR_MAX_LESS_THAN, '%Y-%m-%d %H:%i:%s') <>
                                                              FROM_UNIXTIME(_CUR_MAX_LESS_THAN, '%Y-%m-%d %H:00:00') THEN
                                 # We make the beginning of this hour as the start point of the current interval if no partition but the MAXVALUE one exists or the interval type is different from the current one.
                                 SET _EXP_FIRST_START_TS = UNIX_TIMESTAMP(DATE_FORMAT(_NOW_DT, '%Y-%m-%d %H:00:00'));
                             ELSE
                                 # We get the start point of the current interval here if _CUR_MAX_LESS_THAN is less than _NOW_TS. Otherwise, we get the start point of the next interval.
                                 SET _EXP_FIRST_START_TS = _NOW_TS + ((_CUR_MAX_LESS_THAN - _NOW_TS) % _INTERVALSECS);
                             END IF;
            WHEN 'DAY' THEN SET _INTERVALSECS = _INTERVAL_VALUE * 86400;

                            IF _CUR_MAX_LESS_THAN IS NULL OR FROM_UNIXTIME(_CUR_MAX_LESS_THAN, '%Y-%m-%d %H:%i:%s') <>
                                                             FROM_UNIXTIME(_CUR_MAX_LESS_THAN, '%Y-%m-%d 00:00:00') THEN
                                # We make the beginning of today as the start point of the current interval if no partition but the MAXVALUE one exists or the interval is different from the current one.
                                SET _EXP_FIRST_START_TS = UNIX_TIMESTAMP(DATE_FORMAT(_NOW_DT, '%Y-%m-%d 00:00:00'));
                            ELSE
                                # We get the start point of the current interval here if _CUR_MAX_LESS_THAN is less than _NOW_TS. Otherwise, we get the start point of the next interval.
                                SET _EXP_FIRST_START_TS = _NOW_TS + ((_CUR_MAX_LESS_THAN - _NOW_TS) % _INTERVALSECS);
                            END IF;
            END CASE;

        # We need to add an interval to it to get the start point of the next interval if _EXP_FIRST_START_TS is the start point of the current interval.
        IF _EXP_FIRST_START_TS <= _NOW_TS THEN SET _EXP_FIRST_START_TS = _EXP_FIRST_START_TS + _INTERVALSECS; END IF;

        SET _EXP_MAX_LESS_THAN = _EXP_FIRST_START_TS + _INTERVALSECS * _INTERVALS;

        # intervals with a variable length
    ELSEIF _INTERVAL_TYPE = 'MONTH' THEN

        CASE _INTERVAL_TYPE
            WHEN 'MONTH' THEN SET _MONTH_FIRST_DAY_DT = DATE_FORMAT(_NOW_DT, '%Y-%m-01 00:00:00');

                              IF _CUR_MAX_LESS_THAN IS NULL OR FROM_UNIXTIME(_CUR_MAX_LESS_THAN, '%Y-%m-%d %H:%i:%s') <>
                                                               FROM_UNIXTIME(_CUR_MAX_LESS_THAN, '%Y-%m-01 00:00:00') THEN
                                  # We make the first day of this month as the start point of the current interval if no partition but the MAXVALUE one exists or the interval type is different from the current one.
                                  SET _EXP_FIRST_START_DT = _MONTH_FIRST_DAY_DT;
                              ELSE
                                  # We get the start point of the current interval here if _CUR_MAX_LESS_THAN is less than the first day of this month. Otherwise, we get the start point of the next interval.
                                  SET _MONTH_OFFSET =
                                              PERIOD_DIFF(DATE_FORMAT(FROM_UNIXTIME(_CUR_MAX_LESS_THAN), '%Y%m'),
                                                          DATE_FORMAT(_MONTH_FIRST_DAY_DT, '%Y%m')) % _INTERVAL_VALUE;
                                  SET _EXP_FIRST_START_DT = DATE_ADD(_MONTH_FIRST_DAY_DT, INTERVAL _MONTH_OFFSET MONTH);
                              END IF;

            # We need to add an interval to it to get the start point of the next interval if _EXP_FIRST_START_DT is the start point of the current interval.
                              IF _EXP_FIRST_START_DT <= _MONTH_FIRST_DAY_DT THEN
                                  SET _EXP_FIRST_START_DT =
                                          DATE_ADD(_EXP_FIRST_START_DT, INTERVAL _INTERVAL_VALUE MONTH);
                              END IF;
            END CASE;

        SET _EXP_MAX_LESS_THAN =
                UNIX_TIMESTAMP(DATE_ADD(_EXP_FIRST_START_DT, INTERVAL _INTERVAL_VALUE * _INTERVALS MONTH));

    ELSE
        SELECT 'Invalid interval type specified.' AS Error;
        LEAVE main;
    END IF;

    SET @create_partition_sql = 'PARTITION bf99991231235959 VALUES LESS THAN MAXVALUE);';
    SET __LESS_THAN_TS = _EXP_MAX_LESS_THAN;
    SET __LESS_THAN_DT = FROM_UNIXTIME(__LESS_THAN_TS);
    SET __INTERVAL = 1;

    sql_loop:
    LOOP
        IF __INTERVAL > _INTERVALS THEN
            LEAVE sql_loop;
        END IF;

        IF __LESS_THAN_TS <= _CUR_MAX_LESS_THAN THEN
            LEAVE sql_loop;
        END IF;

        SET _NEW_PARTITION_NAME = DATE_FORMAT(__LESS_THAN_DT, 'bf%Y%m%d%H%i%s');
        SET @create_partition_sql =
                CONCAT('PARTITION ', _NEW_PARTITION_NAME, ' VALUES LESS THAN (', __LESS_THAN_TS, '), ',
                       @create_partition_sql);
        SET _PARTITIONS_TO_CREATE = IF(_PARTITIONS_TO_CREATE = "", _NEW_PARTITION_NAME,
                                       CONCAT(_NEW_PARTITION_NAME, ", ", _PARTITIONS_TO_CREATE));

        # Determine the previous VALUES LESS THAN value.
        IF _INTERVAL_TYPE IN ('HOUR', 'DAY') THEN
            SET __LESS_THAN_TS = __LESS_THAN_TS - _INTERVALSECS;
            SET __LESS_THAN_DT = FROM_UNIXTIME(__LESS_THAN_TS);
        ELSEIF _INTERVAL_TYPE = 'MONTH' THEN
            SET __LESS_THAN_DT = DATE_SUB(__LESS_THAN_DT, INTERVAL _INTERVAL_VALUE month);
            SET __LESS_THAN_TS = UNIX_TIMESTAMP(__LESS_THAN_DT);
        END IF;

        SET __INTERVAL = __INTERVAL + 1;
    END LOOP;

    IF _PARTITIONS_TO_CREATE <> "" THEN
        # Complement the SQL statement with the forepart.
        SET @create_partition_sql =
                CONCAT('ALTER TABLE ', _SCHEMA_NAME, '.', _TABLE_NAME, ' REORGANIZE PARTITION bf99991231235959 INTO (',
                       @create_partition_sql);

        # Execute the SQL statement.
        PREPARE __STMT FROM @create_partition_sql;
        EXECUTE __STMT;
        DEALLOCATE PREPARE __STMT;

        SELECT CONCAT(_SCHEMA_NAME, ".", _TABLE_NAME) AS `table`, _PARTITIONS_TO_CREATE AS `partitions_created`;
    ELSE
        # No partition has been created, so print out "N/A" (Not Applicable) to indicate that no change has been made.
        SELECT CONCAT(_SCHEMA_NAME, ".", _TABLE_NAME) AS `table`, "N/A" AS `partitions_created`;
    END IF;

END$$
DELIMITER ;

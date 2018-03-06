from Mariadb import Mariadb


# Note to self, grab both min and max at the same time!
SELECT
    P.f_id, P.id, P.callsign, F.status,
    MIN_T.min_time, MIN_T.start_lat, MIN_T.start_lon,
    MAX_T.max_time, MAX_T.end_lat, MAX_T.end_lon,
    ALT.max_alt, ALT.min_alt
FROM BeelineGPS P
JOIN (SELECT flight_id AS f_id, status FROM Flights) F ON F.f_id = P.f_id
JOIN (
    SELECT id, lat AS end_lat, lon AS end_lon, MAX(time) AS max_time
    FROM BeelineGPS GROUP BY f_id, callsign
    ) MAX_T ON MAX_T.id = P.id
JOIN (
    SELECT id, lat AS start_lat, lon AS start_lon, MIN(time) AS min_time
    FROM BeelineGPS GROUP BY f_id, callsign
    ) MIN_T ON MIN_T.id = P.id
JOIN (
    SELECT id, MAX(alt) AS max_alt, MIN(alt) AS min_alt FROM BeelineGPS GROUP BY f_id, callsign
    ) ALT ON ALT.id = P.id
;


# working (tested) version:

SELECT
    P.f_id, P.id, P.callsign, F.status,
    MIN_T.min_time, MIN_T.start_lat, MIN_T.start_lon,
    MAX_T.max_time, MAX_T.end_lat, MAX_T.end_lon,
    MAX_ALT.max_alt, MIN_ALT.min_alt
FROM BeelineGPS P
JOIN (SELECT flight_id AS f_id, status FROM Flights) F ON F.f_id = P.f_id
JOIN (
    SELECT id, lat AS end_lat, lon AS end_lon, MAX(time) AS max_time
    FROM BeelineGPS GROUP BY f_id, callsign
    ) MAX_T ON MAX_T.id = P.id
JOIN (
    SELECT id, lat AS start_lat, lon AS start_lon, MIN(time) AS min_time
    FROM BeelineGPS GROUP BY f_id, callsign
    ) MIN_T ON MIN_T.id = P.id
JOIN (
    SELECT id, MAX(alt) AS max_alt FROM BeelineGPS GROUP BY f_id, callsign
    ) MAX_ALT ON MAX_ALT.id = P.id
JOIN (
    SELECT id, MIN(alt) AS min_alt FROM BeelineGPS GROUP BY f_id, callsign
    ) MIN_ALT ON MIN_ALT.id = P.id
;

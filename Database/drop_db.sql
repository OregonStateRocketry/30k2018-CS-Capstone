ALTER TABLE `BeelineGPS` DROP FOREIGN KEY `BeelineGPS_fk0`;

ALTER TABLE `Rocket_Avionics` DROP FOREIGN KEY `Rocket_Avionics_fk0`;

ALTER TABLE `TeleMega` DROP FOREIGN KEY `TeleMega_fk0`;

ALTER TABLE `Payload_Avionics` DROP FOREIGN KEY `Payload_Avionics_fk0`;

ALTER TABLE `Event_Logs` DROP FOREIGN KEY `Event_Logs_fk0`;

ALTER TABLE `raw_aprs` DROP FOREIGN KEY `raw_aprs_fk0`;

ALTER TABLE `Parser_Status` DROP FOREIGN KEY `Parser_Status_fk0`;

DROP TABLE IF EXISTS `Flights`;

DROP TABLE IF EXISTS `BeelineGPS`;

DROP TABLE IF EXISTS `Rocket_Avionics`;

DROP TABLE IF EXISTS `TeleMega`;

DROP TABLE IF EXISTS `Payload_Avionics`;

DROP TABLE IF EXISTS `Event_Logs`;

DROP TABLE IF EXISTS `raw_aprs`;

DROP TABLE IF EXISTS `Parser_Status`;


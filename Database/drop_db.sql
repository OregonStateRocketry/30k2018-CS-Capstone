CREATE TABLE IF NOT EXISTS `BeelineGPS`;

ALTER TABLE `BeelineGPS` DROP FOREIGN KEY IF EXISTS `BeelineGPS_fk0`;

ALTER TABLE `Rocket_Avionics` DROP FOREIGN KEY IF EXISTS `Rocket_Avionics_fk0`;

ALTER TABLE `TeleMega` DROP FOREIGN KEY IF EXISTS `TeleMega_fk0`;

ALTER TABLE `Payload_Avionics` DROP FOREIGN KEY IF EXISTS `Payload_Avionics_fk0`;

ALTER TABLE `Event_Logs` DROP FOREIGN KEY IF EXISTS `Event_Logs_fk0`;

ALTER TABLE `raw_aprs` DROP FOREIGN KEY IF EXISTS `raw_aprs_fk0`;

CREATE TABLE `Parser_Status` (
	`parser_id` varchar(25) NOT NULL AUTO_INCREMENT,
	`using_f_id` INT,
	`last_activity` DATETIME NOT NULL,
	`status` VARCHAR(25),
	PRIMARY KEY (`parser_id`)
) IF NOT EXISTS;

ALTER TABLE `Parser_Status` DROP FOREIGN KEY IF EXISTS `Parser_Status_fk0`;

DROP TABLE IF EXISTS `Flights`;

DROP TABLE IF EXISTS `BeelineGPS`;

DROP TABLE IF EXISTS `Rocket_Avionics`;

DROP TABLE IF EXISTS `TeleMega`;

DROP TABLE IF EXISTS `Payload_Avionics`;

DROP TABLE IF EXISTS `Event_Logs`;

DROP TABLE IF EXISTS `raw_aprs`;

DROP TABLE IF EXISTS `Parser_Status`;

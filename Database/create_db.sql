CREATE TABLE `Flights` (
	`flight_id` INT NOT NULL AUTO_INCREMENT,
	`start_timestamp` DATETIME NOT NULL,
	`last_timestamp` DATETIME,
	`launch_lat` VARCHAR(25),
	`launch_lon` VARCHAR(25),
	`max_alt` INT(6) DEFAULT '0',
	`launch_alt` INT(6),
	`status` VARCHAR(25) NOT NULL DEFAULT 'Inactive',
	PRIMARY KEY (`flight_id`)
);

CREATE TABLE `BeelineGPS` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`time` DATETIME NOT NULL,
	`lat` VARCHAR(25) NOT NULL,
	`lon` VARCHAR(25) NOT NULL,
	`alt` INT(6) NOT NULL DEFAULT '0',
	`callsign` VARCHAR(25) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Rocket_Avionics` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`time` DATETIME NOT NULL,
	`acc_x` DECIMAL NOT NULL,
	`acc_y` DECIMAL NOT NULL,
	`gyro_x` DECIMAL NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `TeleMega` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`time` DATETIME NOT NULL,
	`lat` VARCHAR(25) NOT NULL,
	`lon` VARCHAR(25) NOT NULL,
	`alt` INT(6) NOT NULL DEFAULT '0',
	`callsign` VARCHAR(25) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Payload_Avionics` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`time` DATETIME NOT NULL,
	`acc_x` DECIMAL NOT NULL,
	`acc_y` DECIMAL NOT NULL,
	`gyro_x` DECIMAL NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Event_Logs` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`time` DATETIME NOT NULL,
	`event_type` VARCHAR(255) NOT NULL,
	`data` VARCHAR(255),
	`status` VARCHAR(25),
	PRIMARY KEY (`id`)
);

CREATE TABLE `raw_aprs` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`p_id` varchar(25) NOT NULL,
	`time` DATETIME NOT NULL,
	`data` VARCHAR(255) NOT NULL,
	`callsign` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Parser_Status` (
	`parser_id` varchar(25) NOT NULL,
	`using_f_id` INT,
	`last_activity` DATETIME NOT NULL,
	`status` VARCHAR(25),
	PRIMARY KEY (`parser_id`)
);

ALTER TABLE `BeelineGPS` ADD CONSTRAINT `BeelineGPS_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `Rocket_Avionics` ADD CONSTRAINT `Rocket_Avionics_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `TeleMega` ADD CONSTRAINT `TeleMega_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `Payload_Avionics` ADD CONSTRAINT `Payload_Avionics_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `Event_Logs` ADD CONSTRAINT `Event_Logs_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `raw_aprs` ADD CONSTRAINT `raw_aprs_fk0` FOREIGN KEY (`p_id`) REFERENCES `Parser_Status`(`parser_id`);

ALTER TABLE `Parser_Status` ADD CONSTRAINT `Parser_Status_fk0` FOREIGN KEY (`using_f_id`) REFERENCES `Flights`(`flight_id`);


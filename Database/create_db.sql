CREATE TABLE IF NOT EXISTS `Flights` (
    `flight_id` INT NOT NULL AUTO_INCREMENT,
    `start_timestamp` TIMESTAMP NOT NULL,
    `last_timestamp` TIMESTAMP,
    `launch_lat` VARCHAR(255),
    `launch_lon` VARCHAR(255),
    `max_alt` INT(6) DEFAULT '0',
    `launch_alt` INT(6),
    `status` VARCHAR(255) NOT NULL DEFAULT 'inactive',
    PRIMARY KEY (`flight_id`)
);

CREATE TABLE IF NOT EXISTS `BeelineGPS` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `f_id` INT NOT NULL,
    `time` TIMESTAMP NOT NULL,
    `lat` VARCHAR(255) NOT NULL,
    `lon` VARCHAR(255) NOT NULL,
    `alt` INT(6) NOT NULL DEFAULT '0',
    `callsign` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Rocket_Avionics` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `f_id` INT NOT NULL,
    `time` TIMESTAMP NOT NULL,
    `acc_x` DECIMAL NOT NULL,
    `acc_y` DECIMAL NOT NULL,
    `gyro_x` DECIMAL NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `TeleMega` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `f_id` INT NOT NULL,
    `time` TIMESTAMP NOT NULL,
    `lat` VARCHAR(255) NOT NULL,
    `lon` VARCHAR(255) NOT NULL,
    `alt` INT(6) NOT NULL DEFAULT '0',
    `callsign` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Payload_Avionics` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `f_id` INT NOT NULL,
    `time` TIMESTAMP NOT NULL,
    `acc_x` DECIMAL NOT NULL,
    `acc_y` DECIMAL NOT NULL,
    `gyro_x` DECIMAL NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Event_Logs` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `f_id` INT NOT NULL,
    `event_type` VARCHAR(255) NOT NULL,
    `data` VARCHAR(255),
    `status` VARCHAR(255),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `raw_aprs` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `time` TIMESTAMP NOT NULL,
    `callsign` VARCHAR(255) NOT NULL,
    `data` VARCHAR(255) NOT NULL,
    `p_id` INT NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Parser_Status` (
    `parser_id` INT NOT NULL AUTO_INCREMENT,
    `using_f_id` INT,
    `last_activity` TIMESTAMP NOT NULL,
    `status` VARCHAR(255),
    PRIMARY KEY (`parser_id`)
);

ALTER TABLE `BeelineGPS` ADD CONSTRAINT `BeelineGPS_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `Rocket_Avionics` ADD CONSTRAINT `Rocket_Avionics_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `TeleMega` ADD CONSTRAINT `TeleMega_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `Payload_Avionics` ADD CONSTRAINT `Payload_Avionics_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `Event_Logs` ADD CONSTRAINT `Event_Logs_fk0` FOREIGN KEY (`f_id`) REFERENCES `Flights`(`flight_id`);

ALTER TABLE `raw_aprs` ADD CONSTRAINT `raw_aprs_fk0` FOREIGN KEY (`p_id`) REFERENCES `Parser_Status`(`parser_id`);

ALTER TABLE `Parser_Status` ADD CONSTRAINT `Parser_Status_fk0` FOREIGN KEY (`using_f_id`) REFERENCES `Flights`(`flight_id`);


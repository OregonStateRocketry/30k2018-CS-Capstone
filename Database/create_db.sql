CREATE TABLE `Flights` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`status` VARCHAR(25) NOT NULL DEFAULT 'Inactive',
	`description` VARCHAR(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE `Callsigns` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`callsign` varchar(25) NOT NULL UNIQUE,
	PRIMARY KEY (`id`, `callsign`)
);

CREATE TABLE `Avionics_State` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`state` varchar(25) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `TeleMega_Sensor` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`time` DATETIME NOT NULL,
	`orient` INT(8) NOT NULL,
	`accel` INT(16) NOT NULL,
	`pres` INT(32) NOT NULL,
	`temp` INT(16) NOT NULL,
	`accel_x` INT(16) NOT NULL,
	`accel_y` INT(16) NOT NULL,
	`accel_z` INT(16) NOT NULL,
	`gyro_x` INT(16) NOT NULL,
	`gyro_y` INT(16) NOT NULL,
	`gyro_z` INT(16) NOT NULL,
	`mag_x` INT(16) NOT NULL,
	`mag_y` INT(16) NOT NULL,
	`mag_z` INT(16) NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`f_id`) REFERENCES `Flights`(`id`)
);

CREATE TABLE `Event_Logs` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`time` DATETIME(4) DEFAULT CURRENT_TIMESTAMP,
	`event_type` VARCHAR(255),
	`data` VARCHAR(255),
	`status` VARCHAR(25),
	PRIMARY KEY (`id`),
	FOREIGN KEY (`f_id`) REFERENCES `Flights`(`id`)
);

CREATE TABLE `Parser_Status` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`serialNum` varchar(25) NOT NULL UNIQUE,
	`using_f_id` INT,
	`last_activity` DATETIME DEFAULT CURRENT_TIMESTAMP,
	`status` VARCHAR(25),
	`callsign` VARCHAR(25),
	PRIMARY KEY (`id`, `serialNum`),
	FOREIGN KEY (`using_f_id`) REFERENCES `Flights`(`id`)
);

CREATE TABLE `raw_aprs` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`p_id` INT NOT NULL,
	`time` DATETIME(4) DEFAULT CURRENT_TIMESTAMP,
	`data` VARCHAR(255) NOT NULL,
	`callsign` VARCHAR(25),
	PRIMARY KEY (`id`),
	FOREIGN KEY (`p_id`) REFERENCES `Parser_Status`(`id`)
);

CREATE TABLE `TeleMega_Voltage` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`time` DATETIME NOT NULL,
	`state` INT(8) NOT NULL,
	`v_batt` INT(16) NOT NULL,
	`v_pyro` INT(16) NOT NULL,
	`pyro_sense` INT(8) NOT NULL,
	`ground_pres` INT(32) NOT NULL,
	`ground_accel` INT(16) NOT NULL,
	`accel_plus_g` INT(16) NOT NULL,
	`accel_minus_g` INT(16) NOT NULL,
	`acceleration` INT(16) NOT NULL,
	`speed` INT(16) NOT NULL,
	`height` INT(16) NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`f_id`) REFERENCES `Flights`(`id`)
);

CREATE TABLE `BeelineGPS` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`c_id` INT NOT NULL,
	`p_id` INT NOT NULL,
	`time` DATETIME(4) DEFAULT CURRENT_TIMESTAMP,
	`lat` VARCHAR(25),
	`lon` VARCHAR(25),
	`alt` INT(6) DEFAULT '0',
	PRIMARY KEY (`id`),
	FOREIGN KEY (`f_id`) REFERENCES `Flights`(`id`),
	FOREIGN KEY (`c_id`) REFERENCES `Callsigns`(`id`),
	FOREIGN KEY (`p_id`) REFERENCES `Parser_Status`(`id`)
);

CREATE TABLE `Payload_Avionics` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`s_id` INT NOT NULL,
	`time` DATETIME(4) NOT NULL,
	`acc_x` FLOAT,
	`acc_y` FLOAT,
	`acc_z` FLOAT,
	`gyro_x` FLOAT,
	`gyro_y` FLOAT,
	`gyro_z` FLOAT,
	`mag_x` FLOAT,
	`mag_y` FLOAT,
	`mag_z` FLOAT,
	`temp` FLOAT,
	`alt` INT,
	`prop_pid` INT,
	`prop_pwm` INT,
	`counter_pid` INT,
	`counter_pwm` INT,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`f_id`) REFERENCES `Flights`(`id`),
	FOREIGN KEY (`s_id`) REFERENCES `Avionics_State`(`id`)
);

CREATE TABLE `Rocket_Avionics` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f_id` INT NOT NULL,
	`s_id` INT NOT NULL,
	`time` DATETIME(4) NOT NULL,
	`acc_x` FLOAT,
	`acc_y` FLOAT,
	`acc_z` FLOAT,
	`gyro_x` FLOAT,
	`gyro_y` FLOAT,
	`gyro_z` FLOAT,
	`mag_x` FLOAT,
	`mag_y` FLOAT,
	`mag_z` FLOAT,
	`temp` FLOAT,
	`alt` INT,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`f_id`) REFERENCES `Flights`(`id`),
	FOREIGN KEY (`s_id`) REFERENCES `Avionics_State`(`id`)
);

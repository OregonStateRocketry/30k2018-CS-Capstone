DROP TABLE IF EXISTS payload.Avionics;
DROP TABLE IF EXISTS payload.Event_Logs;

CREATE TABLE `Avionics` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`time` DATETIME(3) DEFAULT NOW(3),
	`acc1_x` FLOAT,
	`acc1_y` FLOAT,
	`acc1_z` FLOAT,
	`gyro1_x` FLOAT,
	`gyro1_y` FLOAT,
	`gyro1_z` FLOAT,
	`acc2_x` FLOAT,
	`acc2_y` FLOAT,
	`acc2_z` FLOAT,
	`gyro2_x` FLOAT,
	`gyro2_y` FLOAT,
	`gyro2_z` FLOAT,
	`acc3_x` FLOAT,
	`acc3_y` FLOAT,
	`acc3_z` FLOAT,
	`gyro3_x` FLOAT,
	`gyro3_y` FLOAT,
	`gyro3_z` FLOAT,
	`mag_x` FLOAT,
	`mag_y` FLOAT,
	`mag_z` FLOAT,
	`temperature` FLOAT,
	`prop_pid` INT,
	`prop_pwm` INT,
	`counter_pid` INT,
	`counter_pwm` INT,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Event_Logs` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`time` DATETIME NOT NULL,
	`event_type` VARCHAR(255) NOT NULL,
	`data` VARCHAR(255),
	`status` VARCHAR(25),
	PRIMARY KEY (`id`)
);

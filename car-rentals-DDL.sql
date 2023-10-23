-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema car-rentals
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema car-rentals
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `car-rentals` DEFAULT CHARACTER SET utf8 ;
USE `car-rentals` ;

-- -----------------------------------------------------
-- Table `car-rentals`.`car-type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car-rentals`.`car-type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  `num-passengers` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

CREATE UNIQUE INDEX `type_UNIQUE` ON `car-rentals`.`car-type` (`type` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `car-rentals`.`car`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car-rentals`.`car` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'VIN',
  `type` VARCHAR(45) NOT NULL,
  `miles` DECIMAL NOT NULL DEFAULT 0,
  `next-maintenance` DECIMAL NOT NULL DEFAULT 10000,
  `VIN` VARCHAR(45) NOT NULL,
  `available` VARCHAR(1) BINARY NULL,
  `status` VARCHAR(45) NULL DEFAULT 'Available',
  PRIMARY KEY (`id`),
  CONSTRAINT `car-type-id`
    FOREIGN KEY (`type`)
    REFERENCES `car-rentals`.`car-type` (`type`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `type_idx` ON `car-rentals`.`car` (`type` ASC) VISIBLE;

CREATE UNIQUE INDEX `vin_uniq` ON `car-rentals`.`car` (`VIN` ASC) INVISIBLE;

CREATE INDEX `available_idx` ON `car-rentals`.`car` (`available` ASC) VISIBLE;

CREATE INDEX `status_idx` ON `car-rentals`.`car` (`status` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `car-rentals`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car-rentals`.`customer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(300) NULL,
  `phone` VARCHAR(45) NULL,
  `address` VARCHAR(4000) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

CREATE INDEX `name_idx` ON `car-rentals`.`customer` (`name` ASC) INVISIBLE;

CREATE INDEX `email_idx` ON `car-rentals`.`customer` (`email` ASC) INVISIBLE;

CREATE INDEX `phone_idx` ON `car-rentals`.`customer` (`phone` ASC) VISIBLE;

CREATE FULLTEXT INDEX `address_idx` ON `car-rentals`.`customer` (`address`) VISIBLE;


-- -----------------------------------------------------
-- Table `car-rentals`.`booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car-rentals`.`booking` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer-id` INT NOT NULL,
  `car-id` INT NOT NULL,
  `dt-start` DATETIME NOT NULL,
  `dt-booked` DATETIME NOT NULL DEFAULT now(),
  `dt-expect-return` DATETIME NOT NULL,
  `dt-actual-return` DATETIME NULL DEFAULT NULL,
  `amt-owed` DECIMAL(2) NOT NULL,
  `amt-paid` DECIMAL(2) NOT NULL DEFAULT 0,
  `cancelled` VARCHAR(1) BINARY NULL DEFAULT 'N',
  PRIMARY KEY (`id`),
  CONSTRAINT `booking-customer-id`
    FOREIGN KEY (`customer-id`)
    REFERENCES `car-rentals`.`customer` (`id`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `booking-car-id`
    FOREIGN KEY (`car-id`)
    REFERENCES `car-rentals`.`car` (`id`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `customer-id_idx` ON `car-rentals`.`booking` (`customer-id` ASC) VISIBLE;

CREATE INDEX `car-id_idx` ON `car-rentals`.`booking` (`car-id` ASC) VISIBLE;

CREATE INDEX `start_idx` ON `car-rentals`.`booking` (`dt-start` ASC) INVISIBLE;

CREATE INDEX `exp-return_idx` ON `car-rentals`.`booking` (`dt-expect-return` ASC) INVISIBLE;

CREATE INDEX `actual_idx` ON `car-rentals`.`booking` (`dt-actual-return` ASC) INVISIBLE;

CREATE INDEX `billing_idx` ON `car-rentals`.`booking` (`amt-paid` ASC, `amt-owed` ASC) VISIBLE;

CREATE INDEX `cancelled_idx` ON `car-rentals`.`booking` (`cancelled` ASC) INVISIBLE;


-- -----------------------------------------------------
-- Table `car-rentals`.`payment-info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `car-rentals`.`payment-info` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer` INT NOT NULL,
  `type` VARCHAR(45) NOT NULL COMMENT 'CC, Paypal, Zelle, etc.',
  `routing-data` VARCHAR(4000) NOT NULL COMMENT 'A string to route the payment request such as a credit card token, or a paypal or zelle account',
  PRIMARY KEY (`id`),
  CONSTRAINT `payment-info-customer-id`
    FOREIGN KEY (`customer`)
    REFERENCES `car-rentals`.`customer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `customer_idx` ON `car-rentals`.`payment-info` (`customer` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

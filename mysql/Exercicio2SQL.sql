-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Exercicio02
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Exercicio02
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Exercicio02` ;
USE `Exercicio02` ;

-- -----------------------------------------------------
-- Table `Exercicio02`.`Categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Exercicio02`.`Categoria` (
  `idCategoria` INT NOT NULL AUTO_INCREMENT,
  `NoCategoria` VARCHAR(45) NOT NULL,
  `descricaoCategoria` VARCHAR(45) NULL,
  PRIMARY KEY (`idCategoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Exercicio02`.`Produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Exercicio02`.`Produto` (
  `idProduto` INT NOT NULL AUTO_INCREMENT,
  `NoProduto` VARCHAR(45) NOT NULL,
  `VlPreco` DECIMAL(8,2) NOT NULL,
  `QtEstoque` INT NOT NULL,
  `idCategoria` INT NOT NULL,
  PRIMARY KEY (`idProduto`),
  INDEX `fk_Produto_Categoria_idx` (`idCategoria` ASC) VISIBLE,
  CONSTRAINT `fk_Produto_Categoria`
    FOREIGN KEY (`idCategoria`)
    REFERENCES `Exercicio02`.`Categoria` (`idCategoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

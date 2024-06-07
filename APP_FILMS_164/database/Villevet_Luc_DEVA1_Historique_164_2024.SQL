-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.30 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour villevet_luc_deva1_historique_164_2024
DROP DATABASE IF EXISTS `villevet_luc_deva1_historique_164_2024`;
CREATE DATABASE IF NOT EXISTS `villevet_luc_deva1_historique_164_2024` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `villevet_luc_deva1_historique_164_2024`;

-- Listage de la structure de table villevet_luc_deva1_historique_164_2024. t_compte
DROP TABLE IF EXISTS `t_compte`;
CREATE TABLE IF NOT EXISTS `t_compte` (
  `ID_compte` int NOT NULL AUTO_INCREMENT,
  `Pseudo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Droits` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_compte`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- Listage des données de la table villevet_luc_deva1_historique_164_2024.t_compte : ~4 rows (environ)
INSERT INTO `t_compte` (`ID_compte`, `Pseudo`, `Password`, `Droits`) VALUES
	(1, 'LucVillevet', NULL, 'Admin'),
	(2, 'CompteCommun', NULL, NULL),
	(3, 'ModeIncognito', '007', NULL),
	(4, 'ViLu', 'OrifInfo2009', NULL);

-- Listage de la structure de table villevet_luc_deva1_historique_164_2024. t_donnees
DROP TABLE IF EXISTS `t_donnees`;
CREATE TABLE IF NOT EXISTS `t_donnees` (
  `ID_donnee` int NOT NULL AUTO_INCREMENT,
  `FK_compte` int DEFAULT NULL,
  `FK_timbre` int DEFAULT NULL,
  `FK_emplacement` int DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Heure` time DEFAULT NULL,
  `Commentaire` varchar(100) DEFAULT NULL,
  `Date_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Date_modification` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_donnee`) USING BTREE,
  KEY `FK_compte` (`FK_compte`) USING BTREE,
  KEY `FK_timbre` (`FK_timbre`) USING BTREE,
  KEY `FK_emplacement` (`FK_emplacement`) USING BTREE,
  CONSTRAINT `FK_compte` FOREIGN KEY (`FK_compte`) REFERENCES `t_compte` (`ID_compte`),
  CONSTRAINT `FK_emplacement` FOREIGN KEY (`FK_emplacement`) REFERENCES `t_lieu` (`ID_lieu`),
  CONSTRAINT `FK_timbre` FOREIGN KEY (`FK_timbre`) REFERENCES `t_timbre` (`ID_timbre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- Listage des données de la table villevet_luc_deva1_historique_164_2024.t_données : ~4 rows (environ)
INSERT INTO `t_donnees` (`ID_donnee`, `FK_compte`, `FK_timbre`, `FK_emplacement`, `Date`, `Heure`, `Commentaire`, `Date_creation`, `Date_modification`) VALUES
	(1, 4, 1, 2, '2024-02-28', '08:00:00', NULL, '2024-02-28 08:00:00', '2024-05-01 08:30:04'),
	(2, 4, 2, 2, '2024-02-28', '16:00:00', NULL, '2024-02-28 16:00:00', '2024-05-01 08:30:18'),
	(3, 4, 1, 2, '2024-03-13', '08:00:00', NULL, '2024-03-13 08:00:00', '2024-05-01 08:30:22'),
	(4, 4, 2, 2, '2024-03-13', '16:00:00', NULL, '2024-03-13 16:00:00', '2024-05-01 08:30:36');

-- Listage de la structure de table villevet_luc_deva1_historique_164_2024. t_lieu
DROP TABLE IF EXISTS `t_lieu`;
CREATE TABLE IF NOT EXISTS `t_lieu` (
  `ID_lieu` int NOT NULL AUTO_INCREMENT,
  `Emplacement` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ID_lieu`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- Listage des données de la table villevet_luc_deva1_historique_164_2024.t_lieu : ~4 rows (environ)
INSERT INTO `t_lieu` (`ID_lieu`, `Emplacement`) VALUES
	(1, 'Entrée Nord'),
	(2, 'Entrée Sud'),
	(3, 'Entrée Ouest'),
	(4, 'Entrée Est');

-- Listage de la structure de table villevet_luc_deva1_historique_164_2024. t_timbre
DROP TABLE IF EXISTS `t_timbre`;
CREATE TABLE IF NOT EXISTS `t_timbre` (
  `ID_timbre` int NOT NULL AUTO_INCREMENT,
  `Type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ID_timbre`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- Listage des données de la table villevet_luc_deva1_historique_164_2024.t_timbre : ~4 rows (environ)
INSERT INTO `t_timbre` (`ID_timbre`, `Type`) VALUES
	(1, 'Entrée'),
	(2, 'Sortie'),
	(3, 'Passage ou Présence'),
	(4, 'Autre');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

/*
SQLyog Community v13.1.7 (64 bit)
MySQL - 8.0.32 : Database - old_gtv
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`gtv` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `gtv`;

/*Table structure for table `cates` */

DROP TABLE IF EXISTS `cates`;

CREATE TABLE `cates` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(32) DEFAULT NULL,
  `href` varchar(128) DEFAULT NULL,
  `count` int DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `title_index` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=1033 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Table structure for table `videos` */

DROP TABLE IF EXISTS `videos`;

CREATE TABLE `videos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL,
  `href` varchar(64) NOT NULL,
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cover` varchar(128) DEFAULT NULL,
  `image` varchar(128) DEFAULT NULL,
  `date` timestamp NULL DEFAULT NULL,
  `views` int DEFAULT '0' COMMENT '播放量',
  `comments` int DEFAULT '0' COMMENT '评论量',
  `category` varchar(256) DEFAULT NULL COMMENT '类别',
  `recommend` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '相关推荐',
  PRIMARY KEY (`id`),
  UNIQUE KEY `href_index` (`href`)
) ENGINE=InnoDB AUTO_INCREMENT=76777 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

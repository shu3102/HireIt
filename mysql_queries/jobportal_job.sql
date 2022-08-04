-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: jobportal
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `job`
--

DROP TABLE IF EXISTS `job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `job_title` varchar(30) NOT NULL,
  `job_type` varchar(20) DEFAULT NULL,
  `job_description` varchar(800) DEFAULT NULL,
  `job_salary` decimal(7,0) DEFAULT NULL,
  `company_id` int NOT NULL,
  PRIMARY KEY (`job_id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `job_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`company_id`) ON DELETE CASCADE,
  CONSTRAINT `job_chk_1` CHECK ((`job_salary` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job`
--

LOCK TABLES `job` WRITE;
/*!40000 ALTER TABLE `job` DISABLE KEYS */;
INSERT INTO `job` VALUES (1,'Data Analyst','Intern','A successful data analyst needs to have a combination of technical as well leadership skills. A background in Mathematics, Statistics, Computer Science, Information Management, or Economics can serve as a solid foundation to build your career as a data analyst.  ',1100,1),(2,'Software Developer','Full-time','Researching, designing, implementing, and managing software programs. Testing and evaluating new programs. Identifying areas for modification in existing programs and subsequently developing these modifications. Writing and implementing efficient code.\n',26949,1),(3,'Machine Learning','Intern','We are looking for an expert in machine learning to help us extract value from our data. You will lead all the processes from data collection, cleaning, and preprocessing, to training models and deploying them to production.\n\nThe ideal candidate will be passionate about artificial intelligence and stay up-to-date with the latest developments in the field.',876,2),(4,'Software Engineering Intern','Intern','Company seeks an intern with experience in software design, coding and debugging. The intern will gain exciting real-world software engineering experience at a thriving company.\n\nWe frequently work in small teams to solve problems, explore new technologies, and learn from one another. The ideal intern for this environment will be enthusiastic and collaborative.',1000,3),(5,'Analyst','Intern','An analyst gathers, interprets, and uses complex data to develop actionable steps that will improve processes and optimize results. Day-to-day, he or she assesses company and client needs, receives robust information, and analyzes it, looking for telltale trends or areas for improvement. The analyst then delivers that information to stakeholders, and uses it to enhance the efficiency and effectiveness of a service, product, or system.',500,3),(6,'ML Developer','Full-time','A machine learning (ML) developer is an expert on using data to training models. The models are then used to automate processes like image classification, speech recognition, and market forecasting.',3000,5),(7,'Analyst','Intern','An analyst gathers, interprets, and uses complex data to develop actionable steps that will improve processes and optimize results. Day-to-day, he or she assesses company and client needs, receives robust information, and analyzes it, looking for telltale trends or areas for improvement. The analyst then delivers that information to stakeholders, and uses it to enhance the efficiency and effectiveness of a service, product, or system.',600,6),(8,'Analyst','Intern','A machine learning (ML) developer is an expert on using data to training models. The models are then used to automate processes like image classification, speech recognition, and market forecasting.',78451,7),(9,'Software Developer','Intern','An analyst gathers, interprets, and uses complex data to develop actionable steps that will improve processes and optimize results. Day-to-day, he or she assesses company and client needs, receives robust information, and analyzes it, looking for telltale trends or areas for improvement. The analyst then delivers that information to stakeholders, and uses it to enhance the efficiency and effectiveness of a service, product, or system.',789,9);
/*!40000 ALTER TABLE `job` ENABLE KEYS */;
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-06 20:52:51

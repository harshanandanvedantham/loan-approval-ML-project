CREATE DATABASE  IF NOT EXISTS `loanwise_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `loanwise_db`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: loanwise_db
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `loan_applications`
--

DROP TABLE IF EXISTS `loan_applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loan_applications` (
  `application_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `no_of_dependents` int NOT NULL,
  `education` varchar(30) NOT NULL,
  `self_employed` varchar(10) NOT NULL,
  `income_annum` bigint NOT NULL,
  `loan_amount` bigint NOT NULL,
  `loan_term` int NOT NULL,
  `cibil_score` int NOT NULL,
  `residential_assets_value` bigint NOT NULL,
  `commercial_assets_value` bigint NOT NULL,
  `luxury_assets_value` bigint NOT NULL,
  `bank_asset_value` bigint NOT NULL,
  `predicted_status` varchar(20) NOT NULL,
  `predicted_probability` decimal(7,3) NOT NULL,
  `model_name` varchar(100) DEFAULT NULL,
  `model_version` varchar(50) DEFAULT NULL,
  `explanation` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`application_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `loan_applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loan_applications`
--

LOCK TABLES `loan_applications` WRITE;
/*!40000 ALTER TABLE `loan_applications` DISABLE KEYS */;
INSERT INTO `loan_applications` VALUES (1,1,2,'Graduate','No',1111234243,5353566,16,600,145678997,566577,44444444,22556899,'Approved',100.000,'DecisionTreeClassifier',NULL,'{\"shap\": {\"all_factors\": [{\"impact\": 0.4022928411975666, \"feature\": \"Cibil Score\", \"direction\": \"positive\"}, {\"impact\": -0.01324236435459737, \"feature\": \"Loan Term\", \"direction\": \"negative\"}, {\"impact\": -0.008456059093346338, \"feature\": \"Income Annum\", \"direction\": \"negative\"}, {\"impact\": -0.0045530714600018896, \"feature\": \"Luxury Assets Value\", \"direction\": \"negative\"}, {\"impact\": -0.003109804305262307, \"feature\": \"Loan Amount\", \"direction\": \"negative\"}, {\"impact\": 0.0017482291179667228, \"feature\": \"Residential Assets Value\", \"direction\": \"positive\"}, {\"impact\": 0.0015435465118107349, \"feature\": \"No Of Dependents\", \"direction\": \"positive\"}, {\"impact\": 0.0011723785261694786, \"feature\": \"Commercial Assets Value\", \"direction\": \"positive\"}, {\"impact\": -0.00040975786109571737, \"feature\": \"Self Employed No\", \"direction\": \"negative\"}, {\"impact\": -0.00023439058448035104, \"feature\": \"Bank Asset Value\", \"direction\": \"negative\"}, {\"impact\": 0.00013624151673733394, \"feature\": \"Education Graduate\", \"direction\": \"positive\"}, {\"impact\": 0.00013195944203402645, \"feature\": \"Education Not Graduate\", \"direction\": \"positive\"}, {\"impact\": 0.0, \"feature\": \"Self Employed Yes\", \"direction\": \"negative\"}], \"negative_factors\": [{\"impact\": -0.01324236435459737, \"feature\": \"Loan Term\", \"direction\": \"negative\"}, {\"impact\": -0.008456059093346338, \"feature\": \"Income Annum\", \"direction\": \"negative\"}, {\"impact\": -0.0045530714600018896, \"feature\": \"Luxury Assets Value\", \"direction\": \"negative\"}, {\"impact\": -0.003109804305262307, \"feature\": \"Loan Amount\", \"direction\": \"negative\"}, {\"impact\": -0.00040975786109571737, \"feature\": \"Self Employed No\", \"direction\": \"negative\"}], \"positive_factors\": [{\"impact\": 0.4022928411975666, \"feature\": \"Cibil Score\", \"direction\": \"positive\"}, {\"impact\": 0.0017482291179667228, \"feature\": \"Residential Assets Value\", \"direction\": \"positive\"}, {\"impact\": 0.0015435465118107349, \"feature\": \"No Of Dependents\", \"direction\": \"positive\"}, {\"impact\": 0.0011723785261694786, \"feature\": \"Commercial Assets Value\", \"direction\": \"positive\"}, {\"impact\": 0.00013624151673733394, \"feature\": \"Education Graduate\", \"direction\": \"positive\"}]}, \"rules\": {\"negative_reasons\": [\"Low CIBIL score may indicate higher credit risk.\"], \"positive_reasons\": [\"Requested loan amount is relatively low compared to annual income.\", \"Declared assets are substantial relative to the requested loan.\", \"Applicant has recorded bank assets.\"]}, \"confidence\": 100.0, \"prediction\": \"approved\"}','2026-11-02 18:49:34'),(2,3,0,'Graduate','No',15000000,50000010,5,400,8000000,3000000,2000000,5000000,'Rejected',100.000,'DecisionTreeClassifier',NULL,'{\"shap\": {\"all_factors\": [{\"impact\": 0.5403997506431878, \"feature\": \"Cibil Score\", \"direction\": \"positive\"}, {\"impact\": 0.09428495329291388, \"feature\": \"Loan Term\", \"direction\": \"positive\"}, {\"impact\": 0.02216329962471449, \"feature\": \"Income Annum\", \"direction\": \"positive\"}, {\"impact\": -0.015913354458383846, \"feature\": \"Loan Amount\", \"direction\": \"negative\"}, {\"impact\": -0.010119149480485524, \"feature\": \"Bank Asset Value\", \"direction\": \"negative\"}, {\"impact\": -0.01006498841124492, \"feature\": \"Residential Assets Value\", \"direction\": \"negative\"}, {\"impact\": 0.004500225611244061, \"feature\": \"Self Employed No\", \"direction\": \"positive\"}, {\"impact\": -0.0010438126477723385, \"feature\": \"Luxury Assets Value\", \"direction\": \"negative\"}, {\"impact\": -0.000987559308006574, \"feature\": \"Commercial Assets Value\", \"direction\": \"negative\"}, {\"impact\": -0.0003090323813594479, \"feature\": \"Education Graduate\", \"direction\": \"negative\"}, {\"impact\": 0.00013410226732226587, \"feature\": \"No Of Dependents\", \"direction\": \"positive\"}, {\"impact\": -0.0000641834056312345, \"feature\": \"Education Not Graduate\", \"direction\": \"negative\"}, {\"impact\": 0.0, \"feature\": \"Self Employed Yes\", \"direction\": \"negative\"}], \"negative_factors\": [{\"impact\": -0.015913354458383846, \"feature\": \"Loan Amount\", \"direction\": \"negative\"}, {\"impact\": -0.010119149480485524, \"feature\": \"Bank Asset Value\", \"direction\": \"negative\"}, {\"impact\": -0.01006498841124492, \"feature\": \"Residential Assets Value\", \"direction\": \"negative\"}, {\"impact\": -0.0010438126477723385, \"feature\": \"Luxury Assets Value\", \"direction\": \"negative\"}, {\"impact\": -0.000987559308006574, \"feature\": \"Commercial Assets Value\", \"direction\": \"negative\"}], \"positive_factors\": [{\"impact\": 0.5403997506431878, \"feature\": \"Cibil Score\", \"direction\": \"positive\"}, {\"impact\": 0.09428495329291388, \"feature\": \"Loan Term\", \"direction\": \"positive\"}, {\"impact\": 0.02216329962471449, \"feature\": \"Income Annum\", \"direction\": \"positive\"}, {\"impact\": 0.004500225611244061, \"feature\": \"Self Employed No\", \"direction\": \"positive\"}, {\"impact\": 0.00013410226732226587, \"feature\": \"No Of Dependents\", \"direction\": \"positive\"}]}, \"rules\": {\"negative_reasons\": [\"Low CIBIL score may indicate higher credit risk.\", \"Declared assets are relatively low compared to the requested loan.\"], \"positive_reasons\": [\"Loan-to-income ratio is within the middle range of this illustrative assessment.\", \"Applicant has recorded bank assets.\"]}, \"confidence\": 100.0, \"prediction\": \"rejected\"}','2026-11-02 19:48:05');
/*!40000 ALTER TABLE `loan_applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'sai','sai@gmail.com','scrypt:32768:8:1$jNnOokL4MCxOUjNB$631a4fdf744e7eddb4f153631659c89e8b625c0269ed09cc2ddf9e13272c9d3e515e7d697c0cd3b880722d460583d64e8676f69b7b923146bcf39d4da127ca99','2026-11-02 17:45:08'),(2,'vijay','vijay@gmail.com','scrypt:32768:8:1$eo9sYEvIV4h7VLm7$7ed7f4a6de20fcd1cf1f3179d017e52580f86338acb526ed695da3516886a8f1ca6ee3784331048ebd2db61cd2145f191931cf74ee07c236e9bc50969147a35d','2026-11-02 19:07:07'),(3,'K. Vijay Bhaskar','kamarsuvijaybhaskar@gmail.com','scrypt:32768:8:1$pmEgtDqDgtvWXwzo$774e608e31ad7f7116c971cca6fe2f5a5040d6c1eab9844b39e6115ac0a0c7cb547c5e861ae114411c3dd6a798cf2a487bd73d526768f442bee6c7358e07ade8','2026-11-02 19:45:15');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'loanwise_db'
--

--
-- Dumping routines for database 'loanwise_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-03  1:27:40

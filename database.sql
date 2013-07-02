-- MySQL dump 10.13  Distrib 5.5.31, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ibo2013-django
-- ------------------------------------------------------
-- Server version	5.5.31-0ubuntu0.12.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add message',5,'add_message'),(14,'Can change message',5,'change_message'),(15,'Can delete message',5,'delete_message'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add site',8,'add_site'),(23,'Can change site',8,'change_site'),(24,'Can delete site',8,'delete_site'),(25,'Can add publisher',9,'add_publisher'),(26,'Can change publisher',9,'change_publisher'),(27,'Can delete publisher',9,'delete_publisher'),(28,'Can add author',10,'add_author'),(29,'Can change author',10,'change_author'),(30,'Can delete author',10,'delete_author'),(31,'Can add book',11,'add_book'),(32,'Can change book',11,'change_book'),(33,'Can delete book',11,'delete_book'),(34,'Can add language',12,'add_language'),(35,'Can change language',12,'change_language'),(36,'Can delete language',12,'delete_language'),(37,'Can add question',13,'add_question'),(38,'Can change question',13,'change_question'),(39,'Can delete question',13,'delete_question'),(40,'Can add version node',14,'add_versionnode'),(41,'Can change version node',14,'change_versionnode'),(42,'Can delete version node',14,'delete_versionnode'),(43,'Can add exam',15,'add_exam'),(44,'Can change exam',15,'change_exam'),(45,'Can delete exam',15,'delete_exam'),(49,'Can add exam question',17,'add_examquestion'),(50,'Can change exam question',17,'change_examquestion'),(51,'Can delete exam question',17,'delete_examquestion'),(52,'Can add translation',18,'add_translation'),(53,'Can change translation',18,'change_translation'),(54,'Can delete translation',18,'delete_translation'),(55,'Can add exam permission',19,'add_exampermission'),(56,'Can change exam permission',19,'change_exampermission'),(57,'Can delete exam permission',19,'delete_exampermission');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'admin','','','jonas.helfer@yahoo.de','sha1$16221$90cd7ca9fd7af3c8eeb5fa5ed01a764c30b9e685',1,1,1,'2013-06-27 01:26:44','2013-02-23 17:28:35'),(5,'test','','','','sha1$fc7ee$17606c03d277c7126092e8f186d8f2ce57c8b4c7',0,1,0,'2013-06-02 01:17:32','2013-06-02 01:17:09'),(6,'alice','','','','sha1$8cb55$422fea2588d0b81eca3c68d885fb338f8d94ab51',0,1,0,'2013-06-27 01:27:00','2013-06-23 17:58:50');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_author`
--

DROP TABLE IF EXISTS `books_author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(40) NOT NULL,
  `email` varchar(75) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_author`
--

LOCK TABLES `books_author` WRITE;
/*!40000 ALTER TABLE `books_author` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_book`
--

DROP TABLE IF EXISTS `books_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `publisher_id` int(11) NOT NULL,
  `publication_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `books_book_22dd9c39` (`publisher_id`),
  CONSTRAINT `publisher_id_refs_id_c5b274bb` FOREIGN KEY (`publisher_id`) REFERENCES `books_publisher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_book`
--

LOCK TABLES `books_book` WRITE;
/*!40000 ALTER TABLE `books_book` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_book_authors`
--

DROP TABLE IF EXISTS `books_book_authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_book_authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `book_id` (`book_id`,`author_id`),
  KEY `books_book_authors_752eb95b` (`book_id`),
  KEY `books_book_authors_cc846901` (`author_id`),
  CONSTRAINT `author_id_refs_id_9e7e386` FOREIGN KEY (`author_id`) REFERENCES `books_author` (`id`),
  CONSTRAINT `book_id_refs_id_cfbcf262` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_book_authors`
--

LOCK TABLES `books_book_authors` WRITE;
/*!40000 ALTER TABLE `books_book_authors` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_book_authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_publisher`
--

DROP TABLE IF EXISTS `books_publisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `books_publisher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(60) NOT NULL,
  `state_province` varchar(30) NOT NULL,
  `country` varchar(50) NOT NULL,
  `website` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_publisher`
--

LOCK TABLES `books_publisher` WRITE;
/*!40000 ALTER TABLE `books_publisher` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_publisher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2013-02-23 18:13:06',1,12,'1','English',1,''),(2,'2013-02-23 18:13:11',1,12,'2','Deutsch',1,''),(3,'2013-02-23 18:13:20',1,12,'3','中文',1,''),(4,'2013-02-23 18:16:08',1,15,'1','Exam: ibo2013-test1',1,''),(5,'2013-02-23 18:16:34',1,13,'1','first question',1,''),(6,'2013-02-23 18:17:15',1,14,'1','VersionNode: first question (v 1)',1,''),(7,'2013-02-23 18:18:26',1,14,'2','VersionNode: first question (v 2)',1,''),(8,'2013-02-23 22:21:43',1,15,'1','Exam: ibo2013-test1',2,'Changed questions.'),(9,'2013-02-23 22:21:56',1,13,'2','second question',1,''),(10,'2013-02-23 22:22:23',1,13,'3','第3问题',1,''),(11,'2013-02-23 22:25:45',1,15,'1','Exam: ibo2013-test1',2,'Changed questions.'),(12,'2013-02-23 23:03:08',1,15,'2','Exam: exam2',1,''),(13,'2013-02-24 23:41:17',1,12,'1','English',1,''),(15,'2013-02-24 23:41:50',1,12,'2','Deutsch',1,''),(16,'2013-02-24 23:41:56',1,13,'1','Question1',1,''),(17,'2013-02-24 23:47:54',1,12,'1','English',1,''),(18,'2013-02-24 23:47:57',1,13,'1','Question1',1,''),(19,'2013-02-24 23:48:05',1,13,'2','Question2',1,''),(20,'2013-02-24 23:48:16',1,12,'2','Deutsch',1,''),(21,'2013-02-24 23:48:28',1,15,'1','Exam: TestExam1',1,''),(22,'2013-02-24 23:48:57',1,14,'1','VersionNode: Question1 (v 1)',1,''),(23,'2013-02-24 23:53:54',1,14,'2','VersionNode: Question1 (v 1)',1,''),(24,'2013-02-24 23:54:15',1,14,'3','VersionNode: Question2 (v 1)',1,''),(25,'2013-02-24 23:56:58',1,17,'1','ExamQuestion object',1,''),(26,'2013-02-25 00:05:03',1,17,'2','ExamQuestion object',1,''),(27,'2013-02-25 00:08:11',1,14,'5','VersionNode: Question2 (v 1)',1,''),(28,'2013-05-05 23:34:59',1,13,'3','Question 3',1,''),(29,'2013-05-27 23:39:28',1,4,'2','jonas',1,''),(30,'2013-05-27 23:42:51',1,4,'3','robert',1,''),(31,'2013-05-27 23:43:13',1,4,'3','robert',2,'Changed email.'),(32,'2013-05-27 23:45:13',1,4,'4','test',1,''),(33,'2013-05-27 23:45:39',1,4,'4','test',2,'Changed first_name, last_name and email.'),(34,'2013-05-27 23:56:57',1,4,'3','robert',2,'Changed is_staff.'),(35,'2013-05-28 00:07:24',1,4,'2','jonas',2,'Changed is_staff.'),(36,'2013-06-02 01:16:46',1,4,'2','jonas',3,''),(37,'2013-06-02 01:16:46',1,4,'3','robert',3,''),(38,'2013-06-02 01:16:46',1,4,'4','test',3,''),(39,'2013-06-02 01:17:09',1,4,'5','test',1,''),(40,'2013-06-02 21:57:26',1,15,'2','Exam: Exam2',1,''),(41,'2013-06-23 17:58:50',1,4,'6','alice',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'message','auth','message'),(6,'content type','contenttypes','contenttype'),(7,'session','sessions','session'),(8,'site','sites','site'),(9,'publisher','books','publisher'),(10,'author','books','author'),(11,'book','books','book'),(12,'language','question','language'),(13,'question','question','question'),(14,'version node','question','versionnode'),(15,'exam','question','exam'),(17,'exam question','question','examquestion'),(18,'translation','question','translation'),(19,'exam permission','question','exampermission');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('024310e1c3c0bef6b1433d1c54660b45','ZGVkNTExYmFkYmQ1YjEzOTU5OTdiOGEwZjU0YjMxODI3YTE4YThkNjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-06-01 23:45:16'),('085cf17fa75e9ad409128fa8a08a1f93','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-03-09 18:05:43'),('20ef749177b1d353884751acd7eded17','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-06-16 21:57:10'),('25bbef7cdc76bf8bb9c2bd8c635b9cf9','ZGVkNTExYmFkYmQ1YjEzOTU5OTdiOGEwZjU0YjMxODI3YTE4YThkNjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-06-01 23:32:01'),('3db0949cb48b495ee3f4207fba7c7d01','YjI1MmE1OTRlZTRiZTNhMmNiODA5ZThkNzNmODk1ZmI5OGFlYjE4NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQV1Lg==\n','2013-06-16 01:17:32'),('456b81c952f6d12aa00d16520468c36a','NzNmOWZkOTYwMjRmZDQ0Y2I2YjU0NzRjOWVmM2UyZDJjYzViZWVlNzqAAn1xAShVCnRlc3Rjb29r\naWVVBndvcmtlZHECVQ1fYXV0aF91c2VyX2lkigEBVRJfYXV0aF91c2VyX2JhY2tlbmRVKWRqYW5n\nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kdS4=\n','2013-06-30 03:58:55'),('4e062f8bb0285fca0c8ab5c3943b608b','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-06-30 04:01:08'),('537ea5945ea4baa0911a9ff389db5d1e','NjJmYWJhMjI5NWNkMDJiMmI0ODhhMjY2N2JkNzc4NmM1N2VjYzQyMTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQJ1Lg==\n','2013-06-11 00:09:36'),('5ba24a636d15b6ed37ada58d25a374ae','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-07-09 15:26:34'),('68b977de34c5f2945b487827de9ef9ea','NjdkMzkyMGQ3Yzc5NmY2MGJkNmIyN2QyNDgzOGY0MjM3MjMzMDc2ZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQZ1Lg==\n','2013-07-11 01:27:00'),('692223f4770da7080ad48647520facf7','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-03-10 23:40:08'),('71d85e1796ae758fa8a0a99bc73a5e49','ZGVkNTExYmFkYmQ1YjEzOTU5OTdiOGEwZjU0YjMxODI3YTE4YThkNjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-06-01 23:37:54'),('78b3f2dcea54552a17427cd6b1426ca1','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-05-19 16:08:27'),('79e2d9bdfd387d1e504017f0a0bb6c51','ZGVkNTExYmFkYmQ1YjEzOTU5OTdiOGEwZjU0YjMxODI3YTE4YThkNjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2013-06-30 21:09:55'),('a5bce6b794b50c49667b03344a59b59d','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-06-30 20:57:53'),('c57593d768b028987d0682301733d2ee','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-07-04 17:10:30'),('ccadd412d2dd9b364e46c939393222e1','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-07-06 22:34:10'),('cf520c0f1d316db437342c49ccb12157','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-07-07 00:57:15'),('d709b57a74bde410a8507ac2c80bef4d','NjdkMzkyMGQ3Yzc5NmY2MGJkNmIyN2QyNDgzOGY0MjM3MjMzMDc2ZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQZ1Lg==\n','2013-07-07 17:59:37'),('f3d98646dbdf51c94bbb4f6d2374c594','Mjc0NjJkZDFjODcwOGRjODhiNDNhYjU2ODRmY2Q3MWY3NTlkNWM0MTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-06-02 00:00:11');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_exam`
--

DROP TABLE IF EXISTS `question_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_exam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_exam`
--

LOCK TABLES `question_exam` WRITE;
/*!40000 ALTER TABLE `question_exam` DISABLE KEYS */;
INSERT INTO `question_exam` VALUES (1,'TestExam1'),(2,'Exam2');
/*!40000 ALTER TABLE `question_exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_exam_languages`
--

DROP TABLE IF EXISTS `question_exam_languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_exam_languages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_id` int(11) NOT NULL,
  `language_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `exam_id` (`exam_id`,`language_id`),
  KEY `question_exam_languages_6b01437f` (`exam_id`),
  KEY `question_exam_languages_7ab48146` (`language_id`),
  CONSTRAINT `exam_id_refs_id_60e59817` FOREIGN KEY (`exam_id`) REFERENCES `question_exam` (`id`),
  CONSTRAINT `language_id_refs_id_8885f356` FOREIGN KEY (`language_id`) REFERENCES `question_language` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_exam_languages`
--

LOCK TABLES `question_exam_languages` WRITE;
/*!40000 ALTER TABLE `question_exam_languages` DISABLE KEYS */;
INSERT INTO `question_exam_languages` VALUES (1,1,1),(2,1,2),(3,1,3),(7,1,9),(9,1,10),(11,1,11),(13,1,12),(15,1,13),(17,1,14),(19,1,15),(21,1,16),(23,1,17),(25,1,18),(27,1,19),(29,1,22),(31,1,23),(33,1,24),(4,2,1),(5,2,2),(6,2,3),(8,2,9),(10,2,10),(12,2,11),(14,2,12),(16,2,13),(18,2,14),(20,2,15),(22,2,16),(24,2,17),(26,2,18),(28,2,19),(30,2,22),(32,2,23),(34,2,24);
/*!40000 ALTER TABLE `question_exam_languages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_exampermission`
--

DROP TABLE IF EXISTS `question_exampermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_exampermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_id` int(11) NOT NULL,
  `language_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_exampermission_6b01437f` (`exam_id`),
  KEY `question_exampermission_7ab48146` (`language_id`),
  KEY `question_exampermission_fbfc09f1` (`user_id`),
  CONSTRAINT `exam_id_refs_id_9de059c6` FOREIGN KEY (`exam_id`) REFERENCES `question_exam` (`id`),
  CONSTRAINT `language_id_refs_id_aa0c8e35` FOREIGN KEY (`language_id`) REFERENCES `question_language` (`id`),
  CONSTRAINT `user_id_refs_id_51ab99fc` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_exampermission`
--

LOCK TABLES `question_exampermission` WRITE;
/*!40000 ALTER TABLE `question_exampermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_exampermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_examquestion`
--

DROP TABLE IF EXISTS `question_examquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_examquestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `position` int(11) NOT NULL,
  `points` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_examquestion_6b01437f` (`exam_id`),
  KEY `question_examquestion_1f92e550` (`question_id`),
  CONSTRAINT `exam_id_refs_id_3ecc44f5` FOREIGN KEY (`exam_id`) REFERENCES `question_exam` (`id`),
  CONSTRAINT `question_id_refs_id_86ad0256` FOREIGN KEY (`question_id`) REFERENCES `question_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_examquestion`
--

LOCK TABLES `question_examquestion` WRITE;
/*!40000 ALTER TABLE `question_examquestion` DISABLE KEYS */;
INSERT INTO `question_examquestion` VALUES (1,1,1,9,0.50),(2,1,2,11,1.00),(3,1,3,4,1.00),(4,1,5,1,1.00),(5,1,6,3,1.00),(6,1,8,5,1.00),(7,1,9,6,1.00),(8,1,10,8,1.00),(9,1,11,12,100.00),(10,1,12,10,100.00),(11,1,13,7,5.00),(12,2,14,2,10.00),(13,2,15,3,15.00),(14,2,16,1,5.00),(15,1,17,2,50.00);
/*!40000 ALTER TABLE `question_examquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_language`
--

DROP TABLE IF EXISTS `question_language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_language`
--

LOCK TABLES `question_language` WRITE;
/*!40000 ALTER TABLE `question_language` DISABLE KEYS */;
INSERT INTO `question_language` VALUES (18,'Alicelang'),(19,'Alicelang2'),(13,'China'),(2,'Deutsch'),(1,'English'),(3,'Francais'),(20,'Gobbledygook'),(22,'Gobbledygook2'),(23,'Gobbledygook3'),(6,'Hulu'),(17,'Jonashua'),(4,'Klingon'),(5,'Lappi'),(9,'Pipa'),(11,'Pipax'),(7,'Purlipu'),(16,'Shanyu'),(12,'SOPA'),(14,'Switzerland_DE'),(15,'Switzerland_FR'),(10,'Tibibi'),(24,'Whooza');
/*!40000 ALTER TABLE `question_language` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_language_coordinators`
--

DROP TABLE IF EXISTS `question_language_coordinators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_language_coordinators` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `language_id` (`language_id`,`user_id`),
  KEY `user_id_refs_id_1ed37bb3` (`user_id`),
  CONSTRAINT `language_id_refs_id_785c2be4` FOREIGN KEY (`language_id`) REFERENCES `question_language` (`id`),
  CONSTRAINT `user_id_refs_id_1ed37bb3` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_language_coordinators`
--

LOCK TABLES `question_language_coordinators` WRITE;
/*!40000 ALTER TABLE `question_language_coordinators` DISABLE KEYS */;
INSERT INTO `question_language_coordinators` VALUES (1,1,1),(2,1,5),(12,2,1),(3,4,1),(4,5,5),(5,6,1),(6,7,1),(8,9,1),(9,10,1),(10,11,5),(11,12,5),(13,13,1),(14,14,1),(15,15,1),(16,16,1),(17,17,1),(23,18,1),(24,18,5),(19,19,1),(25,20,6),(32,22,5),(33,22,6),(31,23,5),(34,24,6);
/*!40000 ALTER TABLE `question_language_coordinators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_language_editors`
--

DROP TABLE IF EXISTS `question_language_editors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_language_editors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `language_id` (`language_id`,`user_id`),
  KEY `user_id_refs_id_3bc8d6e3` (`user_id`),
  CONSTRAINT `language_id_refs_id_ef7a254c` FOREIGN KEY (`language_id`) REFERENCES `question_language` (`id`),
  CONSTRAINT `user_id_refs_id_3bc8d6e3` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_language_editors`
--

LOCK TABLES `question_language_editors` WRITE;
/*!40000 ALTER TABLE `question_language_editors` DISABLE KEYS */;
INSERT INTO `question_language_editors` VALUES (1,4,5),(2,5,5),(3,6,5),(4,7,1),(6,9,1),(7,10,1),(8,11,1),(9,12,1),(10,13,1),(11,14,1),(12,15,1),(13,16,1),(14,17,1),(20,18,1),(21,18,5),(22,18,6),(16,19,6),(23,20,6),(28,22,6),(27,23,6),(29,24,6);
/*!40000 ALTER TABLE `question_language_editors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_question`
--

DROP TABLE IF EXISTS `question_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `primary_language_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_question_d9dc0779` (`primary_language_id`),
  CONSTRAINT `primary_language_id_refs_id_4a9c791b` FOREIGN KEY (`primary_language_id`) REFERENCES `question_language` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_question`
--

LOCK TABLES `question_question` WRITE;
/*!40000 ALTER TABLE `question_question` DISABLE KEYS */;
INSERT INTO `question_question` VALUES (1,'Question1',1),(2,'Question2',1),(3,'Question 3',1),(4,'title',1),(5,'title',1),(6,'title',1),(7,'Eat this title!',1),(8,'Eat this!',1),(9,'Try it out, man',1),(10,'another one',1),(11,'reorder questions',1),(12,'reorder questions',1),(13,'question number 5',1),(14,'First Question',1),(15,'Second Question',1),(16,'Question 3',1),(17,'Frage 12',1);
/*!40000 ALTER TABLE `question_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_translation`
--

DROP TABLE IF EXISTS `question_translation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_translation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_id` int(11) NOT NULL,
  `origin_id` int(11) NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `question_translation_9358c897` (`target_id`),
  KEY `question_translation_bd654448` (`origin_id`),
  KEY `language_id` (`language_id`),
  CONSTRAINT `origin_id_refs_id_4c972f70` FOREIGN KEY (`origin_id`) REFERENCES `question_versionnode` (`id`),
  CONSTRAINT `target_id_refs_id_4c972f70` FOREIGN KEY (`target_id`) REFERENCES `question_versionnode` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_translation`
--

LOCK TABLES `question_translation` WRITE;
/*!40000 ALTER TABLE `question_translation` DISABLE KEYS */;
INSERT INTO `question_translation` VALUES (1,2,3,5),(2,2,4,6),(3,2,11,40),(4,2,43,44),(5,2,13,45),(6,2,46,47),(7,2,48,49),(8,2,50,51),(9,2,39,52),(10,2,4,53),(11,3,4,54),(12,3,55,56),(13,2,55,57),(14,2,14,58),(15,2,59,60),(16,2,61,62),(17,2,7,63),(18,2,64,65),(19,2,66,67),(20,2,68,69),(21,2,43,70),(22,2,71,72),(23,3,68,76),(24,3,75,77),(25,2,74,78),(26,2,75,80),(27,2,79,81),(28,2,73,82),(29,3,74,83),(30,3,71,84),(31,3,66,85),(32,3,79,86),(33,3,79,87),(34,2,88,89),(35,3,92,93),(36,3,88,94),(37,3,88,95),(38,3,88,96),(39,2,73,97),(40,2,79,98),(41,2,91,99),(42,3,100,101),(43,3,73,103),(44,10,104,105),(45,10,59,106),(46,13,104,107),(47,13,102,108),(48,13,14,109),(49,13,71,110),(50,13,79,111),(51,13,113,114),(52,14,102,115),(53,15,102,116),(54,2,39,117),(55,2,59,118),(56,2,61,119),(57,2,113,120),(58,2,113,121),(59,2,112,122),(60,2,112,123),(61,2,112,124),(62,2,112,125),(63,2,112,126),(64,7,14,127),(65,3,14,128),(66,3,14,129),(67,3,112,130),(68,16,113,131),(69,22,14,132),(70,22,39,133),(71,22,75,134),(72,18,92,135),(73,18,92,136),(74,18,90,137);
/*!40000 ALTER TABLE `question_translation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_versionnode`
--

DROP TABLE IF EXISTS `question_versionnode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_versionnode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `comment` longtext NOT NULL,
  `question_id` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `language_id` int(11) NOT NULL,
  `flag` tinyint(1) NOT NULL,
  `checkout` tinyint(1) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_versionnode_1f92e550` (`question_id`),
  KEY `question_versionnode_7ab48146` (`language_id`),
  CONSTRAINT `language_id_refs_id_fd76610e` FOREIGN KEY (`language_id`) REFERENCES `question_language` (`id`),
  CONSTRAINT `question_id_refs_id_d0e228ec` FOREIGN KEY (`question_id`) REFERENCES `question_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_versionnode`
--

LOCK TABLES `question_versionnode` WRITE;
/*!40000 ALTER TABLE `question_versionnode` DISABLE KEYS */;
INSERT INTO `question_versionnode` VALUES (2,'First version of first question','',1,1,1,0,0,'2013-02-24 23:53:54'),(3,'Second Question, first version','',2,1,1,0,0,'2013-02-24 23:54:15'),(4,'second version of second question','',2,2,1,0,0,'2013-02-25 00:07:11'),(5,'Dies ist die Deutsche Version der zweiten Frage','',2,1,2,0,0,'2013-02-25 00:08:11'),(6,'Das sollte die zweite Version der deutschen Frage 2 sein.','',2,2,2,0,0,'2013-02-25 00:08:35'),(7,'second version of first question','',1,2,1,0,0,'2013-02-25 04:51:39'),(8,'Dritte Version\r\n','',2,3,2,0,0,'2013-02-25 04:51:56'),(9,'Vierte Version','',2,4,2,0,1,'2013-05-05 23:14:21'),(10,'A question with a first version!','',3,1,1,0,0,'2013-05-05 23:37:23'),(11,'A question with a second version','',3,2,1,0,0,'2013-05-05 23:37:34'),(12,'a question WITH a version\r\n','',4,1,1,0,0,'2013-05-05 23:48:49'),(13,'Mambo Number 5','',5,1,1,0,0,'2013-05-06 00:10:55'),(14,'This will crash...\r\n','',6,1,1,0,0,'2013-05-06 00:13:48'),(15,'Meaningful names','',8,1,1,0,0,'2013-05-06 00:15:14'),(16,'Some more text','',8,2,1,0,0,'2013-05-18 22:04:10'),(17,'Changed version of some more text','',8,3,1,0,0,'2013-05-18 22:04:25'),(18,'Second change of some more text','',8,4,1,0,0,'2013-05-18 22:05:16'),(19,'Third change of some more text','',8,5,1,0,0,'2013-05-18 22:05:32'),(20,'Fourth change of some more text that ought to work.','',8,6,1,0,0,'2013-05-18 22:06:53'),(21,'Fourth change of some more text that ought to work.','',8,7,1,0,0,'2013-05-18 22:07:51'),(22,'Fourth change of some more text that ought to work.','',8,8,1,0,0,'2013-05-18 22:08:36'),(23,'Fifth change of some more text, let\'s see what it does.','',8,9,1,0,0,'2013-05-18 22:08:51'),(24,'This sixth change came at a later date!','',8,10,1,0,0,'2013-05-18 22:10:51'),(25,'The seventh change followed right after that','',8,11,1,0,0,'2013-05-18 22:11:28'),(26,'The eighth change is strange and followed a bit later.','',8,12,1,0,0,'2013-05-18 23:06:12'),(27,'The ninth change included a newline\r\nAnd I don\'t know how to deal with that!','',8,13,1,0,0,'2013-05-18 23:07:02'),(28,'Well, this is awkward','',8,14,1,0,0,'2013-05-18 23:07:15'),(29,'Well, this is really awkward.','',8,15,1,0,0,'2013-05-18 23:07:29'),(30,'Why doesn\'t it work any more?','',8,16,1,0,0,'2013-05-18 23:07:44'),(31,'Now it\'s working again?\r\n','',8,17,1,0,0,'2013-05-18 23:07:56'),(32,'Nope.','',8,18,1,0,0,'2013-05-18 23:08:02'),(33,'This should work. Nope?\r\n','',8,19,1,0,0,'2013-05-18 23:08:28'),(34,'Now, if that doesn\'t work, then what does?','',8,20,1,0,0,'2013-05-18 23:08:41'),(35,'Now, it worked. But why?','',8,21,1,0,0,'2013-05-18 23:08:54'),(36,'Okay, umpteenth version is pretty good.\r\n','',8,22,1,0,0,'2013-05-18 23:09:12'),(37,'Okay, the version after that is pretty good too.','',8,23,1,0,0,'2013-05-18 23:09:24'),(38,'Can we deal with small changes?','',8,24,1,0,0,'2013-05-18 23:09:37'),(39,'Can we deal with microchanges?','',8,25,1,0,0,'2013-05-18 23:09:44'),(40,'A question with a first version!','',3,1,2,0,0,'2013-05-05 23:37:23'),(41,'Another version here...','',2,5,2,0,0,'2013-05-27 01:22:25'),(42,'And yet another version','',2,6,2,0,0,'2013-05-27 01:27:16'),(43,'Okay, what\'s the next version going to be?','',3,3,1,0,0,'2013-05-27 02:12:13'),(44,'Gut, was wird die naechste Version sein?','',3,2,2,0,0,'2013-05-27 02:27:37'),(45,'Mambo nummer 5','',5,1,2,0,0,'2013-05-27 16:53:06'),(46,'First version of question number 10','',10,1,1,0,0,'2013-05-27 17:00:30'),(47,'Erste Version der Frage nummer 10','',10,1,2,0,0,'2013-05-27 17:00:51'),(48,'Second version of question number 10','',10,2,1,0,0,'2013-05-27 17:01:16'),(49,'Zweite Version der Frage nummer 10','',10,2,2,0,0,'2013-05-27 17:02:30'),(50,'Third version of question number 10','',10,3,1,0,0,'2013-05-27 17:04:21'),(51,'Dritte Version der Frage nummer 10','',10,3,2,0,0,'2013-05-27 17:04:37'),(52,'Koennen wir mit mikroveraenderungen umgehen?','',8,1,2,0,0,'2013-05-27 17:07:43'),(53,'Zweite Version der zweiten Frage','',2,7,2,0,0,'2013-05-27 17:08:10'),(54,'Deuxieme version de la deuxieme question','',2,1,3,0,0,'2013-05-27 17:10:00'),(55,'Third version of second question','',2,3,1,0,0,'2013-05-27 17:10:29'),(56,'Troisieme version de la deuxieme question','',2,2,3,0,0,'2013-05-27 17:39:19'),(57,'Dritte Version der zweiten Frage','',2,8,2,0,0,'2013-05-27 17:39:38'),(58,'Das wird nicht funktionieren','',6,1,2,0,0,'2013-05-27 17:59:12'),(59,'First version of try it out man','',9,1,1,0,0,'2013-05-27 18:00:01'),(60,'Erste version von \"Try it out man\"','',9,1,2,0,0,'2013-05-27 18:00:21'),(61,'q5, first version','',13,1,1,0,0,'2013-05-27 18:00:51'),(62,'q5, erste Version','',13,1,2,0,0,'2013-05-27 18:01:03'),(63,'zweite Version der ersten Frage','',1,1,2,0,0,'2013-05-27 18:01:25'),(64,'first version of reorder question','',12,1,1,0,0,'2013-05-27 18:01:49'),(65,'Erste Version der neusortier-frage','',12,1,2,0,0,'2013-05-27 18:02:09'),(66,'And another first version','',11,1,1,0,0,'2013-05-27 18:02:32'),(67,'Und noch eine erste Version','',11,1,2,0,0,'2013-05-27 18:02:44'),(68,'Fourth version of second question','',2,4,1,0,0,'2013-05-27 18:03:03'),(69,'Vierte Version der zweiten Frage','',2,9,2,0,0,'2013-05-27 18:03:21'),(70,'Gut, was wird die naechste Version sein? Jetzt ist das Deutsche voraus!','',3,3,2,0,0,'2013-05-27 18:04:09'),(71,'Okay, this is the next Version!','',3,4,1,0,0,'2013-05-27 18:04:44'),(72,'Gut, das ist die naechste Version!','',3,4,2,0,0,'2013-05-27 18:05:10'),(73,'Mambo number 6','',5,2,1,0,0,'2013-06-02 17:48:13'),(74,'Second version of reorder question','',12,2,1,0,0,'2013-06-02 17:49:17'),(75,'third version of first question','',1,3,1,0,0,'2013-06-02 17:49:43'),(76,'Quatrieme version de la deuxieme question','',2,3,3,0,0,'2013-06-02 17:51:05'),(77,'Troisieme version de la deuxieme question','',1,1,3,0,0,'2013-06-02 17:55:41'),(78,'Zweite Version der neusortier-frage','',12,2,2,0,0,'2013-06-02 21:44:04'),(79,'Fourth version of question number 10','',10,4,1,0,0,'2013-06-02 21:46:08'),(80,'Dritte Version der ersten Frage','',1,2,2,0,0,'2013-06-02 21:46:38'),(81,'Vierte Version der Frage nummer 10','',10,4,2,0,0,'2013-06-02 21:49:23'),(82,'Mambo nummer 6','',5,2,2,0,0,'2013-06-02 21:51:03'),(83,'Deuxieme version de la question \"reorder\"','',12,1,3,0,0,'2013-06-02 21:51:56'),(84,'Alors, ceci est la prochaine version!','',3,1,3,0,0,'2013-06-02 21:52:32'),(85,'blabla','',11,1,3,0,0,'2013-06-02 21:53:46'),(86,'blubli','',10,1,3,0,0,'2013-06-02 21:54:00'),(87,'blublu','',10,2,3,0,0,'2013-06-02 21:54:20'),(88,'Fifth version of second question','',2,5,1,0,0,'2013-06-02 21:55:02'),(89,'Fünfte Version der zweiten Frage','',2,10,2,0,1,'2013-06-02 21:55:42'),(90,'Text goes here','',14,1,1,0,0,'2013-06-02 21:59:19'),(91,'txt','',16,1,1,0,0,'2013-06-02 22:00:30'),(92,'more txt','',15,1,1,0,0,'2013-06-02 22:00:39'),(93,'blah','',15,1,3,0,0,'2013-06-02 22:00:54'),(94,'<script>alert(\"hello\")</script>','',2,4,3,0,0,'2013-06-04 02:17:40'),(95,'Cinquieme version de la deuxieme question','',2,5,3,0,0,'2013-06-04 02:22:40'),(96,'Cinquieme version de la deuxieme question','',2,6,3,0,0,'2013-06-04 02:22:43'),(97,'Mambo nummer 6 Hallo Jönu','',5,3,2,0,0,'2013-06-13 17:12:12'),(98,'Vierte Version der Frage nummer 100','',10,5,2,1,0,'2013-06-13 17:12:27'),(99,'txt','',16,1,2,0,0,'2013-06-13 17:13:27'),(100,'Blabla Frage 12','',17,1,1,0,0,'2013-06-13 17:17:49'),(101,'Das isch e Übersetzig','',17,1,3,0,0,'2013-06-13 17:18:22'),(102,'Blabla Frage 12 version 2','',17,2,1,0,0,'2013-06-13 17:18:39'),(103,'Mambo Nummer füüüf','',5,1,3,1,0,'2013-06-13 18:26:32'),(104,'Mambo number 6 Isch suüper','',5,3,1,0,0,'2013-06-13 18:27:09'),(105,'Mambo XIV','',5,1,10,0,0,'2013-06-16 04:01:40'),(106,'This question is translated...','',9,1,10,0,0,'2013-06-16 04:01:52'),(107,'aisndief','',5,1,13,0,0,'2013-06-16 20:55:26'),(108,'Blabla','',17,1,13,0,0,'2013-06-16 20:55:33'),(109,'bibi','',6,1,13,0,0,'2013-06-16 20:55:41'),(110,'Bubu','',3,1,13,0,0,'2013-06-16 20:55:47'),(111,'sidnfe','',10,1,13,0,0,'2013-06-16 20:55:51'),(112,'And another version','',3,5,1,0,0,'2013-06-16 20:56:17'),(113,'Ah, first question found.','',5,4,1,0,0,'2013-06-16 20:56:31'),(114,'aisndief !!','',5,2,13,0,0,'2013-06-16 20:56:51'),(115,'sdfwe','',17,1,14,0,0,'2013-06-16 20:58:30'),(116,'aniowefwe','',17,1,15,0,0,'2013-06-16 20:58:42'),(117,'Koennen wir mit mikroveraenderungen umgehen? +flag','',8,2,2,1,0,'2013-06-16 21:45:03'),(118,'Erste version von \"Try it out man\"','',9,2,2,1,0,'2013-06-16 21:45:09'),(119,'q5, erste Version','',13,2,2,0,1,'2013-06-16 21:45:15'),(120,'Mambo nummer 6 Hallo Jönu','',5,4,2,0,0,'2013-06-16 21:45:43'),(121,'Mambo nummer 6 Hallo Jönu','Die rischtige Antwort ...\r\n\r\nIsch finde diese Frage scheisse.',5,5,2,0,0,'2013-06-16 21:53:45'),(122,'Gut, das ist die naechste Version!','Was ne doofe Frage. mussama no ubasetza',3,5,2,0,0,'2013-06-16 21:54:10'),(123,'Gut, das ist die naechste Version! nowas','Was ne doofe Frage. mussama no ubasetza',3,6,2,0,1,'2013-06-16 21:54:24'),(124,'Gut, das ist die naechste Version! nowas','Was ne doofe Frage. mussama no ubasetza check dis out.',3,7,2,0,1,'2013-06-16 21:54:37'),(125,'Gut, das ist die naechste Version! nowas','Was ne doofe Frage. mussama no ubasetza check dis out.',3,8,2,0,0,'2013-06-17 05:51:24'),(126,'Gut, das ist die naechste Version! nowas','Was ne doofe Frage. mussama no ubasetza check dis out.',3,9,2,0,0,'2013-06-17 05:51:25'),(127,'Ianie','asinewd',6,1,7,0,0,'2013-06-23 03:15:01'),(128,'aionoeifwe','dw',6,1,3,0,0,'2013-06-23 03:15:14'),(129,'aionoeifwe','dw',6,2,3,0,1,'2013-06-23 03:15:21'),(130,'Alors, ceci est la prochaine version!','',3,2,3,1,0,'2013-06-23 03:15:30'),(131,'Shan is the best girl in the whole world!','hihi',5,1,16,0,0,'2013-06-23 03:17:46'),(132,'aewfwe','wefwe',6,1,22,0,0,'2013-06-27 01:22:01'),(133,'hubbu\r\n','asda',8,1,22,0,0,'2013-06-27 01:25:53'),(134,'sdas','',1,1,22,0,0,'2013-06-27 01:25:59'),(135,'new version','web',15,1,18,0,0,'2013-06-27 01:29:17'),(136,'new versioner asd','web',15,2,18,0,0,'2013-06-27 01:29:24'),(137,'soinwe','',14,1,18,0,0,'2013-06-27 01:29:34');
/*!40000 ALTER TABLE `question_versionnode` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-06-26 19:40:29

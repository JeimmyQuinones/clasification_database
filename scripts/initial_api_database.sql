
CREATE TABLE `typeIdentifiedData` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `alias` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `date_create` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
);

CREATE TABLE `databaseScan` (
  `id` char(36) NOT NULL,
  `host` varchar(50) NOT NULL,
  `port` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `date_create` datetime NOT NULL,
  `date_scan` datetime DEFAULT NULL,
  `lates_version` int DEFAULT NULL,
  `user_create_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_create_id` (`user_create_id`),
  CONSTRAINT `databaseScan_ibfk_1` FOREIGN KEY (`user_create_id`) REFERENCES `users` (`id`)
) ;

CREATE TABLE `scanDomain` (
  `id` char(36) NOT NULL,
  `name` varchar(200) NOT NULL,
  `database_id` char(36) NOT NULL,
  `version_scan` int NOT NULL,
  `date_scan` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `database_id` (`database_id`),
  CONSTRAINT `scanDomain_ibfk_1` FOREIGN KEY (`database_id`) REFERENCES `databaseScan` (`id`)
);

CREATE TABLE `scanTables` (
  `id` char(36) NOT NULL,
  `domain_id` char(36) NOT NULL,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `domain_id` (`domain_id`),
  CONSTRAINT `scanTables_ibfk_1` FOREIGN KEY (`domain_id`) REFERENCES `scanDomain` (`id`)
);

CREATE TABLE `scanDetailTables` (
  `id` char(36) NOT NULL,
  `table_id` char(36) NOT NULL,
  `nameColumn` varchar(200) NOT NULL,
  `typeIdentified_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `table_id` (`table_id`),
  KEY `typeIdentified_id` (`typeIdentified_id`),
  CONSTRAINT `scanDetailTables_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `scanTables` (`id`),
  CONSTRAINT `scanDetailTables_ibfk_2` FOREIGN KEY (`typeIdentified_id`) REFERENCES `typeIdentifiedData` (`id`)
);
INSERT INTO `typeIdentifiedData` VALUES (1,'FIRST_NAME','first,give,firstname'),(2,'LAST_NAME','last,surname,lastname'),(3,'IP_ADDRESS','ip,address'),(4,'CREDIT_CARD_NUMBER','card,number,credit,nocard'),(5,'N/A',''),(6,'USERNAME','username,usname,user'),(7,'EMAIL_ADDRESS','email,mail');


 





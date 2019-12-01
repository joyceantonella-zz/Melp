# Melp
API provided by flask to retrieve, post and put data to a database.
In this scenario the database is running at host and the requirements for being compatible are following the next structure:<br/>
CREATE TABLE `Restaurants` (
  `id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `name` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `site` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `street` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lng` float DEFAULT NULL
) 
<br/>
The table is based on the one specified in the mail. <br/>
But for lat and lng is recommended the use of decimal(15,13), because of the need of precision.
And handle this in the application with a single conversion to float in order to be properly fitten within pyhton variables.

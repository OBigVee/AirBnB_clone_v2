-- Script prepares MySQL server 
-- a database hbnb_dev_db
-- a new user hbnb_dev (in localhost)
-- the password of hbnb_dev should be set to hbnb_dev_pwd
-- hbnb_dev should have all privileges on the database hbnb_dev_db(and only this database)
-- hbnb_dev should have SELECT privilege on the database performance_schema (and only this database)
-- if the database hbnb_dev_db or the user hbnb_dev already exists, your script should not fail

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@localhost IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON 'hbnb_dev_db'.* TO 'hbnb_dev'@localhost WITH GRANT OPTION;
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@localhost WITH GRANT OPTION;
FLUSH PRIVILEGES;
# This Project use Django Framework and MySQL
1. In order to run this project in your computer install django using "pip install django" command 
2. Use "pip install mysqlclient" to install mysqlclient for Django as MySQl is used in project
3. Database Schema of the project is as follows:</br>
    
    a.CREATE DATABASE InterviewDB;</br>
    b . CREATE TABLE users (
        name VARCHAR(100) NOT NULL,
        email_id VARCHAR(100) NOT NULL,
        PRIMARY KEY (email_id));</br>
     c. CREATE TABLE interviews (
        id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        startTime DATETIME NOT NULL,
        endTime DATETIME NOT NULL,
        PRIMARY KEY (id));    </br>
# Features of this project
With this project admin can schedule interview and can send mail regarding interview . 
After scheduling interview , admin can also delete interview details .

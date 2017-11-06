CREATE TABLE IF NOT EXISTS company_orgtechnics.employees
(
    employee_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    first_name varchar(20) NOT NULL,
    last_name varchar(20) NOT NULL,
    position enum('chief', 'responsible', 'worker') NOT NULL,
    department varchar(20) NOT NULL
);
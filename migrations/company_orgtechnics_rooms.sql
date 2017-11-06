CREATE TABLE IF NOT EXISTS company_orgtechnics.rooms
(
    room_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    number int(11) NOT NULL,
    area int(11),
    department_id int(11) NOT NULL,
    CONSTRAINT rooms_departments_department_id_fk FOREIGN KEY (department_id) REFERENCES departments (department_id)
);
CREATE INDEX rooms_departments_department_id_fk ON company_orgtechnics.rooms (department_id);
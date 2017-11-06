CREATE TABLE IF NOT EXISTS company_orgtechnics.departments
(
    department_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    full_name varchar(20) NOT NULL,
    short_name varchar(5) NOT NULL,
    chief int(11) NOT NULL,
    responsible int(11) NOT NULL,
    CONSTRAINT departments_chief_employee_id_fk FOREIGN KEY (chief) REFERENCES employees (employee_id),
    CONSTRAINT departments_employees_employee_id_fk FOREIGN KEY (chief) REFERENCES employees (employee_id),
    CONSTRAINT departments_responsible_employee_id_fk FOREIGN KEY (responsible) REFERENCES employees (employee_id)
);
CREATE INDEX departments_chief_employee_id_fk ON company_orgtechnics.departments (chief);
CREATE INDEX departments_responsible_employee_id_fk ON company_orgtechnics.departments (responsible);
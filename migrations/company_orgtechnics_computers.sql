CREATE TABLE company_orgtechnics.computers
(
    comp_id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    comp_name varchar(20) NOT NULL,
    model varchar(20) NOT NULL,
    date_buyed date,
    cost int(11),
    date_changed date,
    room_id int(11) NOT NULL,
    CONSTRAINT computers_rooms_room_id_fk FOREIGN KEY (room_id) REFERENCES rooms (room_id)
);
CREATE INDEX computers_rooms_room_id_fk ON company_orgtechnics.computers (room_id);
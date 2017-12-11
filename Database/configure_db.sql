# Add trigger to update Flights last_timestamp field when new BeelineGPS records added
delimiter $$
create trigger Flights_Update_Last_Timestamp
  before insert on BeelineGPS
  for each row begin
    declare f_last_t timestamp;
    select last_timestamp into f_last_t from Flights where flight_id=NEW.f_id;
    if NEW.time > f_last_t then
      update Flights set last_timestamp=NEW.time where flight_id=NEW.f_id;
    end if;
end$$
delimiter ;


LOAD DATA INFILE '/tmpdata/all_comms_sites.csv' INTO TABLE properties FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (
  `uarn`,
  @property_identifier,
  @business_name,
  @number,
  @street,
  @town,
  @county,
  @postcode,
  @rateable_value,
  @current_from_date,
  @current_to_date,
  @lat,
  @lng
)
SET `property identifier` = NULLIF(@property_identifier, ''),
  `business name` = NULLIF(@business_name, ''),
  `number` = NULLIF(@number, ''),
  `street` = NULLIF(@street, ''),
  `town` = NULLIF(@town, ''),
  `county` = NULLIF(@county, ''),
  `postcode` = NULLIF(@postcode, ''),
  `rateable value` = NULLIF(@rateable_value, ''),
  `current from date` = NULLIF(@current_from_date, ''),
  `current to date` = NULLIF(@current_to_date, ''),
  `lat` = NULLIF(@lat, ''),
  `lng` = NULLIF(@lng, '');
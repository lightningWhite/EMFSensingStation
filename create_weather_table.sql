CREATE TABLE WEATHER_MEASUREMENT(
    ID BIGINT NOT NULL AUTO_INCREMENT, 
    REMOTE_ID BIGINT, 
    AMBIENT_TEMPERATURE DECIMAL(6,1) NOT NULL, 
    AIR_PRESSURE DECIMAL(6,1) NOT NULL, 
    HUMIDITY DECIMAL(6,1) NOT NULL, 
    WIND_DIRECTION_DEGREES DECIMAL(6,1) NULL, 
    WIND_DIRECTION_STRING VARCHAR(3) NULL, 
    WIND_SPEED DECIMAL(6,1) NOT NULL, 
    WIND_GUST DECIMAL(6,1) NOT NULL, 
    PRECIPITATION DECIMAL(6,1) NOT NULL, 
    SHORTWAVE_RADIATION DECIMAL(6,1) NOT NULL, 
    CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    PRIMARY KEY ( ID )
);
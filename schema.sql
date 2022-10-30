DROP TABLE IF EXISTS artists ;

CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    spotify_id VARCHAR(30) DEFAULT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    created TIMESTAMP DEFAULT now(),
    updated TIMESTAMP DEFAULT now(),
    edited TIMESTAMP DEFAULT NULL
) ;

INSERT INTO artists (spotify_id, name)
VALUES
    ('2CIMQHirSU0MQqyYHq0eOx', ''),
    ('57dN52uHvrHOxijzpIgu3E', ''),
    ('1vCWHaC5f2uS3yhpwWbIA6', ''),
    ('4FVS2fGhv66N8QLEj77EEP', '') ;

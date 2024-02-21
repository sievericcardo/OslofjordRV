CREATE TABLE IF NOT EXISTS example (
    record_number int NOT NULL UNIQUE,
    suitable_temperature boolean,
    suitable_spawning_temperature boolean,
    preferred_spawning_temperature boolean
);
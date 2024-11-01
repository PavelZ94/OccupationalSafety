DROP TABLE IF EXISTS user_mistakes;

CREATE TABLE user_mistakes (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INT,
    name TEXT,
    mistake TEXT,
    description TEXT,
    level TEXT,
    place TEXT,
    photo BYTEA
);

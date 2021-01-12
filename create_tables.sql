-- create responses table
CREATE TABLE IF NOT EXISTS responses (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    write_time TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR,
    message VARCHAR,
    response VARCHAR
);
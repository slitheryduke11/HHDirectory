DROP TABLE IF EXISTS contact;

CREATE TABLE contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lastname TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT,
    favorite INTEGER NOT NULL DEFAULT 0
);

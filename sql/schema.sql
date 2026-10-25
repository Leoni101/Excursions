CREATE TABLE IF NOT EXISTS excursions (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    duration INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    excursion_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (excursion_id) REFERENCES excursions(id)
);
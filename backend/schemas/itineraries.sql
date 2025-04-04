CREATE TABLE "Itineraries" (
    "Itineraryid"     INTEGER NOT NULL UNIQUE,
    "Userid"        INTEGER NOT NULL,
    "Title"     TEXT NOT NULL,
    "Date"       DATE NOT NULL,
    "Details"      TEXT NOT NULL,
    "Created"       DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("Itineraryid" AUTOINCREMENT),
    CONSTRAINT "user"
        FOREIGN KEY ("Userid") 
        REFERENCES "User"("Userid")
        ON DELETE CASCADE
);
CREATE TABLE "Activities" (
    "Activityid" INTEGER NOT NULL UNIQUE,
    "Name"      TEXT NOT NULL,
    "Type"     INTEGER NOT NULL,
    "Location"  TEXT NOT NULL,
    "Price"     TEXT NOT NULL,
    PRIMARY KEY("Activityid" AUTOINCREMENT)
);
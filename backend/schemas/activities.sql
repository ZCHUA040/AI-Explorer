CREATE TABLE "Activities" (
    "Activityid" INTEGER NOT NULL UNIQUE,
    "Name"      TEXT NOT NULL,
    "Type"     INTEGER NOT NULL,
    "Location"  TEXT NOT NULL,
    "Price"     TEXT NOT NULL,
    "Price_Category"    TEXT NOT NULL,
    "Image"     TEXT NOT NULL,
    "Description"   TEXT NOT NULL,
    PRIMARY KEY("Activityid" AUTOINCREMENT)
);
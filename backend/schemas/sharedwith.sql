CREATE TABLE "SharedWith" (
    "id"     INTEGER NOT NULL UNIQUE,
    "Userid"        INTEGER NOT NULL,
    "Itineraryid"     INTEGER NOT NULL,
    "Sharedid"      INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT),
    CONSTRAINT "user"
        FOREIGN KEY ("Userid") 
        REFERENCES "User"("Userid")
        ON DELETE CASCADE,
    CONSTRAINT "itinerary"
        FOREIGN KEY ("Itineraryid") 
        REFERENCES "Itineraries" ("Itineraryid") 
        ON DELETE CASCADE,
    CONSTRAINT "shared"
        FOREIGN KEY ("Sharedid") 
        REFERENCES "User"("Userid")
        ON DELETE CASCADE,
);
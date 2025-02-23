BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "albums" (
	"artist_name"	TEXT NOT NULL,
	"header"	TEXT,
	"rel_link"	TEXT NOT NULL,
	"full_link"	TEXT NOT NULL,
	PRIMARY KEY("artist_name","header","rel_link")
);
CREATE TABLE IF NOT EXISTS "artist_wikis" (
	"artist_name"	TEXT NOT NULL,
	"link"	TEXT NOT NULL,
	"discography_found"	INTEGER NOT NULL CHECK("discography_found" IN (0, 1)),
	PRIMARY KEY("artist_name")
);
CREATE TABLE IF NOT EXISTS "node_list" (
	"artist_name"	TEXT NOT NULL,
	"importance"	INT,
	PRIMARY KEY("artist_name")
);
COMMIT;

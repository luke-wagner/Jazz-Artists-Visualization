BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "albums" (
	"artist_name"	TEXT NOT NULL,
	"header"	TEXT,
	"rel_link"	TEXT NOT NULL,
	"full_link"	TEXT NOT NULL,
	PRIMARY KEY("artist_name","header","rel_link")
);
CREATE TABLE IF NOT EXISTS "artists" (
	"artist_name"	TEXT NOT NULL,
	"importance"	INTEGER,
	"link"	TEXT,
	"discography_found"	INTEGER CHECK("discography_found" IN (0, 1)),
	PRIMARY KEY("artist_name")
);
CREATE TABLE IF NOT EXISTS "decode" (
	"decode_type_id"	TEXT NOT NULL,
	"decode_value"	TEXT NOT NULL,
	"short_desc"	TEXT,
	"long_desc"	TEXT,
	PRIMARY KEY("decode_type_id","decode_value")
);
CREATE TABLE IF NOT EXISTS "script_progress" (
	"script_name"	TEXT,
	"process_identifier"	TEXT NOT NULL,
	"key"	TEXT NOT NULL,
	"value"	INTEGER NOT NULL,
	PRIMARY KEY("process_identifier","key")
);
COMMIT;

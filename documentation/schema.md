The database follows the following schema
=========================================

CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	username VARCHAR(144) NOT NULL, 
	email VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	accesslevel INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT _user_uc UNIQUE (username, email), 
	UNIQUE (username), 
	UNIQUE (email)
);
CREATE TABLE author (
	date_created DATETIME, 
	date_modified DATETIME, 
	id INTEGER NOT NULL, 
	name VARCHAR(25), 
	tag VARCHAR(12), 
	PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "group" (
	date_created DATETIME, 
	date_modified DATETIME, 
	id INTEGER NOT NULL, 
	name VARCHAR(30) NOT NULL, 
	abbreviation VARCHAR(7), 
	PRIMARY KEY (id)
);
CREATE TABLE role (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(12) NOT NULL, 
	account_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
);
CREATE TABLE alias (
	date_created DATETIME, 
	date_modified DATETIME, 
	id INTEGER NOT NULL, 
	name VARCHAR(30) NOT NULL, 
	tag VARCHAR(12), 
	is_primary BOOLEAN, 
	author_id INTEGER, 
	PRIMARY KEY (id), 
	CHECK (is_primary IN (0, 1)), 
	FOREIGN KEY(author_id) REFERENCES author (id)
);
CREATE TABLE membership (
	id INTEGER NOT NULL, 
	author_id INTEGER, 
	group_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES author (id), 
	FOREIGN KEY(group_id) REFERENCES "group" (id)
);
CREATE TABLE collection (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	author_id INTEGER NOT NULL, 
	filename VARCHAR(12) NOT NULL, 
	uploader_id INTEGER NOT NULL, 
	collection BLOB NOT NULL, 
	group_id INTEGER, 
	public BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES author (id), 
	FOREIGN KEY(uploader_id) REFERENCES account (id), 
	FOREIGN KEY(group_id) REFERENCES "group" (id), 
	CHECK (public IN (0, 1))
);

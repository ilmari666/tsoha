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


Relationships as described in yuml [yuml.me](http://yuml.me) markup
----------------------------

```

[Account|id:INT(PK);date_created:DATETIME;date_modified:DATETIME;username:VARCHAR(144);email:VARCHAR(144);password:VARCHAR(144);accesslevel:INTEGER]
[Author|id:INT(PK);date_created:DATETIME;date_modified:DATETIME;name:VARCHAR(25);tag:VARCHAR(12)]
[Group|id:INT(PK);date_created:DATETIME;date_modified:DATETIME;name:VARCHAR(30);abbreviation VARCHAR(7)];
[Role|id:INT(PK);date_created:DATETIME;date_modified:DATETIME;name:VARCHAR(12);account_id:INT(FK)];
[Membership|id:INT(PK);author_id:INT(FK);group_id:INT(FK)];
[Collection|id:INT(PK);date_created:DATETIME;date_modified:DATETIME;name:VARCHAR(144);author_id:INT(FK);filename:VARCHAR(12);uploader_id:INT(FK);colly:BLOB;group_id:INT(FK);public:BOOLEAN]


[Account]1-1-*[Role]
[Collection]*-1[Account]
[Collection]1-1[Author]<
[Collection]*-0-1[Group]
[Author]1-*[Membership]
[Membership]*-1[Group]

```


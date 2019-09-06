Stories:
==========

### Anyone
*Anyone can view published collections
```SELECT * FROM COLLECTIONS WHERE public=True```

*Anyone can view groups with simple stats
```SELECT name, r.abbreviation as abbreviation, count(ms.id) as member_count, r.id as id, release_count 
FROM (select g.abbreviation as abbreviation, g.name as name, g.id as id, count(c.group_id) as release_count 
FROM Crew as g LEFT JOIN (SELECT * FROM Collection WHERE public=true ) AS c  ON g.id=c.group_id GROUP BY c.group_id, g.name, g.id) AS r LEFT JOIN Membership AS  ms ON r.id = ms.group_id GROUP BY r.name, r.id, r.release_count, ms.group_id, r.abbreviation```

*Anyone can view authors
```SELECT * FROM author```

*Anyone can get statistics about collections
```SELECT count(c.id) as collection_count, count(DISTINCT a.id) as author_count, count(DISTINCT u.id) as uploader_count, 
count(DISTINCT g.id) as group_count FROM (SELECT * FROM Collection WHERE public=true) AS c 
LEFT JOIN Author AS a ON (c.author_id=a.id) LEFT JOIN Crew AS g ON (c.group_id=g.id) LEFT JOIN Account AS u ON (c.uploader_id=u.id)```

*Anyone can register.
```INSERT INTO Accounts (username, password, email) VALUES (?,?,?)```

### Registered user

*Registered user can authenticate.
```SELECT USER FROM Accounts WHERE USERNAME=? AND password=?``` 

### Authenticated user
*Authenticated user can create new groups
```INSERT INTO Crew (name, abbreviation) VALUES (?,?)```

*Authenticated user can upload new collections
```INSERT INTO Collection (name, author_id, filename, uploader_id, colly, group_id) VALUES (?,?,?,?,?,?)```

*Authenticated user can logout

### Authenticated user with admin role
*Admin can add priviledge groups
```UPDATE Role SET (name=?) WHERE user_id=?```

*Admin can edit and publish collections
```UPDATE Account SET (username, email, public) VALUES (?,?,?)```

*Admin can delete collections
```DELETE FROM Account WHERE id = ?```

*Admin can edit and delete users
```UPDATE Account SET (username, email) VALUES (?,?) WHERE id =?
DELETE FROM Account WHERE id=?
DELETE FROM Role WHERE user_id=?
DELETE FROM Collections WHERE uploader_id=?
```
*Admin can edit authors
```UPDATE Author SET (name, tag) VALUES (?, ?) WHERE id = ?```

*Admin can delete authors
```DELETE FROM Author WHERE id=?```

*Admin can edit groups
```UPDATE GROUP SET (name, abbreviation) VALUES (?,?) WHERE id = ?```

*Admin can delete groups
```DELETE FROM Group WHERE id=?```

*Admin can create memberships
```INSERT INTO membership (group_id, author_id) VALUES (?,?)```

*Admin can delete memberships
```DELETE FROM membership WHERE group_id = ? AND author_id = ?```

*Admin can add authors to groups
```INSERT INTO membership (group_id, member_id) VALUES (?,?)```


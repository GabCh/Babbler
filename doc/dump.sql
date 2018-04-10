CREATE DATABASE Babbler;
USE Babbler;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'choupi';
set global sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

CREATE TABLE IF NOT EXISTS Babblers(username char(24), 
					  publicName char(24), 
                      password char(64), 
                      PRIMARY KEY(username));


CREATE TABLE IF NOT EXISTS Babbles(id integer, 
					 username char(24), 
                     message TEXT, 
                     time_s TIMESTAMP, 
                     PRIMARY KEY(id), 
                     FOREIGN KEY(username) REFERENCES Babblers(username));
                                        

CREATE TABLE IF NOT EXISTS Tag(id integer,
				 tag char(30),
				 FOREIGN KEY(id) REFERENCES Babbles(id) ON DELETE CASCADE);
                 


CREATE TABLE IF NOT EXISTS Follows(follower char(24),
					 followed char(24),
                     FOREIGN KEY(follower) REFERENCES Babblers(username) ON DELETE CASCADE,
                     FOREIGN KEY(followed) REFERENCES Babblers(username) ON DELETE CASCADE);


INSERT INTO Babblers VALUES ('GabCh', 'Gabriel Chantal', '9565d745fe9e4faa336a798a1c9dba561cab20676e7b1a8e4c669aa2dc333bf6');
INSERT INTO Babblers VALUES ('Jannik', 'Jannik Lévesque', '86d9727170343eccb6f9d44906fb658ed95678c1d3434059d042de3df449ab6f');
INSERT INTO Babblers VALUES ('gablalib', 'Gabriel Laliberté', '69273868226b6eadd48685b28d69bb45bc907df6a2a8b373bff1f2155b541b9d');

INSERT INTO Babbles VALUES (1, 'Jannik', 'In et ora pascebantur praetenturis igitur provincialium praetenturis et se contulerunt in opibus ibique opibus Lycaoniam maritima et se in in mox inveniretur itinera praetenturis praetenturis relicta opibus Isauriae adventicium contulerunt cum cum mox maritima provincialium in ora ora intersaepientes et Isauriae adnexam adventicium relicta in itinera relicta opibus relicta.', 
							'2018-02-12 12:06:14');
INSERT INTO Babbles VALUES (2, 'GabCh', 'Supplicio Mihi sit sequi sed vindicanda excusatione tegenda sit haud autem non futura supplicio qualis.', '2018-02-15 16:22:55');
INSERT INTO Babbles VALUES (3, 'gablalib', 'Luctuosam quicquid et ita levibus ad victoriam caedibus animus ad corpus aut cogitatum suae salutis existimans luctuosam et cogitatum suae.', '2018-03-05 18:22:15');
INSERT INTO Babbles VALUES (4, 'Jannik', 'Luctuosam quicquid et ita levibus ad victoriam caedibus animus ad corpus aut cogitatum suae salutis existimans luctuosam et cogitatum suae.', '2018-03-05 18:22:15');
INSERT INTO Babbles VALUES (5, 'GabCh', ' suae salutis existimans luctuosa', '2018-04-01 00:00:00');

INSERT INTO Tag VALUES (1, 'banane');
INSERT INTO Tag VALUES (2, 'blessed');
INSERT INTO Tag VALUES (1, 'banane');
INSERT INTO Tag VALUES (5, 'blessed');
INSERT INTO Tag VALUES (1, 'banane');
INSERT INTO Tag VALUES (3, 'blessed');
INSERT INTO Tag VALUES (1, 'banane');
INSERT INTO Tag VALUES (4, 'bacon');
INSERT INTO Tag VALUES (1, 'banane');
INSERT INTO Tag VALUES (2, 'blessed');
INSERT INTO Tag VALUES (1, 'banane');
INSERT INTO Tag VALUES (5, 'mapleSirop');
INSERT INTO Tag VALUES (1, 'weed');
INSERT INTO Tag VALUES (3, 'blessed');
INSERT INTO Tag VALUES (1, 'banane');
INSERT INTO Tag VALUES (4, 'blessed');

INSERT INTO Follows VALUES ('Jannik', 'GabCh');
INSERT INTO Follows VALUES ('Jannik', 'gablalib');
INSERT INTO Follows VALUES ('gablalib', 'GabCh');
INSERT INTO Follows VALUES ('GabCh', 'gablalib');
INSERT INTO Follows VALUES ('GabCh', 'Jannik');
INSERT INTO Follows VALUES ('gablalib', 'Jannik');

USE Babbler;

CREATE TABLE IF NOT EXISTS Babblers(username char(12), 
					  publicName char(24), 
                      password char(64), 
                      PRIMARY KEY(username));


CREATE TABLE IF NOT EXISTS Babbles(id integer, 
					 username char(12), 
                     message TEXT, 
                     time_s TIMESTAMP, 
                     PRIMARY KEY(id), 
                     FOREIGN KEY(username) REFERENCES Babblers(username));
                                        

CREATE TABLE IF NOT EXISTS Tag(id integer,
				 tag char(30),
				 FOREIGN KEY(id) REFERENCES Babbles(id) ON DELETE CASCADE);
                 


CREATE TABLE IF NOT EXISTS Follows(follower char(12),
					 followed char(12),
                     FOREIGN KEY(follower) REFERENCES Babblers(username) ON DELETE CASCADE,
                     FOREIGN KEY(followed) REFERENCES Babblers(username) ON DELETE CASCADE);


INSERT INTO Babblers VALUES ('GabCh', 'Gabriel Chantal', '3c47979469a88dab6244d218a7b5555681f5098cd0eb4853d1b8966103107f43');
INSERT INTO Babblers VALUES ('Jannik', 'Jannik Lévesque', '3bb3404dad8a122929562e71ac56f5ddd9f189df7b5283dbbdac27504875194c');
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

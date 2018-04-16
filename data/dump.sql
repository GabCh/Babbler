CREATE DATABASE Babbler;
USE Babbler;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'babblerisawesome';
set global sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

CREATE TABLE IF NOT EXISTS Babblers(username char(32),
					  publicName char(32),
                      password char(64), 
                      PRIMARY KEY(username));

CREATE TABLE IF NOT EXISTS Babbles(id integer, 
					 username char(32),
                     message TEXT, 
                     time_s TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                     nbLikes integer,
                     nbComments integer,
                     PRIMARY KEY(id), 
                     FOREIGN KEY(username) REFERENCES Babblers(username) ON DELETE CASCADE);

CREATE INDEX babbleUserIdx USING HASH ON Babbles (username);

CREATE TABLE IF NOT EXISTS Tag(id integer,
							   tag char(32),
							   FOREIGN KEY(id) REFERENCES Babbles(id) ON DELETE CASCADE);                               


CREATE TABLE IF NOT EXISTS Follows(follower char(32),
					 followed char(32),
                     FOREIGN KEY(follower) REFERENCES Babblers(username) ON DELETE CASCADE,
                     FOREIGN KEY(followed) REFERENCES Babblers(username) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS Likes(id integer, 
								 username char(12),
                                 FOREIGN KEY(id) REFERENCES Babbles(id) ON DELETE CASCADE,
                                 FOREIGN KEY(username) REFERENCES Babblers(username) ON DELETE CASCADE);
                                 
CREATE INDEX LikesIndex USING HASH ON Likes (username, id);
                                 
CREATE TABLE IF NOT EXISTS Comments(babbleID integer,
									commentID integer,
									username char(12),
                                    message TEXT,
                                    time_s TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                    nbLikes integer,
                                    PRIMARY KEY(commentID),
                                    FOREIGN KEY(babbleID) REFERENCES Babbles(id) ON DELETE CASCADE,
                                    FOREIGN KEY(username) REFERENCES Babblers(username) ON DELETE CASCADE);

CREATE INDEX commentIDX USING HASH ON Comments (babbleID);
                                    
CREATE TABLE IF NOT EXISTS CommentLikes(id integer, 
										username char(12),
										FOREIGN KEY(id) REFERENCES Comments(commentID) ON DELETE CASCADE,
										FOREIGN KEY(username) REFERENCES Babblers(username) ON DELETE CASCADE);

CREATE INDEX CommentLikesIndex USING HASH ON CommentLikes (username, id);
                                        

delimiter //
CREATE TRIGGER likeBabble 
AFTER INSERT ON Likes
FOR EACH ROW
BEGIN
	UPDATE Babbles
    SET nbLikes = nbLikes + 1
    WHERE id = NEW.id;
END;//
delimiter ;

delimiter //
CREATE TRIGGER unlikeBabble 
AFTER DELETE ON Likes
FOR EACH ROW
BEGIN
	UPDATE Babbles
    SET nbLikes = nbLikes - 1
    WHERE id = OLD.id;
END;//
delimiter ;

delimiter //
CREATE TRIGGER likeComment 
AFTER INSERT ON CommentLikes
FOR EACH ROW
BEGIN
	UPDATE Comments
    SET nbLikes = nbLikes + 1
    WHERE commentID = NEW.id;
END;//
delimiter ;

delimiter //
CREATE TRIGGER unlikeComment 
AFTER DELETE ON CommentLikes
FOR EACH ROW
BEGIN
	UPDATE Comments
    SET nbLikes = nbLikes - 1
    WHERE commentID = OLD.id;
END;//
delimiter ;

delimiter //
CREATE TRIGGER commentBabble 
AFTER INSERT ON Comments
FOR EACH ROW
BEGIN
	UPDATE Babbles
    SET nbComments = nbComments + 1
    WHERE id = NEW.babbleID;
END;//
delimiter ;

delimiter //
CREATE TRIGGER deleteComment 
AFTER DELETE ON Comments
FOR EACH ROW
BEGIN
	UPDATE Babbles
    SET nbComments = nbComments - 1
    WHERE id = OLD.babbleID;
END;//
delimiter ;

INSERT INTO Babblers VALUES ('GabCh', 'Gabriel Chantal', '9565d745fe9e4faa336a798a1c9dba561cab20676e7b1a8e4c669aa2dc333bf6');
INSERT INTO Babblers VALUES ('Jannik', 'Jannik Lévesque', '86d9727170343eccb6f9d44906fb658ed95678c1d3434059d042de3df449ab6f');
INSERT INTO Babblers VALUES ('gablalib', 'Gabriel Laliberté', '69273868226b6eadd48685b28d69bb45bc907df6a2a8b373bff1f2155b541b9d');

INSERT INTO Babbles VALUES (1, 'Jannik', 'In et ora pascebantur praetenturis igitur provincialium praetenturis et se contulerunt in opibus ibique opibus Lycaoniam maritima et se in in mox inveniretur itinera praetenturis praetenturis relicta opibus Isauriae adventicium contulerunt cum cum mox maritima provincialium in ora ora intersaepientes et Isauriae adnexam adventicium relicta in itinera relicta opibus relicta.', 
							'2018-02-12 12:06:14', 0, 0);
INSERT INTO Babbles VALUES (2, 'GabCh', 'Supplicio Mihi sit sequi sed vindicanda excusatione tegenda sit haud autem non futura supplicio qualis.', '2018-02-15 16:22:55', 0, 0);
INSERT INTO Babbles VALUES (3, 'gablalib', 'Luctuosam quicquid et ita levibus ad victoriam caedibus animus ad corpus aut cogitatum suae salutis existimans luctuosam et cogitatum suae.', '2018-03-05 18:22:15', 0, 0);
INSERT INTO Babbles VALUES (4, 'Jannik', 'Luctuosam quicquid et ita levibus ad victoriam caedibus animus ad corpus aut cogitatum suae salutis existimans luctuosam et cogitatum suae.', '2018-03-05 18:22:15', 0, 0);
INSERT INTO Babbles VALUES (5, 'GabCh', ' suae salutis existimans luctuosa', '2018-04-01 00:00:00', 0, 0);

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
INSERT INTO Tag VALUES (3, 'blessed');
INSERT INTO Tag VALUES (1, 'banane');
INSERT INTO Tag VALUES (4, 'blessed');

INSERT INTO Follows VALUES ('Jannik', 'GabCh');
INSERT INTO Follows VALUES ('Jannik', 'gablalib');
INSERT INTO Follows VALUES ('gablalib', 'GabCh');
INSERT INTO Follows VALUES ('GabCh', 'gablalib');
INSERT INTO Follows VALUES ('GabCh', 'Jannik');
INSERT INTO Follows VALUES ('gablalib', 'Jannik');

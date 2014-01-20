from connect import *

users = """
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(64),
    password VARCHAR(256),
    salt INT,
    PRIMARY KEY(id)
)
"""

genres = """
CREATE TABLE IF NOT EXISTS genres (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(64),
    PRIMARY KEY(id)
)
"""

genreBlacklists = """
CREATE TABLE IF NOT EXISTS genreBlacklists (
    id INT NOT NULL AUTO_INCREMENT,
    userID INT,
    genreID INT,
    FOREIGN KEY (userID) REFERENCES users(id),
    FOREIGN KEY (genreID) REFERENCES genres(id),
    PRIMARY KEY(id)
)
"""

songs = """
CREATE TABLE IF NOT EXISTS songs (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(64),
    PRIMARY KEY(id)
    )
"""

activities = """
CREATE TABLE IF NOT EXISTS activities (
    id INT NULL AUTO_INCREMENT,
    name VARCHAR(64),
    PRIMARY KEY(id)
)
"""

music = """
CREATE TABLE IF NOT EXISTS music (
    id INT NOT NULL AUTO_INCREMENT,
    userID INT,
    songID INT,
    genre VARCHAR(64),
    time TIME,
    date DATE,
    position POINT,
    activity INT,
    mostRecentApp VARCHAR(64),
    skipped BOOL,
    skipLen INT,
    mood INT,
    FOREIGN KEY (userID) REFERENCES users(id),
    FOREIGN KEY (songID) REFERENCES songs(id),
    FOREIGN KEY (activity) REFERENCES activities(id),
    INDEX userIdx (userID),
    PRIMARY KEY(id)
    )
"""

def createAll():
    execute(users)
    execute(genres)
    execute(genreBlacklists)
    execute(songs)
    execute(activities)
    execute(music)


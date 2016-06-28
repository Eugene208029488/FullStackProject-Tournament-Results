-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS players, matches CASCADE;
CREATE TABLE players (
    playerid serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    created timestamp DEFAULT current_timestamp
);

CREATE TABLE matches (
    matchid serial PRIMARY KEY,
    winner integer NOT NULL,
    loser integer NOT NULL,
    created timestamp DEFAULT current_timestamp
);

alter table matches add foreign key (winner) REFERENCES players(playerid);
alter table matches add foreign key (loser) REFERENCES players(playerid);

CREATE VIEW total_matches AS
    SELECT playerid, count(winner) as matches from players left join matches
    on playerid=winner or playerid = loser group by playerid;

CREATE VIEW total_wins AS
    SELECT playerid, count(winner) as wins from players left join matches
    on playerid=winner group by playerid;

-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players(
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	noOfWins integer DEFAULT 0 NOT NULL,
	noOfLosses integer DEFAULT 0 NOT NULL,
	noOfGamesPlayed integer DEFAULT 0 NOT NULL
);


CREATE TABLE games(
	id SERIAL PRIMARY KEY,
	player1 integer references players(id) NOT NULL,
	player2 integer references players(id) NOT NULL,
	roundPlayed integer DEFAULT 0 NOT NULL,
	winner integer references players(id)
);

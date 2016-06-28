#Tournament Results

Develop a database schema to store the game matches between players and write Python code to query this data and determine the winners of various games.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.  **I also implemented logic to prevent rematched between players.**

This project has two parts: defining the database schema (SQL table definitions) using PostgresSQL, and writing Python code to query and update the database.

#Technology used:
1. PostgresSQL - database

#Instructions
1. Login to vagrant
  * type '*vagrant ssh*'
  * cd <folder with tournament files are stored>  ex. cd /vagrant/tournament
2. Create a new database and named it "tournament".
  * once login to vagrant...type '*psql*' to launch PostgresSQL
  * type the following to create the database.  '*CREATE DATABASE tournament*'
3. Run tournament.sql to create the tables and view under the new database.
  * while still login to psql, type the following to launch the SQL script.  '*\i tournament.sql*'
  * type '*\q*' to quit PostgresSQL
4. Exit out from PostgresSQL and run "tournament_test.py" code.
  * type "*python tournament_test.py*"


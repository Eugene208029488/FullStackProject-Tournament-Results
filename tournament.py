#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    return


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    return

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    player_cnt = c.fetchone()
    if player_cnt:
        player_cnt = player_cnt[0]
    else:
        player_cnt = 0
    DB.close()
    return player_cnt

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)",(name,))
    DB.commit()
    return

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT players.playerid, name, wins, matches
        FROM players
        left join total_wins on players.playerid = total_wins.playerid
        left join total_matches on players.playerid = total_matches.playerid
        order by wins desc, players.playerid asc
        """)
    standings = c.fetchall()
    DB.close()
    return standings

def checkMatch(player1, player2):
    """Returns a true if match between player1 and player2 already exist

    Args:
        player1: id of player1
        player2: id of player2

    Will check the "matches" table to see if there's already a match between
    player1 and player2

    Returns: True or False
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT *
        FROM matches
        where (winner = %s or winner = %s) and
              (loser = %s or loser = %s)
        """,(player1,player2,player1,player2,))
    rcnt = c.rowcount
    DB.close()
    if rcnt > 0:
        return True
    else:
        return False

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)",(winner, loser,))
    DB.commit()
    return

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings =playerStandings()
    pairing=[]
    tracker={}

    for index1 in range(len(standings)):
        for index2 in range(index1+1,len(standings)):
            # check if standings[index1] vs standing[index2] already exist
            try:
                if checkMatch(standings[index1][0], standings[index2][0]):
                    #print('match already exist for {} vs {}'.format(standings[index1][0], standings[index2][0]))
                    continue
                if tracker[standings[index1][0]] == 'done':
                    #print 'breaking out index1 is done'
                    break
                if tracker[standings[index2][0]] == 'done':
                    #print 'continueing 2nd loop index2 is done'
                    continue
            except KeyError:
                pass
            pairing.append((standings[index1][0],standings[index1][1],standings[index2][0],standings[index2][1],))
            tracker[standings[index1][0]] = 'done'
            tracker[standings[index2][0]] = 'done'
            #print('pairing ',  standings[index1][0], standings[index2][0])
            break
    return pairing




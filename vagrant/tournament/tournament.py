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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from games;")
    conn.commit()
    cursor.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from players;")
    conn.commit()
    cursor.close()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select count(*) from players;")
    count = cursor.fetchone()
    countValue = count[0]
    cursor.close()
    conn.close()
    return countValue

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into players (name) values(%s);",(name,))
    conn.commit()
    cursor.close()
    conn.close()


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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select id, name, noOfWins, noOfGamesPlayed from players order by noOfWins desc;")
    playerList = cursor.fetchall()
    # posts = [{'content': str(row[0]), 'time': str(row[1])} for row in postsFromSQL]
	# playerStandings = {}
    # for p in playerList:
	#   playerStandings{'id':str(p[0]), 'name':str(p[1]), 'wins':str(p[2]), 'matches':str(p[3])}
    conn.commit()
    cursor.close()
    conn.close()    
    return playerList


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select noOfWins, noOfGamesPlayed from players where id = '%s';",(winner,))
    queryResult = cursor.fetchone()
    noOfWins_value = queryResult[0]
    noOfGamesPlayed_winner_value = queryResult[1]
    cursor.execute("select noOfLosses, noOfGamesPlayed from players where id = '%s';",(loser,))
    queryResult = cursor.fetchone()
    noOfLosses_value = queryResult[0]
    noOfGamesPlayed_loser_value = queryResult[1]
	
	# Update the players no of wins and losses
    cursor.execute("update players set noOfWins = %s, noOfGamesPlayed = %s where id = '%s';",(noOfWins_value+1, noOfGamesPlayed_winner_value+1, winner,))
    cursor.execute("update players set noOfLosses = %s, noOfGamesPlayed = %s where id = '%s';",(noOfLosses_value+1, noOfGamesPlayed_loser_value+1, loser,))

    conn.commit()
    cursor.close()
    conn.close()    	
	
	
 
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
    conn = connect()
    cursor = conn.cursor()
	
	# Get all registered players sorted by number of wins.
    cursor.execute("select * from players order by noOfWins desc;")
    players = cursor.fetchall()
    pairings = []

    # Get a player and match with the next one closest in no. of wins.
    # Case of even number of players.
    if (len(players)%2) == 0:
        i=0
    	while i < len(players):
            pairings.append((players[i][0], players[i][1], players[i+1][0], players[i+1][1]))
            i=i+2
    # Create games for each match up and add to database.
    for pair in pairings:
		cursor.execute("insert into games (player1, player2) values (%s, %s)",(pair[0],pair[2]))
	
    conn.commit()
    cursor.close()
    conn.close()
    return pairings
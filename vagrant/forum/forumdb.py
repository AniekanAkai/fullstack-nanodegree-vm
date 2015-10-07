#
# Database access functions for the web forum.
# 
import psycopg2
import time
import logging
from cgi import escape

## Database connection
dbconn = psycopg2.connect("dbname=forum")

## Get posts from database.
def GetAllPosts():
    '''
	Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    dbconn = psycopg2.connect("dbname=forum")
    dbcursor = dbconn.cursor()
    dbcursor.execute("select * from posts;")
    postsFromSQL = dbcursor.fetchall()
    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in postsFromSQL]
    posts.sort(key=lambda row: row['time'], reverse=True)
    dbconn.commit()
    dbcursor.close()
    dbconn.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''
    Add a new post to the database.
    Args:
      content: The text content of the new post.
    '''
    content = escape(content)
    dbconn = psycopg2.connect("dbname=forum")
    dbcursor = dbconn.cursor()
    t = time.strftime('%c', time.localtime())
    dbcursor.execute("insert into posts values(%s);",(content,))# DB.append((t, content))
    dbconn.commit()
    dbcursor.close()
    dbconn.close()

def Delete(id):
    '''
    Delete post with corresponding id from the database.
    Args:
      id - The key identifier for a post in the database
    '''
    dbconn = psycopg2.connect("dbname=forum")
    dbcursor = dbconn.cursor()
    dbcursor.execute("delete from posts where id = (%s)",(id,))
    dbconn.commit()
    dbcursor.close()
    dbconn.close()
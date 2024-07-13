import sqlite3 as sql


def main():
    """ create tables to work with """

    con = sql.connect("main.db")
    cur = con.cursor()

    # ATTENTION! Use deletion carefully! Dropping tables includes ALL entries!
    #cur.execute("DROP TABLE IF EXISTS taskz")
    #cur.execute("DROP INDEX IF EXISTS users.user")
    #cur.execute("DROP TABLE IF EXISTS users")

    # create a user table
    cur.execute(""" CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL, 
                hash TEXT NOT NULL) """)
    
    # create unique on usernames, so each name is just allowed once
    cur.execute(""" CREATE UNIQUE INDEX IF NOT EXISTS user ON users(username) """)
    
    # create a task table for tasks to be stored
    cur.execute(""" CREATE TABLE IF NOT EXISTS taskz (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user INTEGER NOT NULL, 
                title TEXT NOT NULL, 
                text TEXT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                date NUMERIC, 
                checked INTEGER DEFAULT 0, 
                FOREIGN KEY(user) REFERENCES users(id)) """)
    
    con.commit()
    con.close()


if __name__ == "__main__":
    main()
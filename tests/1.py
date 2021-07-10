import sqlite3

con = sqlite3.connect('../sqlite/store.db')
con.execute('CREATE TABLE IF NOT EXISTS confessions_reports(confession_id integer, author_id integer, guild_id integer, reporter_id integer, confession_content integer)')
con.commit()
import sqlite3


def connect_db():
    base = sqlite3.connect('F:\\TgChallengeBot\\ChallengeBot\\db.sqlite3')
    return base


def post_one():
    cur = connect_db().cursor()
    cur.execute("""SELECT content FROM UserAndPost_post WHERE active = 1 
ORDER BY id DESC LIMIT 1""")
    result = cur.fetchone()
    cur.close()
    if result:
        return result[0]
    return None


def chek_status(username):
    cur = connect_db().cursor()
    cur.execute(f"""SELECT name, lastname, id, live FROM UserAndPost_members 
WHERE user_name = '{username}'""")
    result = cur.fetchone()
    cur.close()
    return result


def chek_all_status():
    cur = connect_db().cursor()
    cur.execute(f"""SELECT user_name, live FROM UserAndPost_members
                WHERE live > 0
                ORDER BY live DESC""")
    result = cur.fetchall()
    cur.close()
    return result


def perform_task(time, member_id, type_challenge):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO UserAndPost_report (time, member_id, type_challenge)
VALUES(?, ?, ?)""", (time, member_id, type_challenge))


def update_live_morning_video(date, type_challenge):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute(f"""UPDATE UserAndPost_members
SET live = live - 1
WHERE (id NOT IN (SELECT member_id FROM UserAndPost_report)
AND live != 0)
OR
id IN (
SELECT member_id 
FROM UserAndPost_report 
WHERE time < '{date}' 
AND type_challenge != '{type_challenge}'
)
AND live != 0
 """)



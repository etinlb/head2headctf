import sqlite3
from pprint import pprint
"""
Container for functions that do database things
"""

ACTIVE_MATCH_QUERY = "SELECT * FROM match_data WHERE active = 1";

def connect_db(db_file, row_factory=sqlite3.Row):
    conn = sqlite3.connect(db_file)
    conn.row_factory = row_factory
    return conn

def declare_winner(conn, username):
    user = find_user(g.db, request.form["username"])
    match_query = "SELECT * FROM match WHERE user_id_1 = (?) or user_id_2 = (?) and active = 1"

    match_id = execute_trans(conn, match_query, (user["id"],))

    if match_id is False:
        print("THAT USER WASN'T IN A MATCH")
        return




def stop_challenge(conn, user):
    return execute_trans(conn, "UPDATE USERS set next_score = 0, current_flag = '' where id = (?)",
                         (user["id"],))


def set_user_score(conn, user, score):
    return execute_trans(conn, "UPDATE USERS set score = (?) where id = (?)", (score, user["id"]))


def add_user_next_score(conn, user):
    return set_user_score(conn, user, user["score"] + user["next_score"])


def execute_trans(conn, statement, args_tup):
    try:
        cur = conn.cursor()
        cur.execute(statement, args_tup)
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        print("Rolling back. Transaction " + statement +
              " failed with args " + str(args_tup) + "Error: " + e.message)
        conn.rollback()

    return False


def insert_challenge(conn, label, description):
    return execute_trans(conn, "INSERT INTO challenge (label, description) " +
                               "VALUES (?,?)", (label, description))


def register_user(conn, username):
    return execute_trans(conn, "INSERT INTO users (username) VALUES (?)", (username,))


def get_current_flag(conn, user_id, challenge_id):
    select_flag = "SELECT * FROM flags WHERE user_id = (?) AND current_challenge_id = (?)"
    flag = query_db(conn, select_flag, args=(user_id, challenge_id), one=True)
    if flag is None:
        return None

    return flag["flag"]

def stop_match(conn, match_id, winner=None, score=0):
    stop_query = ""
    argument_tup = ()

    if winner is None:
        stop_query = "UPDATE match set active = 0, score=(?) where id=(?)"
        argument_tup = (score, match_id)
    else:
        stop_query = "UPDATE match set active = 0, score=(?), winner=(?) where id=(?)"
        argument_tup = (score, winner, match_id)

    return execute_trans(conn, stop_query, argument_tup)


def stop_running_matches(conn, winner=None, score=0):
    stop_query = ""
    argument_tup = ()

    if winner is None:
        stop_query = "UPDATE match set active = 0, score=(?) where active = 1"
        argument_tup = (score,)
    else:
        stop_query = "UPDATE match set active = 0, score=(?), winner=(?) where " \
                     "active = 0"
        argument_tup = (score, winner)

    return execute_trans(conn, stop_query, argument_tup)


def start_match(conn, user_id_1, user_id_2, timestamp):
    # start a new match
    insert_statement = "INSERT INTO match (active, user_id_1, user_id_2, timestarted)" \
                       "VALUES (1, (?), (?), (?))"
    argument_tup = (user_id_1, user_id_2, timestamp)

    return execute_trans(conn, insert_statement, argument_tup)


def start_challenge(conn, user_id, flag, next_score):
    # set current flag in user
    update_user_query = "UPDATE USERS set current_flag = (?), next_score = (?) where id = (?)"

    return execute_trans(conn, update_user_query, (flag, next_score, user_id))


def get_all_users(conn):
    user_query = "SELECT * FROM USERS"
    return query_db(conn, user_query)


def query_db(conn, query, args=(), one=False):
    # pprint(query)
    # pprint(args)
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def find_user(conn, username):
    query = "SELECT * FROM USERS WHERE username = (?)"
    user = query_db(conn, query, args=(username,), one=True)
    # pprint(user["username"])
    return user

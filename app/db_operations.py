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
    match_query = "SELECT * FROM match_data WHERE username1 = (?) or username2 = (?) and active = 1"

    match = query_db(conn, match_query, (username, username), True)

    if match is None:
        print("THAT USER WASN'T IN A MATCH")
        return

    set_winner_query = "UPDATE match set winner = (?), active = 0 WHERE id = (?)"

    winner_id = match["user_id_1"] if match["username1"] == username else match["user_id_2"]

    stop_challenge(conn, match["user_id_1"])
    stop_challenge(conn, match["user_id_2"])

    return execute_trans(conn, set_winner_query, (winner_id, match["id"]))


def insert_challenge(conn, snap_shot_name, scenario_name, category, difficulty, flag, score=50, description=""):
    insert_query = "INSERT INTO challenge (snap_shot_name, scenario_name, description, category, difficulty, score, flag) VALUES (?,?,?,?,?,?,?)"
    return execute_trans(conn, insert_query, (snap_shot_name, scenario_name, description, category, difficulty, score, flag))

def get_challenge(conn, snap_shot_name):
    return query_db(conn, "SELECT * FROM challenge WHERE snap_shot_name = (?)", (snap_shot_name,), True)


def stop_challenge(conn, user_id):
    return execute_trans(conn, "UPDATE USERS set next_score = 0, current_flag = '' where id = (?)",
                         (user_id,))


def set_user_score(conn, user, score):
    return execute_trans(conn, "UPDATE USERS set score = (?) where id = (?)", (score, user["id"]))


def add_user_next_score(conn, user):
    return set_user_score(conn, user, user["score"] + user["next_score"])

def start_trans(conn):
    return conn.cursor()

def commit_transaction(conn):
    return conn.commit()

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

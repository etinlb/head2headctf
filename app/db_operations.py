import sqlite3
from pprint import pprint
"""
Container for functions that do database things
"""

INSERT_FLAG_QUERY = "INSERT INTO flags (challenge_id, user_id, flag) VALUES (?,?,?)"


def connect_db(db_file, row_factory=sqlite3.Row):
    conn = sqlite3.connect(db_file)
    conn.row_factory = row_factory
    return conn


def stop_challenge(conn, user):
    return execute_trans(conn, "UPDATE USERS set next_score = 0, current_flag = '' where id = (?)", (user["id"],))


def set_user_score(conn, user, score):
    """Should be in db operations"""
    return execute_trans(conn, "UPDATE USERS set score = (?) where id = (?)", (score, user["id"]))


def add_user_next_score(conn, user):
    """Should be in db operations"""
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


def start_challenge(conn, user_id, flag, next_score):
    # set current flag in user
    update_user_query = "UPDATE USERS set current_flag = (?), next_score = (?) where id = (?)"

    return execute_trans(conn, update_user_query, (flag, next_score, user_id))


def get_or_create_vulnerable_service(conn, user, service_name):
    service_query = "SELECT * FROM vulnerable_services WHERE user_id = (?) AND service = (?)"
    service = query_db(
        conn, service_query, args=(user["id"], service_name), one=True)

    if not service:
        insert_query = "INSERT INTO vulnerable_services (user_id, service) VALUES (?,?)"
        success = execute_trans(conn, insert_query, (user["id"], service_name))
        if success:
            service = query_db(
                conn, service_query, args=(user["id"], service_name), one=True)
        else:
            raise ValueError(
                "Can't insert " + service_name + " for user " + str(user))

    return service


def update_vulnerable_services(conn, ip, service_name, vulnerable, is_up):
    user = user_for_ip(conn, ip)
    service = get_or_create_vulnerable_service(conn, user, service_name)
    update_query = "UPDATE vulnerable_services set vulnerable = (?)"
    args = [vulnerable]
    if is_up:
        update_query += ", uptime = (?), available = 1" + str()
        args.append(service["uptime"] + 1)
    else:
        update_query += ", downtime = (?), available = 0"
        args.append(service["downtime"] + 1)

    update_query += " WHERE user_id = (?) AND service = (?)"
    args.append(user["id"])
    args.append(service_name)

    return execute_trans(conn, update_query, args)


def get_all_users(conn):
    user_query = "SELECT * FROM USERS"
    return query_db(conn, user_query)


def query_db(conn, query, args=(), one=False):
    pprint(query)
    pprint(args)
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def find_user(conn, username):
    query = "SELECT * FROM USERS WHERE username = (?)"
    user = query_db(conn, query, args=(username,), one=True)
    pprint(user["username"])
    return user


# if __name__ == '__main__':
#     # Self test stuff
#     print("hello")
#     conn = connect_db("self_test.db")
#     register_user(conn, "user1", "123.2.2.1")
#     register_user(conn, "user2", "123.2.2.2")
#     # Add services
#     update_vulnerable_services(conn, "123.2.2.1", "service1", True, True)
#     update_vulnerable_services(conn, "123.2.2.1", "service2", True, True)
#     update_vulnerable_services(conn, "123.2.2.1", "service3", True, False)
#     update_vulnerable_services(conn, "123.2.2.2", "service1", True, True)
#     update_vulnerable_services(conn, "123.2.2.2", "service2", False, True)
#     update_vulnerable_services(conn, "123.2.2.2", "service3", False, True)
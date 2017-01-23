from flask import render_template, request, g, redirect, url_for
from app import app
from app.db_operations import *
from pprint import pprint

DATABASE = "data.db"


@app.before_request
def before_request():
    g.db = connect_db(DATABASE, sqlite3.Row)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route("/")
def scoreboard():
    users = get_all_users(g.db)
    return render_template('scoreboard.html', users=users)


@app.route("/register_user")
def score():
    print("made it here")
    # users = get_all_users(g.db)
    # current_user = match_user_to_ip(request.remote_addr, users)
    return "hello"
#     return render_template('scoreboard.html',  current_user=current_user)


@app.route("/submitflag")
def submitflag(error=None):
    users = get_all_users(g.db)
    return render_template('submit_flag.html', users=users, error=error)


@app.route('/postflag', methods=['POST'])
def postflag():
    pprint(request.form)
    user = find_user(g.db, request.form["username"])

    if user is None:
        return "NO USER ASSFACE"

    flag = user["current_flag"]
    pprint(flag)
    pprint(flag == request.form["flag"])
    if(flag == request.form["flag"]):
        add_user_next_score(g.db, user)
        stop_challenge(g.db, user)

    return str(flag == request.form["flag"])

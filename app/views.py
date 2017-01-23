from flask import render_template, request, g, redirect, url_for, jsonify
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    # redirect to register if already registered
    if request.method == 'GET':
        return render_template('register.html')

    if find_user(g.db, request.form["username"]):
        return "user by that name already exists!"
    else:
        register_user(g.db, request.form["username"])
        return redirect(url_for('scoreboard', _external=True, _scheme='https'))


@app.route("/submitflag")
def submitflag(error=None):
    users = get_all_users(g.db)
    return render_template('submit_flag.html', users=users, error=error)


@app.route('/postflag', methods=['POST'])
def postflag():
    pprint(request.form)
    user = find_user(g.db, request.form["username"])

    ret_dict = {"success": False}
    if user is None:
        ret_dict["error_msg"] = "NO USER BY THAT NAME"
        return jsonify(**ret_dict)


    flag = user["current_flag"]
    pprint(flag)
    pprint(flag == request.form["flag"])
    if (flag == request.form["flag"]):
        add_user_next_score(g.db, user)
        # For now we can just stop all running matches
        stop_running_matches(conn)

    ret_dict["success"] = flag == request.form["flag"]

    return jsonify(**ret_dict)

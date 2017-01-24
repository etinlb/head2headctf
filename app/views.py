from flask import render_template, request, g, redirect, url_for, jsonify
from app import app
from app.db_operations import *
from pprint import pprint
from threading import Timer

import app.vm_management as vm
import ctf_db as hack
import time


TIMER_AMOUNT = 600


def kill_vms():
    vm.kill_vms()
    db = connect_db(DATABASE, sqlite3.Row)
    try:
        stop_running_matches(db)
    except Exception as e:
        pass

    if db is not None:
        db.close()


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
    active_match = get_active_match(g.db)
    match_data = {}
    if active_match is not None:
        match_data["player_1"] = active_match["username1"]
        match_data["player_2"] = active_match["username2"]
        match_data["timeleft"] = TIMER_AMOUNT - (int(time.time()) - active_match["timestarted"])
    else:
        match_data = None

    if match_data["timeleft"] < 0:
        match_data = None

    pprint(match_data)
    return render_template('scoreboard.html', users=users, active_match=match_data)


@app.route('/startvm', methods = ['POST'])
def post():
    # Get the parsed contents of the form data
    json = request.json
    users = []
    if len(json) < 2:
        return "NOPE"

    for entry in json:
        try:
            if (entry["username"] != "maint"):
                users.append((entry["username"], entry["domain_name"], entry["snapshot_name"]))
            vm.start_domain("qemu+ssh://root@192.168.200.1/system", entry["domain_name"], entry["snapshot_name"])
        except Exception as e:
            pass

    hack.start_contest_by_snapshot(g.db, users[0][0], users[1][0],
                                         users[0][1], users[1][1],
                                         users[0][2], users[1][2])
    t = Timer(TIMER_AMOUNT, kill_vms)
    t.start() # after 30 seconds, "hello, world" will be printed

    return "Started"

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


@app.route("/submitflag", methods=['GET', 'POST'])
def submitflag(error=None):
    if request.method == 'GET':
        return render_submission_form(error)
    else:
        return process_flag_submission(request.form["username"], request.form["flag"].lower())


@app.route("/viewdomains", methods=['GET'])
def viewdomains(error=None):
    connection_str = "qemu+ssh://root@192.168.200.1/system"
    domains = vm.get_domains_and_snapshots("qemu+ssh://root@192.168.200.1/system")
    users = get_all_users(g.db)
    return render_template("domains.html", domains=domains, users=users)


@app.route("/viewdomains_database", methods=['GET'])
def viewdomains_database(error=None):
    domains = get_all_domain_data(g.db)
    users = get_all_users(g.db)
    return render_template("domains.html", domains=domains, users=users)


def render_submission_form(error=None):
    users = get_all_users(g.db)
    return render_template('submit_flag.html', users=users, error=error)


def process_flag_submission(username, flag):
    user = find_user(g.db, username)

    ret_dict = {"success": False}
    if user is None:
        ret_dict["error_msg"] = "NO USER BY THAT NAME"
        return jsonify(**ret_dict)

    current_flag = user["current_flag"]
    pprint(current_flag)
    pprint(current_flag.lower() == flag.lower())

    if (current_flag.lower() == flag.lower()):
        add_user_next_score(g.db, user)
        declare_winner(g.db, user["username"])
        # For now we can just stop all running matches
        stop_running_matches(g.db)
        vm.kill_vms()
        ret_dict["success"] = True

    return jsonify(**ret_dict)

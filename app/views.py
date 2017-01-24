from flask import render_template, request, g, redirect, url_for, jsonify
from app import app
from app.db_operations import *
from pprint import pprint

import app.vm_management as vm

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


@app.route("/submitflag", methods=['GET', 'POST'])
def submitflag(error=None):
    if request.method == 'GET':
        return render_submission_form(error)
    else:
        return process_flag_submission(request.form["username"], request.form["flag"])


@app.route("/viewdomains", methods=['GET'])
def viewdomains(error=None):
    connection_str = "qemu+ssh://root@192.168.200.1/system"
    domains = vm.get_domains_and_snapshots("qemu+ssh://root@192.168.200.1/system")
    users = get_all_users(g.db)
    return render_template("domains.html", domains=domains, users=users)


# @app.route("/startvm/<domainname>/<snapshot>", methods=['GET', 'POST'])
# def start_domain(domainname="", snapshot=""):
#     print(domainname)
#     print(snapshot)
#     vm.start_domain("qemu+ssh://root@192.168.200.1/system", domainname, snapshot)

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
    pprint(current_flag == flag)

    if (current_flag == flag):
        add_user_next_score(g.db, user)
        declare_winner(g.db, user["username"])
        # For now we can just stop all running matches
        stop_running_matches(g.db)
        vm.kill_vms()
        ret_dict["success"] = True

    return jsonify(**ret_dict)

from argparse import ArgumentParser
from app.db_operations import *
from pprint import pprint

import sqlite3
import time
import app.vm_management as vm

DATABASE = "data.db"

DEFAULT_SCORE = 50

conn = connect_db(DATABASE)

def start_contest_by_snapshot(conn, username_1, username_2, user_1_domain,  user_2_domain, snapshot):
    print(username_1)
    user_1 = find_user(conn, username_1)
    if user_1 is None:
        print("No user found for " + username_1)
        return False

    user_2 = find_user(conn, username_2)
    if user_2 is None:
        print("No user found for " + username_2)
        return False

    user_1_challenge = get_challenge(conn, user_1_domain, snapshot)
    user_2_challenge = get_challenge(conn, user_2_domain, snapshot)

    if user_1_challenge is None:
        print("NO challenge with both " + user_1_domain + " and " + snapshot)
        return False

    if user_2_challenge is None:
        print("NO challenge with both " + user_2_domain + " and " + snapshot)
        return False

    start_challenge(conn, user_1["id"], user_1_challenge["flag"], user_1_challenge["score"])
    start_challenge(conn, user_2["id"], user_2_challenge["flag"], user_2_challenge["score"])

    stop_running_matches(conn)
    start_match(conn, user_1["id"], user_2["id"], int(time.time()))


def start_contest(conn, username_1, username_2, flag_1, flag_2, score):
    print(username_1)
    user_1 = find_user(conn, username_1)
    if user_1 is None:
        print("No user found for " + username_1)
        return False

    user_2 = find_user(conn, username_2)
    if user_2 is None:
        print("No user found for " + username_2)
        return False

    start_challenge(conn, user_1["id"], flag_1, score)
    start_challenge(conn, user_2["id"], flag_2, score)

    stop_running_matches(conn)
    start_match(conn, user_1["id"], user_2["id"], int(time.time()))

    return True



if __name__ == "__main__":
    parser = ArgumentParser(description='Edit the ctf database')

    action_parser = parser.add_subparsers(help='what to do', dest='command')

    start_parser = action_parser.add_parser("start", help="Start a head to head challenge")
    start_parser.add_argument('username_1')
    start_parser.add_argument('username_2')
    start_parser.add_argument('domain_1')
    start_parser.add_argument('domain_2')
    start_parser.add_argument('snapshot')
    # start_parser.add_argument('flag_1')
    # start_parser.add_argument('flag_2')
    # start_parser.add_argument('--score', dest='score', default=DEFAULT_SCORE, help="Score for the challenge")

    add_user_parser = action_parser.add_parser("add_user")
    add_user_parser.add_argument('username')

    add_snapshot = action_parser.add_parser("add_snapshot")
    add_snapshot.add_argument('domain')
    add_snapshot.add_argument('snapshot')


    add_challenge_parser = action_parser.add_parser("add_challenge")
    add_challenge_parser.add_argument('domain')
    add_challenge_parser.add_argument('snapshot')
    add_challenge_parser.add_argument('flag')
    add_challenge_parser.add_argument('-c', '--category', dest='category', default="", help="Category of challenge")
    add_challenge_parser.add_argument('-d', '--difficulty', dest='difficulty', default="", help="How hard")
    add_challenge_parser.add_argument('-s', '--score', dest='score', default=50, help="How many scores do they get?")

    populate_challenge = action_parser.add_parser("populate", help="Populate challenge database")

    args = parser.parse_args()

    print(args.command)
    if args.command == "start":
        print("starting")
        start_contest_by_snapshot(conn, args.username_1, args.username_2, args.domain_1, args.domain_2, args.snapshot)
    elif args.command == "add_user":
        print("starting")
        add_user(conn, args.username)
    elif args.command == "add_challenge":
        print("Inserting")
        insert_challenge(conn, args.domain, args.snapshot, args.category, args.difficulty, args.flag, score=args.score)
    elif args.command == "populate":
        connection_str = "qemu+ssh://root@192.168.200.1/system"
        domains = vm.get_domains_and_snapshots(connection_str)
        for domain in domains:
            insert_challenge(conn, domain["domain_name"], domain["snapshot_name"], "test", 1, domain["description"], score=50)
    elif args.command == "add_snapshot":
        domain = get_domain(conn, args.domain)
        pprint(domain)
        snapshot = get_snapshot(conn, args.snapshot)

        if domain is None:
            domain_id = insert_domain(conn, args.domain)
        else:
            domain_id = domain["id"]

        if snapshot is None:
            snapshot_id = insert_snapshot(conn, args.snapshot)
        else:
            snapshot_id = snapshot["id"]

        insert_domain_snapshot_join(conn, domain_id, snapshot_id)

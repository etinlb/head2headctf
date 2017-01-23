import sqlite3
from argparse import ArgumentParser

from app.db_operations import connect_db, start_challenge, register_user, insert_challenge, find_user
from pprint import pprint

DATABASE = "data.db"

DEFAULT_SCORE = 50

connection = connect_db(DATABASE)


def add_user(conn, username):
    pprint(register_user(conn, username))


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

    return True



if __name__ == "__main__":
    parser = ArgumentParser(description='Edit the ctf database')

    action_parser = parser.add_subparsers(help='what to do', dest='command')

    start_parser = action_parser.add_parser("start", help="Start a head to head challenge")
    start_parser.add_argument('username_1')
    start_parser.add_argument('username_2')
    start_parser.add_argument('flag_1')
    start_parser.add_argument('flag_2')
    start_parser.add_argument('--score', dest='score', default=DEFAULT_SCORE, help="Score for the challenge")

    add_user_parser = action_parser.add_parser("add_user")
    add_user_parser.add_argument('username')


    add_challenge_parser = action_parser.add_parser("add_challenge")

    # add_challenge_parser.add_argument(label, description)


    # parser.add_argument('--starting-delay', default=DEFAULT_START_DELAY, type=int,
    #                     help='the amount of time in seconds between each attack check')

    parser.add_argument('--prod', action='store_true',
                        help='start server in production mode, i.e. available outside network)')

    # parser.add_argument('--no-attack', action='store_true',
    #                     help="Don't spawn attack thread")

    args = parser.parse_args()

    print(args.command)
    if args.command == "start":
        print("starting")
        start_contest(connection, args.username_1, args.username_2,
                      args.flag_1, args.flag_2, args.score)
    elif args.command == "add_user":
        print("starting")
        add_user(connection, args.username)


    # if not args.no_attack:
    #     attack_interval = args.attack_interval
    #     starting_delay = args.starting_delay
    #     attacker = AttackCoordinator(DATABASE,
    #                                  attack_interval=attack_interval,
    #                                  starting_delay=starting_delay)
    #     log.info("Spawning attack thread")
    #     t = Thread(target=attacker.attack_loop)
    #     t.daemon = True  # catches ctrl-c interupts
    #     t.start()
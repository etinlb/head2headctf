from flask import Flask, render_template, request, g, redirect, url_for
from threading import Thread
from argparse import ArgumentParser
from db_operations import *

import sqlite3
import os.path

DATABASE = "data.db"



# boiler plate code form the tutorial

# if __name__ == "__main__":
#     parser = ArgumentParser(description='Start the attack server')
#     # parser.add_argument('--attack-interval', default=DEFAULT_ATTACK_INTERVAL, type=int,
#     #                     help='the amount of time in seconds between each attack check')

#     # parser.add_argument('--starting-delay', default=DEFAULT_START_DELAY, type=int,
#     #                     help='the amount of time in seconds between each attack check')

#     parser.add_argument('--prod', action='store_true',
#                         help='start server in production mode, i.e. available outside network)')

#     # parser.add_argument('--no-attack', action='store_true',
#     #                     help="Don't spawn attack thread")

#     args = parser.parse_args()

#     # if not args.no_attack:
#     #     attack_interval = args.attack_interval
#     #     starting_delay = args.starting_delay
#     #     attacker = AttackCoordinator(DATABASE,
#     #                                  attack_interval=attack_interval,
#     #                                  starting_delay=starting_delay)
#     #     log.info("Spawning attack thread")
#     #     t = Thread(target=attacker.attack_loop)
#     #     t.daemon = True  # catches ctrl-c interupts
#     #     t.start()

#     if args.prod:
#         app.run(host='0.0.0.0')
#     else:
#         app.run(host='0.0.0.0', debug=True)
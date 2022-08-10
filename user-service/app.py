import asyncio
import json
import logging
import random
import string
import math
import sys
import time
import os

import tornado.ioloop
import tornado.web

from tornado.log import enable_pretty_logging

user_db = {}


"""
PLEASE DO NO MAKE ANY UNNECESSARY CHANGES TO THE CODE
"""


def generate_random_user_id():
    all_chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(all_chars, k=10)).lower()


class BaseHandler(tornado.web.RequestHandler):
    async def prepare(self):
        ...

    def write_json(self, data, status=200):
        self.write(json.dumps(data))
        self.set_header("Content-Type", "application/json")
        self.set_status(status)


class PingHandler(BaseHandler):
    async def get(self):
        duration = random.randint(0, 5) - 1
        await asyncio.sleep(duration)
        self.write("Ok!")


class UsersHandler(BaseHandler):
    async def get(self):
        self.write_json({"users": user_db})

    async def post(self):
        name = self.get_argument(name="name", default=None)
        email = self.get_argument(name="email", default=None)
        if not name or not email:
            self.write_json({"message": "name and email not given"}, 400)
            return

        user_id = generate_random_user_id()
        user_db[user_id] = {
            "name": name,
            "email": email,
        }
        self.write_json({"user_id": user_id})


class UserHandler(BaseHandler):
    async def get(self, user_id):
        if not user_id:
            self.write_json({"message": "please provide valid user_id"}, 400)
            return

        user = user_db.get(user_id)
        if not user:
            self.write_json({"message": "user not found!"}, 404)
            return

        return self.write_json({"user": user})


def make_app():
    endpoints = [
        tornado.web.url(r"/ping", PingHandler),
        tornado.web.url(r"/v1/users", UsersHandler),
        tornado.web.url(r"/v1/users/(?P<user_id>[^/]+)", UserHandler),
    ]
    return tornado.web.Application(endpoints)


def app_startup_operation():
    duration = random.randint(3, 5)
    logging.info("Running startup operations for {}s".format(duration))
    time.sleep(duration)
    logging.info("Done with startup operations!")


MAX_CRASH = int(os.environ["MAX_CRASH"] if "MAX_CRASH" in os.environ else 5)
if MAX_CRASH <= 1:
    MAX_CRASH = 2

if __name__ == "__main__":
    enable_pretty_logging()
    # just some delay before anything
    # so that after the container restarts,
    # we can see some delay
    time.sleep(1)

    logging.info("App starting ...")

    # another delay before deciding to crash or continue
    time.sleep(2)
    logging.info(f"MAX_CRASH is {MAX_CRASH}")
    if math.ceil(random.randint(1, MAX_CRASH)) == MAX_CRASH:
        logging.error("About to crash ...")

        # the suspense delay...
        time.sleep(random.randint(1, 3))
        logging.error("I crashed! Help!")
        sys.exit()

    app_startup_operation()
    app = make_app()
    port = 8001
    app.listen(port)
    logging.info(f"Listening to the incoming requests at port {port}")
    tornado.ioloop.IOLoop.current().start()

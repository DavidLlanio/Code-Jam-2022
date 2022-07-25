import os
import time
from hashlib import md5
from pprint import pprint
from random import randint

from pymongo import MongoClient, errors


class Credentials:
    """Handlers for the Credentials table"""

    def __init__(self, db):
        """Inititalization.

        Initializes the table with the
        unique condition enforced on usernames
        """
        self.credentials = db.credentials
        self.credentials.create_index("password")
        self.credentials.create_index("image_url")
        self.credentials.create_index("generic_name")
        self.credentials.create_index("username", unique=True)

    # Helper and testing functions start here
    def locate_user(self, username):
        """Locates the user data given the username"""
        user_data = self.credentials.find_one({"username": username})
        return user_data

    def show_table(self):
        """Shows the table. Useful for debugging"""
        cursor = self.credentials.find({})
        for document in cursor:
            pprint(document)

    def drop_all(self):
        """Drops the table.

        Good for testing and
        being data efficient.
        """
        self.credentials.drop()
        print("Deletion successful!")

    def hash(self, input_data):
        """Hashes and returns the hex digest."""
        return md5(input_data.encode()).hexdigest()

    # End of helper functions
    def login(self, username, password):
        """Tries to log the user in.

        Returns a T/F output for now.
        """
        hashed_password = self.hash(password)
        user_password = self.locate_user(username)["password"]
        if user_password == hashed_password:
            return True
        else:
            return False

    def save_credentials(self, username, password, image_url):
        """The create operation.

        Creates the user per the information
        provided.
        """
        first = [
            "Vanilla",
            "Chocolate",
            "Strawberry",
            "Blueberry",
            "Stale",
            "Broke",
            "Ded",
        ]
        last = ["IceCream", "Fudge", "Cracker", "Ehe", "NPC"]
        first_name = first[randint(0, len(first) - 1)]
        last_name = last[randint(0, len(last) - 1)]
        generic_af_username = first_name + last_name
        password_hash = self.hash(password)
        user = {
            "username": username,
            "password": password_hash,
            "image_url": image_url,
            "generic_name": generic_af_username,
        }
        try:
            self.credentials.insert_one(user)
        except errors.DuplicateKeyError:
            pprint("Write failed! Duplicate username")

    def change_password(self, username, password, new_password):
        """Password change.

        If the login attempt succeeds,
        allows the user to change their password.
        """
        if self.login(username, password):
            new_password_hash = self.hash(new_password)
            self.credentials.update_one(
                {"username": username}, {"$set": {"password": new_password_hash}}
            )
            print("Password update successful!")
        else:
            print("Access denied: User identity could not be established.")

    def change_avatar(self, username, new_avatar_url):
        """Avatar change.

        Assuming that the user is logged in already,
        changes their avatar.
        """
        self.credentials.update_one(
            {"username": username}, {"$set": {"image_url": new_avatar_url}}
        )
        print("Avatar URL update successful!")

    def change_username(self, username, password, new_username):
        """Username change.

        If the login attempt succeeds, and if
        the username doesn't conflict with an existing
        username, allows the user to change their username.
        """
        if self.login(username, password):
            try:
                self.credentials.update_one(
                    {"username": username}, {"$set": {"username": new_username}}
                )
            except errors.DuplicateKeyError:
                pprint("Write failed! Duplicate username")

        else:
            print("Write failed! User identity could not be established!")


class Messages:
    """Handlers for the Messages table"""

    def __init__(self, db):
        """Inititalization.

        Initializes the table.
        """
        self.messages = db.messages
        self.messages.create_index("timestamp")
        self.messages.create_index("edit_timestamp")
        self.messages.create_index("sender_username")
        self.messages.create_index("editor_username")
        self.messages.create_index("current_text")
        self.messages.create_index("pre_edit_text")

    # Helpers start here
    def locate_message(self, id):
        """Locates the message given the message id"""
        message_data = self.messages.find_one({"_id": id})
        return message_data

    def show_table(self):
        """Shows the table. Useful for debugging"""
        cursor = self.messages.find({})
        for document in cursor:
            pprint(document)

    def drop_all(self):
        """Drops the table.

        Good for testing and
        being data efficient.
        """
        self.messages.drop()
        print("Deletion successful!")

    def add_message(self, current_text, sender_username):
        """Adds a single message.

        edit_timestamp, editor_username and pre_edit_text
        are all null values in an un-edited message,
        in case anyone needs to validate something.
        """
        timestamp = time.time()
        message_data = {
            "timestamp": timestamp,
            "edit_timestamp": None,
            "sender_username": sender_username,
            "editor_username": None,
            "current_text": current_text,
            "pre_edit_text": None,
        }
        result = self.messages.insert_one(message_data)
        return result.inserted_id

    def edit_message(self, id, current_text, editor_username):
        """Edits a single message.

        Records timestamp for the edit, swaps pre-
        and post-edit message states, and runs an
        update_one() operation.
        """
        message_data = self.locate_message(id)
        edit_timestamp = time.time()
        pre_edit_text = message_data["current_text"]
        self.messages.update_one(
            {"_id": id},
            {
                "$set": {
                    "edit_timestamp": edit_timestamp,
                    "editor_username": editor_username,
                    "current_text": current_text,
                    "pre_edit_text": pre_edit_text,
                }
            },
        )


if __name__ == "__main__":
    # url_start = "mongodb+srv://"
    # username = urllib.parse.quote_plus("codejam2022")
    # password = urllib.parse.quote_plus("Yellowjacket@1024")
    # url_end = "@atlascluster.ig1mf.mongodb.net/?retryWrites=true&w=majority"
    # client = MongoClient(url_start + username + ":" + password + url_end)

    client = MongoClient(
        host=["database:27017"],
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
    )
    db = client.yellowjacket
    messages = Messages(db)
    print("Old table")
    messages.show_table()
    message_one = messages.add_message("Hello world!", "cooltas")
    message_two = messages.add_message("Watch me change this lol", "malitas")
    print("After two additions")
    messages.show_table()
    messages.edit_message(message_one, "Am dum", "malitas")
    messages.edit_message(message_two, "I can do it too, ya dum dum!", "cooltas")
    print("After spicy edits")
    messages.show_table()
    messages.drop_all()
    print("Nothing should appear past this point!")
    messages.show_table()

    # Testing for credentials table
    # credentials = Credentials(db)
    # print("Old table")
    # credentials.show_table()
    # credentials.save_credentials("objecttas", "some_stuff", "some_url")
    # print("New table")
    # credentials.show_table()
    # credentials.change_password("objecttas", "some_password", "new_password")
    # credentials.change_password("objecttas", "some_stuff", "new_stuff")
    # print("Table when password is changed")
    # credentials.show_table()
    # print("Login successful:", credentials.login("objecttas", "some_password"))
    # print("Login successful:", credentials.login("objecttas", "some_stuff"))
    # print("Login successful:", credentials.login("objecttas", "new_stuff"))
    # credentials.change_avatar("objecttas", "cool_url")
    # print("After avatar update:")
    # credentials.show_table()
    # credentials.change_username("objecttas", "new_stuff", "cooltas")
    # print("After username update:")
    # credentials.show_table()
    # credentials.drop_all()
    # credentials.show_table()
    # print("Nothing should appear after this point!")
    # credentials.show_table()

import time
from hashlib import md5
from pprint import pprint
from random import randint
from pymongo import errors

__all__: list[str] = ["Credentials", "Messages", "Admin"]


class Credentials:
    """Handlers for the Credentials table"""

    @classmethod
    def create_credentials(cls,client):
        self = Credentials()
        db = client.yellowjacket
        self.credentials = db.credentials
        self.credentials.create_index("password")
        self.credentials.create_index("image_url")
        self.credentials.create_index("generic_name")
        self.credentials.create_index("username", unique=True)
        return self

    # Helper and testing functions start here
    async def locate_user(self, username: str) -> dict:
        """Locates the user data given the username"""
        user_data = await self.credentials.find_one({"username": username})
        return user_data

    async def show_table(self) -> None:
        """Shows the table. Useful for debugging"""
        cursor = await self.credentials.find({})
        async for document in cursor:
            pprint(document)

    async def drop_all(self) -> None:
        """Drops the table.

        Good for testing and
        being data efficient.
        """
        await self.credentials.drop()
        print("Deletion successful!")

    def hash(self, input_data: str) -> str:
        """Hashes and returns the hex digest."""
        return md5(input_data.encode()).hexdigest()

    # End of helper functions
    async def login(self, username: str, password: str) -> bool:
        """Tries to log the user in.

        Returns a T/F output for now.
        """
        hashed_password = self.hash(password)
        user_password = await self.locate_user(username)["password"]
        if user_password == hashed_password:
            return True
        else:
            return False

    async def save_credentials(
        self, username: str, password: str, image_url: str
    ) -> None:
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
            await self.credentials.insert_one(user)
        except errors.DuplicateKeyError:
            pprint("Write failed! Duplicate username")

    async def change_password(
        self, username: str, password: str, new_password: str
    ) -> None:
        """Password change.

        If the login attempt succeeds,
        allows the user to change their password.
        """
        if await self.login(username, password):
            new_password_hash = self.hash(new_password)
            await self.credentials.update_one(
                {"username": username}, {"$set": {"password": new_password_hash}}
            )
            print("Password update successful!")
        else:
            print("Access denied: User identity could not be established.")

    async def change_avatar(self, username: str, new_avatar_url: str) -> None:
        """Avatar change.

        Assuming that the user is logged in already,
        changes their avatar.
        """
        await self.credentials.update_one(
            {"username": username}, {"$set": {"image_url": new_avatar_url}}
        )
        print("Avatar URL update successful!")

    async def change_username(
        self, username: str, password: str, new_username: str
    ) -> None:
        """Username change.

        If the login attempt succeeds, and if
        the username doesn't conflict with an existing
        username, allows the user to change their username.
        """
        if await self.login(username, password):
            try:
                await self.credentials.update_one(
                    {"username": username}, {"$set": {"username": new_username}}
                )
            except errors.DuplicateKeyError:
                pprint("Write failed! Duplicate username")

        else:
            print("Write failed! User identity could not be established!")


class Messages:
    """Handlers for the Messages table"""

    @classmethod
    def create_messages(cls, client):
        self = Messages()
        db = client.yellowjacket
        self.messages = db.messages
        self.messages.create_index("timestamp")
        self.messages.create_index("edit_timestamp")
        self.messages.create_index("sender_username")
        self.messages.create_index("editor_username")
        self.messages.create_index("current_text")
        self.messages.create_index("pre_edit_text")
        self.messages.create_index("pre_mutation_text")
        return self

    # Helpers start here
    async def locate_message(self, id: str) -> dict:
        """Locates the message given the message id"""
        message_data = await self.messages.find_one({"_id": id})
        return message_data

    async def show_table(self) -> None:
        """Shows the table. Useful for debugging"""
        cursor = self.messages.find({})
        async for document in cursor:
            pprint(document)

    async def drop_all(self) -> None:
        """Drops the table.

        Good for testing and
        being data efficient.
        """
        await self.messages.drop()
        print("Deletion successful!")

    async def add_message(self, current_text: str, sender_username: str) -> None:
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
        result = await self.messages.insert_one(message_data)
        return result.inserted_id

    async def edit_message(
        self, id: str, current_text: str, editor_username: str
    ) -> None:
        """Edits a single message.

        Records timestamp for the edit, swaps pre-
        and post-edit message states, and runs an
        update_one() operation.
        """
        message_data = await self.locate_message(id)
        edit_timestamp = time.time()
        pre_edit_text = message_data["current_text"]
        await self.messages.update_one(
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

    async def double_english(self):
        """Makes your english *sophisticated*"""
        await self.messages.update_many(
            {
                "current_text": {
                    "$regex": "^(.*?[\S]+or[\S]*.*?)|(.*?[\S]*or[\S]+.*?)$"
                }
            },  # noqa W605
            [
                {
                    "$set": {
                        "current_text": {
                            "$replaceAll": {
                                "input": "$current_text",
                                "find": "or",
                                "replacement": "ouur",
                            }
                        }
                    }
                }
            ],
        )


class Admin:
    """Handlers for the admin table."""

    @classmethod
    async def create_admin(cls, client):
        self = Admin()
        db = client.yellowjacket
        self.admin = db.admin
        self.admin.create_index("channel", unique=True)
        defaults = {
            "channel": "main",
            "randomize_username": False,
            "allow_edit_messages": False,
            "allow_edit_avatars": False,
            "sort_by_alpha": False,
            "double_english": False,
        }
        try:
            await self.admin.insert_one(defaults)
        except errors.DuplicateKeyError:
            print("Default already exists.")
        return self

    async def show_table(self) -> None:
        """Shows the table. Useful for debugging"""
        cursor = await self.admin.find({})
        for document in cursor:
            pprint(document)

    async def drop_all(self) -> None:
        """Drops the table.

        Good for testing and
        being data efficient.
        """
        await self.admin.drop()
        print("Deletion successful!")

    async def change_properties(
        self,
        properties: dict[str, bool],
        channel: str = "main",
    ) -> None:
        """Changes specified properties."""
        await self.admin.update_one({"channel": channel}, {"$set": properties})
        return await self.pull_table(channel)

    async def pull_table(self, channel: str = "main") -> dict[str, bool]:
        """Returns the table with the specified channel name."""
        return await self.admin.find_one({"channel": channel})

    async def add_permissions(
        self,
        channel: str,
        randomize_username: bool,
        allow_edit_messages: bool,
        allow_edit_avatars: bool,
        sort_by_alpha: bool,
        double_english: bool,
    ) -> None:
        """The create operation.

        Creates a new permission set as required.
        Note that channel names must be unique.
        """
        permissions = {
            "channel": channel,
            "randomize_username": randomize_username,
            "allow_edit_messages": allow_edit_messages,
            "allow_edit_avatars": allow_edit_avatars,
            "sort_by_alpha": sort_by_alpha,
            "double_english": double_english,
        }
        await self.admin.insert_one(permissions)

import asyncio
import os

import database
from database import Admin, Credentials, Messages
from motor import motor_asyncio

# Note: To run these tests,
# TODO: Get this file up to current standard for _database.py
# docker compose -f "docker-compose.dbtesting.yaml" up --build

# Testing for messages table
async def main():
    client = motor_asyncio.AsyncIOMotorClient(
        host=["database:27017"],
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
    )
    messages = Messages.create_messages(client)
    print("Old table")
    await messages.show_table()
    message_one = await messages.add_message("Hello world!", "cooltas")
    message_two = await messages.add_message("Watch me change this lol", "malitas")
    print("After two additions")
    await messages.show_table()
    await messages.edit_message(message_one, "Am dum", "malitas")
    await messages.edit_message(message_two, "I can do it too, ya dum dum!", "cooltas")
    print("After spicy edits")
    await messages.show_table()
    await messages.drop_all()
    print("Nothing should appear past this point!")
    await messages.show_table()

    # Testing for credentials table
    credentials = await Credentials.create_credentials(client)
    print("Old table")
    await credentials.show_table()
    await credentials.show_table()
    await credentials.save_credentials("objecttas", "some_stuff", "some_url")
    print("New table")
    await credentials.show_table()
    await credentials.change_password("objecttas", "some_password", "new_password")
    await credentials.change_password("objecttas", "some_stuff", "new_stuff")
    print("Table when password is changed")
    await credentials.show_table()
    print("Login successful:", await credentials.login("objecttas", "some_password"))
    print("Login successful:", await credentials.login("objecttas", "some_stuff"))
    print("Login successful:", await credentials.login("objecttas", "new_stuff"))
    credentials.change_avatar("objecttas", "cool_url")
    print("After avatar update:")
    await credentials.show_table()
    await credentials.change_username("objecttas", "new_stuff", "cooltas")
    print("After username update:")
    await credentials.show_table()
    await credentials.drop_all()
    await credentials.show_table()
    print("Nothing should appear after this point!")
    await credentials.show_table()

if(__name__=="__main__"):
    asyncio.run(main())
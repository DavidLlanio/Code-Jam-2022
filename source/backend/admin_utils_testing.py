import asyncio
import os

import admin_utils
import database
from motor import motor_asyncio

# Note: To run these tests,
# docker compose -f "docker-compose.admintesting.yaml" up --build


async def main():
    """Testing script"""
    client = motor_asyncio.AsyncIOMotorClient(
        host=["database:27017"],
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
    )
    settings = await admin_utils.Settings.create_table(client)
    print("Current table:")
    print(settings.return_channel_document())

    print("Changing properties")
    await settings.update_settings({"randomize_username": True})
    print("Post change:")
    print(settings.return_channel_document())
    messages = database.Messages.create_messages(client)
    await messages.add_message("Hello world", "abc")
    await messages.add_message("A or B", "pqr")
    await messages.add_message("It's an uncolored color", "abc")
    await messages.add_message("I'm a sophisticated brit and I say colour", "earlgrey")
    await messages.show_table()
    await messages.double_english()
    await messages.show_table()
    await messages.drop_all()


if __name__ == "__main__":
    asyncio.run(main())

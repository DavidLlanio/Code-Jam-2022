import admin_utils
import database

# Note: To run these tests,
# docker compose -f "docker-compose.admintesting.yaml" up --build

settings = admin_utils.Settings()
print("Current table:")
print(settings.return_channel_document())

print("Changing properties")
settings.update_settings({"randomize_username": True})
print("Post change:")
print(settings.return_channel_document())

messages = database.Messages()
messages.add_message("Hello world", "abc")
messages.add_message("A or B", "pqr")
messages.add_message("It's an uncolored color", "abc")
messages.add_message("I'm a sophisticated brit and I say colour", "earlgrey")
messages.double_english()
messages.show_table()

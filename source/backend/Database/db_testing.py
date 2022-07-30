from database import Admin, Credentials, Messages

# Note: To run these tests,
# TODO: Get this file up to current standard for _database.py
# docker compose -f "docker-compose.dbtesting.yaml" up --build

# Testing for messages table
messages = Messages.create_messages()
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
credentials = Credentials()
print("Old table")
credentials.show_table()
credentials.save_credentials("objecttas", "some_stuff", "some_url")
print("New table")
credentials.show_table()
credentials.change_password("objecttas", "some_password", "new_password")
credentials.change_password("objecttas", "some_stuff", "new_stuff")
print("Table when password is changed")
credentials.show_table()
print("Login successful:", credentials.login("objecttas", "some_password"))
print("Login successful:", credentials.login("objecttas", "some_stuff"))
print("Login successful:", credentials.login("objecttas", "new_stuff"))
credentials.change_avatar("objecttas", "cool_url")
print("After avatar update:")
credentials.show_table()
credentials.change_username("objecttas", "new_stuff", "cooltas")
print("After username update:")
credentials.show_table()
credentials.drop_all()
credentials.show_table()
print("Nothing should appear after this point!")
credentials.show_table()

# Testing for admin
admin = Admin()
print("Old table")
admin.show_table()
admin.change_property("double_english", True)
admin.change_property("randomize_username", True)
print("After perms change:")
admin.show_table()
admin.add_permissions(
    channel="fluff",
    randomize_username=True,
    allow_edit_messages=True,
    allow_edit_avatars=True,
    sort_by_alpha=True,
    double_english=True,
)
print("Post addition of fluff channel:")
admin.show_table()
admin.drop_all()
print("Nothing should appear beyond this point!")
admin.show_table()

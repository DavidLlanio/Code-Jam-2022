import admin_utils

settings = admin_utils.Settings()
print("Current table:")
print(settings.return_channel_document())

print("Changing properties")
settings.update_settings({"randomize_username": True})
print("Post change:")
print(settings.return_channel_document())

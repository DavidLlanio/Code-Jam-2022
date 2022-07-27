import admin_utils

# Note: To run these tests,
# docker compose -f "docker-compose.admintesting.yaml" up --build

settings = admin_utils.Settings()
print("Current table:")
print(settings.return_channel_document())

print("Changing properties")
settings.update_settings({"randomize_username": True})
print("Post change:")
print(settings.return_channel_document())

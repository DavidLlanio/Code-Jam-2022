from typing import List

import database

__all__: List[str] = ["Settings"]


class Settings(object):
    """Singleton object that stores and updates the administration settings"""

    def __new__(cls):
        """It's a singleton?"""
        if not hasattr(cls, "instance"):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """Gets the table as a dict from the db.

        Additional: Can pass a "channel" argument to it
        in the future so that you can choose which channel's
        settings you want to pull.
        """
        self.admin = database.Admin()
        self.admin_table = self.admin.pull_table()

    def return_channel_document(self) -> dict[str, bool]:
        """Returns the current admin_table."""
        return self.admin_table

    def return_frontend_settings(self) -> dict[str, bool]:
        """Retrieves the settings and remaps them to the frontend short names"""
        settings = self.admin_table
        settings_remap = {
            "randomize_username": "ai",
            "uep": "allow_edit_messages",
            "upep": "allow_edit_avatars",
            "as": "sort_by_alpha",
            "de": "double_english",
        }
        frontend_mapped_settings = {settings_remap[k]: settings[k] for k in settings}

        return frontend_mapped_settings

    def update_settings(self, settings_to_update: dict[str, bool]) -> None:
        """Edits the required properties"""
        self.admin_table = self.admin.change_properties(settings_to_update)

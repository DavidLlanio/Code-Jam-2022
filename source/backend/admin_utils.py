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

    def update_settings(self, settings_to_update: dict[str, bool]) -> None:
        """Edits the required properties"""
        self.admin_table = self.admin.change_properties(settings_to_update)

class Settings(object):
    """Singleton object that stores and updates the administration settings"""

    def __new__(cls):
        """It's a singleton?"""
        if not hasattr(cls, "instance"):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """On initialization, gets the settings from the database"""
        # TODO: get these from database
        self.randomize_username = False
        self.allow_edit_messages = False
        self.allow_edit_avatars = False

    def get_settings(self) -> dict[str, bool]:
        """Returns all the settings and their values in dictionary form"""
        return {
            "randomize_username": self.randomize_username,
            "allow_edit_messages": self.allow_edit_messages,
            "allow_edit_avatars": self.allow_edit_avatars,
        }

    def update_settings(self, settings_to_update: dict[str, bool]) -> None:
        """Given a dictionary of updated values, will update the settings and return the changed settings and values"""
        self.randomize_username = settings_to_update.get(
            "randomize_username", self.randomize_username
        )
        self.allow_edit_messages = settings_to_update.get(
            "allow_edit_messages", self.allow_edit_messages
        )
        self.allow_edit_avatars = settings_to_update.get(
            "allow_edit_avatars", self.allow_edit_avatars
        )

        # TODO: update database too!
        pass

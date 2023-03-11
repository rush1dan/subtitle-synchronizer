class Data:
    files = []
    on_data_registered = None

    SCREEN_RES_FACTOR = 1.0

    @classmethod
    def set_data(cls, files: list[str]):
        cls.files = files
        cls.on_data_registered(cls.files)
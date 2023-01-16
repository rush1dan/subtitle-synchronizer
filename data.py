class Data:
    files = []
    on_data_registered = None

    @classmethod
    def set_data(cls, files: list[str]):
        cls.files = files
        cls.on_data_registered(cls.files)
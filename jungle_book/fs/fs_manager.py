import os


class FileSystemManager:
    @staticmethod
    def remove(path):
        try:
            os.remove(path)
        except Exception as e:
            return e

    @staticmethod
    def path_exists(path):
        pass

    @staticmethod
    def create_path(user_id):
        pass

    @staticmethod
    def remove_path(user_id):
        pass

from abc import ABC


class User(ABC):
    """
    This is  an abstract class for the user class
    """
    def __init__(self, username, name, role, password):
        self.username = username
        self.name = name
        self.__password = password
        self.role = role 

    def login(self, username, password):
        pass

    def register(self, username, name, role, password):
        pass   

    def logout(self):
        pass

    def reset_password(self):
        pass

    def change_password(self):
        pass





from user import User

class NIMC():

  def __init__(self) -> None:
    self._count = 0
    self._users = {}

  def __str__(self):
    return "NIMC portal"

  def register_user(self, name:str, address:str="", state="", lga="", dob="", passport=""):
    self._count += 1
    user = User(name=name, nin=self._count, address=address, state=state, lga=lga, dob=dob, passport=passport)
    self._users[self._count] = user
    return user

  def get_user(self, nin) -> User|None:
    return self._users.get(nin)

  def get_nin(self, name) -> int|None:
    """ Returns first instance of user that matches given name"""
    for nin, user in self._users.items():
      if user.name == name:
        return nin
    return None

  def search_user_by_name(self, name) -> dict:
    """ Return dictionary of nin:user that matches the given name"""
    users = {}
    for nin, user in self._users.items():
      if name in user.name:
        users[nin] = user
    return users

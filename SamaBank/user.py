
class User():
  ''' User class for all users '''

  def __init__(self, name:str, nin:int, address:str="", state="", lga="", dob="", passport=""):
    self.name =  name
    self._nin = nin
    self.address = address
    self.state = state
    self.lga = lga
    self.dob = dob
    self.passport = passport

  def __str__(self):
    return f"Name: {self.name}; NIN: {self.nin}"
  
  def __hash__(self) -> int:
    return hash((self.nin,))
  
  def __eq__(self, __value: object) -> bool:
    return (isinstance(__value, type(self)) and (self.nin,) == (__value.nin,))

  @property
  def nin(self):
    return self._nin

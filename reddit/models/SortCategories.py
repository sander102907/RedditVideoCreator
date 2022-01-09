import enum
  
# creating enumerations using class
class SortCategories(enum.Enum):
    confidence = "confidence"
    controversial = "controversial"
    new = "new" 
    old = "old"
    q_and_a = "q&a"
    top = "top"

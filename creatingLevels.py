import Autodesk
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document

# strat transaction
t = Transaction(doc, "Create Grids")
t.Start()

# create an instance of a level
level_1 = Level.Create(doc, 3000/304.8)  

# access parameter DATUM_TEXT and set its value to a string
level_1_name = level_1.get_Parameter(BuiltInParameter.DATUM_TEXT)
level_1_name.Set("1 Etage")

# commit transaction
t.Commit()
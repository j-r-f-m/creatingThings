import Autodesk
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document

# create two points
p_1 = XYZ(0, 0, 0)
p_2 = XYZ(50, 0, 0)

# create a line between the two points
line_1 = Line.CreateBound(p_1, p_2)

# strat transaction
t = Transaction(doc, "Create Grids")
t.Start()

# create a grid
grid_1 = Grid.Create(doc, line_1)

"""
Define name of created grid by accessing the the parameter DATUM_TEXT and then
setting its value to a string
"""
name = grid_1.get_Parameter(BuiltInParameter.DATUM_TEXT)
name.Set("A")

# commit transaction
t.Commit()

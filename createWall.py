
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *


uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# get all OST_Levels in the document
levels = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

walls = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements()

# iterate thorugh the levels array and find the level with elevation = 0.0
for level in levels:
    elevation = level.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
    if elevation == 0.0:
        # variable gets defined in a loop
        level_id = level.Id
        level_elevation = level.Elevation
        break

for wall in walls:
    if wall.Name == 'STB 200':
        wall_type_id = wall.Id
        break

# points for curve
p_1 = XYZ(0, 0, level_elevation)
p_2 = XYZ(50, 0, level_elevation)

print(p_1)

# create Line
line_1 = Line.CreateBound(p_1, p_2)

# Start a new transaction
t = Transaction(doc, "Create column")
t.Start()

# Create a new family instance
new_wall = Wall.Create(
    doc, line_1, level_id, True)

# Commit the transaction
t.Commit()

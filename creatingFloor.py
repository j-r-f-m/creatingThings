""
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')



from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *
from Autodesk.Revit.DB import CurveLoop
from System.Collections.Generic import List

# get the current Revit application and document
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# get all OST_Levels in the document
levels = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

# get all floor types in the document
floor_types = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Floors).WhereElementIsElementType().ToElements()

# points for slab
p_1 = XYZ(0, 0, 0)
p_2 = XYZ(10, 0, 0)
p_3 = XYZ(10, 10, 0)
p_4 = XYZ(0, 10, 0)

# lines for slab
line_1 = Line.CreateBound(p_1, p_2)
line_2 = Line.CreateBound(p_2, p_3)
line_3 = Line.CreateBound(p_3, p_4)
line_4 = Line.CreateBound(p_4, p_1)


# iterate thorugh the levels array and find the level with elevation = 0.0
for level in levels:
    elevation = level.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
    if elevation == 0.0:
        # variable gets defined in a loop
        level_id = level.Id
        break

print(level_id)

slab_type_id = None
# iterate through the floor collector and find the desired floor type
for type in floor_types:
    # get the name of the current type
    if type.Name == 'STB 200':
        slab_type_id = type.Id
        break


print("slab_type_id")
print(slab_type_id)

# create a curve loop
curveLoop = CurveLoop()
print(curveLoop)

curveLoop.Append(line_1)
curveLoop.Append(line_2)
curveLoop.Append(line_3)
curveLoop.Append(line_4)

print(curveLoop)

# create an IList[CurveLoop] for the floor boundary
floorBoundary = List[CurveLoop]()
floorBoundary.Add(curveLoop)

print(floorBoundary)

# # Start a new transaction
t = Transaction(doc, "Create column")
t.Start()

floor = Floor.Create(doc, floorBoundary, slab_type_id, level_id)


# Commit the transaction
t.Commit()
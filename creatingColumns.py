
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')



from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *


uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# initialize variable that will hold the column family symbol
column_family_symbol = None

# get all family symbols in the document
collector = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()

# for element in collector:
#     print(f"Family: {element.Family.Name}, Symbol: {element.Name}")

 # iterate through the collector and find the desired column family symbol
for element in collector:
    if element.Family.Name == 'STB Stütze - rechteckig' and element.Name == 'STB 200 x 200':
        column_family_symbol = element
        break

print("element: ", column_family_symbol.Family.Name)

if column_family_symbol is None:
    TaskDialog.Show('Revit', 'Column family symbol not found')
    exit()

# get all OST_Levels in the document
levels = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

# iterate thorugh the levels array and find the level with elevation = 0.0
for level in levels:
    elevation = level.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsDouble()
    if elevation == 0.0:
        # variable gets defined in a loop
        level_0 = level

print(level_0.Elevation)


# Start a new transaction
t = Transaction(doc, "Create column")
t.Start()

# Activate the column family symbol
column_family_symbol.Activate()

# define the location of the new column as x=0, y=0, z=level_0.Elevation
location = XYZ(0, 0, level_0.Elevation)
# Create a new family instance
new_column = doc.Create.NewFamilyInstance(
    location, column_family_symbol, level_0, StructuralType.Column)

# Commit the transaction
t.Commit()

"""
Select a wall and create a rebar
"""
# Follow this tutorial: https://www.youtube.com/watch?v=Iqp9e4oAvh8

import Autodesk

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Structure import Rebar, RebarBarType, RebarHookType, RebarStyle, RebarHookOrientation

# get the current Revit application and document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collect all RebarBarType elements in the document
collector = FilteredElementCollector(doc).OfClass(RebarBarType).ToElements()

bar_type = None
# You can loop through this list to find a specific RebarBarType
for rebar_type in collector:
    if rebar_type.Name == "ø10, Dmin=4ϕ":
        bar_type = rebar_type
        break
print("bar_type: ", bar_type.Name)

#hide current script window
__window__.Hide()

# get reference to current selection
sel = uidoc.Selection.PickObject(Selection.ObjectType.Element,"Select an element")
# get element from reference
wall = doc.GetElement(sel)

# show current script window
__window__.Show()
__window__.Topmost = True

# print("selected element")

# get the location curve of the wall
curve = wall.Location.Curve
# get the start point of the curve (x, y, z)
p_1 = curve.GetEndPoint(0)
# get the end point of the curve in foot
p_2 = curve.GetEndPoint(1)

print(p_1)
print(p_2)

# get the direction of the wall
direction_y = curve.Direction
# get the direction of the wall in x
direction_x = direction_y.CrossProduct(XYZ.BasisZ).Normalize()

print(direction_y)
print(direction_x)

# get start and end points of the rebar
rebar_p_1 = p_1
rebar_p2 = XYZ(p_1.X, p_1.Y, p_1.Z + 3000/304.8)
print(rebar_p2)

# create a line from the start and end points of the rebar
lines = [Line.CreateBound(rebar_p_1, rebar_p2)]
print(lines)

t = Transaction(doc, "selection")
t.Start()
#
rebar = Structure.Rebar.CreateFromCurves(doc, Structure.RebarStyle.Standard, bar_type, None, None, wall, direction_y, lines, Structure.RebarHookOrientation.Left,Structure.RebarHookOrientation.Left, True, True)
t.Commit()
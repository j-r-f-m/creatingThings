"""
Select a wall and create a rebar
"""
# Follow this tutorial: https://www.youtube.com/watch?v=Iqp9e4oAvh8

import Autodesk

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Structure import Rebar, RebarBarType, RebarHookType, RebarStyle, RebarHookOrientation

def new_point(p_1, x, y, z, x_dir, y_dir) :
    new_point_1 = p_1 + x * x_dir
    new_point_2 = new_point_1 + y * y_dir
    return(XYZ(new_point_2.X, new_point_2.Y, new_point_2.Z + z))

# get the current Revit application and document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collect all RebarBarType elements in the document
collector = FilteredElementCollector(doc).OfClass(RebarBarType).ToElements()

# get desired rebar type from collector
bar_type = None
for rebar_type in collector:
    if rebar_type.Name == "ø10, Dmin=4ϕ":
        bar_type = rebar_type
        break
# print("bar_type: ", bar_type.Name)

#hide current script window
__window__.Hide()

# get reference to current selection
sel = uidoc.Selection.PickObject(Selection.ObjectType.Element,"Select an element")
# get element from reference
wall = doc.GetElement(sel)
# get the type id of the wall
type_id = wall.GetTypeId()
type = doc.GetElement(type_id)
w_width = type.Width

w_height = wall.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM).AsDouble()

print("w_width: ", w_width)
print("type_id: ", type_id)
print("type: ", type)

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

cc_ext = doc.GetElement(wall.get_Parameter(BuiltInParameter.CLEAR_COVER_EXTERIOR).AsElementId()).CoverDistance
cc_int = doc.GetElement(wall.get_Parameter(BuiltInParameter.CLEAR_COVER_INTERIOR).AsElementId()).CoverDistance


# get the direction of the wall
direction_y = curve.Direction
print("direction_y: ", direction_y)
# get the direction of the wall in x
direction_x = direction_y.CrossProduct(XYZ.BasisZ).Normalize()
print("direction_x: ", direction_x)

# p_1_new = p_1 + w_width/2*direction_x

# get the diameter of the rebar
rebar_diameter = bar_type.get_Parameter(BuiltInParameter.REBAR_BAR_DIAMETER).AsDouble()
print("rebar_diameter: ", rebar_diameter)

x_offset = w_width/2 - cc_ext - rebar_diameter/2
y_offset = 50/304.8



# print(direction_y)
# print(direction_x)

# Vertical rebar
# get start and end points of the rebar
rebar_p_1 = new_point(p_1, x_offset, y_offset, 0, direction_x, direction_y)
rebar_p2 = new_point(rebar_p_1,0,0,w_height + 1000/304.8, direction_x, direction_y)

# create a line from the start and end points of the rebar
lines = [Line.CreateBound(rebar_p_1, rebar_p2)]
# print(lines)

# Horizontal rebar
# horizontal_x_offset = w_width/2 - cc_ext - rebar_diameter/2
# horizontal_rebar_p1 = new_point
# lines_horizontal = [Line.CreateBound(rebar_p_1, rebar_p2)]

# Vertical rebar layout rule:
step = 100/304.8
length = p_1.DistanceTo(p_2)
count = length / step

t = Transaction(doc, "selection")
t.Start()
#
rebar = Structure.Rebar.CreateFromCurves(doc, Structure.RebarStyle.Standard, bar_type, None, None, wall, direction_y, lines, Structure.RebarHookOrientation.Left,Structure.RebarHookOrientation.Left, True, True)

rebar.get_Parameter(BuiltInParameter.REBAR_ELEM_LAYOUT_RULE).Set(3)
rebar.get_Parameter(BuiltInParameter.REBAR_ELEM_BAR_SPACING).Set(step)
rebar.get_Parameter(BuiltInParameter.REBAR_ELEM_QUANTITY_OF_BARS).Set(count)
rebar.GetShapeDrivenAccessor().BarsOnNormalSide = True

# rebar_horizontal = Structure.Rebar.CreateFromCurves(doc, Structure.RebarStyle.Standard, bar_type, None, None, wall, direction_x, lines, Structure.RebarHookOrientation.Left,Structure.RebarHookOrientation.Left, True, True)

t.Commit()
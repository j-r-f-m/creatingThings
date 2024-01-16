"""
This script is used to select an element and change ID-Kommentare  value.
"""

#https://www.youtube.com/watch?v=Iqp9e4oAvh8

import Autodesk

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Structure import Rebar, RebarBarType, RebarHookType, RebarStyle, RebarHookOrientation

# get the current Revit application and document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

collector = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()

# for element in collector:
#     print(f"Family: {element.Family.Name}, Symbol: {element.Name}")

 # iterate through the collector and find the desired column family symbol
for element in collector:
    if element.Family.Name == 'Gerader Stab' and element.Name == 'Gerader Stab':
        reabr_family_symbol = element
        break

print("element: ", reabr_family_symbol.Family.Name)



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

curve = wall.Location.Curve
p_1 = curve.GetEndPoint(0)
p_2 = curve.GetEndPoint(1)

direction_y = curve.Direction
direction_x = direction_y.CrossProduct(XYZ.BasisZ).Normalize()

print(direction_y)
print(direction_x)

# print(curve)
# print(p_1)  
# print(p_2)  

# with Transaction(doc, "Reinforce") as t:
#     t.Start()
#     rebar = Structure.Rebar.CreateFromCurves(doc, Structure.RebarStyle.Standard, bar_type, None, None, wall, direction_y, lines, Structure.RebarHookOrientation.Left, True, True)
#     t.Commit()
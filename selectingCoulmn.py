from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB.Structure import Rebar,RebarBarType, RebarStyle, RebarHookOrientation
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, BuiltInCategory, TransactionGroup

# select column
def pickobject():
    from Autodesk.Revit.UI.Selection import ObjectType
    __window__.Hide()
    ref = uidoc.Selection.PickObject(ObjectType.Element)
    column = doc.GetElement(ref.ElementId)
    __window__.Show()
    __window__.Topmost = True
    return column

column = pickobject()

print("Selected column")
print(column)





from Autodesk.Revit.DB import Transaction, FamilySymbol
from Autodesk.Revit.DB.Structure import Rebar, RebarBarType, RebarStyle, RebarHookOrientation
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, BuiltInCategory, TransactionGroup

from Autodesk.Revit.DB import XYZ
from Autodesk.Revit.DB.Structure import Rebar

def create_rebar(doc, wall, bar_shape, bar_type):
    new_rebars = []

    bar = Rebar.CreateFromRebarShape(doc, bar_shape, bar_type, wall, XYZ(2, 0, 2), XYZ(1, 0, 0), XYZ(0, 0, 1))
    # call regenerate so that the TotalLength will be calculated before the transaction is committed
    doc.Regenerate()
    new_rebars.append(bar)

    # add a second bar adjacent to the first one
    bar_length = bar.TotalLength
    bar = Rebar.CreateFromRebarShape(doc, bar_shape, bar_type, wall, XYZ(2 + bar_length, 0, 2), XYZ(1, 0, 0), XYZ(0, 0, 1))
    new_rebars.append(bar)

    return new_rebars

rebar_family_symbol = None

# Get all RebarBar Families in the document
collector = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()


# Find the desired RebarShape
for element in collector:
    print("Family.Name: ", element.Family.Name, "Name: ", element.Name)
    if element.Family.Name == 'Bügel Geschlossen' and element.Name == 'Bügel Geschlossen':
        rebar_family_symbol = element
        break

print("rebar_family_symbol: ", rebar_family_symbol)


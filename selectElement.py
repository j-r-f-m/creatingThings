"""
This script is used to select an element and change ID-Kommentare  value.
"""

import Autodesk

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# get the current Revit application and document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# hide current script window
__window__.Hide()

# get reference to current selection
sel = uidoc.Selection.PickObject(Selection.ObjectType.Element,"Select an element")
# get element from reference
el = doc.GetElement(sel)

# show current script window
__window__.Show()
__window__.Topmost = True


# debug
print("continue")

t = Transaction(doc, "selection")
t.Start()

# get parameter you want to set
par1 = el.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
# INPUT VALUE you want to set
# set value for previously selected parameter
par1.Set("halsdsddslo")

t.Commit()
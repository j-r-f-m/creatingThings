
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')



from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *


uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

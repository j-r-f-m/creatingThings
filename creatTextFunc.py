from Autodesk.Revit.DB import XYZ, FilteredElementCollector, BuiltInCategory, Line
from Autodesk.Revit.DB.Structure import Rebar, RebarBarType, RebarStyle, RebarHookOrientation

# Get the first column in the document
column = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).FirstElement()

# Get the first RebarBarType in the document
bar_type = FilteredElementCollector(doc).OfClass(RebarBarType).FirstElement()

# Define the rebar shape
start_point = XYZ(0, 0, 0)
end_point = XYZ(0, 0, 1)  # Change this to match the height of your column
curve = Line.CreateBound(start_point, end_point)

# Create the rebar
rebar = Rebar.CreateFromCurvesAndShape(doc, RebarStyle.Standard, bar_type, None, None, column, XYZ(0, 0, 1), [curve], RebarHookOrientation.Right, RebarHookOrientation.Right)
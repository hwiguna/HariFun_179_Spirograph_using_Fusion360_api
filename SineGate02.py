import adsk
from math import sin, cos, pi

def main():
    # create a new sketch on the xy plane
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent  # get the root component of the active design.
    sketches = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    # Compute a circle by hand so we could create a plane at each point
    segments = 60
    path_max_angle = 2*pi
    path_radius = 2000
    path_points = adsk.core.ObjectCollection.create()

    wave_max_angle = path_max_angle * 8
    wave_base_height = 300
    wave_height = 100

    for seg in range(segments):
        path_angle = seg * path_max_angle / segments
        x = cos(path_angle) * path_radius
        y = sin(path_angle) * path_radius

        path_point = adsk.core.Point3D.create(x, y, 0)
        path_points.add(path_point)

    # Create a construction plane at each path point
    splines = sketch.sketchCurves.sketchFittedSplines
    myPath = splines.add(path_points)

    # === Create construction plane input ===
    construction_planes = rootComp.constructionPlanes
    for seg in range(segments):
        planeInput = construction_planes.createInput()    # build input parameters for creating the construction plane
        distance = adsk.core.ValueInput.createByReal(seg/(segments-1))
        planeInput.setByDistanceOnPath(myPath, distance)  # Add construction plane by distance on path
        myPlane = construction_planes.add(planeInput)

        # compute wave height at each segment
        wave_angle = seg * wave_max_angle / segments
        myRadius = wave_base_height + sin(wave_angle) * wave_height

        # Create a sketch on the newly created construction plane
        mySketch = sketches.add(myPlane) # create the sketch
        circles = mySketch.sketchCurves.sketchCircles # no circles yet on this new sketch
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        circle1 = circles.addByCenterRadius(centerPoint, myRadius)  # add circle onto our sketch
        circle2 = circles.addByCenterRadius(centerPoint, myRadius-50)  # add smaller circle

        prof = mySketch.profiles.item(0)  # Get the profile defined by the circle
        # Create an extrusion input

        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(5)  # Define that the extent is a distance extent of 5 cm
        extInput.setDistanceExtent(True, distance)  # Set the distance extent to be symmetric
        extInput.isSolid = True  # Set the extrude to be a solid one
        extrude = extrudes.add(extInput)  # Create an cylinder

main()

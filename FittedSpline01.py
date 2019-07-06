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

    # Spirograph math stolen from: https://www.101computing.net/python-turtle-spirograph/
    R, r, d = 125, 75, 125
    theta = 0.2
    steps = int(6*pi/theta)
    angle = 0

    points = adsk.core.ObjectCollection.create()
    for t in range(steps):
        angle += theta
        x = (R - r)*cos(angle) + d * cos(((R-r)/r)*angle)
        y = (R - r)*sin(angle) - d * sin(((R-r)/r)*angle)
        point = adsk.core.Point3D.create(x, y, 0)
        points.add(point)

    # connect start and end
    first = points[0]
    points.add(first)

    # Turn those points into fitted spline
    splines = sketch.sketchCurves.sketchFittedSplines
    splines.add(points)

main()

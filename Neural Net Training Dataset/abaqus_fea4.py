# -*- coding: utf-8 -*-
"""
Python script to run abaqus analysis (Draft 4)

@author: roshan94
"""
# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=253.52082824707, 
    height=157.929397583008)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
import sys
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()
#: A new model database has been created.
#: The model "Model-1" has been created.

buckling_load_e1 = []
buckling_load_e2 = []
buckling_load_e3 = []

### Printing function
def log(print_str):
    print >> sys.stdout, print_str
    
#sys.stdout.write(sys.argv[1])
#current_fibre_radius = float(sys.argv[-3]) # in mm
#current_fibre_angle = float(sys.argv[-2]) # in degrees
#current_matrix_E = float(sys.argv[-1]) # in N/mm^2
current_fibre_radius = 65
current_fibre_angle = 30
current_matrix_E = 1.5e5

log('Starting Abaqus Job')

### Creating the parts
## Create Matrix
session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-15.0, 15.0), point2=(15.0, -15.0))
s.ObliqueDimension(vertex1=v[3], vertex2=v[0], textPoint=(9.36742401123047, 
    22.3940620422363), value=3048.0)
s.ObliqueDimension(vertex1=v[2], vertex2=v[3], textPoint=(36.8749465942383, 
    -12.0127124786377), value=3048.0)
s.Spot(point=(0.0, 0.0))
s.Spot(point=(-1524.0, 1524.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=5745.18, 
    farPlane=5920.27, width=505.976, height=227.728, cameraPosition=(-45.3815, 
    43.5995, 5832.72), cameraTarget=(-45.3815, 43.5995, 0))
s.move(vector=(1524.0, -1524.0), objectList=(g[2], g[3], g[4], g[5], v[4], 
    v[5]))
session.viewports['Viewport: 1'].view.setValues(nearPlane=3578.35, 
    farPlane=8087.09, width=14745.9, height=6636.78, cameraPosition=(-659.72, 
    724.541, 5832.72), cameraTarget=(-659.72, 724.541, 0))
p = mdb.models['Model-1'].Part(name='matrix', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['matrix']
p.BaseSolidExtrude(sketch=s, depth=254.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['matrix']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
# Datum Points for Assembly
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(0.0, 0.0, 127.0))
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(-508.0, 508.0, 127.0))
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(508.0, -508.0, 127.0))
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(-1016.0, 1016.0, 127.0))
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(1016.0, -1016.0, 127.0))

## Create Fibre
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(18.75, -1.25))
s1.RadialDimension(curve=g[2], textPoint=(28.1022720336914, 10.0847473144531), 
    radius=current_fibre_radius)
session.viewports['Viewport: 1'].view.setValues(nearPlane=131.322, 
    farPlane=245.801, width=330.823, height=148.896, cameraPosition=(-29.1353, 
    14.7041, 188.562), cameraTarget=(-29.1353, 14.7041, 0))
p = mdb.models['Model-1'].Part(name='fibre', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['fibre']
p.BaseSolidExtrude(sketch=s1, depth=4310.0)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
# Datum Point for Assembly
p = mdb.models['Model-1'].parts['fibre']
p.DatumPointByCoordinate(coords=(0.0, 0.0, 2155.0))

### Assembly
## Adding Matrix
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['matrix']
a.Instance(name='matrix-1', part=p, dependent=ON)

## Appending Fibre 1
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-1', part=p, dependent=ON)
p1 = a.instances['fibre-1']
p1.translate(vector=(1629.0, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 10.0, 0.0), angle=90.0)
#: The instance fibre-1 was rotated by 90. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 10., 0.
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 0.0, 10.0), angle=current_fibre_angle)
#: The instance fibre-1 was rotated by "current_fibre_angle". degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-1', ), vector=(-2781.272655, -220.05722, 
    1756.0))
#: The instance fibre-1 was translated by -2.781272655E+03, -220.05722, 1.756E+03 with respect to the assembly coordinate system

## Appending Fibre 2
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-2', part=p, dependent=ON)
p1 = a.instances['fibre-2']
p1.translate(vector=(1629.0, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 10.0, 0.0), angle=90.0)
#: The instance fibre-2 was rotated by 90. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 10., 0.
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 0.0, 10.0), angle=current_fibre_angle)
#: The instance fibre-2 was rotated by "current_fibre_angle". degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-2', ), vector=(-2273.272655, -728.05722, 
    1756.0))
#: The instance fibre-2 was translated by -2.273272655E+03, -728.05722, 1.756E+03 with respect to the assembly coordinate system

## Appending Fibre 3
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-3', part=p, dependent=ON)
p1 = a.instances['fibre-3']
p1.translate(vector=(1629.0, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-3', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 10.0, 0.0), angle=90.0)
#: The instance fibre-3 was rotated by 90. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 10., 0.
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-3', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 0.0, 10.0), angle=current_fibre_angle)
#: The instance fibre-3 was rotated by "current_fibre_angle". degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-3', ), vector=(-1765.272655, -1236.05722, 
    1756.0))
#: The instance fibre-3 was translated by -1.765272655E+03, -1.23605722E+03, 1.756E+03 with respect to the assembly coordinate system

## Appending Fibre 4
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-4', part=p, dependent=ON)
p1 = a.instances['fibre-4']
p1.translate(vector=(1898.29088861188, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-4', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 10.0, 0.0), angle=90.0)
#: The instance fibre-4 was rotated by 90. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 10., 0.
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-4', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 0.0, 10.0), angle=current_fibre_angle)
#: The instance fibre-4 was rotated by "current_fibre_angle". degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-4', ), vector=(-1257.272655, -1744.05722, 
    2025.290889))
#: The instance fibre-4 was translated by -1.257272655E+03, -1.74405722E+03, 2.025290889E+03 with respect to the assembly coordinate system

## Appending Fibre 5
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-5', part=p, dependent=ON)
p1 = a.instances['fibre-5']
p1.translate(vector=(2406.29088861188, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-5', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 10.0, 0.0), angle=90.0)
#: The instance fibre-5 was rotated by 90. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 10., 0.
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-5', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 0.0, 10.0), angle=current_fibre_angle)
#: The instance fibre-5 was rotated by "current_fibre_angle". degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-5', ), vector=(-749.272655, -2252.05722, 
    2533.290889))
#: The instance fibre-5 was translated by -749.272655, -2.25205722E+03, 2.533290889E+03 with respect to the assembly coordinate system

## Merging Matrix and Fibres
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanMerge(name='Part-1', instances=(a.instances['matrix-1'], 
    a.instances['fibre-1'], a.instances['fibre-2'], a.instances['fibre-3'], 
    a.instances['fibre-4'], a.instances['fibre-5'], ), keepIntersections=ON, 
    originalInstances=SUPPRESS, mergeNodes=BOUNDARY_ONLY, 
    nodeMergingTolerance=1e-06, domain=BOTH)

### Cutting Overhanging Fibre Material from Merged Part
## Cutting from face 1
p = mdb.models['Model-1'].parts['fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[38], sketchUpEdge=e[30], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-10.062224, 1509.0, 
    127.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=6117.13, gridSpacing=152.92, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.rectangle(point1=(-879.29, 1605.66), point2=(802.83, -1567.43))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[38], sketchUpEdge=e1[30], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Cutting from face 2
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[31], sketchUpEdge=e[18], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(1539.0, -35.881674, 
    127.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
s1.rectangle(point1=(-917.575, 1565.275), point2=(701.675, -1619.25))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[31], sketchUpEdge=e1[18], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Cutting from face 3
session.viewports['Viewport: 1'].view.setValues(nearPlane=11490.5, 
    farPlane=20076.5, width=11511.2, height=4873.6, cameraPosition=(3936.43, 
    -13126.3, 8292.81), cameraUpVector=(-0.104367, 0.791882, 0.60169), 
    cameraTarget=(-14.5129, -880.954, -21.635))
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[26], sketchUpEdge=e[19], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(46.361314, -1539.0, 
    127.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.rectangle(point1=(-809.625, 1565.275), point2=(863.6, -1565.275))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[26], sketchUpEdge=e1[19], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Cutting from face 4
session.viewports['Viewport: 1'].view.setValues(nearPlane=11129, 
    farPlane=20103.3, width=11149.1, height=4720.29, cameraPosition=(-13581.8, 
    -6705.38, 5785.8), cameraUpVector=(0.0988019, 0.940857, 0.324077), 
    cameraTarget=(-856.524, -572.334, -142.134))
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[23], sketchUpEdge=e[20], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-1509.0, 1.228855, 
    127.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
s1.rectangle(point1=(-755.65, 1565.275), point2=(701.675, -1619.25))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[23], sketchUpEdge=e1[20], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

### Assigning Materials and Sections
## Creating Matrix Material
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='matrix_material')
mdb.models['Model-1'].materials['matrix_material'].Elastic(table=((current_matrix_E, 
    0.29), ))

## Creating Fibre Material
mdb.models['Model-1'].Material(name='fibre_material')
mdb.models['Model-1'].materials['fibre_material'].Elastic(table=((121000.0, 
    0.34), ))

## Creating Matrix Section
mdb.models['Model-1'].HomogeneousSolidSection(name='matrix_section', 
    material='matrix_material', thickness=None)

## Creating Fibre Section
mdb.models['Model-1'].HomogeneousSolidSection(name='fibre_section', 
    material='fibre_material', thickness=None)

## Assigning Matrix Section to Matrix Set
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
region = p.Set(cells=cells, name='matrix_set')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='matrix_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning Fibre Section to Fibre Set 1
session.viewports['Viewport: 1'].view.setValues(nearPlane=13027.5, 
    farPlane=19297.3, width=7029.51, height=2976.14, viewOffsetX=-207.243, 
    viewOffsetY=528.253)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
region = p.Set(cells=cells, name='fibre_set1')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning Fibre Section to Fibre Set 2
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
region = p.Set(cells=cells, name='fibre_set2')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning Fibre Section to Fibre Set 3
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
region = p.Set(cells=cells, name='fibre_set3')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning Fibre Section to Fibre Set 4
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='fibre_set4')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning Fibre Section to Fibre Set 5
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
region = p.Set(cells=cells, name='fibre_set5')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

### Creating Linear Buckling Step
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
mdb.models['Model-1'].BuckleStep(name='Step-1', previous='Initial', numEigen=3, 
    vectors=6, maxIterations=300)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

### Creating Constraint Surface Pin Sets
## Creating Reference Points 
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON, 
    adaptiveMeshConstraints=OFF)
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(0.0, 1524.0, 127.0))
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(0.0, -1524.0, 127.0))

## Creating Top Surface Pin Set
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#40000 ]', ), )
region3=a.Set(faces=faces1, name='top_pin_set')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[16], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-1', refPointRegion=region1, 
    pinRegion=region3)

## Creating Bottom Surface Pin Set
session.viewports['Viewport: 1'].view.setValues(nearPlane=14661.7, 
    farPlane=23696.2, width=15624.5, height=6615.05, cameraPosition=(4266.82, 
    -16316.2, 9388.7), cameraUpVector=(0.568767, 0.744704, 0.349169), 
    cameraTarget=(-389.497, -1714.94, 2052.51))
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#10000 ]', ), )
region3=a.Set(faces=faces1, name='bottom_surface_pin')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[17], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-2', refPointRegion=region1, 
    pinRegion=region3)

### Creating Boundary Conditions
## Creating Bottom Surface Encastre Condition
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, interactions=OFF, constraints=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14180.4, 
    farPlane=23531.2, width=15111.6, height=6397.9, cameraPosition=(12697.6, 
    12406.3, 6645.03), cameraUpVector=(-0.875513, 0.480346, -0.0523921), 
    cameraTarget=(572.234, 1561.54, 1739.53))
session.viewports['Viewport: 1'].view.setValues(nearPlane=14212.9, 
    farPlane=23096.8, width=15146.3, height=6412.58, cameraPosition=(8810.89, 
    -13600.5, 9493.01), cameraUpVector=(0.371645, 0.879971, 0.295857), 
    cameraTarget=(187.872, -1010.31, 2021.17))
a = mdb.models['Model-1'].rootAssembly
region = a.sets['bottom_surface_pin']
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1', 
    region=region, localCsys=None)

## Creating Top Surface Displacement Condition
session.viewports['Viewport: 1'].view.setValues(nearPlane=14099.7, 
    farPlane=23246.8, width=15025.7, height=6361.53, cameraPosition=(12228.2, 
    12636.1, 6570.9), cameraUpVector=(-0.854548, 0.475213, -0.209573), 
    cameraTarget=(492.649, 1329.64, 1760.56))
a = mdb.models['Model-1'].rootAssembly
region = a.sets['top_pin_set']
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', 
    region=region, u1=0.0, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, buckleCase=PERTURBATION_AND_BUCKLING, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

### Creating Load
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#40000 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='top_surface')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=1.0)

### Meshing 
## Assigning Mesh Elements to Matrix
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
    bcs=OFF, predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#20 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Assigning Mesh Elements to Fibre 1
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#4 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Assigning Mesh Elements to Fibre 2
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#8 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Assigning Mesh Elements to Fibre 3
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#10 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Assigning Mesh Elements to Fibre 4
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Assigning Mesh Elements to Fibre 5
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#2 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Meshing the comoposite
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=240.0, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()

### Create, verify and submit job
## Create Parallelized Job
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.Job(name='Buckling_Job', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
    numDomains=4, numGPUs=0)

## Perform Data Check
mdb.jobs['Buckling_Job'].submit(consistencyChecking=OFF, datacheckJob=True)
#: Abaqus Warning: The following input options are not supported by parallel execution of element operations: buckle. Only the solver will be executed in parallel for this analysis.
#: The job input file "Buckling_Job.inp" has been submitted for analysis.
#: Job Buckling_Job: Analysis Input File Processor completed successfully.
#: Job Buckling_Job: Abaqus/Standard completed successfully.
#: Job Buckling_Job completed successfully. 

## Submit Job and wait for completion
mdb.jobs['Buckling_Job'].submit(consistencyChecking=OFF)
#: Abaqus Warning: The following input options are not supported by parallel execution of element operations: buckle. Only the solver will be executed in parallel for this analysis.
#: The job input file "Buckling_Job.inp" has been submitted for analysis.
#: Job Buckling_Job: Analysis Input File Processor completed successfully.
#: Job Buckling_Job: Abaqus/Standard completed successfully.
#: Job Buckling_Job completed successfully. 
mdb.jobs['Buckling_Job'].waitForCompletion()

## Visualize Results
#o3 = session.openOdb(name='C:/temp/Buckling_Job.odb')
#: Model: C:/temp/Buckling_Job.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             2
#: Number of Element Sets:       10
#: Number of Node Sets:          15
#: Number of Steps:              1
#session.viewports['Viewport: 1'].setValues(displayedObject=o3)
#session.viewports['Viewport: 1'].makeCurrent()
#session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
#    CONTOURS_ON_DEF, ))
#session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
#session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )

## Extract and Store Eigenvalues
print('Extracting and Storing Eigenvalues')
o1 = visualization.openOdb('Buckling_Job.odb')
Step = o1.steps['Step-1']
for i_frame in Step.frames:
    if (i_frame == 1):
        Mode_desc = i_frame.description
        Eigenval_pos = Mode_desc.find('EigenValue') + 13
        Eigenval_str = Mode_desc[Eigenval_pos:]
        buckling_load_e1.append(Eigenval_str)
    elif (i_frame == 2):
        Mode_desc = i_frame.description
        Eigenval_pos = Mode_desc.find('EigenValue') + 13
        Eigenval_str = Mode_desc[Eigenval_pos:]
        buckling_load_e2.append(Eigenval_str)
    elif (i_frame == 3):
        Mode_desc = i_frame.description
        Eigenval_pos = Mode_desc.find('EigenValue') + 13
        Eigenval_str = Mode_desc[Eigenval_pos:]
        buckling_load_e3.append(Eigenval_str)
o1.close()
print('Eigenvalues stored....')

log('Eigen Value One: ' + str(buckling_load_e1) + 'Endone, Eigen Value Two: ' + str(buckling_load_e2) + 'Endtwo, Eigen Value Three: ' + str(buckling_load_e3) + ' Endthree')


# -*- coding: utf-8 -*-
"""
Python script to run abaqus analysis (Draft 3)

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
import visualization
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
    
sys.stdout.write(sys.argv[1])
current_fibre_radius = float(sys.argv[-3]) # in mm
current_fibre_angle = float(sys.argv[-2]) # in degrees
current_matrix_E = float(sys.argv[-1]) # in N/mm^2

#log('Starting Sketch')
### Sketching parts
## Sketching matrix
session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-20.0, 15.0), point2=(20.0, -15.0))
s.ObliqueDimension(vertex1=v[3], vertex2=v[0], textPoint=(8.62397766113281, 
    19.872875213623), value=3048.0)
s.ObliqueDimension(vertex1=v[2], vertex2=v[3], textPoint=(33.3064041137695, 
    -1.18644332885742), value=3048.0)
session.viewports['Viewport: 1'].view.setValues(nearPlane=3780.32, 
    farPlane=7891.7, width=13446.3, height=6051.88, cameraPosition=(-2902.8, 
    1898.12, 5836.01), cameraTarget=(-2902.8, 1898.12, 0))
s.Spot(point=(-1524.0, 1524.0))
s.move(vector=(1524.0, -1524.0), objectList=(g[2], g[3], g[4], g[5], v[4]))
session.viewports['Viewport: 1'].view.setValues(nearPlane=4217.87, 
    farPlane=7454.15, width=9352.27, height=4209.24, cameraPosition=(-530.063, 
    359.252, 5836.01), cameraTarget=(-530.063, 359.252, 0))
p = mdb.models['Model-1'].Part(name='matrix', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['matrix']
p.BaseSolidExtrude(sketch=s, depth=254.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['matrix']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
# Adding datum points for assembly
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

## Sketching fibre
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(6.25, -8.75))
s1.RadialDimension(curve=g[2], textPoint=(23.4929122924805, 8.8983039855957), 
    radius=current_fibre_radius)
session.viewports['Viewport: 1'].view.setValues(nearPlane=119.365, 
    farPlane=257.758, width=452.616, height=203.712, cameraPosition=(-29.9552, 
    8.76801, 188.562), cameraTarget=(-29.9552, 8.76801, 0))
p = mdb.models['Model-1'].Part(name='fibre', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['fibre']
p.BaseSolidExtrude(sketch=s1, depth=4310.0)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['fibre']
# Adding datum point for assembly
p.DatumPointByCoordinate(coords=(0.0, 0.0, 2155.0))

### Assembly
# Starting with matrix
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['matrix']
a.Instance(name='matrix-1', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']

## Appending fibre 1
a.Instance(name='fibre-1', part=p, dependent=ON)
p1 = a.instances['fibre-1']
p1.translate(vector=(1634.0, 0.0, 0.0))
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
    1761.0))
#: The instance fibre-1 was translated by -2.781272655E+03, -220.05722, 1.761E+03 with respect to the assembly coordinate system

## Appending fibre 2
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-2', part=p, dependent=ON)
p1 = a.instances['fibre-2']
p1.translate(vector=(1634.0, 0.0, 0.0))
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
    1761.0))
#: The instance fibre-2 was translated by -2.273272655E+03, -728.05722, 1.761E+03 with respect to the assembly coordinate system

## Appending fibre 3
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-3', part=p, dependent=ON)
p1 = a.instances['fibre-3']
p1.translate(vector=(1634.0, 0.0, 0.0))
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
    1761.0))
#: The instance fibre-3 was translated by -1.765272655E+03, -1.23605722E+03, 1.761E+03 with respect to the assembly coordinate system

## Appending fibre 4
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

## Appending fibre 5
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

## Merging assmebled parts
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanMerge(name='merged_part', instances=(
    a.instances['matrix-1'], a.instances['fibre-1'], a.instances['fibre-2'], 
    a.instances['fibre-3'], a.instances['fibre-4'], a.instances['fibre-5'], ), 
    keepIntersections=ON, originalInstances=SUPPRESS, mergeNodes=BOUNDARY_ONLY, 
    nodeMergingTolerance=1e-06, domain=BOTH)

### Removing extra fibre material from merged_part
## Extrude Cut from face 1 
p = mdb.models['Model-1'].parts['fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['merged_part']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['merged_part']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[38], sketchUpEdge=e[30], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-4.629858, 1509.0, 
    127.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=6117.13, gridSpacing=152.92, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['merged_part']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['merged_part']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[23], ))
p = mdb.models['Model-1'].parts['merged_part']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[30], ))
p = mdb.models['Model-1'].parts['merged_part']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[28], ))
p = mdb.models['Model-1'].parts['merged_part']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[31], ))
p = mdb.models['Model-1'].parts['merged_part']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[38], sketchUpEdge=e1[30], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Extrude Cut from face 2
p = mdb.models['Model-1'].parts['merged_part']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[31], sketchUpEdge=e[18], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(1544.0, -36.201041, 
    127.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['merged_part']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['merged_part']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[19], ))
p = mdb.models['Model-1'].parts['merged_part']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[18], ))
p = mdb.models['Model-1'].parts['merged_part']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[21], ))
p = mdb.models['Model-1'].parts['merged_part']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[20], ))
p = mdb.models['Model-1'].parts['merged_part']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[31], sketchUpEdge=e1[18], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

##  Extrude Cut from face 3
session.viewports['Viewport: 1'].view.setValues(nearPlane=11360.9, 
    farPlane=20784, width=10706.2, height=4818.6, cameraPosition=(11442.4, 
    -9237.76, 6017.1), cameraUpVector=(0.377726, 0.871669, -0.312275), 
    cameraTarget=(269.654, -732.056, -107.608))
p = mdb.models['Model-1'].parts['merged_part']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[26], sketchUpEdge=e[19], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(51.79368, -1539.0, 
    127.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['merged_part']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['merged_part']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[20], ))
p = mdb.models['Model-1'].parts['merged_part']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[19], ))
p = mdb.models['Model-1'].parts['merged_part']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[16], ))
p = mdb.models['Model-1'].parts['merged_part']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[21], ))
p = mdb.models['Model-1'].parts['merged_part']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[26], sketchUpEdge=e1[19], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Extrude Cut from face 4
session.viewports['Viewport: 1'].view.setValues(nearPlane=11882.9, 
    farPlane=19576.4, width=11198.1, height=5040, cameraPosition=(-13280.4, 
    1945.3, 9289.49), cameraUpVector=(0.48598, 0.867439, -0.106644), 
    cameraTarget=(-1199.46, -67.5194, 86.8489))
p = mdb.models['Model-1'].parts['merged_part']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[23], sketchUpEdge=e[20], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-1504.0, 0.909488, 
    127.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['merged_part']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['merged_part']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[21], ))
p = mdb.models['Model-1'].parts['merged_part']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[20], ))
p = mdb.models['Model-1'].parts['merged_part']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[18], ))
p = mdb.models['Model-1'].parts['merged_part']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[22], ))
p = mdb.models['Model-1'].parts['merged_part']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[23], sketchUpEdge=e1[20], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

### Assign materials and sections 
## Create matrix material
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='matrix_material')
mdb.models['Model-1'].materials['matrix_material'].Elastic(table=((current_matrix_E, 
    0.3), ))

## Create fibre material
mdb.models['Model-1'].Material(name='fibre_material')
mdb.models['Model-1'].materials['fibre_material'].Elastic(table=((121000.0, 
    0.3), ))


## Create matrix section
mdb.models['Model-1'].HomogeneousSolidSection(name='matrix_section', 
    material='matrix_material', thickness=None)

## Create fibre section
mdb.models['Model-1'].HomogeneousSolidSection(name='fibre_section', 
    material='fibre_material', thickness=None)

## Assigning matrix section to matrix set
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
region = p.Set(cells=cells, name='matrix_set')
p = mdb.models['Model-1'].parts['merged_part']
p.SectionAssignment(region=region, sectionName='matrix_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning fibre section to fibre set 1
session.viewports['Viewport: 1'].view.setValues(nearPlane=12499.6, 
    farPlane=20149.2, width=11779.3, height=5301.59, cameraPosition=(-13898.1, 
    5392.52, 6771.68), cameraUpVector=(0.560133, 0.770927, -0.303188), 
    cameraTarget=(-1234.84, 129.902, -57.345))
session.viewports['Viewport: 1'].view.setValues(nearPlane=13492.2, 
    farPlane=19156.6, width=6463.78, height=2909.2, viewOffsetX=415.95, 
    viewOffsetY=197.509)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
region = p.Set(cells=cells, name='fibre_set1')
p = mdb.models['Model-1'].parts['merged_part']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning fibre section to fibre set 2
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
region = p.Set(cells=cells, name='fibre_set2')
p = mdb.models['Model-1'].parts['merged_part']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning fibre section to fibre set 3
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
region = p.Set(cells=cells, name='fibre_set3')
p = mdb.models['Model-1'].parts['merged_part']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning fibre section to fibre set 4
session.viewports['Viewport: 1'].view.setValues(nearPlane=13236.4, 
    farPlane=19412.5, width=8121.94, height=3655.5, viewOffsetX=387.247, 
    viewOffsetY=143.677)
session.viewports['Viewport: 1'].view.setValues(nearPlane=13213.5, 
    farPlane=19340.6, width=8107.91, height=3649.18, cameraPosition=(-4929.87, 
    -13786.1, 7296.99), cameraUpVector=(-0.207624, 0.791206, 0.575226), 
    cameraTarget=(-774.612, -957.024, 28.1075), viewOffsetX=386.578, 
    viewOffsetY=143.428)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='fibre_set4')
p = mdb.models['Model-1'].parts['merged_part']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

## Assigning fibre section to fibre set 5
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
region = p.Set(cells=cells, name='fibre_set5')
p = mdb.models['Model-1'].parts['merged_part']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

### Create linear buckle step
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
mdb.models['Model-1'].BuckleStep(name='Step-1', previous='Initial', numEigen=3, 
    vectors=6, maxIterations=300)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

### Create constraint surface sets
## Create reference points on top and bottom surfaces
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON, 
    adaptiveMeshConstraints=OFF)
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(0.0, 1524.0, 127.0))
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(0.0, -1524.0, 127.0))

## Create top surface constraint set
session.viewports['Viewport: 1'].view.setValues(nearPlane=15191.6, 
    farPlane=21213.2, width=6812.82, height=3066.29, viewOffsetX=860.906, 
    viewOffsetY=946.956)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['merged_part-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#40000 ]', ), )
region3=a.Set(faces=faces1, name='top_pin_set')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[16], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-1', refPointRegion=region1, 
    pinRegion=region3)

## Create bottom surface constraint set
session.viewports['Viewport: 1'].view.setValues(nearPlane=14792, 
    farPlane=21612.8, width=10229.5, height=4604.07, viewOffsetX=1508.53, 
    viewOffsetY=865.968)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14531.3, 
    farPlane=21320.8, width=10049.3, height=4522.95, cameraPosition=(9229.16, 
    -12170.4, 9810.92), cameraUpVector=(-0.912922, 0.193503, 0.359346), 
    cameraTarget=(931.102, -2005.21, -983.04), viewOffsetX=1481.95, 
    viewOffsetY=850.71)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['merged_part-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#10000 ]', ), )
region3=a.Set(faces=faces1, name='bottom_set_pin')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[17], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-2', refPointRegion=region1, 
    pinRegion=region3)

### Define Boundary Conditions
## Define Bottom Face Encastre Condition
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, interactions=OFF, constraints=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14614.7, 
    farPlane=21272.8, width=10107, height=4548.91, cameraPosition=(7884.19, 
    9301.92, 13421.3), cameraUpVector=(-0.434752, 0.591417, -0.679129), 
    cameraTarget=(-448.644, -244.839, 2102.2), viewOffsetX=1490.45, 
    viewOffsetY=855.592)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14758.5, 
    farPlane=20961.6, width=10206.4, height=4593.67, cameraPosition=(4207.79, 
    -12539, 12320.9), cameraUpVector=(-0.500339, 0.777041, 0.381927), 
    cameraTarget=(-561.07, -2144.43, -245.276), viewOffsetX=1505.11, 
    viewOffsetY=864.008)
a = mdb.models['Model-1'].rootAssembly
region = a.sets['bottom_set_pin']
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1', 
    region=region, localCsys=None)

## Define Top Surface Displacement Condition
session.viewports['Viewport: 1'].view.setValues(nearPlane=14338.4, 
    farPlane=21382.5, width=9915.86, height=4462.9, cameraPosition=(6994.11, 
    13338.7, 9941.64), cameraUpVector=(-0.889326, 0.222974, -0.399226), 
    cameraTarget=(658.282, -394.457, 2198.6), viewOffsetX=1462.26, 
    viewOffsetY=839.412)
a = mdb.models['Model-1'].rootAssembly
region = a.sets['top_pin_set']
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', 
    region=region, u1=0.0, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, buckleCase=PERTURBATION_AND_BUCKLING, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

## Define load
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['merged_part-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#40000 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='top_surface')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=1.0)

### Define Meshes for each region
## Define matrix mesh
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
    bcs=OFF, predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['merged_part']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=13084.9, 
    farPlane=19897.5, width=8029, height=3627.54, cameraPosition=(-13347.8, 
    -8851.98, -3819.89), cameraUpVector=(-0.128683, 0.951268, -0.280233), 
    cameraTarget=(-680.515, -838.346, -656.169), viewOffsetX=382.815, 
    viewOffsetY=142.032)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#20 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Define fibre set 1 mesh
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#4 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Define fibre set 2 mesh
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#8 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Define fibre set 3 mesh
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#10 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Define fibre set 4 mesh
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Define fibre set 5 mesh
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#2 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['merged_part']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))

## Mesh composite
p = mdb.models['Model-1'].parts['merged_part']
p.seedPart(size=240.0, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['merged_part']
p.generateMesh()

## Create Job
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)

## Conduct data check and submit
mdb.jobs['Job-1'].submit(consistencyChecking=OFF, datacheckJob=True)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Job Job-1: Abaqus/Standard completed successfully.
#: Job Job-1 completed successfully. 
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Job Job-1: Abaqus/Standard completed successfully.
#: Job Job-1 completed successfully.
mdb.jobs['Job-1'].waitForCompletion()

### Visualize Results
#o3 = session.openOdb(name='C:/temp/Job-1.odb')
#: Model: C:/temp/Job-1.odb
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
    #CONTOURS_ON_DEF, ))
#session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
#session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
#session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3 )
#session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=2 )
#session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1 ) 

## Extract and Store Eigenvalues
print('Extracting and Storing Eigenvalues')
o1 = visualization.openOdb('Job-1.odb')
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


# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:09:11 2020

@author: roshan94
"""

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=291.291015625, 
    height=181.659729003906)
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

output_buckling_load_e1 = []
output_buckling_load_e2 = []
output_buckling_load_e3 = []

#print('Starting FEA....')
#try:
    #float(sys.argv[1])
    #print('True')
#except:
    #print('false')

### Printing function
def log(print_str):
    print >> sys.stdout, print_str
    
sys.stdout.write(sys.argv[1])
current_fibre_radius = float(sys.argv[-3])
current_fibre_angle = float(sys.argv[-2])
current_matrix_E = float(sys.argv[-1])

#log('Starting Sketch')
### Sketching parts
## Sketching matrix
session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-20.0, 15.0), point2=(15.0, -15.0))
s.ObliqueDimension(vertex1=v[3], vertex2=v[0], textPoint=(4.15086364746094, 
    20.0789451599121), value=3048.0)
s.ObliqueDimension(vertex1=v[2], vertex2=v[3], textPoint=(29.056037902832, 
    2.57894515991211), value=3048.0)
s.Spot(point=(0.0, 0.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=12.3669, 
    farPlane=364.757, width=1972.37, height=960.712, cameraPosition=(-140.842, 
    335.502, 188.562), cameraTarget=(-140.842, 335.502, 0))
s.Spot(point=(-1524.0, 1524.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=1935.26, 
    farPlane=2016.39, width=401.241, height=195.438, cameraPosition=(3.16954, 
    31.6039, 1975.82), cameraTarget=(3.16954, 31.6039, 0))
s.move(vector=(1524.0, -1524.0), objectList=(g[2], g[3], g[4], g[5], v[4], 
    v[5]))
session.viewports['Viewport: 1'].view.setValues(nearPlane=388.458, 
    farPlane=3563.19, width=15701, height=7647.74, cameraPosition=(952.041, 
    1108.97, 1975.82), cameraTarget=(952.041, 1108.97, 0))
p = mdb.models['Model-1'].Part(name='matrix', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['matrix']
p.BaseSolidExtrude(sketch=s, depth=254.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['matrix']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']


## Sketching fibre
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(10.0, 0.0))
s1.RadialDimension(curve=g[2], textPoint=(21.1232757568359, -7.92105293273926), 
    radius=current_fibre_radius)
session.viewports['Viewport: 1'].view.setValues(nearPlane=119.197, 
    farPlane=257.926, width=776.486, height=378.215, cameraPosition=(24.347, 
    22.7378, 188.562), cameraTarget=(24.347, 22.7378, 0))
p = mdb.models['Model-1'].Part(name='fibre', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['fibre']
p.BaseSolidExtrude(sketch=s1, depth=4309.872)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

# Setting reference points for assembly
p = mdb.models['Model-1'].parts['fibre']
p.ReferencePoint(point=(0.0, 0.0, 2154.936))
p = mdb.models['Model-1'].parts['matrix']
p.ReferencePoint(point=(0.0, 0.0, 127.0))
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(-508.0, 508.0, 127.0))
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(-1016.0, 1016.0, 127.0))
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(508.0, -508.0, 127.0))
p = mdb.models['Model-1'].parts['matrix']
p.DatumPointByCoordinate(coords=(1016.0, -1016.0, 127.0))

### Assembly
## Inserting matrix
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['matrix']
a.Instance(name='matrix-1', part=p, dependent=ON)

## Inserting Fibre 1
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
session.viewports['Viewport: 1'].view.setValues(nearPlane=8634.56, 
    farPlane=18251.1, width=11392.5, height=5549.11, viewOffsetX=925.242, 
    viewOffsetY=774.426)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 0.0, 10.0), angle=current_fibre_angle)
#: The instance fibre-1 was rotated by 'current_fibre_angle'. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-1', ), vector=(-2539.769859, -507.769859, 
    1756.0))
#: The instance fibre-1 was translated by -2.539769859E+03, -507.769859, 1.756E+03 with respect to the assembly coordinate system
session.viewports['Viewport: 1'].view.setValues(nearPlane=11050.6, 
    farPlane=17719.9, width=14580.3, height=7101.83, cameraPosition=(6284.61, 
    4831.71, 12229.1), cameraUpVector=(-0.542308, 0.691615, -0.477043), 
    cameraTarget=(-82.0243, -771.657, 2125.56), viewOffsetX=1184.14, 
    viewOffsetY=991.121)

## Inserting Fibre 2
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
#: The instance fibre-2 was rotated by 'current_fibre_angle'. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-2', ), vector=(-2031.769859, -1015.769859, 
    1756.0))
#: The instance fibre-2 was translated by -2.031769859E+03, -1.015769859E+03, 1.756E+03 with respect to the assembly coordinate system

## Inserting Fibre 3
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
#: The instance fibre-3 was rotated by 'current_fibre_angle'. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-3', ), vector=(-1523.769859, -1523.769859, 
    1756.0))
#: The instance fibre-3 was translated by -1.523769859E+03, -1.523769859E+03, 1.756E+03 with respect to the assembly coordinate system

## Inserting Fibre 4
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-4', part=p, dependent=ON)
p1 = a.instances['fibre-4']
p1.translate(vector=(1666.80286683502, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-4', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 10.0, 0.0), angle=90.0)
#: The instance fibre-4 was rotated by 90. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 10., 0.
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-4', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 0.0, 10.0), angle=current_fibre_angle)
#: The instance fibre-4 was rotated by 'current_fibre_angle'. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-4', ), vector=(-1015.769859, -2031.769859, 
    1793.802867))
#: The instance fibre-4 was translated by -1.015769859E+03, -2.031769859E+03, 1.793802867E+03 with respect to the assembly coordinate system

## Inserting Fibre 5
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-5', part=p, dependent=ON)
p1 = a.instances['fibre-5']
p1.translate(vector=(2174.80286683502, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-5', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 10.0, 0.0), angle=90.0)
#: The instance fibre-5 was rotated by 90. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 10., 0.
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-5', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
    0.0, 0.0, 10.0), angle=current_fibre_angle)
#: The instance fibre-5 was rotated by 'current_fibre_angle'. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 0., 10.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('fibre-5', ), vector=(-507.769859, -2539.769859, 
    2301.802867))
#: The instance fibre-5 was translated by -507.769859, -2.539769859E+03, 2.301802867E+03 with respect to the assembly coordinate system

## Merging matrix and fibres
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanMerge(name='Part-1', instances=(a.instances['matrix-1'], 
    a.instances['fibre-1'], a.instances['fibre-2'], a.instances['fibre-3'], 
    a.instances['fibre-4'], a.instances['fibre-5'], ), keepIntersections=ON, 
    originalInstances=SUPPRESS, mergeNodes=BOUNDARY_ONLY, 
    nodeMergingTolerance=1e-06, domain=BOTH)

### Extrude cutting extra fibre material
## Cut Extrude Face 1
p = mdb.models['Model-1'].parts['matrix']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
#print(len(f))
log(len(f))
t = p.MakeSketchTransform(sketchPlane=f[46], sketchUpEdge=e[44], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-17.804368, 1509.0, 
    127.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=6117.13, gridSpacing=152.92, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['Part-1']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[37], ))
p = mdb.models['Model-1'].parts['Part-1']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[44], ))
p = mdb.models['Model-1'].parts['Part-1']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[42], ))
p = mdb.models['Model-1'].parts['Part-1']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[45], ))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[46], sketchUpEdge=e1[44], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Cut Extrude Face 2
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[37], sketchUpEdge=e[30], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(1539.0, -33.739831, 
    127.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['Part-1']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[31], ))
p = mdb.models['Model-1'].parts['Part-1']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[30], ))
p = mdb.models['Model-1'].parts['Part-1']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[33], ))
p = mdb.models['Model-1'].parts['Part-1']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[32], ))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[37], sketchUpEdge=e1[30], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Cut Extrude Face 3
session.viewports['Viewport: 1'].view.setValues(nearPlane=11816.7, 
    farPlane=19274.1, width=10874.8, height=5296.95, cameraPosition=(8181.77, 
    -11268.3, 7274.29), cameraUpVector=(0.151325, 0.893574, 0.422641), 
    cameraTarget=(109.325, -794.161, -55.8232))
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[32], sketchUpEdge=e[31], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(33.739832, -1539.0, 
    127.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['Part-1']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[32], ))
p = mdb.models['Model-1'].parts['Part-1']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[31], ))
p = mdb.models['Model-1'].parts['Part-1']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e1[28], ))
p = mdb.models['Model-1'].parts['Part-1']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s, edges=(e[33], ))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[32], sketchUpEdge=e1[31], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Cut Extrude Face 4
session.viewports['Viewport: 1'].view.setValues(nearPlane=12203.6, 
    farPlane=18879.5, width=11230.8, height=5470.37, cameraPosition=(-12564.3, 
    -6248.16, 7747.46), cameraUpVector=(-0.0254483, 0.998608, 0.046203), 
    cameraTarget=(-921.844, -544.639, -32.3039))
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[27], sketchUpEdge=e[31], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-1509.0, 17.804369, 
    127.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
p = mdb.models['Model-1'].parts['Part-1']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[32], ))
p = mdb.models['Model-1'].parts['Part-1']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[31], ))
p = mdb.models['Model-1'].parts['Part-1']
e1, p1 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e1[29], ))
p = mdb.models['Model-1'].parts['Part-1']
e, p2 = p.edges, p.elemEdges
p.projectEdgesOntoSketch(sketch=s1, edges=(e[33], ))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[27], sketchUpEdge=e1[31], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

### Material and Section Assignment
## Create Matrix Material
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='Matrix_Material')
mdb.models['Model-1'].materials['Matrix_Material'].Elastic(table=((current_matrix_E, 
    0.3), ))

## Create Fibre Material
mdb.models['Model-1'].Material(name='Fibre_Material')
mdb.models['Model-1'].materials['Fibre_Material'].Elastic(table=((121000.0, 
    0.3), ))

## Create Matrix Section
mdb.models['Model-1'].HomogeneousSolidSection(name='Matrix_section', 
    material='Matrix_Material', thickness=None)

## Create Fibre Section
mdb.models['Model-1'].HomogeneousSolidSection(name='Fibre_Section', 
    material='Fibre_Material', thickness=None)

## Assigning Sections (5 fibre sections and 1 matrix section)
session.viewports['Viewport: 1'].view.setValues(nearPlane=13125.7, 
    farPlane=18791.9, width=11354.6, height=5530.67, viewOffsetX=-123.386, 
    viewOffsetY=-22.4589)
session.viewports['Viewport: 1'].view.setValues(nearPlane=13269.3, 
    farPlane=17057.9, width=11478.9, height=5591.18, cameraPosition=(1630.53, 
    5302.93, 14236.2), cameraUpVector=(-0.195393, 0.762781, -0.61643), 
    cameraTarget=(-112.857, 83.0392, 153.75), viewOffsetX=-124.736, 
    viewOffsetY=-22.7046)
session.viewports['Viewport: 1'].view.setValues(nearPlane=12096.5, 
    farPlane=17795.3, width=10464.4, height=5097.04, cameraPosition=(13105.6, 
    3725.37, 6294.53), cameraUpVector=(-0.45833, 0.828868, -0.320799), 
    cameraTarget=(-155.454, 48.8258, 31.1114), viewOffsetX=-113.712, 
    viewOffsetY=-20.6979)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
region = p.Set(cells=cells, name='fibre_set1')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Fibre_Section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='fibre_set2')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Fibre_Section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
session.viewports['Viewport: 1'].view.setValues(nearPlane=11807.3, 
    farPlane=18074.7, width=10214.2, height=4975.18, cameraPosition=(11965.6, 
    8953.24, 98.4427), cameraUpVector=(-0.810243, 0.535883, -0.23735), 
    cameraTarget=(-194.744, -31.6807, 90.4632), viewOffsetX=-110.993, 
    viewOffsetY=-20.203)
session.viewports['Viewport: 1'].view.setValues(nearPlane=12058.8, 
    farPlane=17910.9, width=10431.7, height=5081.14, cameraPosition=(10995.7, 
    7704.5, 6789.86), cameraUpVector=(-0.690893, 0.640364, -0.33556), 
    cameraTarget=(-132.915, 23.4039, 25.4503), viewOffsetX=-113.357, 
    viewOffsetY=-20.6333)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
region = p.Set(cells=cells, name='fibre_set3')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Fibre_Section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
region = p.Set(cells=cells, name='fibre_set4')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Fibre_Section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
region = p.Set(cells=cells, name='fibre_set5')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Fibre_Section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
region = p.Set(cells=cells, name='matrix_section')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Matrix_section', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

### Define Linear Buckling Step
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
mdb.models['Model-1'].BuckleStep(name='Step-1', previous='Initial', numEigen=3, 
    vectors=6, maxIterations=300)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

### Define Top and Bottom Surface Ties (Interaction)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON, 
    adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14698.8, 
    farPlane=21590.8, width=13174.9, height=6417.28, cameraPosition=(10107.3, 
    12508, 8609.24), cameraUpVector=(-0.606027, 0.417938, -0.676801), 
    cameraTarget=(177.255, 436.564, 1611.91))
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(0.0, 1524.0, 127.0)) # Top Surface Reference Point
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(0.0, -1524.0, 127.0)) # Bottom Surface Reference Point

## Top Pin Set
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#400000 ]', ), )
region3=a.Set(faces=faces1, name='top_set_pin')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[16], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-1', refPointRegion=region1, 
    pinRegion=region3)

## Bottom Pin Set
session.viewports['Viewport: 1'].view.setValues(nearPlane=15440.6, 
    farPlane=21828.4, width=13839.8, height=6741.17, cameraPosition=(8761.29, 
    -13249.5, 9953.08), cameraUpVector=(0.583169, 0.805028, -0.108828), 
    cameraTarget=(102.026, -1003.01, 1687.02))
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#100000 ]', ), )
region3=a.Set(faces=faces1, name='bottom_pin_set')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[17], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-2', refPointRegion=region1, 
    pinRegion=region3)

### Define Constraints
## Bottom Surface Encastre Constraint
session.viewports['Viewport: 1'].view.setValues(nearPlane=16339.5, 
    farPlane=21889.4, width=14645.6, height=7133.64, cameraPosition=(4252.47, 
    11872.8, 14521.1), cameraUpVector=(-0.237126, 0.517467, -0.822192), 
    cameraTarget=(-263.062, 1031.19, 2056.9))
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, interactions=OFF, constraints=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=16325.8, 
    farPlane=22325.8, width=14633.3, height=7127.68, cameraPosition=(5317.67, 
    -13266.8, 13182.2), cameraUpVector=(0.43211, 0.880209, 0.19625), 
    cameraTarget=(-152.229, -1584.56, 1917.59))
a = mdb.models['Model-1'].rootAssembly
region = a.sets['bottom_pin_set']
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=15679.8, 
    farPlane=22189.5, width=14054.3, height=6845.64, cameraPosition=(11128.3, 
    10632.6, 11196.4), cameraUpVector=(-0.691326, 0.589753, -0.417444), 
    cameraTarget=(509.293, 1136.29, 1691.52))

## Top Surface Displacement Constraint
a = mdb.models['Model-1'].rootAssembly
region = a.sets['top_set_pin']
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', 
    region=region, u1=0.0, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, buckleCase=PERTURBATION_AND_BUCKLING, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

### Define Load
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#400000 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='top_surface')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=-1.0)
mdb.models['Model-1'].loads['Load-1'].setValues(magnitude=1.0)

### Meshing
## Assigning Tetrahedral Meshing Elements to each region
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
session.viewports['Viewport: 1'].view.setValues(nearPlane=12445.9, 
    farPlane=17523.7, width=5799.05, height=2831.9, viewOffsetX=-116.996, 
    viewOffsetY=560.981)
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
session.viewports['Viewport: 1'].view.setValues(nearPlane=12035.5, 
    farPlane=17934.2, width=11076.1, height=5408.88, viewOffsetX=1086.04, 
    viewOffsetY=670.723)
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
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=150.0, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Part-1']

## Generating Mesh
p.generateMesh()

### Creating the job
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.Job(name='Buckling_job', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)

## Job Data Check
mdb.jobs['Buckling_job'].submit(consistencyChecking=OFF, datacheckJob=True)
#: The job input file "Buckling_job.inp" has been submitted for analysis.

## Submit job and wait for results
#: Job Buckling_job: Analysis Input File Processor completed successfully.
#: Job Buckling_job: Abaqus/Standard completed successfully.
#: Job Buckling_job completed successfully. 
mdb.jobs['Buckling_job'].submit(consistencyChecking=OFF)
#: The job input file "Buckling_job.inp" has been submitted for analysis.
#: Job Buckling_job: Analysis Input File Processor completed successfully.
#: Job Buckling_job: Abaqus/Standard completed successfully.
#: Job Buckling_job completed successfully. 
mdb.jobs['Buckling_job'].waitForCompletion()

### Results Visualization (from example run)
#o3 = session.openOdb(name='C:/temp/Buckling_job.odb')
#: Model: C:/temp/Buckling_job.odb
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

print('Job completed')
    
## Extract and Store Eigenvalues
print('Extracting and Storing Eigenvalues')
o3 = session.openOdb(name='C:/temp/Job-1.odb')
Step = odb.steps.values[0]
for i_frame in Step.frames:
    if (i_frame == 0):
        output_buckling_load_e1.append(Step.frames[i_frame].description)
    elif (i_frame == 1):
        output_buckling_load_e2.append(Step.frames[i_frame].description)
    elif (i_frame == 2):
        output_buckling_load_e3.append(Step.frames[i_frame].description)
print('Eigenvalues stored....')

log('Eigen Value One: ' + str(output_buckling_load_e1) + 'Endone, Eigen Value Two: ' + str(output_buckling_load_e2) + 'Endtwo, Eigen Value Three: ' + str(output_buckling_load_e3) + ' Endthree')

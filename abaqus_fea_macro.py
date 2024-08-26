# -*- coding: utf-8 -*-
"""
Python script to run abaqus analysis (From Macro)

@author: roshan94
"""
from abaqus import *
from abaqusConstants import *
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
#import time
from odbAccess import *
import os.path

import sys

buckling_load_e1 = []
buckling_load_e2 = []
buckling_load_e3 = []

## Printing function
def log(print_str):
    print >> sys.__stdout__, print_str

current_fibre_radius = float(sys.argv[-4]) # in mm
current_fibre_angle = float(sys.argv[-3]) # in degrees
current_matrix_E = float(sys.argv[-2]) # in N/mm^2
current_job_no = int(sys.argv[-1]) # to create unique job file

#current_fibre_radius = 121.336121
#current_fibre_angle = 6.98156022e+01
#current_matrix_E = 4.45168454e+05
#current_job_no = 66

#log(current_fibre_radius)
#log(current_fibre_angle)
#log(current_matrix_E)
#log(current_job_no)

    
#log('Starting Abaqus Job')

### Sketching parts
## Sketching matrix
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(point1=(-30.0, 25.0), point2=(0.0, 0.0))
s1.ObliqueDimension(vertex1=v[3], vertex2=v[0], textPoint=(-10.5206680297852, 28.6126556396484), value=3048.0)
s1.ObliqueDimension(vertex1=v[2], vertex2=v[3], textPoint=(15.6176376342773, 15.1862182617188), value=3048.0)
s1.Spot(point=(-1524.0, 1524.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=928.526, farPlane=3518.23, width=9938.03, height=4632.66, cameraPosition=(-3302.99, 1413.18, 2223.38), cameraTarget=(-3302.99, 1413.18, 0))
s1.move(vector=(1524.0, -1524.0), objectList=(g[2], g[3], g[4], g[5], v[4]))
p = mdb.models['Model-1'].Part(name='matrix', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['matrix']
p.BaseSolidExtrude(sketch=s1, depth=254.0)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['matrix']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
# Creating Datum Points for Assembly
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
# Store pointOn information for the four faces and edges for Cut Extrude later
#pointOn_rightface = p.faces[0].pointOn
pointOn_rightface = (1524.0, 0.0, 10.0)
#pointOn_bottomface = p.faces[1].pointOn
pointOn_bottomface = (0.0, -1524.0, 10.0)
#pointOn_leftface = p.faces[2].pointOn
pointOn_leftface = (-1524.0, 0.0, 10.0)
#pointOn_topface = p.faces[3].pointOn
pointOn_topface = (0.0, 1524.0, 10.0)
#pointOn_rightedge = p.edges[0].pointOn
pointOn_rightedge = (1524.0, 0.0, 254.0)
#pointOn_bottomedge = p.edges[6].pointOn
pointOn_bottomedge = (0.0, -1524.0, 254.0)
#pointOn_leftedge = p.edges[7].pointOn
pointOn_leftedge = (-1524.0, 0.0, 254.0)
#pointOn_topedge = p.edges[10].pointOn
pointOn_topedge = (0.0, 1524.0, 254.0)

## Sketching fibre with origin at centre
fibre_length = 5000.0
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(12.5, -16.25))
s.RadialDimension(curve=g[2], textPoint=(-41.494556427002, 14.4040946960449), radius=current_fibre_radius)
p = mdb.models['Model-1'].Part(name='fibre', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['fibre']
p.BaseSolidExtrude(sketch=s, depth=(fibre_length/2))
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].view.setValues(nearPlane=3903.73, farPlane=6896.61, width=2040.4, height=901.549, cameraPosition=(-2533.88, 638.987, -3476.94), cameraUpVector=(-0.126619, -0.943404, 0.306524))
p = mdb.models['Model-1'].parts['fibre']
f, e = p.faces, p.edges
fibre_sketchplane = f.findAt((0.0, 0.0, 0.0))
fibre_sketchedge = e.findAt((0.0, current_fibre_radius, 0.0))
t = p.MakeSketchTransform(sketchPlane=fibre_sketchplane, sketchUpEdge=fibre_sketchedge, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=421.59, gridSpacing=10.53, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['fibre']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(-current_fibre_radius, 0.0))
s1.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
p = mdb.models['Model-1'].parts['fibre']
f1, e1 = p.faces, p.edges
fibre_sketchplane2 = f1.findAt((0.0, 0.0, 0.0))
fibre_sketchedge2 = e1.findAt((0.0, current_fibre_radius, 0.0))
p.SolidExtrude(sketchPlane=fibre_sketchplane2, sketchUpEdge=fibre_sketchedge2, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s1, depth=(fibre_length/2), flipExtrudeDirection=OFF)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['fibre']
p.DatumPointByCoordinate(coords=(0.0, 0.0, 0.0))

### Assembly
## Adding matrix
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['matrix']
a.Instance(name='matrix-1', part=p, dependent=ON)

## Appending fibre 1 
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-1', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 10.0, 0.0), angle=90.0)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 10.0), angle=25.0)
a = mdb.models['Model-1'].rootAssembly
final_position = (0.0, 0.0, 127.0)
a.translate(instanceList=('fibre-1', ), vector=final_position)

## Appending fibre 2 
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-2', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 10.0, 0.0), angle=90.0)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 10.0), angle=25.0)
a = mdb.models['Model-1'].rootAssembly
final_position = (-508.0, 508.0, 127.0)
a.translate(instanceList=('fibre-2', ), vector=final_position)

## Appending fibre 3 
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-3', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-3', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 10.0, 0.0), angle=90.0)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-3', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 10.0), angle=25.0)
a = mdb.models['Model-1'].rootAssembly
final_position = (508.0, -508.0, 127.0)
a.translate(instanceList=('fibre-3', ), vector=final_position)

## Appending fibre 4 
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-4', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-4', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 10.0, 0.0), angle=90.0)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-4', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 10.0), angle=25.0)
a = mdb.models['Model-1'].rootAssembly
final_position = (-1016.0, 1016.0, 127.0)
a.translate(instanceList=('fibre-4', ), vector=final_position)

## Appending fibre 5 
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['fibre']
a.Instance(name='fibre-5', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-5', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 10.0, 0.0), angle=90.0)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('fibre-5', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 10.0), angle=25.0)
a = mdb.models['Model-1'].rootAssembly
final_position = (1016.0, -1016.0, 127.0)
a.translate(instanceList=('fibre-5', ), vector=final_position)

## Merging matrix and fibres
a.InstanceFromBooleanMerge(name='Part-1', instances=(a.instances['matrix-1'], a.instances['fibre-1'], a.instances['fibre-2'], a.instances['fibre-3'], a.instances['fibre-4'], a.instances['fibre-5'], ), keepIntersections=ON, originalInstances=SUPPRESS, mergeNodes=BOUNDARY_ONLY, nodeMergingTolerance=1e-06, domain=BOTH)

### Cutting out extra fibre material from composite
## Cutting fibre material from top face
p = mdb.models['Model-1'].parts['fibre']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
f_pt = pointOn_topface
e_pt = pointOn_topedge
top_face = f.findAt(f_pt)
top_edge = e.findAt(e_pt)
t = p.MakeSketchTransform(sketchPlane=top_face, sketchUpEdge=top_edge, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-4.629858, 1509.0, 127.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=6117.13, gridSpacing=152.92, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.rectangle(point1=(-3000.00, 3000.00), point2=(3000.00, -3000.00))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
top_face2 = f1.findAt(f_pt)
top_edge2 = e1.findAt(e_pt)
p.CutExtrude(sketchPlane=top_face2, sketchUpEdge=top_edge2, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Cutting extra fibre from right face
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
f_pt = pointOn_rightface
e_pt = pointOn_rightedge
right_face = f.findAt(f_pt)
right_edge = e.findAt(e_pt)
t = p.MakeSketchTransform(sketchPlane=right_face, sketchUpEdge=right_edge, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(1544.0, -36.201041, 127.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
s1.rectangle(point1=(-3000.00, 3000.00), point2=(3000.00, -3000.00))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
right_face2 = f1.findAt(f_pt)
right_edge2 = e1.findAt(e_pt)
p.CutExtrude(sketchPlane=right_face2, sketchUpEdge=right_edge2, sketchPlaneSide=SIDE1, 
sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

## Cutting extra fibre from bottom face(macro part3: change in camera POV not coded)
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
f_pt = pointOn_bottomface
e_pt = pointOn_bottomedge
bottom_face = f.findAt(f_pt)
bottom_edge = e.findAt(e_pt)
t = p.MakeSketchTransform(sketchPlane=bottom_face, sketchUpEdge=bottom_edge, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(51.79368, -1539.0, 127.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.rectangle(point1=(-3000.00, 3000.00), point2=(3000.00, -3000.00))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
bottom_face2 = f1.findAt(f_pt)
bottom_edge2 = e1.findAt(e_pt)
p.CutExtrude(sketchPlane=bottom_face2, sketchUpEdge=bottom_edge2, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=ON)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
    
## Cutting extra fibre from left face
p = mdb.models['Model-1'].parts['Part-1']
f, e = p.faces, p.edges
f_pt = pointOn_leftface
e_pt = pointOn_leftedge
left_face = f.findAt(f_pt)
left_edge = e.findAt(e_pt)
t = p.MakeSketchTransform(sketchPlane=left_face, sketchUpEdge=left_edge, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-1504.0, 0.909488, 127.0))
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=8636.0, gridSpacing=215.9, transform=t)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
s1.rectangle(point1=(-3000.00, 3000.00), point2=(3000.00, -3000.00))
p = mdb.models['Model-1'].parts['Part-1']
f1, e1 = p.faces, p.edges
left_face2 = f1.findAt(f_pt)
left_edge2 = e1.findAt(e_pt)
p.CutExtrude(sketchPlane=left_face2, sketchUpEdge=left_edge2, sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
s1.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

### Material Creation and Section Assignment
## Creating Matrix Material
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='matrix_material')
mdb.models['Model-1'].materials['matrix_material'].Elastic(table=((current_matrix_E, 0.29), ))

## Create Fibre Material
mdb.models['Model-1'].Material(name='fibre_material')
mdb.models['Model-1'].materials['fibre_material'].Elastic(table=((121000.0, 0.34), ))

## Create Matrix Section
mdb.models['Model-1'].HomogeneousSolidSection(name='matrix_section', material='matrix_material', thickness=None)

## Create Fibre Section
mdb.models['Model-1'].HomogeneousSolidSection(name='fibre_section', material='fibre_material', thickness=None)
    
## Find Regions and Create Sets using FindAt
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
#mat_point = f[-1].pointOn
mat_point = (0,0,254.0)
#fib1_point = f[1].pointOn
fib1_point = (-1016.0,1016.0,127.0)
#fib2_point = f[4].pointOn
fib2_point = (-508.0,508.0,127.0)
#fib3_point = f[7].pointOn
fib3_point = (0,0,127.0)
#fib4_point = f[10].pointOn
fib4_point = (508.0,-508.0,127.0)
#fib5_point = f[13].pointOn # test with longer fibre length (doesn't work for current fibre length)
fib5_point = (1016.0,-1016.0,127.0)

c  = p.cells
mat_cells = c.findAt((mat_point,))
fib1_cells = c.findAt((fib1_point,))
fib2_cells = c.findAt((fib2_point,))
fib3_cells = c.findAt((fib3_point,))
fib4_cells = c.findAt((fib4_point,))
fib5_cells = c.findAt((fib5_point,))

mat_set = p.Set(cells=mat_cells, name='matrix_set')
fib1_set = p.Set(cells=fib1_cells, name='fibre_set1')
fib2_set = p.Set(cells=fib2_cells, name='fibre_set2')
fib3_set = p.Set(cells=fib3_cells, name='fibre_set3')
fib4_set = p.Set(cells=fib4_cells, name='fibre_set4')
fib5_set = p.Set(cells=fib5_cells, name='fibre_set5')

## Assign matrix section to matrix set
p = mdb.models['Model-1'].parts['Part-1']
#c = p.cells
#cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
#region = p.Set(cells=cells, name='matrix_set')
region = mat_set
#p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='matrix_section', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

## Assign fibre section to fibre set 1
p = mdb.models['Model-1'].parts['Part-1']
#c = p.cells
#cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
#region = p.Set(cells=cells, name='fibre_set1')
region = fib1_set
#p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

## Assign fibre section to fibre set 2
p = mdb.models['Model-1'].parts['Part-1']
#c = p.cells
#cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
#region = p.Set(cells=cells, name='fibre_set2')
region = fib2_set
#p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

## Assign fibre section to fibre set 3
#session.viewports['Viewport: 1'].view.setValues(nearPlane=13280.7, farPlane=18868.5, width=5703.24, height=2519.97, viewOffsetX=-646.004, viewOffsetY=313.102)
p = mdb.models['Model-1'].parts['Part-1']
#c = p.cells
#cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
#region = p.Set(cells=cells, name='fibre_set3')
region = fib3_set
#p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

## Assign fibre section to fibre set 4    
p = mdb.models['Model-1'].parts['Part-1']
#c = p.cells
#cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
#region = p.Set(cells=cells, name='fibre_set4')
region = fib4_set
#p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
    
## Assign fibre section to fibre set 5
p = mdb.models['Model-1'].parts['Part-1']
#c = p.cells
#cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
#region = p.Set(cells=cells, name='fibre_set5')
region = fib5_set
#p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='fibre_section', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

### Define Linear Buckling Step
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON)
mdb.models['Model-1'].BuckleStep(name='Step-1', previous='Initial', numEigen=3, vectors=6, maxIterations=300)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, constraints=ON, connectors=ON, engineeringFeatures=ON, adaptiveMeshConstraints=OFF)
    
### Define Top and Bottom Pin Sets
## Create Top and Bottom Reference Points
Rf_top = (0.0, 1524.0, 127.0)
Rf_bottom = (0.0, -1524.0, 127.0)
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=Rf_top)
a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=Rf_bottom)
    
## Define Top Pin Set
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
#faces1 = f1.getSequenceFromMask(mask=('[#40000 ]', ), )
faces1 = f1.findAt((pointOn_topface,))
region3=a.Set(faces=faces1, name='top_set_pin')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
#refPoints1=(r1[16], ) # TRY TO SUBSITUTE ON TESTING!!!
refPoints1 = (r1.values()[1], )
#refPoints1 = (Rf_top,)
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-1', refPointRegion=region1, pinRegion=region3)
session.viewports['Viewport: 1'].view.setValues(nearPlane=14456, farPlane=23032.1, width=14761.2, height=6522.24, cameraPosition=(11883.8, -9935.43, 10836.2), cameraUpVector=(0.302116, 0.945744, -0.119557), cameraTarget=(118.195, -1286.46, 2149.23))
    
## Define Bottom Pin Set
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
#faces1 = f1.getSequenceFromMask(mask=('[#10000 ]', ), )
faces1 = f1.findAt((pointOn_bottomface,))
region3=a.Set(faces=faces1, name='bottom_set_pin')
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
#refPoints1=(r1[17], ) # TRY TO SUBSITUTE ON TESTING!!!
refPoints1 = (r1.values()[0], )
#refPoints1 = (Rf_bottom,)
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Constraint-2', refPointRegion=region1, pinRegion=region3)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, predefinedFields=ON, interactions=OFF, constraints=OFF, engineeringFeatures=OFF)

### Define Boundary Conditions
## Define Bottom Set Encastre Condition
session.viewports['Viewport: 1'].view.setValues(nearPlane=13998.9, farPlane=22217.6, width=14294.4, height=6315.99, cameraPosition=(14704, 6439.37, 8670.08), cameraUpVector=(-0.787715, 0.384634, 0.481209), cameraTarget=(381.938, 244.892, 1946.66))
session.viewports['Viewport: 1'].view.setValues(nearPlane=14069.8, farPlane=22508.8, width=14366.9, height=6348, cameraPosition=(10457, -13429.5, 7029.45), cameraUpVector=(0.0358565, 0.756617, 0.652874), cameraTarget=(119.927, -980.868, 1845.45))
a = mdb.models['Model-1'].rootAssembly
region = a.sets['bottom_set_pin']
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1', region=region, localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=13900.7, farPlane=22368.8, width=14194.3, height=6271.73, cameraPosition=(9246.39, 14982.3, 4736.93), cameraUpVector=(-0.740273, -0.0636828, 0.669283), cameraTarget=(33.9949, 1035.89, 1682.72))
    
## Define Top Set Displacement Condition
a = mdb.models['Model-1'].rootAssembly
region = a.sets['top_set_pin']
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', region=region, u1=0.0, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, buckleCase=PERTURBATION_AND_BUCKLING, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

### Define Load
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].faces
#side1Faces1 = s1.getSequenceFromMask(mask=('[#40000 ]', ), )
side1Faces1 = s1.findAt((pointOn_topface,))
region = a.Surface(side1Faces=side1Faces1, name='top_surface')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', region=region, distributionType=UNIFORM, field='', magnitude=1.0)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, bcs=OFF, predefinedFields=OFF, connectors=OFF)

### Meshing individual elements one-at-a-time
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(meshTechnique=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=12456.7, farPlane=17929.6, width=6440.49, height=2855.67, viewOffsetX=-352.914, viewOffsetY=275.14)

def mesh_part(seed_size, dev_factor, min_size_factor):
    ## Meshing matrix
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#20 ]', ), )
    pickedRegions = mat_cells
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    #elemType1 = mesh.ElemType(elemCode=C3D20R)
    #elemType2 = mesh.ElemType(elemCode=C3D15)
    #elemType3 = mesh.ElemType(elemCode=C3D10)
    #p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
    #pickedRegions =(cells, )
    #pickedRegions = mat_cells
    #p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
    #pickedRegions =(cells, )
    pickedRegions = (mat_cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p = mdb.models['Model-1'].parts['Part-1']
    p.seedPart(size=seed_size, deviationFactor=dev_factor, minSizeFactor=min_size_factor)
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#20 ]', ), )
    pickedRegions = (mat_cells, )
    p.generateMesh(regions=pickedRegions)
    #matrix_meshstats = getMeshStats(pickedRegions)
    #log(matrix_meshstats)
    
    ## Meshing fibre 1
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#8 ]', ), )
    pickedRegions = fib1_cells
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    #elemType1 = mesh.ElemType(elemCode=C3D20R)
    #elemType2 = mesh.ElemType(elemCode=C3D15)
    #elemType3 = mesh.ElemType(elemCode=C3D10)
    #p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
    #pickedRegions =(cells, )
    #p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, #elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
    #pickedRegions =(cells, )
    pickedRegions = (fib1_cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#8 ]', ), )
    pickedRegions = (fib1_cells, )
    p.generateMesh(regions=pickedRegions)
    
    ## Meshing fibre 2
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#10 ]', ), )
    pickedRegions = fib2_cells
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    #elemType1 = mesh.ElemType(elemCode=C3D20R)
    #elemType2 = mesh.ElemType(elemCode=C3D15)
    #elemType3 = mesh.ElemType(elemCode=C3D10)
    #p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
    #pickedRegions =(cells, )
    #p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
    #pickedRegions =(cells, )
    pickedRegions = (fib2_cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#10 ]', ), )
    pickedRegions = (fib2_cells, )
    p.generateMesh(regions=pickedRegions)
    
    ## Meshing fibre 3
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions = fib3_cells
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    #elemType1 = mesh.ElemType(elemCode=C3D20R)
    #elemType2 = mesh.ElemType(elemCode=C3D15)
    #elemType3 = mesh.ElemType(elemCode=C3D10)
    #p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    #pickedRegions =(cells, )
    #p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    #pickedRegions =(cells, )
    pickedRegions = (fib3_cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions = (fib3_cells, )
    p.generateMesh(regions=pickedRegions)
    
    ## Mehing fibre 4
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#2 ]', ), )
    pickedRegions = fib4_cells
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    #elemType1 = mesh.ElemType(elemCode=C3D20R)
    #elemType2 = mesh.ElemType(elemCode=C3D15)
    #elemType3 = mesh.ElemType(elemCode=C3D10)
    #p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    #pickedRegions =(cells, )
    #p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    #pickedRegions =(cells, )
    pickedRegions = (fib4_cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#2 ]', ), )
    pickedRegions = (fib4_cells, )
    p.generateMesh(regions=pickedRegions)
    
    ## Meshing fibre 5
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#4 ]', ), )
    pickedRegions = fib5_cells
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    #elemType1 = mesh.ElemType(elemCode=C3D20R)
    #elemType2 = mesh.ElemType(elemCode=C3D15)
    #elemType3 = mesh.ElemType(elemCode=C3D10)
    #p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    #pickedRegions =(cells, )
    #p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    #pickedRegions =(cells, )
    pickedRegions = (fib5_cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, elemType3))
    p = mdb.models['Model-1'].parts['Part-1']
    #c = p.cells
    #pickedRegions = c.getSequenceFromMask(mask=('[#4 ]', ), )
    pickedRegions = (fib5_cells, )
    p.generateMesh(regions=pickedRegions)
    

seedsize = 160
devfac = 0.075
minsizefac = 0.01
mesh_part(seedsize, devfac, minsizefac)

### Initiate Job
job_name = 'Buckling_job_' + str(current_job_no)
#log(job_name)
mdb.Job(name=job_name, model='Model-1', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, numDomains=4, numGPUs=0)
#mdb.Job(name='Job-2', model='Model-1', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,     memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,     explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,     modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',     scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)

## Perform Data Check
#mdb.jobs[job_name].submit(consistencyChecking=ON, datacheckJob=True)
    
## Submit Job
mdb.jobs[job_name].submit(consistencyChecking=OFF)
#log('Job Started')

## Wait for Completion
mdb.jobs[job_name].waitForCompletion()
#log('Job Completed')

### Re-mesh part and resubmit job if aborted
job_successful = True
#sta_filepath = 'C://temp//' + job_name + '.sta' # For testing 
sta_filepath = 'H://Desktop//MSEN 655 - Material Design Studio//python code//Neural Net Training Dataset//' + job_name + '.sta' # For actual runs
#time.sleep(2)
remesh_count = 0
if (not os.path.exists(sta_filepath)):
    job_successful = False
    while(not job_successful):
        remesh_count += 1
        seedsize = seedsize - 20
        #devfac = devfac
        #minsizefac = minsizefac
        mesh_part(seedsize, devfac, minsizefac)
        job_name_mod = job_name + '_' + str(remesh_count)
        mdb.Job(name=job_name_mod, model='Model-1', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, numDomains=4, numGPUs=0)
        # Submit Job and wait for completion
        mdb.jobs[job_name_mod].submit(consistencyChecking=OFF)
        mdb.jobs[job_name_mod].waitForCompletion()
        sta_filepath_mod = 'H://Desktop//MSEN 655 - Material Design Studio//python code//Neural Net Training Dataset//' + job_name_mod + '.sta' # For actual runs
        #sta_filepath_mod = 'c://temp//' + job_name_mod + '.sta' # For testing
        if (os.path.exists(sta_filepath_mod) or remesh_count == 3):
            job_successful = True
            


if (remesh_count == 0):
    job_name_final = job_name
else:
    job_name_final = job_name_mod
    

    
## Extract and Store Eigenvalues
#log('Extracting and Storing Eigenvalues')
odb_filename = job_name_final + '.odb'
o1 = openOdb(odb_filename)
#time.sleep(2)
Step = o1.steps['Step-1']
for i in range(4):
    if (i == 1):
        Mode_desc = Step.frames[i].description
        #log(Mode_desc)
        Eigenval_pos = Mode_desc.find('EigenValue') + 14
        Eigenval_str = Mode_desc[Eigenval_pos:]
        buckling_load_e1.append(Eigenval_str)
    elif (i == 2):
        Mode_desc = Step.frames[i].description
        #log(Mode_desc)
        Eigenval_pos = Mode_desc.find('EigenValue') + 14
        Eigenval_str = Mode_desc[Eigenval_pos:]
        buckling_load_e2.append(Eigenval_str)
    elif (i == 3):
        Mode_desc = Step.frames[i].description
        #log(Mode_desc)
        Eigenval_pos = Mode_desc.find('EigenValue') + 14
        Eigenval_str = Mode_desc[Eigenval_pos:]
        buckling_load_e3.append(Eigenval_str)
    else:
        continue

o1.close()
#log('Eigenvalues stored....')

log('Eigen Value One: ' + str(buckling_load_e1) + 'Endone, Eigen Value Two: ' + str(buckling_load_e2) + 'Endtwo, Eigen Value Three: ' + str(buckling_load_e3) + ' Endthree')


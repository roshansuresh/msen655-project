# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2019 replay file
# Internal Version: 2018_09_24-13.41.51 157541
# Run by roshan94 on Sat May  2 00:58:58 2020
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.32292, 1.32407), width=194.733, 
    height=131.348)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile('abaqus_fea_macro.py', __main__.__dict__)
#: Warning: findAt could not find a geometric entity at (-508.0, 508.0, 127.0)
#: Warning: findAt could not find a geometric entity at (0.0, 0.0, 127.0)
#: Warning: findAt could not find a geometric entity at (508.0, -508.0, 127.0)
#* ERROR: Only regions of the same dimension may be
#* selected for each element type assignment
#* File "abaqus_fea_macro.py", line 679, in <module>
#*     mesh_part(seedsize, devfac, minsizefac)
#* File "abaqus_fea_macro.py", line 581, in mesh_part
#*     p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
#* elemType3))

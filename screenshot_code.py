#### Taking the screenshot
    # displaying
    fileName = 'C:/temp/screenshots/best'+str(gen)
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)   
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setProjection(projection=PERSPECTIVE)
    # saving the screenshot
    session.printOptions.setValues(vpDecorations=OFF, compass=ON)
    session.printToFile(fileName=fileName, format=PNG, 
        canvasObjects=(session.viewports['Viewport: 1'], ))
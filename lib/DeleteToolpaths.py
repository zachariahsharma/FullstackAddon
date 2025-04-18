#Author- Zachariah Sharma
#Description-
import adsk.core, adsk.fusion, adsk.cam, traceback

def waitForGeneration(setup):
    while len([True for operation in setup.operations if operation.isGenerating == True]) > 0:
        pass

def DeleteToolpaths():
    ui = None
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = app.activeProduct

    # Ensure we are in the CAM workspace
    cam = adsk.cam.CAM.cast(design)
    if not cam:
        ui.messageBox("Switch to the CAM workspace.")
        return
    # Get all setups
    pastCache = 0
    allSetups = cam.setups
    # Iterate through setups
    for setup in allSetups:
        # Get toolpaths in the setup
        pastCache = 0
        while True:
            waitForGeneration(setup)
            toolpaths = setup.operations
            if pastCache == len(toolpaths):
                break
            # Iterate through toolpaths
            pastCache = len(toolpaths)
            for toolpath in toolpaths:
                # Check the machining time of the toolpath
                if "Empty" in str(toolpath.warning) or "empty" in str(toolpath.warning):
                    toolpath.deleteMe()
                elif "Drill" in toolpath.name and toolpath.isToolpathValid == False:
                    toolpath.deleteMe()
            cam.generateAllToolpaths(False)

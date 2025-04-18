#Author-
#Description-
import adsk.core, adsk.fusion, adsk.cam, traceback
from ..config import MMGBASEPATH
import os
import json

def export(name):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct

        # Ensure we are in the CAM workspace
        cam = adsk.cam.CAM.cast(design)
        if not cam:
            ui.messageBox("Switch to the CAM workspace.")
            return
        # Get all setups
        allSetups = cam.setups
        folder_path = MMGBASEPATH + f"/{name}/"
        baseDir = os.path.dirname(os.path.realpath(__file__))
        absolutePath = os.path.join(baseDir, 'templates/Laguna.cps')
        for setup in allSetups:
            releventToolpaths = {"Drills": [], 'Profiles': adsk.core.ObjectCollection.create(), '1/8': adsk.core.ObjectCollection.create()}
            for toolpath in setup.operations:
                description = json.loads(toolpath.tool.toJson())['description']
                if toolpath.strategy == 'drill':
                    releventToolpaths['Drills'].append(toolpath)
                elif "1/8" in str(description):
                    releventToolpaths['1/8'].add(toolpath)
                else:
                    releventToolpaths['Profiles'].add(toolpath)
            for toolpath in releventToolpaths['Drills']:
                postProcessInput = adsk.cam.PostProcessInput.create(str(toolpath.name).split(' ')[0], absolutePath, folder_path, adsk.cam.PostOutputUnitOptions.MillimetersOutput)
                postProcessInput.isOpenInEditor = False
                cam.postProcess(toolpath, postProcessInput)
            postProcessInput = adsk.cam.PostProcessInput.create("025Profile", absolutePath, folder_path, adsk.cam.PostOutputUnitOptions.MillimetersOutput)
            postProcessInput.isOpenInEditor = False
            cam.postProcess(releventToolpaths['Profiles'], postProcessInput)
            postProcessInput = adsk.cam.PostProcessInput.create("125Profile", absolutePath, folder_path, adsk.cam.PostOutputUnitOptions.MillimetersOutput)
            postProcessInput.isOpenInEditor = False
            cam.postProcess(releventToolpaths['1/8'], postProcessInput)
        
    except Exception as e:
        # ui.messageBox(e)
        pass

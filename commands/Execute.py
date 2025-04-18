"""This file acts as the main module for this script."""

import traceback
import adsk.core
import adsk.fusion
import adsk.cam
import os
from ..lib.AutoArrange import AutoArrange
from ..lib.SetupGenerator import SetupGenerator
from ..lib.DeleteToolpaths import DeleteToolpaths
from ..lib.MultiImport import importFiles
from ..lib.NewNCProgram import export
from ..config import STEPBASEPATH

app = adsk.core.Application.get()
ui  = app.userInterface


def start(config):
    """This function is called by Fusion when the script is run."""

    try:
        app = adsk.core.Application.get()
        ui: adsk.core.UserInterface  = app.userInterface
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        importFiles([STEPBASEPATH + child['child'] + '.step' for child in config['Parts']], [child['quantity'] for child in config['Parts']])
        AutoArrange(config["height"], config["width"])
        SetupGenerator(config['machine'], config['depth'], config['Material'], config['Thickness'])
        DeleteToolpaths()
        export(config['name'])
        app.activeDocument.saveAs(config['name'], app.data.activeProject.rootFolder.dataFolders.itemByName('2025 Robot').dataFolders.itemByName('AutoCAMDrop'), config['name'], 'AutoCAM')
        app.activeDocument.close(False)

    except:  
        # ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        app.log(f'Failed:\n{traceback.format_exc()}')
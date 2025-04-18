# Created by Portland CNC
# URL: https://pdxcnc.com

import adsk.core, adsk.fusion, traceback
import os

def importFiles(filenames, quantities):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent
        for filename, quantity in zip(filenames, quantities):
            try:
                # Extract the file name without extension to use as the component name
                componentName = os.path.splitext(os.path.basename(filename))[0]
                
                # Import the file directly into the root component
                importOptions = app.importManager.createSTEPImportOptions(filename)
                quantity = int(quantity)
                for _ in range(quantity):
                    app.importManager.importToTarget(importOptions, rootComp)

                    # Find the last created occurrence and rename it
                    lastOcc = rootComp.occurrences[-1]
                    lastOcc.component.name = componentName

                # Increment successful import count

            except Exception as e:
                # Increment fail count for this file and add its base name to the failed_files list
                ui.messageBox(f'Error importing {os.path.basename(filename)}: {str(e)}')  # Optional: Log the specific error to the console

        # Modify the message box to include information about failed file names

    except Exception as e:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')

import traceback
import adsk.core
import adsk.fusion
import adsk.cam
import os

def SetupGenerator(machine, truedepth, material, depth):
    app = adsk.core.Application.get()
    ui  = app.userInterface
    camWS: adsk.core.Workspace = ui.workspaces.itemById('FusionSolidEnvironment') 
    camWS: adsk.core.Workspace = ui.workspaces.itemById('CAMEnvironment') 
    comp: adsk.fusion.Component = app.activeProduct.rootComponent
    occurances = []
    for occ in comp.allOccurrences:
        if "Arrange"  in occ.fullPathName and "Envelope"  in occ.fullPathName and len(occ.fullPathName) > 35:
            occurances.append(occ.bRepBodies.item(0))
    camWS.activate()
    cam = adsk.cam.CAM.cast(app.activeDocument.products.itemByProductType('CAMProductType'))
    setupInput = cam.setups.createInput(0)
    setupInput.name = "Setup"
    setup = cam.setups.add(setupInput)
    setup.stockMode = adsk.cam.SetupStockModes.RelativeBoxStock
    setup.parameters.itemByName('job_stockOffsetMode').expression = "'simple'"
    setup.parameters.itemByName('job_stockOffsetXBack').expression = '.5 in'
    setup.parameters.itemByName('job_stockOffsetYFront').expression = '.5 in'
    setup.parameters.itemByName('job_stockOffsetZFront').expression = f'{truedepth-depth} in'
    setup.parameters.itemByName('job_model').value.value = occurances
    setup.parameters.itemByName('wcs_orientation_mode').expression = "'axesXY'"
    setup.parameters.itemByName('wcs_orientation_axisX').value.value = [comp.yConstructionAxis]
    setup.parameters.itemByName('wcs_orientation_axisY').value.value = [comp.xConstructionAxis]
    setup.parameters.itemByName('wcs_orientation_flipX').value.value = True
    setup.parameters.itemByName('wcs_origin_boxPoint').expression = "'top 1'"
    baseDir = os.path.dirname(os.path.realpath(__file__))
    # machine is Swift and IQ, material is Aluminum and Polycarb
    if machine == "Swift" and material == "Aluminum":
        absolutePath = os.path.join(baseDir, 'templates/AluminumSwift.f3dhsm-template')
    elif machine == "Swift" and material == "Polycarb":
        absolutePath = os.path.join(baseDir, 'templates/PolycarbSwift.f3dhsm-template')
    elif machine == "IQ" and material == "Polycarb":
        absolutePath = os.path.join(baseDir, 'templates/PolycarbIQ.f3dhsm-template')
    elif machine == "IQ" and material == "Aluminum":
        absolutePath = os.path.join(baseDir, 'templates/AluminumIQ.f3dhsm-template')
    TemplateFile = adsk.cam.CAMTemplate.createFromFile(absolutePath)
    template = adsk.cam.CreateFromCAMTemplateInput.create()
    template.camTemplate = TemplateFile
    setup.createFromCAMTemplate2(template)
    cam.generateAllToolpaths(skipValid=False)


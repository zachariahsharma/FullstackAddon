import traceback
import adsk.core
import adsk.fusion


def AutoArrange(height, width) -> adsk.fusion.ArrangeFeature:
    app = adsk.core.Application.get()
    ui  = app.userInterface
    try:
        des: adsk.fusion.Design = app.activeProduct
        comp = des.rootComponent
        arrangeFeats = comp.features.arrangeFeatures

        # Create the input.
        arrangeInput: adsk.fusion.ArrangeFeatureInput = arrangeFeats.createInput(
                        adsk.fusion.ArrangeSolverTypes.Arrange2DTrueShapeSolverType)

        # Get the definition object from the input.
        arrangeDefInput: adsk.fusion.ArrangeDefinition2DInput = arrangeInput.definition

        # Modify some of the arrange settings.
        arrangeDefInput.globalRotation = adsk.fusion.ArrangeRotationTypes.AllRotationsArrangeRotationType
        arrangeDefInput.isGlobalDirectionFaceUp = True
        arrangeDefInput.isPartInPartAllowed = True

        # Get the ArrangeComponents collection from the input objects.
        arrComponents = arrangeInput.arrangeComponents

        # Get the occurrences to arrange.
        occ1 = list(comp.allOccurrences)
        for occ in occ1:
            arrcomp = arrComponents.add(occ)
            arrcomp.quantity = 1

        # Define a plane envelope.
        planeEnv = arrangeInput.setPlaneEnvelope(comp.xYConstructionPlane, 
                                                adsk.core.ValueInput.createByString(f'{height} in'),
                                                adsk.core.ValueInput.createByString(f'{width} in'))

        # Modify some additional properties of the envelope.
        planeEnv.originXOffset = adsk.core.ValueInput.createByString('40 cm')
        planeEnv.originYOffset = adsk.core.ValueInput.createByString('0 cm')
        planeEnv.quantity = adsk.core.ValueInput.createByReal(1)
        planeEnv.objectSpacing = adsk.core.ValueInput.createByString('.26 in')
        planeEnv.envelopeSpacing = adsk.core.ValueInput.createByString('0.5 in')

        # Create the arrange feature.
        arrange = arrangeFeats.add(arrangeInput)
        return arrange
    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
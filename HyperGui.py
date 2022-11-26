"""
@author: Alexander Studier-Fischer, Jan Odenthal, Berkin Oezdemir, Isabella Camplisson, University of Heidelberg
"""

from HyperGuiModules import *
import logging
import os

#logging.basicConfig(level=logging.DEBUG)
xSize=None
ySize=None


def main():
    (window, introduction, input_output, image_diagram, hist_calculation, spec_calculation, bp, crop, bs, measure, mda, mda2, circle, rectangle, spec_invest, progressions, prediction) = init()

    listener = ModuleListener()

    # introduction
    Introduction(introduction)

    # histogram calculation
    HistCalculation(hist_calculation, listener)

    # histogram calculation
    SpecCalculation(spec_calculation, listener)

    # analysis and form
    analysis_and_form_frame = frame(input_output, BACKGROUND, 1, 0, 4, 2)
    analysis_and_form_module = AnalysisAndForm(analysis_and_form_frame, listener)
    listener.attach_module(ANALYSIS_AND_FORM, analysis_and_form_module)

    # source and output
    source_and_output_frame = frame(input_output, BACKGROUND, 0, 0, 1, 2)
    source_and_output_module = SourceAndOutput(source_and_output_frame, listener)
    listener.attach_module(SOURCE_AND_OUTPUT, source_and_output_module)

    # save
    save_frame = frame(input_output, BACKGROUND, 5, 0, 1, 1)
    save_module = Save(save_frame, listener)
    listener.attach_module(SAVE, save_module)

    # save csvs
    csv_frame = frame(input_output, BACKGROUND, 0, 2, 6, 1)
    csv_module = CSVSaver(csv_frame, listener)
    listener.attach_module(CSV, csv_module)

    # info
    info_frame = frame(input_output, BACKGROUND, 5, 1, 1, 1)
    info_module = Info(info_frame, listener)
    listener.attach_module(INFO, info_module)

    # parameter specification
    #parameter_frame = frame(input_output, BACKGROUND, 0, 3, 2, 1)
    #parameter_module = Parameter(parameter_frame, listener)
    #listener.attach_module(PARAMETER, parameter_module)

    # original colour
    og_color_frame = frame(image_diagram, BACKGROUND, 0, 0, 7, 6)
    og_color_module = OGColour(og_color_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR, og_color_module)

    # original colour data
    og_color_data_frame = frame(image_diagram, BACKGROUND, 2, 12, 3, 2)
    og_color_data_module = OGColourData(og_color_data_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR_DATA, og_color_data_module)

    # recreated colour
    recreated_color_frame = frame(image_diagram, BACKGROUND, 7, 0, 7, 3)
    recreated_color_module = RecColour(recreated_color_frame, listener)
    listener.attach_module(RECREATED_COLOUR, recreated_color_module)

    # recreated colour data
    rec_color_data_frame = frame(image_diagram, BACKGROUND, 5, 12, 4, 2)
    rec_color_data_module = RecreatedColourData(rec_color_data_frame, listener)
    listener.attach_module(RECREATED_COLOUR_DATA, rec_color_data_module)

    # new colour
    new_color_frame = frame(image_diagram, BACKGROUND, 7, 3, 7, 3)
    new_color_module = NewColour(new_color_frame, listener)
    listener.attach_module(NEW_COLOUR, new_color_module)

    # new colour data
    new_color_data_frame = frame(image_diagram, BACKGROUND, 9, 12, 3, 2)
    new_color_data_module = NewColourData(new_color_data_frame, listener)
    listener.attach_module(NEW_COLOUR_DATA, new_color_data_module)

    # diagram
    diagram_frame = frame(image_diagram, BACKGROUND, 0, 12, 2, 2)
    diagram_module = Diagram(diagram_frame, listener)
    listener.attach_module(DIAGRAM, diagram_module)

    # histogram
    histogram_frame = frame(image_diagram, BACKGROUND, 0, 6, 8, 6)
    histogram_module = Histogram(histogram_frame, listener)
    listener.attach_module(HISTOGRAM, histogram_module)

    # absorption
    absorption_spec_frame = frame(image_diagram, BACKGROUND, 8, 6, 6, 6)
    absorption_module = AbsorptionSpec(absorption_spec_frame, listener)
    listener.attach_module(ABSORPTION_SPEC, absorption_module)
    
    # Batch Processing
    BP_frame = frame(bp, BACKGROUND, 0, 0, 16, 16)
    BP_module = BP(BP_frame, listener)
    listener.attach_module(BP, BP_module)
    
    circle_frame = frame(circle, BACKGROUND, 0, 0, 16, 16)
    circle_module = Circle(circle_frame, listener)
    listener.attach_module(Circle, circle_module)
    
    rectangle_frame = frame(rectangle, BACKGROUND, 0, 0, 16, 16)
    rectangle_module = Rectangle(rectangle_frame, listener)
    listener.attach_module(Rectangle, rectangle_module)
    
    BS_frame = frame(bs, BACKGROUND, 0, 0, 16, 16)
    BS_module = BS(BS_frame, listener)
    listener.attach_module(BS, BS_module)
    
    measure_frame = frame(measure, BACKGROUND, 0, 0, 16, 16)
    measure_module = Measure(measure_frame, listener)
    listener.attach_module(MEASURE, measure_module)
    
    crops_frame = frame(crop, BACKGROUND, 0, 0, 16, 16)
    crops_module = crops(crops_frame, listener)
    listener.attach_module(crop, crops_module)
    
    SI_frame = frame(spec_invest, BACKGROUND, 0, 0, 16, 16)
    SI_module = SpecInvest(SI_frame, listener)
    listener.attach_module(spec_invest, SI_module)
    
    mda_frame = frame(mda, BACKGROUND, 0, 0, 16, 16)
    mda_module = MDA(mda_frame, listener)
    listener.attach_module(mda, mda_module)
    
    mda2_frame = frame(mda2, BACKGROUND, 0, 0, 16, 16)
    mda2_module = MDA2(mda2_frame, listener)
    listener.attach_module(mda2, mda2_module)
    
    prog_frame = frame(progressions, BACKGROUND, 0, 0, 16, 16)
    prog_module = Progressions(prog_frame, listener)
    listener.attach_module(progressions, prog_module)
    
    pred_frame = frame(prediction, BACKGROUND, 0, 0, 16, 16)
    pred_module = Prediction(pred_frame, listener)
    listener.attach_module(PREDICTION, pred_module)

    # colourbar
    colour_frame = frame(image_diagram, BACKGROUND, 12, 12, 2, 2)
    colour_module = Colour(colour_frame, listener)

    if xSize is not None and ySize is not None:
        window.geometry(str(xSize) + "x" + str(ySize))
    
    window.mainloop()
    

if __name__ == '__main__':
    main()

#Added by Jan Odenthal, University of Heidelberg, odenthal@stud.uni-heidelberg.de

from HyperGuiModules.utility import *
from tensorflow.python.keras.models import load_model
from PIL import Image
import numpy as np
import os
import logging
import glob
from tkinter import filedialog, Toplevel, Label, messagebox, Checkbutton
from scipy.ndimage.filters import gaussian_filter
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import xlsxwriter
import copy
import pickle
import math
import cv2


class Prediction: 
    def __init__(self, prediction_frame, listener):
        self.root = prediction_frame 
        self.listener = listener 
        self.x_vals = np.arange(500, 1000, 5)
        
        self.gini_map = None 
        self.softmax_map = None 
        self.prediction_map = None 
        self.ground_truth_map = None 
        
        self.gini_RGB = None 
        self.softmax_RGB = None 
        self.prediction_RGB = None 
        self.ground_truth_RGB = None 
        self.current_RGB = None 
        self.save_RGB = None 
        self.RGB = None 
        self.tt = "SMGI"
        self.curve_sm = "curve"
        
        self.interactive_absorption_spec_graph = None
        self.tw=None
        
        self.model = None 
        
        self.edge_length_x = None 
        self.edge_length_y = None 
        self.gt_dir = None 
        
        self.avGini = None 
        self.avSm = None 
        self.sdGini = None 
        self.sdSm = None 
        self.accuracy = None 
        
        self.image=None 
        self.legend = None
        self.legAx = None
        self.legend_canvas = None
        self.leg_selection = 0
        self.first_value = 0
        self.second_value = 0
        self.third_value = 0
        self.y_high = 1
        self.y_low = 0
        
        self.output_path = None
        self.drop_down_legVar = StringVar()
        self.drop_down_var2 = StringVar()
        self.drop_down_var_dyn = StringVar()
        self.drop_down_var_stock = StringVar()
        self.model_name = None

        self.drop_down_var = StringVar()
        self.choices = ['1. Prediction', 
                        '2. Groundtruth',
                        '3. RGB',
                        '4. Gini',
                        '5. Softmax']
        
        self.choices2 = ['0. derivative', 
                        '1. derivative',
                        '2. derivative',
                        ]
        
        self.choices_dyn = ['static', 
                        'dynamic']
        
        self.choices_stock = ['thoracic+abdominal',
                              'thoracic',
                            'abdominal',
                            "stomach tube"]

        self.organMaskNames = None
        self.dyn = False

        self.info_file_path = None

        self.gini_slider = None 
        self.softmax_slider = None 
        self.select_gt_folder_button = None 
        self.text_accuracy = None 
        self.gradient = "og"
        self.absorption_spec = None
        self.softmax_dist = None
        self.absorption_spec_gradient1 = None
        self.absorption_spec_gradient2 = None

        self.prediction_graph = None
        self.RGB_graph = None
        self.axes = None 
        self.axes_external = None
        self.interactive_prediciton = None 
        self.interactive_RGB = None 

        self.text_pixel_value = None 

        self.info_label = None 
        self.model_path = None


        
        self.output_path = None
        
        self.g_filter = (3,3,1)
        self.color_dict = dict({'stomach': "#ff1100",
                   'jejunum':"#ff9100",
                   'colon':"#ffdd00",
                   'liver': "#80ff00",
                   'gallbladder':"#04b50f",
                   'pancreas':"#03fff2",
                   'kidney':"#0374ff",
                   'spleen':"#050099",
                   'bladder':"#630505",
                   'omentum':"#9a00ed",
                   'lung': "#ed00c9",
                   'heart':"#ff8fee",
                   'cartilage':"#16e7c5",
                   'bone':"#A35F00",
                   'skin': "#a32121",
                   'muscle': "#4a4a4a",
                   'peritoneum': "#8c7fb8",
                   'vena_cava':"#be17c5",
                   'kidney_with_peritoneum':"#bee7c5",
                   'bile_fluid':"#bee70e",
                   'cloth': '#b1b1b1'})
        
        self.all_colors = [(100,100,100), (0,255,0), (0,0,255), (255,170,0), (255,255,0), (0,255,255), (255,0,255), (255,170,170), (120,120,255), (0,255,120), (255,120,120), (255,255,255), (0,120,170), (50,50,200), (30,50,100), (100,50,30), (200,50,90), (120,90,200), (9, 151, 72), (244, 211, 61), (112, 203, 113), (107, 92, 188), (37, 47, 100), (84, 12, 200), (220,20,60), (255,0,0), (0,128,128), (255,215,0), (245,222,179), (188,143,143), (255,69,0), (94,73,168), (188,133,111), (100, 230, 22)]
        self.organs_to_save = [False]*100
        self.cb_organ = [None]*100
        self.colors=copy.deepcopy(self.all_colors[0:23])
        self.min_centroid_size = 400
        
        self.cursor_class = None
        
        self._init_widgets() 

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widgets(self):
        self._build_gini_slider() 
        self._build_RGB_overlay_slider()
        self._build_softmax_slider() 
        self._build_select_model_button() 
        self._build_info_label()
        self._build_reset_button() 
        self._build_drop_down() 
        self._build_prediction_graph() 
        self._build_RGB_graph() 
        self._build_stats() 
        self._build_pixel_value() 
        self._build_select_gt_folder_button() 
        self._build_accuracy() 
        self._build_legend()
        self._search_stock_model()
        self._build_save_buttons()
        self._build_info_label_gini_softmax()
        self._build_legend_buttons()
        self._build_curve_graph()
        self._build_drop_down2()
        self._build_drop_down_dyn()
        self._build_stock_model_button()
        


    # ----------------------------------------------- BUILDERS (MISC) -------------------------------------------------

    def _build_save_buttons(self):
        make_button(self.root, text="Change Output Folder", command=self.__select_output, row=8, column=0,
                    width=15, height=1, columnspan=1, outer_pady=(0, 5), inner_pady=5)
        make_button(self.root, "Save Image", row=8, column=1, command=self.__save_RGB, inner_padx=10,
                                        inner_pady=5, outer_pady=(0, 5), columnspan=1)
        make_button(self.root, "Save CSV", row=8, column=2, command=self.__save_CSV, inner_padx=10,
                                        inner_pady=5, outer_pady=(0, 5), columnspan=1)
        make_button(self.root, "Save bin. masks\nand tif", row=8, column=3, command=self.__save_masks, inner_padx=10,
                                        inner_pady=5, outer_pady=(0, 5), columnspan=1)
        make_button(self.root, "Specify Save", row=8, column=4, command=self.__open_save_masks_dialog, inner_padx=10,
                                        inner_pady=5, outer_pady=(0, 5), columnspan=1)
    
    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Prediction', command=self.__info, width=8)

    def _build_info_label_gini_softmax(self):
        self.gini_label = TButton(self.root, text="Gini", width=8, command=self.__gini_info)
        Style().configure("TButton", relief="solid", background=tkcolour_from_rgb((255, 255, 255)),
                      bordercolor=tkcolour_from_rgb((0, 0, 0)), borderwidth=2)
        Style().theme_use('default')
        self.gini_label.grid(row=0, column=3)
        
        self.soft_label = TButton(self.root, text="Max of Softmax", width=16, command=self.__soft_info)
        Style().configure("TButton", relief="solid", background=tkcolour_from_rgb((255, 255, 255)),
                      bordercolor=tkcolour_from_rgb((0, 0, 0)), borderwidth=2)
        Style().theme_use('default')
        self.soft_label.grid(row=0, column=4)


    def _build_gini_slider(self): 
        self.gini_slider = make_slider(self.root, "", row=1, rowspan=2, column=3, command=self._build_prediction_graph, columnspan=1, orient = "horizontal")

    def _build_softmax_slider(self): 
        self.softmax_slider = make_slider(self.root, "", row=1, rowspan=2, column=4, command=self._build_prediction_graph, columnspan=1, orient = "horizontal")

    def _build_RGB_overlay_slider(self):
        self.RGB_overlay_slider = make_slider(self.root, "", row=8, column=5, columnspan = 3, command=self._build_prediction_graph, orient = "horizontal")

    
    def _build_reset_button(self): 
        self.reset_button = make_button(self.root, "Reset", row=3, column=3, command=self.__reset, inner_padx=10,
                                        inner_pady=5, columnspan=2)
    

    def _build_drop_down(self): 
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__change_mode)
        self.drop_down_menu.configure(highlightthickness=0, width=20,
                                      anchor='w')
        self.drop_down_menu.grid(column=1, row=0, columnspan=2)
        
    def _build_drop_down_dyn(self): 
        self.drop_down_var_dyn.set(self.choices_dyn[0])
        self.drop_down_menu_dyn = OptionMenu(self.root, self.drop_down_var_dyn, *self.choices_dyn, command=self.__change_dyn)
        self.drop_down_menu_dyn.configure(highlightthickness=0, width=10,
                                      anchor='w')
        self.drop_down_menu_dyn.grid(column=12, row=6, columnspan=2)
        
    def _build_drop_down2(self): 
        self.drop_down_var2.set(self.choices2[0])
        self.drop_down_menu2 = OptionMenu(self.root, self.drop_down_var2, *self.choices2, command=self.__set_der)
        self.drop_down_menu2.configure(highlightthickness=0, width=10,
                                      anchor='w')
        self.drop_down_menu2.grid(column=10, row=6, columnspan=2)
        
        self.lower_text = make_text(self.root, content="Lower: ", bg=tkcolour_from_rgb(BACKGROUND), column=10, row=8,
                                    width=7, columnspan=1, pady=(0, 5))
        self.lower_input = make_entry(self.root, row=8, column=11, width=5, columnspan=1)
        self.lower_input.bind('<Return>', self.__update_upper_lower)
        self.lower_input.insert(END, str(self.y_low))
        
        self.upper_text = make_text(self.root, content="Upper: ", bg=tkcolour_from_rgb(BACKGROUND), column=12, row=8,
                                    width=7, columnspan=1, pady=(0, 5))
        self.upper_input = make_entry(self.root, row=8, column=13, width=5, columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper_lower)
        self.upper_input.insert(END, str(self.y_high))
    
    def _build_select_model_button(self): 
        self.model_info_button = make_button(self.root, text="model-info",
                                                   command=self.__load_info, inner_padx=10, inner_pady=5,
                                                   row=2, column=0, width=11)
        self.select_model_button = make_button(self.root, text="Custom model",
                                                   command=self.__select_model, inner_padx=10, inner_pady=5,
                                                   row=3, column=0, width=11)
        
    def _build_stock_model_button(self):
        self.drop_down_var_stock.set(self.choices_stock[0])
        self.drop_down_menu_stock = OptionMenu(self.root, self.drop_down_var_stock, *self.choices_stock, command=self.__set_stock)
        self.drop_down_menu_stock.configure(highlightthickness=0, width=10,
                                      anchor='w')
        self.drop_down_menu_stock.grid(column=0, row=1, columnspan=1)
        
    def _build_select_gt_folder_button(self): 
        self.select_gt_folder_button = make_button(self.root, text="Select GT-Folder",
                                                   command=self.__select_gt_folder, inner_padx=10, inner_pady=5,
                                                    row=4, column=0, rowspan=1, width=11)
        
    def _build_pixel_value(self, event=None): 
        string="Pixelvalues"
        if event is not None:
            pos = self.axes.get_position()
            axesX0 = pos.x0
            axesY0 = pos.y0
            axesX1 = pos.x1
            axesY1 = pos.y1
            canvas = event.widget
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            canvas.canvasx
            cx = canvas.winfo_rootx()
            cy = canvas.winfo_rooty()
            minX=width*axesX0
            maxX=width*axesX1
            minY=height*axesY0
            maxY=height*axesY1
            axWidth=maxX-minX
            conversionFactor = 640/axWidth
            Xc=int((event.x-minX)*conversionFactor)
            Yc=int((event.y-minY)*conversionFactor)
            if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480 and self.gini_map is not None and self.softmax_map is not None:
                X  = np.rot90(self.listener.data_cube) 
                #index = np.argmax(self.prediction_map[Yc,Xc,:])
                #index2 = np.argmax(self.ground_truth_map[Yc,Xc,:]) 
                gini = self.gini_map[Yc, Xc]
                softmax = self.softmax_map[Yc, Xc]
                self.softmax_dist = self.prediction_map[Yc, Xc, :]
                self.cursor_class = np.argmax(self.prediction_map[Yc, Xc, :])
                string = 'x={:.0f}, y={:.0f}; S={:.02f}, G={:.02f}'.format(Xc, Yc, softmax, gini)
                string2 = 'Softmax={:.02f}, Gini={:.02f}'.format(softmax, gini)
                string3 = 'Prediciton: {}'.format(self.organMaskNames[self.cursor_class])
                self.absorption_spec = X[Yc, Xc, :]
                self.absorption_spec_gradient1 = np.gradient(self.absorption_spec)
                self.absorption_spec_gradient2 = np.gradient(self.absorption_spec_gradient1)
                self._build_curve_graph()
                x = cx + event.x
                y = cy + event.y-20
                if self.interactive_prediciton is not None:
                    if self.tt is "SMGI":
                        if self.tw is not None:
                            self.tw.destroy()
                        self.tw = Toplevel(self.root)
                        self.tw.wm_overrideredirect(True)
                        self.tw.wm_geometry("+%d+%d" % (x, y))
                        label = Label(self.tw, text=string2, justify='left',
                                           background='yellow', relief='solid', borderwidth=1,
                                           font=("times", "8", "normal"))
                        label.pack(ipadx=1)
                    if self.tt is "Pred":
                        if self.tw is not None:
                            self.tw.destroy()
                        self.tw = Toplevel(self.root)
                        self.tw.wm_overrideredirect(True)
                        self.tw.wm_geometry("+%d+%d" % (x, y))
                        label = Label(self.tw, text=string3, justify='left',
                                           background='yellow', relief='solid', borderwidth=1,
                                           font=("times", "8", "normal"))
                        label.pack(ipadx=1)
            else:
                if self.tw is not None:
                        self.tw.destroy()
        self.text_pixel_value = make_text(self.root, content=string,
                                  bg=tkcolour_from_rgb(BACKGROUND), column=1, row=1, width=28, columnspan=2, 
                                  state=NORMAL)
    
    def _build_pixel_value_external(self, event=None): 
        string="Pixelvalues"
        if event is not None:
            pos = self.axes_external.get_position()
            axesX0 = pos.x0
            axesY0 = pos.y0
            axesX1 = pos.x1
            axesY1 = pos.y1
            canvas = event.widget
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            minX=width*axesX0
            maxX=width*axesX1
            minY=height*axesY0
            maxY=height*axesY1
            axWidth=maxX-minX
            conversionFactor = 640/axWidth
            Xc=int((event.x-minX)*conversionFactor)
            Yc=int((event.y-minY)*conversionFactor)
            if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480 and self.gini_map is not None and self.softmax_map is not None:
                #index = np.argmax(self.prediction_map[Yc,Xc,:])
                #index2 = np.argmax(self.ground_truth_map[Yc,Xc,:]) 
                gini = self.gini_map[Yc, Xc]
                softmax = self.softmax_map[Yc, Xc]
                string = 'x={:.0f}, y={:.0f}; S={:.02f}, G={:.02f}'.format(Xc, Yc, softmax, gini)
        self.text_pixel_value = make_text(self.root, content=string,
                                  bg=tkcolour_from_rgb(BACKGROUND), column=1, row=1, width=28, columnspan=2, 
                                  state=NORMAL)
        
    def _build_accuracy(self): 
        string="ACCURACY"
        if self.accuracy is not None:
            string = 'ACCURACY: ' + str(self.accuracy)
        self.text_accuracy = make_text(self.root, content=string,
                                  bg=tkcolour_from_rgb(BACKGROUND), column=1, row=2, width=16, columnspan=2,
                                  state=NORMAL)
        
    def _build_legend(self):
        axcolor = 'lightgoldenrodyellow'
        self.legend = Figure(figsize=(3.5, 3))
        self.legend.tight_layout()
        organMaskNamesLeft = []
        organMaskNamesRight = []
        if self.organMaskNames is not None:
            if len(self.organMaskNames) > 24:
                print("Too Many classes!")
                pass
            elif len(self.organMaskNames) >12 and len(self.organMaskNames) <=24:
                organMaskNamesLeft = self.organMaskNames[0:12]
                organMaskNamesRight = self.organMaskNames[12::]
            elif len(self.organMaskNames) <= 12:
                organMaskNamesLeft = self.organMaskNames
            self.legend_elementsLeft = []
            for ii in np.arange(len(organMaskNamesLeft)):
                self.legend_elementsLeft.append(Line2D([0], [0], marker='o', color='w', label=organMaskNamesLeft[ii], markerfacecolor=(self.colors[ii][0]/255, self.colors[ii][1]/255, self.colors[ii][2]/255), markersize=15))
            self.legend_elementsRight = []
            for ii in np.arange(len(organMaskNamesRight)):
                self.legend_elementsRight.append(Line2D([0], [0], marker='o', color='w', label=organMaskNamesRight[ii], markerfacecolor=(self.colors[ii+12][0]/255, self.colors[ii+12][1]/255, self.colors[ii+12][2]/255), markersize=15))
            if len(self.legend_elementsRight) > 0:
                gs = self.legend.add_gridspec(1, 2)
                self.legAxRight = self.legend.add_subplot(gs[0,1])
                self.legAxRight.legend(handles=self.legend_elementsRight, loc='center') 
                self.legAxRight.axis('off') 
            else:
                gs = self.legend.add_gridspec(1, 1)
            self.legAxLeft = self.legend.add_subplot(gs[0,0])
            self.legAxLeft.legend(handles=self.legend_elementsLeft, loc='center') 
            self.legAxLeft.axis('off') 
        self.legend_canvas = FigureCanvasTkAgg(self.legend, master=self.root)
        self.legend_canvas.draw()
        self.legend_canvas.get_tk_widget().grid(column=10, row=0, columnspan=6, rowspan=5)
        
    def _build_legend_buttons(self):
        if self.organMaskNames is not None:
            self.drop_down_legVar.set(self.organMaskNames[0])
            self.drop_down_legend = OptionMenu(self.root, self.drop_down_legVar, *self.organMaskNames, command=self.__change_leg_selection)
        else:
            self.drop_down_legend = OptionMenu(self.root, self.drop_down_legVar, [], command=self.__change_leg_selection)
        self.drop_down_legend.configure(highlightthickness=0, width=12,
                                      anchor='w')
        self.drop_down_legend.grid(column=6, row=0, columnspan = 3, pady=(5, 5))
        
        self.slider_r = make_slider(self.root, "", row=0, rowspan=5, column=6, command=self.__update_preview, columnspan=1, from_=0, to=255)
        self.slider_b = make_slider(self.root, "", row=0, rowspan=5, column=7, command=self.__update_preview, columnspan=1, from_=0, to=255)
        self.slider_g = make_slider(self.root, "", row=0, rowspan=5, column=8, command=self.__update_preview, columnspan=1, from_=0, to=255)

        self.save_color_button = make_button(self.root, "Save", column=8, row=4, width=3, command=self.__save_color, inner_padx=5,
                                        inner_pady=5, columnspan=1)
        self.change_color_button = make_button(self.root, "Set", column=7, row=4, width=3, command=self.__set_color, inner_padx=5,
                                        inner_pady=5, columnspan=1)
        
        self.preview = Figure(figsize=(0.3, 0.3))
        self.prevAx = self.preview.add_subplot(111)
        self.prev_canvas = FigureCanvasTkAgg(self.preview, master=self.root)
        self.prevAx.set_facecolor((self.slider_r.get()/255, self.slider_b.get()/255, self.slider_g.get()/255))
        self.prevAx.set_position([0, 0, 1, 1])
        self.prev_canvas.draw()
        self.prev_canvas.get_tk_widget().grid(column=6, row=4, columnspan=1, rowspan=1, ipady=0, ipadx=0)

    def _build_stats(self): 

        # mean Gini
        self.mean_text_gini = make_text(self.root, content="GINI = " + str(self.avGini),
                                   bg=tkcolour_from_rgb(BACKGROUND), column=1, row=3, width=12, columnspan=1,
                                   state=NORMAL)
        # standard deviation Gini
        self.sd_text_gini = make_text(self.root, content="SD = " + str(self.sdGini), bg=tkcolour_from_rgb(BACKGROUND),
                                 column=2, row=3, width=10, columnspan=1, state=NORMAL)
        
        # mean SM
        self.mean_text_sm = make_text(self.root, content="SOFT = " + str(self.avSm),
                                   bg=tkcolour_from_rgb(BACKGROUND), column=1, row=4, width=12, columnspan=1,
                                   state=NORMAL)
        # standard deviation SM
        self.sd_text_sm = make_text(self.root, content="SD = " + str(self.sdSm), bg=tkcolour_from_rgb(BACKGROUND),
                                 column=2, row=4, width=10, columnspan=1, state=NORMAL)


    # ---------------------------------------------- BUILDERS (GRAPH) ------------------------------------------------

    def _build_prediction_graph(self, event=None):
        # create canvas
        alpha = self.RGB_overlay_slider.get()/100
        self.prediction_graph = Figure(figsize=(5.34, 4))
        self.axes = self.prediction_graph.add_subplot(111)
        self.axes.set_aspect(2/3)
        self.prediction_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        self.axes.get_yaxis().set_visible(False)
        self.axes.get_xaxis().set_visible(False)
        if self.current_RGB is not None:
            softmax = self.softmax_slider.get()/100
            gini = self.gini_slider.get()/100
            newImage=np.copy(self.current_RGB)
            if self.gini_map is not None and self.softmax_map is not None:
                newImage[np.where(self.gini_map<gini)]=[0,0,0]
                newImage[np.where(self.softmax_map<softmax)]=[0,0,0]                
            im=Image.fromarray(newImage.astype('uint8'), 'RGB')
            self.image = self.axes.imshow(im, interpolation='none')
            self.save_RGB = im
            if self.RGB is not None:
                self.axes.imshow(self.RGB, alpha = alpha)
        # draw figure
        self.prediction_graph.tight_layout()
        self.interactive_prediciton = FigureCanvasTkAgg(self.prediction_graph, master=self.root)
        self.interactive_prediciton.draw()
        self.interactive_prediciton.get_tk_widget().grid(column=3, row=5, columnspan=6, rowspan=2, ipady=0, ipadx=0)
        self.interactive_prediciton.get_tk_widget().bind('<Motion>', self._build_pixel_value)
        self.interactive_prediciton.get_tk_widget().bind('<Button-2>', self.__pop_up_prediction)
        self.interactive_prediciton.get_tk_widget().bind('<Button-1>', self.__toggle_tooltip)
        self.interactive_prediciton.get_tk_widget().bind('<Leave>', self.__tooltip_destroy)
        self.accuracy=self.__calc_accuracy()
        self._build_accuracy()
        
    def _build_RGB_graph(self, event=None):
        # create canvas
        self.RGB_graph = Figure(figsize=(5.34, 4))
        self.axes = self.RGB_graph.add_subplot(111)
        self.axes.set_aspect(2/3)
        self.RGB_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        self.axes.get_yaxis().set_visible(False)
        self.axes.get_xaxis().set_visible(False)
        if self.RGB is not None:
            im=Image.fromarray(self.RGB.astype('uint8'), 'RGB')
            self.image = self.axes.imshow(im, interpolation='none')
        # draw figure
        self.RGB_graph.tight_layout()
        self.interactive_RGB = FigureCanvasTkAgg(self.RGB_graph, master=self.root)
        self.interactive_RGB.draw()
        self.interactive_RGB.get_tk_widget().grid(column=0, row=5, columnspan=3, rowspan=2, ipady=0, ipadx=0,
                                                        pady=0)
        self.interactive_RGB.get_tk_widget().bind('<Button-2>', self.__pop_up_RGB)
        
    def _build_curve_graph(self):
        self.interactive_absorption_spec_graph = Figure(figsize=(3.8, 3))
        self.axes_abs = self.interactive_absorption_spec_graph.add_subplot(111)
        self.interactive_absorption_spec_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        
        if self.curve_sm == "curve":
            # plot absorption spec
            y_low = self.y_low
            y_high = self.y_high
            if self.absorption_spec is not None:
                if self.gradient == "og":
                    y_vals = self.absorption_spec
                elif self.gradient == "first":
                    y_vals = self.absorption_spec_gradient1
                elif self.gradient == "second":
                    y_vals = self.absorption_spec_gradient2
                self.axes_abs.plot(self.x_vals, y_vals, '-', lw=0.5)
                self.axes_abs.grid(linestyle=':', linewidth=0.5)
            if y_low is not None and y_high is not None:
                factor = (y_high - y_low) * 0.05
                y_low -= factor
                y_high += factor
            self.interactive_absorption_spec_graph.set_tight_layout(True)
            self.interactive_absorption_spec_graph.tight_layout()
            #self.axes_abs.set_xlim(left=0, right=1000)
            if not self.dyn:
                self.axes_abs.set_ylim(bottom=self.y_low, top=self.y_high)
            
            #commas and non-scientific notation
            self.axes_abs.ticklabel_format(style='plain')
            self.axes_abs.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
            self.axes_abs.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))

        elif self.curve_sm == "SM":
            if self.softmax_dist is not None:
                self.axes_abs.bar(np.arange(self.softmax_dist.shape[0]), self.softmax_dist, color = [[tup_element/255 for tup_element in tup] for tup in self.colors[0:self.softmax_dist.shape[0]]])
                self.axes_abs.grid(linestyle=':', linewidth=0.5)
                self.axes_abs.set_ylim(bottom=0, top=1)
                self.axes_abs.set_xticks(np.arange(self.softmax_dist.shape[0]))
                x_tick_labels = [string[0:3] for string in self.organMaskNames]
                self.axes_abs.set_xticklabels(x_tick_labels, rotation = 90)
          
        # draw figure
        self.interactive_absorption_spec = FigureCanvasTkAgg(self.interactive_absorption_spec_graph, master=self.root)
        self.interactive_absorption_spec.draw()
        self.interactive_absorption_spec.get_tk_widget().grid(column=10, row=5, columnspan=4, rowspan=1)
        self.interactive_absorption_spec.get_tk_widget().bind('<Button-1>', self.__toggle_softmax_curve)
        
    @staticmethod
    def format_axis(x, _):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 4))

    # ------------------------------------------------- UPDATERS --------------------------------------------------
        
    def update_cube(self):
        self.__update_data()
        
    def update_output_path(self):
        self.output_path = os.path.dirname(self.listener.dc_path) + '/'+self.listener.output_folder_hypergui
    
    def update_prediction(self): 
        self._build_prediction_graph()
    
    def update_RGB(self, new_data):
        self.RGB = new_data
        self._build_RGB_graph()
    
    # ------------------------------------------------- Prediction-Related --------------------------------------------------
        
    def _draw_prediction(self, prediction, x, y):
      prediction=np.reshape(prediction, (x, y, prediction.shape[1]))
      predictedClasses=np.argmax(prediction, axis=2) #array of shape [rows, columns]
      emptyX=np.where(np.sum(prediction, axis=2)==0)[0]#If all classes are 0, argmax returns 0 for the corresponding pixel. However, 0 also means background (foil, color: gray). Therfore, we get Coordinates of all pixels having 0 for all classes and set them all to black afterwards, to distinguish them from background.
      emptyY=np.where(np.sum(prediction, axis=2)==0)[1]
      imageArray=np.zeros((predictedClasses.shape[0], predictedClasses.shape[1],3)) # array of shape [rows, columns, colorChannels]
      for jj in range(prediction.shape[2]):#For each class (organ)...
          if(jj==0):
              color=self.colors[0] #...pick a RGB-Value; i.e. Gray
          elif(jj==1):
              color=self.colors[1]
          elif(jj==2): 
              color=self.colors[2]                   
          elif(jj==3):
              color=self.colors[3]
          elif(jj==4):
              color=self.colors[4]
          elif(jj==5):
              color=self.colors[5]
          elif(jj==6):
              color=self.colors[6]
          elif(jj==7):
              color=self.colors[7]
          elif(jj==8): 
              color=self.colors[8]
          elif(jj==9):    
              color=self.colors[9]
          elif(jj==10):
              color=self.colors[10]
          elif(jj==11):
              color=self.colors[11]
          elif(jj==12):
              color=self.colors[12]
          elif(jj==13):
              color=self.colors[13]
          elif(jj==14):
              color=self.colors[14]
          elif(jj==15):
              color=self.colors[15]
          elif(jj==16):
              color=self.colors[16]
          elif(jj==17):
              color=self.colors[17]
          elif(jj==18):
              color=self.colors[18]
          elif(jj==19):
              color=self.colors[19]
          elif(jj==20):
              color=self.colors[20]
          elif(jj==21):
              color=self.colors[21]
          elif(jj==22):
              color=self.colors[22]
          elif(jj==23):
              color=self.colors[23]
          x=np.where(predictedClasses==jj)[0] #... and set the color of all pixels predicted as the corresponding class (organ) to this RGB-Value.
          y=np.where(predictedClasses==jj)[1]
          imageArray[x,y,:]=color
      imageArray[emptyX,emptyY,:]=(0,0,0) #Disinguish between "background" (gray) and none; set none black
      return imageArray
    
    def _giniMap(self, pred): 
        giniMap=np.zeros((pred.shape[0], pred.shape[1]))
        row=np.arange(pred.shape[0])
        column=np.arange(pred.shape[1])
        pred = np.sort(pred, axis=2) #values must be sorted
        n = pred.shape[2]#number of array elements
        width=1/n
        x=np.arange(0,1,width)
        pred=np.cumsum(pred, axis=2)
        AUC = np.trapz(pred, axis=2, dx=width)
        ABC = 0.5-AUC
        giniMap = ABC*2
        return giniMap

    # -------------------------------------------------- OTHER ---------------------------------------------------
 
    def __calc_accuracy(self, thresh = True):
        if self.prediction_map is not None and self.ground_truth_map is not None:
            
            if thresh:
                gini = self.gini_slider.get()/100
                softmax = self.softmax_slider.get()/100
            else:
                gini = 0
                softmax =0
            
            flatPred = self.prediction_map.reshape(480*640, self.prediction_map.shape[2])
            
            visibleGT = np.copy(self.ground_truth_map)
            visibleGT[np.where(self.gini_map<gini)[0], np.where(self.gini_map<gini)[1],0] = 1
            visibleGT[np.where(self.softmax_map<softmax)[0], np.where(self.softmax_map<softmax)[1],0] = 1
            flatGT = visibleGT.reshape(480*640, visibleGT.shape[2])
            weights = flatGT[...,0]==0
            weights[np.where(np.sum(flatPred, axis=1)==0)] = False
            maxPixels=np.sum(weights)#Number of unambigiously-labeld Pixels
            if(maxPixels!=0):
                accuracy=np.sum(np.multiply((np.argmax(flatPred, axis=1)==np.argmax(flatGT, axis=1)),weights))/maxPixels
            else:
                accuracy=0
            return accuracy
        else:
            return None
        
    def __calc_performance(self, thresh = True):
        if thresh:
                gini = self.gini_slider.get()/100
                softmax = self.softmax_slider.get()/100
        else:
            gini = 0
            softmax =0
        
        flatPred = self.prediction_map.reshape(480*640, self.prediction_map.shape[2])
        
        visibleGT = np.copy(self.ground_truth_map)
        visibleGT[np.where(self.gini_map<gini)[0], np.where(self.gini_map<gini)[1],0] = 1
        visibleGT[np.where(self.softmax_map<softmax)[0], np.where(self.softmax_map<softmax)[1],0] = 1
        flatGT = visibleGT.reshape(480*640, visibleGT.shape[2])
        flatGM= self.gini_map.reshape(480*640)
        flatMOS= self.softmax_map.reshape(480*640)
        weights = flatGT[...,0]==0
        weights[np.where(np.sum(flatPred, axis=1)==0)] = False
        maxPixels=np.sum(weights)#Number of unambigiously-labeld Pixels
        if(maxPixels!=0):
            accuracy=np.sum(np.multiply((np.argmax(flatPred, axis=1)==np.argmax(flatGT, axis=1)),weights))/maxPixels
            self.data_array=np.empty((len(self.organMaskNames),9))
            for ii in range(len(self.organMaskNames)):
                meanGini = np.mean(flatGM[np.argmax(flatPred, axis=1)==ii])
                meanMOS= np.mean(flatMOS[np.argmax(flatPred, axis=1)==ii])
                percInPred = np.sum(np.multiply(np.argmax(flatPred, axis=1)==ii,weights))/maxPixels
                if self.gt_dir is not None:
                    sens=np.sum(np.multiply(np.logical_and(np.argmax(flatPred, axis=1)==np.argmax(flatGT, axis=1), np.argmax(flatPred, axis=1)==ii),weights))/np.sum(np.multiply(np.argmax(flatGT, axis=1)==ii,weights))
                    fnr=np.sum(np.multiply(np.logical_and(np.argmax(flatPred, axis=1)!=np.argmax(flatGT, axis=1), np.argmax(flatGT, axis=1)==ii),weights))/np.sum(np.multiply(np.argmax(flatGT, axis=1)==ii,weights))
                    spec=np.sum(np.multiply(np.logical_and(np.argmax(flatPred, axis=1)!=ii, np.argmax(flatGT, axis=1)!=ii),weights))/np.sum(np.multiply(np.argmax(flatGT, axis=1)!=ii,weights))
                    rpr=np.sum(np.multiply(np.logical_and(np.argmax(flatPred, axis=1)==np.argmax(flatGT, axis=1), np.argmax(flatPred, axis=1)==ii),weights))/np.sum(np.multiply(np.argmax(flatPred, axis=1)==ii,weights))
                    fpf=np.sum(np.multiply(np.logical_and(np.argmax(flatPred, axis=1)!=np.argmax(flatGT, axis=1), np.argmax(flatPred, axis=1)==ii),weights))/np.sum(np.multiply(np.argmax(flatPred, axis=1)==ii,weights))
                    percInGT =np.sum(np.multiply(np.argmax(flatGT, axis=1)==ii,weights))/maxPixels
                    row=[meanGini, meanMOS, sens, fnr, spec, rpr, fpf, percInPred, percInGT]
                else:
                    row = [meanGini, meanMOS, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN,  percInPred, np.NaN]
                self.data_array[ii, :]=row
        
    
    def __flat(self, X): 
        X = np.reshape(X, (X.shape[0]*X.shape[1], X.shape[2]))
        return X
        
    def __get_path_to_dir(self, title):  
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askopenfilename(parent=self.root, title=title, initialdir=p, filetypes=[("H5-File", "*.h5")])
        else:
            path = filedialog.askopenfilename(parent=self.root, title=title, filetypes=[("H5-File", "*.h5")])
        return path
    
    def __get_path_to_dir2(self, title):  
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askdirectory(parent=self.root, title=title, initialdir=p)
        else:
            path = filedialog.askdirectory(parent=self.root, title=title)
        return path
    
    def __info(self): 
        info = self.listener.modules[INFO].predic_info
        title = "Prediction Information"
        make_info(title=title, info=info)
        
    def __soft_info(self):
        info = self.listener.modules[INFO].soft_info
        title = "Max of Softmax Information"
        make_info(title=title, info=info)
        
    def __gini_info(self):
        info = self.listener.modules[INFO].gini_info
        title = "Gini Information"
        make_info(title=title, info=info)
    
    def __load_model(self, path):  
        self.model_path = os.path.dirname(path)
        self.__read_legend(os.path.dirname(path) + "/legend")
        self.model=load_model(path)
        self.edge_length_y=self.model.input.shape[1]
        self.edge_length_x=self.model.input.shape[2]
        self.__update_data()
        self.model_name = os.path.basename(os.path.normpath(path))
        if os.path.exists(os.path.dirname(path) + "/batch_info.txt"):
            self.info_file_path = os.path.dirname(path) + "/batch_info.txt"
        else:
            self.info_file_path = None
    
    def __select_model(self):       
        dc_dir_path = self.__get_path_to_dir("Please select a .h5 file")
        self.__load_model(dc_dir_path)
        
    def __select_gt_folder(self): 
        self.gt_dir = self.__get_path_to_dir2("Please select a directory")
        self.__update_data()

    def __update_data(self): 
        if self.model is not None and self.listener.data_cube is not None:
            self.output_path = os.path.dirname(self.listener.dc_path) + '/'+self.listener.output_folder_hypergui
            X  = np.rot90(self.listener.data_cube) 
            X = gaussian_filter(X, self.g_filter)
            imageArrayPred = np.zeros((480, 640, 3))
            pred = np.zeros((480, 640, self.model.output.shape[2]))
            for ii in range(((int)(480/self.edge_length_y))):
                yMin=ii*self.edge_length_y
                yMax=yMin+self.edge_length_y
                for jj in range(((int)(640/self.edge_length_x))):
                    xMin=jj*self.edge_length_x
                    xMax=xMin+self.edge_length_x
                    xChunk=X[yMin:yMax, xMin:xMax,:]
                    xChunk=xChunk[None]
                    predChunk=self.model.predict(xChunk)
                    pred[yMin:yMax, xMin:xMax,:]=np.reshape(predChunk, (self.edge_length_y, self.edge_length_x, self.model.output.shape[2]))
                    imageArrayPred[yMin:yMax, xMin:xMax,:]=self._draw_prediction(predChunk[0], self.edge_length_y, self.edge_length_x)
            if jj*self.edge_length_x<640:
                x_vis = 640-(jj*self.edge_length_x)
                xMin = 640-self.edge_length_x
                xMax = 640
                for ii in range(((int)(480/self.edge_length_y))):
                    yMin=ii*self.edge_length_y
                    yMax=yMin+self.edge_length_y
                    xChunk=X[yMin:yMax, xMin:xMax,:]
                    xChunk=xChunk[None]
                    predChunk=self.model.predict(xChunk)
                    pred[yMin:yMax, xMin:xMax,:]=np.reshape(predChunk, (self.edge_length_y ,self.edge_length_x, self.model.output.shape[2]))
                    imageArrayPred[yMin:yMax, xMin:xMax,:]=self._draw_prediction(predChunk[0], self.edge_length_y, self.edge_length_x)
            self.prediction_map = pred
            self.prediction_RGB = Image.fromarray(imageArrayPred.astype('uint8'), 'RGB')
            self.gini_map = self._giniMap(pred)
            self.gini_RGB = Image.fromarray((np.moveaxis(np.tile(self.gini_map,(3,1,1)),0,-1)*255).astype('uint8'),'RGB')
            self.softmax_map = np.max(pred, axis=2)
            self.softmax_RGB = Image.fromarray((np.moveaxis(np.tile(self.softmax_map,(3,1,1)),0,-1)*255).astype('uint8'),'RGB')
            self.current_RGB = self.prediction_RGB
            self.avGini=np.mean(self.gini_map) 
            self.avSm=np.mean(self.softmax_map) 
            self.sdGini=np.std(self.gini_map) 
            self.sdSm=np.std(self.softmax_map)
            if self.gt_dir is not None:
                string = self.listener.dc_path.split("/")[-2]
                files = glob.glob(self.gt_dir+"/"+string+"_Y.npy")
                if len(files)==1:
                    file=files[0]
                    Y  = np.load(file)
                    self.ground_truth_map = Y
                    self.ground_truth_RGB=self._draw_prediction(self.__flat(Y), 480, 640)
                else:
                    self.ground_truth_RGB = np.zeros((480, 640, 3))   
                    self.ground_truth_map = np.zeros((480, 640, self.model.output.shape[2])) 
            else:
                self.ground_truth_RGB = np.zeros((480, 640, 3))   
                self.ground_truth_map = np.zeros((480, 640, self.model.output.shape[2]))     
            self._build_stats()
            self.update_prediction()
        
    def __change_mode(self, event): 
        choice = self.drop_down_var.get()[:2]
        if choice == '1.':
            self.current_RGB = self.prediction_RGB
        elif choice == '2.':
            self.current_RGB = self.ground_truth_RGB
        elif choice == '3.':
            self.current_RGB = self.RGB
        elif choice == '4.':
            self.current_RGB = self.gini_RGB
        elif choice == '5.':
            self.current_RGB = self.softmax_RGB
        self.update_prediction()
    
    def __change_dyn(self, event):
        choice = self.drop_down_var_dyn.get()
        if choice == 'dynamic':
            self.dyn = True
        elif choice == 'static':
            self.dyn = False
            
    def __change_leg_selection(self, event): 
        choice = self.drop_down_legVar.get()
        self.leg_selection = self.organMaskNames.index(choice) 
        
    def __update_preview(self, event=None):
        a = self.slider_r.get()/255
        b= self.slider_b.get()/255
        c = self.slider_g.get()/255
        self.prevAx.set_facecolor((a, b, c))
        self.prev_canvas.draw()
        self.prev_canvas.get_tk_widget().grid(column=6, row=4, columnspan=1, rowspan=1, ipady=0, ipadx=0,
                                                        pady=0)

    def __pop_up_prediction(self, event):
        w, i, ax= make_popup_image_external(self.prediction_graph, graphsize=(9, 9))
        self.axes_external = ax
        i.get_tk_widget().bind('<Motion> ', self._build_pixel_value_external)
        
    def __pop_up_RGB(self, event):        
        w, i, ax= make_popup_image_external(self.RGB_graph, graphsize=(9, 9))
        self.axes_external = ax
        i.get_tk_widget().bind('<Motion> ', self._build_pixel_value_external)
    
    def __set_color(self):
        a = self.slider_r.get()/255
        b= self.slider_b.get()/255
        c = self.slider_g.get()/255
        code = (int(255*a), int(255*b), int(255*c))
        self.colors[self.leg_selection] = code
        self._build_legend()
        self.__update_data()
        self.__update_preview()
        self.__reset_color_slider()

    def __reset(self):
        self.gini_slider.set(0)
        self.softmax_slider.set(0)
        self._build_prediction_graph()
        
    def __reset_color_slider(self):
        self.slider_r.set(0)
        self.slider_b.set(0)
        self.slider_g.set(0)
        
    def __select_output(self):
        title = "Please select an output folder."
        self.output_path = filedialog.askdirectory(parent=self.root, title=title)
    
    def __get_naming_info(self):
        model = self.model_name[0:-3]
        mode = self.drop_down_var.get()[3::]
        gini = self.gini_slider.get()/100
        sm = self.softmax_slider.get()/100
        return "_prediction_" + mode + "_gini_thresh_" + str(gini) + "_softmax_thresh_" + str(sm) + "_model_" + model
    
    def __save_RGB(self):
        yn = messagebox.askquestion ('Verify','Save with Legend?',icon = 'warning')
        if yn == "yes":
            self.__save_RGB_with_legend()
        else:
            self.__save_RGB_wo_legend()
        
    def __save_RGB_wo_legend(self):
        if self.output_path is None or self.output_path == '':
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        elif self.save_RGB is None:
            messagebox.showerror("Error", "Please generate a prediction to save.")
        else:
            yn = messagebox.askquestion ('Verify','Save with RGB-Overlay?',icon = 'warning')
            if not os.path.exists(self.output_path):
                os.mkdir(self.output_path)
            output_path = self.output_path + "/" + self.__get_naming_info() + '.png'
            plt.clf()
            axes = plt.subplot(111)
            axes.imshow(self.save_RGB)
            if yn == "yes":
                alpha = self.RGB_overlay_slider.get()/100
                axes.imshow(self.RGB, alpha = alpha)
            axes.get_yaxis().set_visible(False)
            axes.get_xaxis().set_visible(False)
            axes.axis('off')
            DPI = plt.gcf().get_dpi()
            plt.gca().set_position([0, 0, 1, 1])
            plt.gca().patch.set_visible(False)
            plt.gcf().patch.set_visible(False)
            plt.gcf().set_size_inches(640.0/float(DPI),480.0/float(DPI))
            plt.savefig(output_path)
            plt.clf()
            
    def __set_der(self, event = None):
        choice = self.drop_down_var2.get()[0]
        if choice == '0':
            self.gradient = "og"
        elif choice == '1':
            self.gradient = "first"
        elif choice == '2':
            self.gradient = "second"
        self.update_prediction()
        
            
    def __save_RGB_with_legend(self):
        
        if self.output_path is None or self.output_path == '':
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        elif self.save_RGB is None:
            messagebox.showerror("Error", "Please generate a prediction to save.")
        else:
            yn = messagebox.askquestion ('Verify','Save with RGB-Overlay?',icon = 'warning')
            if not os.path.exists(self.output_path):
                os.mkdir(self.output_path)
            output_path = self.output_path + "/" + self.__get_naming_info() + '_with_legend.png'
            logging.debug("SAVING IMAGE" + output_path)
            plt.clf()
            if len(self.legend_elementsRight) >0:
                axes = plt.subplot(1,3,1)
                axes_legend1 = plt.subplot(1,3,2)
                axes_legend1.legend(handles=self.legend_elementsLeft, loc='center left', prop={'size': 14}) 
                axes_legend1.axis('off') 
                
                axes_legend2 = plt.subplot(1,3,3)
                axes_legend2.legend(handles=self.legend_elementsRight, loc='center left', prop={'size': 14}) 
                axes_legend2.axis('off') 
                                
                axes.imshow(self.save_RGB)
                if yn == "yes":
                    alpha = self.RGB_overlay_slider.get()/100
                    axes.imshow(self.RGB, alpha = alpha)
                axes.get_yaxis().set_visible(False)
                axes.get_xaxis().set_visible(False)
            
                axes.set_position([0, 0, 2/4, 1])
                axes.axis('off')
                axes.patch.set_visible(False)
                axes_legend1.set_position([2/4, 0, 3/4 , 1])
                axes_legend1.patch.set_visible(False)
                axes_legend1.axis('off')
                
                axes_legend2.set_position([3/4, 0, 1 , 1])
                axes_legend2.patch.set_visible(False)
                axes_legend2.axis('off')
                
                
                plt.gcf().patch.set_visible(False)
                
                fig = plt.gcf()
                DPI = fig.get_dpi()
                fig.set_size_inches(640.0/float(DPI) + 640.0/float(DPI), 480.0/float(DPI))
                plt.savefig(output_path)
                plt.clf()
            else:
                axes = plt.subplot(1,2, 1)
                axes_legend = plt.subplot(1,2,2)
                axes_legend.legend(handles=self.legend_elementsLeft, loc='center left', prop={'size': 14}) 
                axes_legend.axis('off') 
                axes.imshow(self.save_RGB)
                if yn == "yes":
                    alpha = self.RGB_overlay_slider.get()/100
                    axes.imshow(self.RGB, alpha = alpha)
                axes.get_yaxis().set_visible(False)
                axes.get_xaxis().set_visible(False)
            
                axes.set_position([0, 0, 2/3, 1])
                axes_legend.set_position([2/3, 0, 1 , 1])
                axes.axis('off')
                axes_legend.axis('off')
                axes.patch.set_visible(False)
                axes_legend.patch.set_visible(False)
                
                plt.gcf().patch.set_visible(False)
                
                fig = plt.gcf()
                DPI = fig.get_dpi()
                fig.set_size_inches(640.0/float(DPI) + 320.0/float(DPI), 480.0/float(DPI))
                plt.savefig(output_path)
                plt.clf()
    
    def __save_CSV(self):
        if self.output_path is None or self.output_path == '':
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        elif self.save_RGB is None:
            messagebox.showerror("Error", "Please generate an optical spectrum to save.")
        else:
            if not os.path.exists(self.output_path):
                os.mkdir(self.output_path)
            outputs = np.array([])
            cap = np.array([])
            if self.gt_dir is not None:
                th_accuracy = self.accuracy
                unth_accuracy = self.__calc_accuracy(False)
            else:
                th_accuracy = None
                unth_accuracy = None
            ii = 1
            for organ in self.organMaskNames[1::]:
                totalPx = np.sum(np.sum(self.prediction_map, axis = 2)!=0)
                organPx = np.sum(np.argmax(self.prediction_map, axis = 2)==ii)
                perc = organPx / totalPx
                cap = np.append(cap, str(organ))
                c_name = os.path.basename(os.path.normpath(self.listener.dc_path))[0:19]
                output_path = self.output_path + "/_prediction_" + self.model_name[0:-3] + "_on_" + c_name + ".xlsx"
                outputs = np.append(outputs, perc)
                ii=ii+1
            xl = self.__excel_list(cap, outputs, unth_accuracy, th_accuracy, output_path)
            
            if self.gini_slider.get()/100 > 0 or self.softmax_slider.get()/100>0:
                self.__calc_performance(True)
                output_path_goodness_measures_th = self.output_path + "/_performance_" + self.model_name[0:-3] + "_on_" + c_name + "_thresholded_gini_"+str(self.gini_slider.get()/100)+"_Softmax_"+str(self.softmax_slider.get()/100)+".xlsx"
                workbook = xlsxwriter.Workbook(output_path_goodness_measures_th)
                row = 0
                bold = workbook.add_format({'bold': True})
                worksheet = workbook.add_worksheet()
                worksheet.write(0, 0, 'Organ', bold)
                worksheet.write(0, 1, 'Sensitivity: correctly predicted as organ /pixels of organ in GT', bold)
                worksheet.write(0, 2, 'FN-Rate: falsely predicted as NOT organ / pixels of Organ in GT', bold)
                worksheet.write(0, 3, 'Specifity: correctly predicted as NOT organ / pixels of NOT organ in GT', bold)
                worksheet.write(0, 4, 'Right-Positive-Fraction: Correctly predicted as Organ / pixels of Organ in prediciton', bold)
                worksheet.write(0, 5, 'False-Positive-Fraction: Falsely predicted as organ /pixels of organ in Prediction', bold)
                worksheet.write(0, 6, 'Confidence: Mean Gini', bold)
                worksheet.write(0, 7, 'Confidence: Mean Max of Softmax', bold)
                worksheet.write(0, 8, 'Predicted prevalence: perc. of pixels by prediction', bold)
                worksheet.write(0, 9, 'Prevalence: perc. of pixels by GT', bold)
                for organ in self.organMaskNames:
                    worksheet.write(row+1, 0, organ, bold)               
                    for col in range(self.data_array.shape[1]):
                        val= self.data_array[row, col]
                        if np.isnan(val):
                            val=""
                        worksheet.write(row+1, col+1, val)            
                    row=row+1
                
                worksheet.write(row+2, 0, "Mean of Organs", bold) 
                mean_of_organs = np.nanmean(self.data_array, axis=0)
                for col in range(mean_of_organs.shape[0]):
                    val= mean_of_organs[col]
                    if np.isnan(val):
                        val=""
                    worksheet.write(row+2, col+1, val) 
                
                worksheet.write(row+3, 0, "Accuracy  (perc. of correctly predicted pixels)", bold)
                worksheet.write(row+3, 1, self.__calc_accuracy(True))
                        
                workbook.close()
                print("Saved in " +  output_path_goodness_measures_th)
                
            self.__calc_performance(False)
            output_path_goodness_measures = self.output_path + "/_performance_" + self.model_name[0:-3] + "_on_" + c_name + "_unthresholded.xlsx"
            workbook = xlsxwriter.Workbook(output_path_goodness_measures)
            row = 0
            bold = workbook.add_format({'bold': True})
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, 'Organ', bold)
            worksheet.write(0, 6, 'Sensitivity: Pixels correctly predicted as organ / Pixels of organ in GT', bold)
            worksheet.write(0, 7, 'False-Negative-Rate: Pixels falsely predicted as NOT organ / Pixels of organ in GT', bold)
            worksheet.write(0, 3, 'Specifity: Pixels correctly predicted as NOT organ / Pixels of NOT organ in GT', bold)
            worksheet.write(0, 4, 'Right-Positive-Fraction: Pixels correctly predicted as Organ / Pixels of Organ in prediciton', bold)
            worksheet.write(0, 5, 'False-Positive-Fraction: Pixels falsely predicted as organ / Pixels of organ in prediction', bold)
            worksheet.write(0, 1, 'Confidence: Mean Gini', bold)
            worksheet.write(0, 2, 'Confidence: Mean Max of Softmax', bold)
            worksheet.write(0, 8, 'Predicted prevalence: Perc. of pixels by prediction', bold)
            worksheet.write(0, 9, 'Prevalence: Perc. of pixels by GT', bold)
            for organ in self.organMaskNames:
                worksheet.write(row+1, 0, organ, bold)               
                for col in range(self.data_array.shape[1]):
                    val= self.data_array[row, col]
                    if np.isnan(val):
                        val=""
                    worksheet.write(row+1, col+1, val)            
                row=row+1
            
            worksheet.write(row+2, 0, "Mean of Organs", bold) 
            mean_of_organs = np.nanmean(self.data_array, axis=0)
            for col in range(mean_of_organs.shape[0]):
                val= mean_of_organs[col]
                if np.isnan(val):
                    val=""
                worksheet.write(row+2, col+1, val) 
            
            worksheet.write(row+3, 0, "Accuracy  (perc. of correctly predicted pixels)", bold)
            worksheet.write(row+3, 1, self.accuracy)
                
            workbook.close()
            print("Saved in " +  output_path_goodness_measures)
            
            
            
    
    def __excel_list(self, array_one, array_two, unthrsh_ac, thrsh_ac, output_path):
        workbook = xlsxwriter.Workbook(output_path)
        row = 0
        col = 0
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 1, 3)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 3)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 3)
        worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 3)
        worksheet.set_column(7, 7, 20)
        worksheet.write(0, 1, 'Organ', bold)
        worksheet.write(0, 3, 'Fraction', bold)
        worksheet.write(0, 5, 'Unthresholded Accuracy', bold)
        worksheet.write(0, 7, 'Thresholded Accuracy', bold)    
        row += 1       
        for idx, i in enumerate(array_one):
            worksheet.write(row + 1, col + 1, i)
            worksheet.write(row + 1, col + 3, array_two[idx])
            row += 1 
        worksheet.write(row + 1, col + 5, unthrsh_ac)
        worksheet.write(row + 1, col + 7, thrsh_ac)
        workbook.close()
    
    def __select_output(self):
        title = "Please select an output folder."
        self.output_path = filedialog.askdirectory(parent=self.root, title=title)

    def __update_upper_lower(self, event):
        self.y_low = float(self.lower_input.get())
        self.y_high = float(self.upper_input.get())
        self._build_curve_graph()
        
    def __read_legend(self, file):
        with open(file, "rb") as fp:
            b = pickle.load(fp)
        self.organMaskNames = b
        for ii in range(len(self.organMaskNames)):
            string = str(self.organMaskNames[ii])
            string = string.replace('.tif', '')
            string = string.replace('/*_', '')
            string = string.replace(']', '')
            string = string.replace('[', '')
            self.organMaskNames[ii]=string
        if os.path.exists(os.path.dirname(file)+"/colors.txt"):
            d = {}
            with open(os.path.dirname(file)+"/colors.txt") as f:
                for line in f:
                    (key, val) = line.replace(' ', '').replace("\n", "").split(",")
                    d[key] = val

            ii=0
            for organ in self.organMaskNames:
                if organ in d.keys():
                    self.colors[ii] = self.__hex_to_rgb(d[organ])
                ii=ii+1
        self.__read_color_dict()
        self._build_legend()
        self._build_legend_buttons()
        
    def __read_color_dict(self):
        ii=0
        for organ in self.organMaskNames:
                if organ in self.color_dict.keys():
                    self.colors[ii] = self.__hex_to_rgb(self.color_dict[organ])
                ii=ii+1
        
    def __set_stock(self, event):
        choice = self.drop_down_var_stock.get()
        basepath = (os.path.dirname(os.path.dirname(__file__)) + "/Models")
        if choice == "abdominal":
            models = glob.glob(basepath + "/abdominal/*.h5")
        elif choice == "thoracic":
            models = glob.glob(basepath + "/thoracic/*.h5")
        elif choice == "thoracic+abdominal":
            models = glob.glob(basepath + "/thoracic_abdominal/*.h5")
        elif choice == "stomach tube":
            models = glob.glob(basepath + "/stomach_tube/*.h5")
        if(len(models) is not 0):
            self.__load_model(models[0])
        else:
            print("Model not found! Still zipped?")
    
    def __load_info(self):
        if self.info_file_path is not None:
            with open(self.info_file_path, 'r') as file:
                info = file.read()
            title = "Model Information"
            make_info(title=title, info=info)
        else:
            messagebox.showerror("No info-file found", "Sorry, seems like there is no batch_info.txt in the model's folder")
            
    def _search_stock_model(self):
            model_path = (os.path.dirname(os.path.dirname(__file__)) + "/Models")
            models = glob.glob(model_path + "/thoracic_abdominal/*.h5")
            if(len(models) is not 0):
                self.__load_model(models[0])
            else:
                print("Stock model not found! Still zipped?")
            
    def __toggle_tooltip(self, event):
        if self.tw is not None:
            self.tw.destroy()
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        popup = Menu(self.root, tearoff=0)
        popup.add_command(label="Softmax/Gini", command=self.__tooltip_SMGI)
        popup.add_separator()
        popup.add_command(label="Prediction", command=self.__tooltip_Pred)
        popup.add_separator()
        popup.add_command(label="Aus", command=self.__tooltip_off)
        popup.tk_popup(x, y) 
        
    def __toggle_softmax_curve(self, event):
        if self.tw is not None:
            self.tw.destroy()
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        popup = Menu(self.root, tearoff=0)
        popup.add_command(label="Softmax", command=self.__curvesm_sm)
        popup.add_separator()
        popup.add_command(label="Curve", command=self.__curvesm_curve)
        popup.tk_popup(x, y) 

    def __tooltip_SMGI(self):
        self.tt = "SMGI"

    def __tooltip_Pred(self):
        self.tt = "Pred"
        
    def __tooltip_off(self):
        self.tt = None
        if self.tw is not None:
            self.tw.destroy()
        
    def __tooltip_destroy(self, event):
        if self.tw is not None:
            self.tw.destroy()
        
    def __curvesm_sm(self):
        self.curve_sm = "SM"
        self._build_curve_graph()

    def __curvesm_curve(self):
        self.curve_sm = "curve"
        self._build_curve_graph()
    
    def __hex_to_rgb(self, h):
         h = h.lstrip('#')
         return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
     
    def __rgb_to_hex(self, rgb):
         return '#%02x%02x%02x' % rgb
    
    def __save_color(self):
        lin = self.colors[0:len(self.organMaskNames)]
        lin = np.array([self.organMaskNames[ii] + "," + self.__rgb_to_hex(lin[ii]) + "\n" for ii in range(len(self.organMaskNames))])
        f = open(os.path.abspath(self.model_path)+"/colors.txt", "w")
        for line in lin:
            f.write(line)
        f.close()
        print(lin)
    
    def __open_save_masks_dialog(self):
        self.masks_window_frame = Toplevel()
        self.masks_window_frame.geometry("+0+0")
        self.masks_window_frame.configure(bg=tkcolour_from_rgb(BACKGROUND))
        
        self.frame_canvas = Frame(self.masks_window_frame)
        self.frame_canvas.grid(row=2, column=11, columnspan = 2, pady=(5, 0), sticky='nw', rowspan = 10)
        self.frame_canvas.grid_propagate(False)
        self.canvas = Canvas(self.frame_canvas, bg=tkcolour_from_rgb(BACKGROUND))
        self.canvas.grid(row=0, column=1, sticky="news")
        
        self.masks_window = Frame(self.masks_window_frame, bg="blue")
        self.canvas.create_window((0, 0), window=self.masks_window, anchor='nw')

        # points
        print(self.organMaskNames)
        for ii in range(len(self.organMaskNames)):
            self.cb_organ[ii] = self.__create_mask_checkbutton(ii)

        # go button
        make_text(self.masks_window, content="min centr. size", bg=tkcolour_from_rgb(BACKGROUND), column=0, row=12,
                            width=15, pady=(0, 3), padx=(5, 0))
        self.min_centroid_size_entry = make_entry(self.masks_window, row=12, column=1, width=5, columnspan=1, pady=(0, 3))
        self.min_centroid_size_entry.delete(0,END)
        self.min_centroid_size_entry.insert(END, str(self.min_centroid_size))
        self.min_centroid_size_entry.bind("<Key>", self.__updates_centr_size)
        self.masks_window.update_idletasks()
        self.frame_canvas.config(width=350,
                            height=400)
        self.canvas.config(width=350,
                            height=400)
        
    def __create_mask_checkbutton(self, index):
        rom = index % 10
        col = math.floor(index/10)*6
        cb = Checkbutton(self.masks_window, text = self.organMaskNames[index])
        cb.grid(row = rom + 1, column=col, sticky="w", padx=2, pady=2)
        cb.bind('<Button-1>', lambda event: self.__update_mask_check_status(index))
        if self.organs_to_save[index]:
            cb.select()
        else:
            cb.deselect()
        return cb

    def __update_mask_check_status(self, index):
        self.organs_to_save[index] = not self.organs_to_save[index]
        if self.organs_to_save[index]:
            print("selecting")
            self.cb_organ[index].deselect()
            print("seleced")
        else:
            print("deselecting")
            self.cb_organ[index].select() 
            print("deselected")
        print(self.organs_to_save[index])
    
    def __save_masks(self):
        if self.prediction_map is not None:
            temp_prediction_map = (self.prediction_map == self.prediction_map.max(axis=2, keepdims=True)).astype(int)
            ii = 0
            output_path = os.path.dirname(self.listener.dc_path) + "/_prediction_mask"
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            for organ in self.organs_to_save:
                if organ:
                    organ_map = temp_prediction_map[...,ii]
                    softmax = self.softmax_slider.get()/100
                    gini = self.gini_slider.get()/100
                    organ_map[np.where(self.gini_map<gini)]=0
                    organ_map[np.where(self.softmax_map<softmax)]=0 
                    output_path_img = output_path + "/mask_" + self.organMaskNames[ii].replace(" ", "_") + '.tif'
                    output_path_csv = output_path + "/mask_" + self.organMaskNames[ii].replace(" ", "_") + '.csv'
                    im=Image.fromarray((organ_map*255).astype('uint8'), 'L')
                    im.save("./temp.png")
                    im = cv2.imread("./temp.png")
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    (thresh, im) = cv2.threshold(im, 0.5, 255, cv2.THRESH_BINARY)
                    
                    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(im, connectivity=8)
                    sizes = stats[1:, -1]; nb_components = nb_components - 1
                    min_size = self.min_centroid_size
                    img2 = np.zeros((output.shape))+255
                    for i in range(0, nb_components):
                        if sizes[i] >= min_size:
                            img2[output == i + 1] = 0
                            
                    im2=Image.fromarray((img2).astype('uint8'), 'L')
                    im2.save(output_path_img)
                    
                    organ_map_min_size = np.array(im2)
                    np.savetxt(output_path_csv, (1-(organ_map_min_size/255)).astype('uint8'), delimiter=",", fmt="%d")
                ii = ii+1
        return
    

    def __updates_centr_size(self, event= None):
        self.min_centroid_size = int(self.min_centroid_size_entry.get())
        
                    
            
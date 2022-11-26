#Added by Jan Odenthal, University of Heidelberg, odenthal@stud.uni-heidelberg.de

from HyperGuiModules.utility import *
from tensorflow.python.keras.models import load_model
from PIL import Image
import numpy as np
from sklearn.metrics import auc
import os
import logging
import glob
from tkinter import filedialog, Toplevel, Label, messagebox
from scipy.ndimage.filters import gaussian_filter
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
import copy
import random
import pickle
import ast
import os

class Prediction_2: 
    def __init__(self, prediction_frame, listener):
        self.root = prediction_frame 
        self.listener = listener 
        self.x_vals = np.arange(500, 1000, 5)
        self.prediction_map = None 
        

        self.prediction_RGB = None 
        self.current_RGB = None 
        self.save_RGB = None 
        self.RGB = None 
        self.tt = "SMGI"
        self.curve_sm = "curve"
        self.leg_name=""
        
        self.interactive_absorption_spec_graph = None
        self.tw=None
        
        self.model = None 
        
        self.image=None 
        self.legend = None
        self.legAx = None
        self.legend_canvas = None
        
        self.output_path = None
        self.drop_down_legVar = StringVar()
        self.drop_down_var2 = StringVar()
        self.drop_down_var_dyn = StringVar()
        self.drop_down_var_stock = StringVar()
        self.model_name = None

        self.drop_down_var = StringVar()
        
        self.choices2 = ['0. derivative', 
                        '1. derivative',
                        '2. derivative',
                        ]
        
        self.choices_dyn = ['static', 
                        'dynamic']
        
        self.choices_stock = ['arterial ischemia',
                              'venous stasis',
                            'hepatic steatosis',
                            'hepatic fibrosis',
                            'sepsis',
                            'cysts',
                            'echinococcosis',
                            'infarction',
                            'hepatocellular carcinoma',
                            'ICG',
                            'toluidine blue']

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
        
        self.cursor_class = None
        
        self._init_widgets() 

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widgets(self):
        self._build_RGB_overlay_slider()
        self._build_select_model_button() 
        self._build_info_label()
        self._build_prediction_graph() 
        self._build_legend()
        self._search_stock_model()
        self._build_save_buttons()
        self._build_stock_model_button()
        


    # ----------------------------------------------- BUILDERS (MISC) -------------------------------------------------

    def _build_save_buttons(self):
        make_button(self.root, text="Change Output Folder", command=self.__select_output, row=8, column=0,
                    width=15, height=1, columnspan=1, outer_pady=(0, 5), inner_pady=5)
        make_button(self.root, "Save Image", row=8, column=1, command=self.__save_RGB, inner_padx=10,
                                        inner_pady=5, outer_pady=(0, 5), columnspan=1)
    
    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='CONCEPT ONLY', command=self.__info, width=15)

    def _build_RGB_overlay_slider(self):
        self.RGB_overlay_slider = make_slider(self.root, "", row=8, column=2, columnspan = 1, command=self._build_prediction_graph, orient = "horizontal")
        self.RGB_overlay_slider.set(100)

    

    def _build_drop_down(self): 
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__change_mode)
        self.drop_down_menu.configure(highlightthickness=0, width=20,
                                      anchor='w')
        self.drop_down_menu.grid(column=1, row=0, columnspan=2)
    
    def _build_select_model_button(self): 
        self.model_info_button = make_button(self.root, text="model-info",
                                                   command=self.__load_info, inner_padx=10, inner_pady=5,
                                                   row=1, column=1, width=11)
        self.select_model_button = make_button(self.root, text="Custom model",
                                                   command=self.__select_model, inner_padx=10, inner_pady=5,
                                                   row=1, column=2, width=11)
        
    def _build_stock_model_button(self):
        self.drop_down_var_stock.set(self.choices_stock[0])
        self.drop_down_menu_stock = OptionMenu(self.root, self.drop_down_var_stock, *self.choices_stock, command=self.__set_stock)
        self.drop_down_menu_stock.configure(highlightthickness=0, width=10,
                                      anchor='w')
        self.drop_down_menu_stock.grid(column=0, row=1, columnspan=1)
     
    
        
    def _build_legend(self):
        axcolor = 'lightgoldenrodyellow'
        self.legend = Figure(figsize=(1.5,1))
        self.legend.tight_layout()
        self.legend_elements = []
        self.legend_elements.append(Line2D([0], [0], marker='o', color='w', label=self.leg_name, markerfacecolor=(1, 0,0), markersize=15))
        self.legend_elements.append(Line2D([0], [0], marker='o', color='w', label="healthy liver", markerfacecolor=(0,1,0), markersize=15))
        self.legend_elements.append(Line2D([0], [0], marker='o', color='w', label="other", markerfacecolor=(0,0,0), markersize=15))
        gs = self.legend.add_gridspec(1, 1)
        self.legAx = self.legend.add_subplot(gs[0,0])
        self.legAx.legend(handles=self.legend_elements, loc='center') 
        self.legAx.axis('off') 
        self.legend_canvas = FigureCanvasTkAgg(self.legend, master=self.root)
        self.legend_canvas.draw()
        self.legend_canvas.get_tk_widget().grid(column=3, row=5, columnspan=1, rowspan=5)
        



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
        if self.prediction_RGB is not None:
            newImage=np.copy(self.prediction_RGB)              
            im=Image.fromarray(newImage.astype('uint8'), 'RGB')
            self.image = self.axes.imshow(im, interpolation='none')
            self.save_RGB = im
            if self.RGB is not None:
                self.axes.imshow(self.RGB, alpha = alpha)
        # draw figure
        self.prediction_graph.tight_layout()
        self.interactive_prediciton = FigureCanvasTkAgg(self.prediction_graph, master=self.root)
        self.interactive_prediciton.draw()
        self.interactive_prediciton.get_tk_widget().grid(column=0, row=5, columnspan=3, rowspan=1, ipady=0, padx=5)
        self.interactive_prediciton.get_tk_widget().bind('<Button-2>', self.__pop_up_prediction)
        
        
    @staticmethod
    def format_axis(x, _):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 4))

    # ------------------------------------------------- UPDATERS --------------------------------------------------
        
    def update_cube(self, path):
        self.path = os.path.dirname(path)
        self.__update_data()
        
    def update_output_path(self):
        self.output_path = os.path.dirname(self.listener.dc_path) + '/'+self.listener.output_folder_hypergui
    
    def update_prediction(self): 
        self._build_prediction_graph()
    
    def update_RGB(self, new_data):
        self.RGB = new_data
        print("Updating")
    
    
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
        info = self.listener.modules[INFO].predic_2_info
        title = "FOR ILLUSTRATION ONLY"
        make_info(title=title, info=info)

    
    def __load_model(self, path):  
        self.model_name = os.path.basename(os.path.normpath(path))
        self.leg_name = os.path.basename(os.path.dirname(os.path.normpath(path)))
        self.model_path = os.path.dirname(path)
        self._build_legend()
        self.model=load_model(path)
        self.__update_data()
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
            liver_path=self.path+"/liver.tif"
            gt = (np.array(Image.open(liver_path))/255).astype("uint8")
            prediction_RGB = np.zeros([480, 640,3])
            self.liver_px = np.where(gt==0)
            X  = np.rot90(self.listener.data_cube) 
            X = gaussian_filter(X, (5,5,1))
            if self.wholesome:
                ncube = X[self.liver_px[0], self.liver_px[1],:]
                med = np.gradient(np.gradient(np.median(ncube, axis=0)))
                med = (med-np.min(med))/(np.max(med)-np.min(med))
                pred = self.model.predict(med[None])
                print(pred)
                print(med)
                if np.argmax(pred)==0:
                    col = (255,0,0)
                else:
                    col = (0,255,0)
                for ii in range(len(self.liver_px[0])):
                    prediction_RGB[self.liver_px[0][ii], self.liver_px[1][ii],:]=col
            else:
                for ii in np.arange(len(self.liver_px[0])):
                    print(str(ii/len(self.liver_px[0])))
                    a=X[self.liver_px[0][ii], self.liver_px[1][ii],:]
                    a = np.gradient(np.gradient(a))
                    a= (a-np.min(a))/(np.max(a)-np.min(a))
                    pred = self.model.predict(a[None])
                    if np.argmax(pred)==0:
                        prediction_RGB[self.liver_px[0][ii], self.liver_px[1][ii],:]=(255,0,0)
                    else:
                        prediction_RGB[self.liver_px[0][ii], self.liver_px[1][ii],:]=(0,255,0)
            self.prediction_RGB = Image.fromarray(prediction_RGB.astype('uint8'), 'RGB')  
            self.update_prediction()
            self.RGB_overlay_slider.set(50)
            

    def __pop_up_prediction(self, event):
        w, i, ax= make_popup_image_external(self.prediction_graph, graphsize=(9, 9))
        self.axes_external = ax
        i.get_tk_widget().bind('<Motion> ', self._build_pixel_value_external)
        
    def __pop_up_RGB(self, event):        
        w, i, ax= make_popup_image_external(self.RGB_graph, graphsize=(9, 9))
        self.axes_external = ax
        i.get_tk_widget().bind('<Motion> ', self._build_pixel_value_external)
    
        
    def __select_output(self):
        title = "Please select an output folder."
        self.output_path = filedialog.askdirectory(parent=self.root, title=title)
    
    def __get_naming_info(self):
        model = self.model_name[0:-3]
        return "_prediction_" + model
    
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
            logging.debug("SAVING IMAGE" + output_path)
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
            axes = plt.subplot(1,2, 1)
            axes_legend = plt.subplot(1,2,2)
            axes_legend.legend(handles=self.legend_elements, loc='center left', prop={'size': 14}) 
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

    
    def __select_output(self):
        title = "Please select an output folder."
        self.output_path = filedialog.askdirectory(parent=self.root, title=title)
        
        
    def __set_stock(self, event):
        choice = self.drop_down_var_stock.get()
        basepath = (os.path.dirname(os.path.dirname(__file__)) + "/Models")
        if choice == "hepatic steatosis":
            self.wholesome = True
            models = glob.glob(basepath + "/steatosis/*.h5")
        elif choice == "echinococcosis":
            self.wholesome=False
            models = glob.glob(basepath + "/echinococcosis/*.h5")
        else:
            pass
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
            models = glob.glob(model_path + "/steatosis/*.h5")
            if(len(models) is not 0):
                self.wholesome = True
                self.__load_model(models[0])
            else:
                print("Stock model not found! Still zipped?")
        
                    
            
#Added by Jan Odenthal, University of Heidelberg,  odenthal@stud.uni-heidelberg.de
#Commissioned by Universitätsklinikum Heidelberg, Klinik für Allgemein-, Viszeral- und Transplantationschirurgie

from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from skimage.draw import line_aa
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import numpy as np
import logging
import csv
import os
import glob
import math
import shutil
import matplotlib.pyplot as plt
from scipy import ndimage


class BS:
    def __init__(self, bs_frame, listener):
        self.root = bs_frame
        self.listener = listener
        self.stretch_lr = 1
        self.stretch_ud = 1
        self.hypergui_crops = False
        self.stretch_lr_2 = 1
        self.stretch_ud_2 = 1
        self.hypergui_crops = False
        
        self.mode = ""

        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.render_data_cube_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None
        self.current_dc_path_ol = None
        self.shift_ud = 0
        self.shift_lr = 0
        self.tilt = 0
        
        self.shift_ud_2 = 0
        self.shift_lr_2 = 0
        self.tilt_2 = 0
        
        self.save_tif_bool = False
        
        self.checkbox_value_hypergui_crops = IntVar()


        self.data_cube_paths = []
        self.data_cube_path_label = None
        self.path_label = None

        self.rgb_button = None
        self.sto2_button = None
        self.nir_button = None
        self.thi_button = None
        self.twi_button = None
        self.tli_button = None
        self.ohi_button = None
        self.active_image = "RGB"

        self.all_points_remove = None


        self.instant_save_button = None
        self.input_coords_button = None

        self.coords_window = None
        self.input_points_title = None
        self.go_button = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image_data_ol = None
        self.original_image = None
        self.image_array = None

        self.pop_up_graph = None
        self.pop_up_window = None
        self.pop_up_image = None
        self.pop_up = False
        self.tif_save_path_end = None
        self.current_dc_path = None
        
        self.mouse_x = 320
        self.mouse_y = 240
        self.view_mid = [240, 320]
        self.delete_content = True
        
        self.input_pt_title_list = [None for ii in range(100)] 
        self.input_pt_title_x_list = [None for ii in range(100)] 
        self.input_pt_title_y_list = [None for ii in range(100)] 
        self.input_pt_x_list = [None for ii in range(100)]  
        self.input_pt_y_list = [None for ii in range(100)]  
        
        self.measure_point = (None, None)
        self.measure_bool = False
        
        self.save_as_tif_checkbox_value = IntVar()
        


        # coords in dimensions of image, i.e. xrange=[1, 640], yrange=[1, 480]
        self.coords_list = [(None, None) for _ in range(100)]
        self.mask_raw = None

        self._init_widget()

        self.rgb_button.config(foreground="red")
        self.zoom_factor = 1
        
        self.upimage = None
        self.downimage = None

    # ---------------------------------------------- UPDATER AND GETTERS ----------------------------------------------
        

    def get_selected_data_cube_path(self):
        if len(self.selection_listbox.curselection())>0:
            index = self.selection_listbox.curselection()[0]
        else: 
            index = self.current_dc_path
        return self.data_cube_paths[index]
    
    def get_selected_data_cube_path_ol(self):
        if len(self.selection_listbox_ol.curselection())>0:
            index = self.selection_listbox_ol.curselection()[0]
        else: 
            index = self.current_dc_path_ol
        return self.data_cube_paths[index]

    def get_selected_data_paths(self):
        selection = self.selection_listbox.curselection()
        selected_data_paths = [self.data_cube_paths[i] for i in selection]
        return selected_data_paths

    def update_original_image(self, original_image_data, original_image_data_ol):
        self.original_image_data = original_image_data
        self._build_original_image(self.original_image_data, original_image_data_ol)
    
    def update_saved(self, key, value):
        assert type(value) == bool
        self.saves[key] = value

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_tli()
        self._build_ohi()
        self._build_original_image(self.original_image_data, self.original_image_data_ol)
        self._build_select_superdir_button()
        self._build_select_all_subfolders_button()
        self._build_selection_box()
        self._build_selection_box_overlay()
        self._build_next_button()
        self._build_reset_button()
        #self._build_inputs()
        self._build_inputs_slider()
        self._build_save_img_button()
        self._build_subtract_button()
        self._build_addition_button()
        self._build_multiply_button()
        self._build_mean_button()
        self._clean_list_button()
        self._build_checkbox_hypergui_crops()
        

    # ---------------------------------------------- BUILDERS (DISPLAY) -----------------------------------------------

    def _build_rgb(self):
        self.rgb_button = make_button(self.root, text='RGB', width=3, command=self.__update_to_rgb, row=0, column=6,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='StO2', width=4, command=self.__update_to_sto2, row=0, column=7,
                                       columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=3, command=self.__update_to_nir, row=0, column=8,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_thi(self):
        self.thi_button = make_button(self.root, text='THI', width=3, command=self.__update_to_thi, row=0, column=9,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_twi(self):
        self.twi_button = make_button(self.root, text='TWI', width=3, command=self.__update_to_twi, row=0, column=10,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    def _build_tli(self):
        self.tli_button = make_button(self.root, text='TLI', width=3, command=self.__update_to_tli, row=0, column=11,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    def _build_ohi(self):
        self.ohi_button = make_button(self.root, text='OHI', width=3, command=self.__update_to_ohi, row=0, column=12,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


        
        
    # ----------------------------------------------- BUILDERS (MISC) -----------------------------------------------

    def _build_next_button(self):
        self.next_button = make_button(self.root, text='Next (wo. saving)', width=12, command=self.__next,
                                               row=26, column=12, rowspan = 3, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    def _build_reset_button(self):
        self.next_button = make_button(self.root, text='Reset', width=12, command=self.__reset,
                                               row=26, column=6, rowspan = 3, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
    
    def _clean_list_button(self):
        self.next_button = make_button(self.root, text='Clean List', width=12, command=self.__trash_list,
                                               row=0, column=0, rowspan = 1, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)


    def _build_select_superdir_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open OP\nFolder",
                                                   command=self.__add_data_cube_dirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=25, rowspan = 1, column=0, width=11, outer_pady=(5, 5))
    
    def _build_save_img_button(self):
        self.select_data_cube_button = make_button(self.root, text="Save",
                                                   command=self.__save_img, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=25, rowspan = 1, column=1, columnspan=4,  width=11, outer_pady=(5, 5))
        
    def _build_subtract_button(self):
        self.subtract_button = make_button(self.root, text="-",
                                                   command=self.__subtract, inner_padx=10, inner_pady=10,
                                                   outer_padx=5, row=26, rowspan = 1, column=1, width=5, outer_pady=(1, 1))
    def _build_addition_button(self):
        self.subtract_button = make_button(self.root, text="+",
                                                   command=self.__add, inner_padx=10, inner_pady=10,
                                                   outer_padx=5, row=27, rowspan = 2, column=1, width=5, outer_pady=(1, 1))
    def _build_multiply_button(self):
        self.subtract_button = make_button(self.root, text="*",
                                                   command=self.__multiply, inner_padx=10, inner_pady=10,
                                                   outer_padx=5, row=27, rowspan = 2, column=2, width=5, outer_pady=(1, 1))
        
    def _build_mean_button(self):
        self.mean_button = make_button(self.root, text="Mean",
                                                   command=self.__mean, inner_padx=10, inner_pady=10,
                                                   outer_padx=5, row=26, rowspan = 1, column=2, width=5, outer_pady=(1, 1))
        
    def _build_select_all_subfolders_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open Project\nFolder",
                                                   command=self.__add_data_cube_subdirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=26, rowspan=3, column=0, width=11, outer_pady=(5, 5))
    
    def _build_checkbox_hypergui_crops(self):
        hypergui_crops_label = make_label(self.root, "use hypergui_crops", row=0, column=1, columnspan=2,
                                              outer_padx=(35, 15), outer_pady=(10, 15), inner_padx=10, inner_pady=5, wraplength=140)
        hypergui_crops_checkbox = make_checkbox(self.root, text="", row=0, column=1, columnspan=2,
                                                    var=self.checkbox_value_hypergui_crops, sticky=NE, inner_padx=0,
                                                    inner_pady=0, outer_pady=(10, 0), outer_padx=(0, 20))
        hypergui_crops_checkbox.deselect()
        hypergui_crops_checkbox.bind('<Button-1>', self.__update_hypergui_crops_checkbox)



    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, row=1, column=0, rowspan=24, padx=(0, 15), pady=(0, 15), height = 35)
        self.selection_listbox.bind('<<ListboxSelect>>', self.__update_selected_data_cube)
        
    def _build_selection_box_overlay(self):
        self.selection_listbox_ol = make_listbox(self.root, row=1, column=1, columnspan = 4,  rowspan=24, padx=(0, 15), pady=(0, 15), height = 35)
        self.selection_listbox_ol.bind('<<ListboxSelect>>', self.__update_selected_data_cube_ol)
        
    def _build_inputs(self):
        self.lower_scale_text = make_text(self.root, content="Shift LR (a, d)", row=26, column=7, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_shift_lr = make_entry(self.root, row=27, column=7, width=12, pady=5, columnspan=1)
        self.entry_shift_lr.bind('<Return>', self.__update_trans)
        self.entry_shift_lr.insert(END, str(int(self.shift_lr)))
        
        self.lower_scale_text = make_text(self.root, content="Shift UD (w, s)", row=26, column=8, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_shift_ud = make_entry(self.root, row=27, column=8, width=12, pady=5, columnspan=1)
        self.entry_shift_ud.bind('<Return>', self.__update_trans)
        self.entry_shift_ud.insert(END, str(int(self.shift_ud)))
        
        self.lower_scale_text = make_text(self.root, content="Tilt (q, e)", row=26, column=9, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_tilt = make_entry(self.root, row=27, column=9, width=12, pady=5, columnspan=1)
        self.entry_tilt.bind('<Return>', self.__update_trans)
        self.entry_tilt.insert(END, str(round(self.tilt, 2)))
        
        self.lower_scale_text = make_text(self.root, content="Stretch LR (y, x)", row=26, column=10, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_stretch_lr = make_entry(self.root, row=27, column=10, width=12, pady=5, columnspan=1)
        self.entry_stretch_lr.bind('<Return>', self.__update_trans)
        self.entry_stretch_lr.insert(END, str(float(self.stretch_lr)))
        
        self.lower_scale_text = make_text(self.root, content="Stretch UD (c, v)", row=26, column=11, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_stretch_ud = make_entry(self.root, row=27, column=11, width=12, pady=5, columnspan=1)
        self.entry_stretch_ud.bind('<Return>', self.__update_trans)
        self.entry_stretch_ud.insert(END, str(float(self.stretch_ud)))
        
        self.lower_scale_text_2 = make_text(self.root, content="Shift LR (a, d)", row=26, column=7, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_shift_lr_2 = make_entry(self.root, row=28, column=7, width=12, pady=5, columnspan=1)
        self.entry_shift_lr_2.bind('<Return>', self.__update_trans)
        self.entry_shift_lr_2.insert(END, str(int(self.shift_lr_2)))
        
        self.lower_scale_text_2 = make_text(self.root, content="Shift UD (w, s)", row=26, column=8, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_shift_ud_2 = make_entry(self.root, row=28, column=8, width=12, pady=5, columnspan=1)
        self.entry_shift_ud_2.bind('<Return>', self.__update_trans)
        self.entry_shift_ud_2.insert(END, str(int(self.shift_ud_2)))
        
        self.lower_scale_text_2 = make_text(self.root, content="Tilt (q, e)", row=26, column=9, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_tilt_2 = make_entry(self.root, row=28, column=9, width=12, pady=5, columnspan=1)
        self.entry_tilt_2.bind('<Return>', self.__update_trans)
        self.entry_tilt_2.insert(END, str(round(self.tilt_2, 2)))
        
        self.lower_scale_text_2 = make_text(self.root, content="Stretch LR (y, x)", row=26, column=10, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_stretch_lr_2 = make_entry(self.root, row=28, column=10, width=12, pady=5, columnspan=1)
        self.entry_stretch_lr_2.bind('<Return>', self.__update_trans)
        self.entry_stretch_lr_2.insert(END, str(float(self.stretch_lr_2)))
        
        self.lower_scale_text_2 = make_text(self.root, content="Stretch UD (c, v)", row=26, column=11, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.entry_stretch_ud_2 = make_entry(self.root, row=28, column=11, width=12, pady=5, columnspan=1)
        self.entry_stretch_ud_2.bind('<Return>', self.__update_trans)
        self.entry_stretch_ud_2.insert(END, str(float(self.stretch_ud_2)))
    
    def _build_inputs_slider(self):
        
        self.lower_scale_text = make_text(self.root, content="Shift LR (a, d)", row=26, column=7, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text = make_text(self.root, content="Shift UD (w, s)", row=26, column=8, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text = make_text(self.root, content="Tilt (q, e)", row=26, column=9, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text = make_text(self.root, content="Stretch LR (y, x)", row=26, column=10, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text = make_text(self.root, content="Stretch UD (c, v)", row=26, column=11, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text_2 = make_text(self.root, content="Shift LR (a, d)", row=26, column=7, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text_2 = make_text(self.root, content="Shift UD (w, s)", row=26, column=8, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text_2 = make_text(self.root, content="Tilt (q, e)", row=26, column=9, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text_2 = make_text(self.root, content="Stretch LR (y, x)", row=26, column=10, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.lower_scale_text_2 = make_text(self.root, content="Stretch UD (c, v)", row=26, column=11, columnspan=1, width=12,
                                          bg=tkcolour_from_rgb(BACKGROUND), pady=5)
        self.shift_lr_slider = make_slider(self.root, "", row=27, rowspan=1, column=7, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=-320, to=320)
        self.shift_lr_slider.set(0)
        self.shift_ud_slider = make_slider(self.root, "", row=27, rowspan=1, column=8, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=-240, to=240)
        self.shift_ud_slider.set(0)
        self.tilt_slider = make_slider(self.root, "", row=27, rowspan=1, column=9, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=0, to=360)
        self.tilt_slider.set(0)
        self.stretch_lr_slider = make_slider(self.root, "", row=27, rowspan=1, column=10, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=0, to=2, resolution=0.01)
        self.stretch_lr_slider.set(1)
        self.stretch_ud_slider = make_slider(self.root, "", row=27, rowspan=1, column=11, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=0, to=2, resolution=0.01)
        self.stretch_ud_slider.set(1)
        self.shift_lr_slider_2 = make_slider(self.root, "", row=28, rowspan=1, column=7, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=-320, to=320)
        self.shift_lr_slider_2.set(0)
        self.shift_ud_slider_2 = make_slider(self.root, "", row=28, rowspan=1, column=8, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=-240, to=240)
        self.shift_ud_slider_2.set(0)
        self.tilt_slider_2 = make_slider(self.root, "", row=28, rowspan=1, column=9, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=0, to=360)
        self.tilt_slider_2.set(0)
        self.stretch_lr_slider_2 = make_slider(self.root, "", row=28, rowspan=1, column=10, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=0, to=2, resolution=0.01)
        self.stretch_lr_slider_2.set(1)
        self.stretch_ud_slider_2 = make_slider(self.root, "", row=28, rowspan=1, column=11, command=self.__update_trans_slider, columnspan=1, orient = "horizontal", from_=0, to=2, resolution=0.01)
        self.stretch_ud_slider_2.set(1)



    # ---------------------------------------------- BUILDERS (IMAGE) -----------------------------------------------
        
    def _build_original_image(self, data, data_ol):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=1, column=6, rowspan=25,
                                             columnspan=10, inner_pady=300, inner_padx=400, outer_padx=(15, 10),
                                             outer_pady=(15, 10))
        else:
            self.original_image_graph = Figure(figsize=(9, 7))
            self.axes = self.original_image_graph.add_subplot(111)
            self.original_image_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
            self.axes.get_yaxis().set_visible(False)
            self.axes.get_xaxis().set_visible(False)
            
            colorImage  = Image.fromarray(data)
            rotated     = colorImage.rotate(self.tilt_2)
            data = np.array(rotated)
            data = np.roll(data, self.shift_lr_2, axis = 1)
            data = np.roll(data, self.shift_ud_2, axis = 0)
            
            colorImage_bool  = Image.fromarray(self.bark)
            rotated_bool     = colorImage_bool.rotate(self.tilt_2)
            data_bool = np.array(rotated_bool)
            data_bool = np.roll(data_bool, self.shift_lr_2, axis = 1)
            data_bool = np.roll(data_bool, self.shift_ud_2, axis = 0)
            self.bool = data_bool
            
            self.original_image = self.axes.imshow(data, interpolation='none')
            self.downimage = data
            colorImage  = Image.fromarray(data_ol)
            rotated     = colorImage.rotate(self.tilt)
            data_ol = np.array(rotated)
            data_ol = np.roll(data_ol, self.shift_lr, axis = 1)
            data_ol = np.roll(data_ol, self.shift_ud, axis = 0)
            
            colorImage_bool  = Image.fromarray(self.bark_ol)
            rotated_bool     = colorImage_bool.rotate(self.tilt)
            data_ol_bool = np.array(rotated_bool)
            data_ol_bool = np.roll(data_ol_bool, self.shift_lr, axis = 1)
            data_ol_bool = np.roll(data_ol_bool, self.shift_ud, axis = 0)
            self.ol_bool = data_ol_bool
            
            self.axes.imshow(data_ol, alpha = 0.5)
            self.upimage = data_ol
            self.original_image_graph.tight_layout()
            self.original_image_canvas = FigureCanvasTkAgg(self.original_image_graph, master=self.root)
            self.original_image_canvas.draw()
            self.original_image_canvas.get_tk_widget().grid(column=6, row=1, columnspan=10, rowspan=25, ipady=0, ipadx=0)
            self.original_image_canvas.get_tk_widget().bind('<Key-a>', self.__shift_right)
            self.original_image_canvas.get_tk_widget().bind('<Key-d>', self.__shift_left)
            self.original_image_canvas.get_tk_widget().bind('<Key-w>', self.__shift_up)
            self.original_image_canvas.get_tk_widget().bind('<Key-s>', self.__shift_down)
            self.original_image_canvas.get_tk_widget().bind('<Key-q>', self.__tilt_1)
            self.original_image_canvas.get_tk_widget().bind('<Key-e>', self.__tilt_2)
            self.original_image_canvas.get_tk_widget().bind('<Key-y>', self.__stretch_lr_min)
            self.original_image_canvas.get_tk_widget().bind('<Key-x>', self.__stretch_lr_plu)
            self.original_image_canvas.get_tk_widget().bind('<Key-c>', self.__stretch_ud_min)
            self.original_image_canvas.get_tk_widget().bind('<Key-v>', self.__stretch_ud_plu)
            if self.pop_up:
                self.pop_up_graph = self.original_image_graph
                self.pop_up_graph.set_size_inches(8, 8)
                self.pop_up_image = FigureCanvasTkAgg(self.pop_up_graph, master=self.pop_up_window)
                self.pop_up_image.draw()
                self.pop_up_image.get_tk_widget().grid(column=0, row=0)
                self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)

    # ----------------------------------------------- UPDATERS (IMAGE) ------------------------------------------------

    def __update_to_rgb(self):
        self.active_image = "RGB"
        self.rgb_button.config(foreground="red")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.RGB, self.RGB_ol)

    def __update_to_sto2(self):
        self.active_image = "STO2"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="red")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.STO2, self.STO2_ol)

    def __update_to_nir(self):
        self.active_image = "NIR"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="red")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.NIR, self.NIR_ol)

    def __update_to_thi(self):
        self.active_image = "THI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="red")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.THI,self.THI_ol)

    def __update_to_twi(self):
        self.active_image = "TWI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="red")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.TWI, self.TWI_ol)
        
    def __update_to_tli(self):
        self.active_image = "TLI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="red")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.TLI, self.TLI_ol)
        
    def __update_to_ohi(self):
        self.active_image = "OHI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="red")
        self.update_original_image(self.OHI, self.OHI_ol)

    def __close_pop_up(self):
        self.pop_up = False
        self.pop_up_window.destroy()




    # ------------------------------------------------- INPUT POP-UP --------------------------------------------------

    def __update_selected_data_cube(self, event = None):
        if self. hypergui_crops:
            self.__update_selected_data_cube_hypergui_crops()
        else:
            self.__update_selected_data_cube_main()
            
    def __update_selected_data_cube_ol(self, event = None):
        if self. hypergui_crops:
            self.__update_selected_data_cube_ol_hypergui_crops()
        else:
            self.__update_selected_data_cube_ol_main()
            
    def __update_selected_data_cube_main(self, event=None):
        dc_path = self.get_selected_data_cube_path()[0:-33] + "/"
        if self.current_dc_path is not self.selection_listbox.curselection()[0]:
            if len(self.selection_listbox.curselection())>0:
                self.current_dc_path = self.selection_listbox.curselection()[0]
        
        if self.current_dc_path_ol is None:
            self.selection_listbox_ol.select_set(0)
        
        a = Image.open(glob.glob(dc_path +"*RGB-Image.png")[0])
        a = np.asarray(a)
        a = a[30:510, 3:643, :3]
        a = Image.fromarray(a)
        a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
        a = np.asarray(a)
        dark = np.zeros((480, 640,3))
        self.bark = np.zeros((480, 640,3))
        mid_x = int(round(a.shape[0]/2))
        mid_y = int(round(a.shape[1]/2))
        before_midx = mid_x
        before_midy = mid_y
        if before_midx>240:
            before_midx = 240
        if before_midy>320:
            before_midy = 320
        dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
        self.bark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = 1
        dark = dark.astype("uint8")
        self.RGB = dark
        self.bark = self.bark.astype("uint8")
        
        if len(glob.glob(dc_path +"*NIR-Perfusion.png"))>0:
            a = Image.open(glob.glob(dc_path +"*NIR-Perfusion.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.NIR = dark
        else:
            self.NIR = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*TWI.png"))>0:
            a = Image.open(glob.glob(dc_path +"*TWI.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.TWI = dark
        else:
            self.TWI = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*THI.png"))>0:
            a = Image.open(glob.glob(dc_path +"*THI.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.THI = dark
        else:
            self.THI = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*Oxygenation.png"))>0:
            a = Image.open(glob.glob(dc_path +"*Oxygenation.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.STO2 = dark
        else:
            self.STO2 = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*TLI.png"))>0:
            a = Image.open(glob.glob(dc_path +"*TLI.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.TLI = dark
        else:
            self.TLI = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*OHI.png"))>0:
            a = Image.open(glob.glob(dc_path +"*OHI.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.OHI = dark
        else:
            self.OHI = np.zeros((480, 640,3)).astype("uint8")
        
        if self.active_image is "RGB":
            self.__update_to_rgb()
        elif self.active_image is "STO2":
            self.__update_to_sto2()
        elif self.active_image is "NIR":
            self.__update_to_nir()
        elif self.active_image is "TWI":
            self.__update_to_twi()
        elif self.active_image is "THI":
            self.__update_to_thi()
        elif self.active_image is "OHI":
            self.__update_to_ohi()
        elif self.active_image is "TLI":
            self.__update_to_tli()
    
    def __update_selected_data_cube_hypergui_crops(self, event=None):
        dc_path = self.get_selected_data_cube_path()[0:-33] + "/_hypergui_crops/"
        if self.current_dc_path is not self.selection_listbox.curselection()[0]:
            if len(self.selection_listbox.curselection())>0:
                self.current_dc_path = self.selection_listbox.curselection()[0]
        
        if self.current_dc_path_ol is None:
            self.selection_listbox_ol.select_set(0)
        
        a = Image.open(dc_path +"RGB.png")
        a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
        a = np.asarray(a)
        dark = np.zeros((480, 640,3))
        self.bark = np.zeros((480, 640,3))
        mid_x = int(round(a.shape[0]/2))
        mid_y = int(round(a.shape[1]/2))
        before_midx = mid_x
        before_midy = mid_y
        if before_midx>240:
            before_midx = 240
        if before_midy>320:
            before_midy = 320
        dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
        self.bark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = 1
        dark = dark.astype("uint8")
        self.RGB = dark
        self.bark = self.bark.astype("uint8")
        
        if len(glob.glob(dc_path + "NIR.png"))>0:
            a = Image.open(dc_path +"NIR.png")
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.NIR = dark
        else:
            self.NIR = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path + "TWI.png"))>0:
            a = Image.open(dc_path +"TWI.png")
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.TWI = dark
        else:
            self.TWI = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path + "THI.png"))>0:
            a = Image.open(dc_path +"THI.png")
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.THI = dark
        else:
            self.THI = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path + "STO2.png"))>0:
            a = Image.open(dc_path +"STO2.png")
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.STO2 = dark
        else:
            self.STO2 = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path + "TLI.png"))>0:
            a = Image.open(dc_path +"TLI.png")
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.TLI = dark
        else:
            self.TLI = np.zeros((480, 640,3)).astype("uint8")
            
        if len(glob.glob(dc_path + "OHI.png"))>0:
            a = Image.open(dc_path +"OHI.png")
            a = a.resize((int(a.size[0]*self.stretch_lr_2), int(a.size[1]*self.stretch_ud_2)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.OHI = dark
        else:
            self.OHI = np.zeros((480, 640,3)).astype("uint8")
        
        if self.active_image is "RGB":
            self.__update_to_rgb()
        elif self.active_image is "STO2":
            self.__update_to_sto2()
        elif self.active_image is "NIR":
            self.__update_to_nir()
        elif self.active_image is "TWI":
            self.__update_to_twi()
        elif self.active_image is "THI":
            self.__update_to_thi()
        elif self.active_image is "OHI":
            self.__update_to_ohi()
        elif self.active_image is "TLI":
            self.__update_to_tli()
            
    def __update_selected_data_cube_ol_hypergui_crops(self, event=None):
        dc_path = self.get_selected_data_cube_path_ol()[0:-33] + "/_hypergui_crops/"
        if self.current_dc_path_ol is not self.selection_listbox_ol.curselection()[0]:
            if len(self.selection_listbox_ol.curselection())>0:
                self.current_dc_path_ol = self.selection_listbox_ol.curselection()[0]
        
        a = Image.open(dc_path +"RGB.png")
        a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
        a = np.asarray(a)
        dark = np.zeros((480, 640,3))
        self.bark_ol = np.zeros((480, 640,3))
        mid_x = int(round(a.shape[0]/2))
        mid_y = int(round(a.shape[1]/2))
        before_midx = mid_x
        before_midy = mid_y
        if before_midx>240:
            before_midx = 240
        if before_midy>320:
            before_midy = 320
        dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
        self.bark_ol[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = 1
        dark = dark.astype("uint8")
        self.RGB_ol = dark
        self.bark_ol = self.bark_ol.astype("uint8")
        
        if len(glob.glob(dc_path +"NIR.png"))>0:
            a = Image.open(dc_path +"NIR.png")
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.NIR_ol = dark
        else:
            self.NIR_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"TWI.png"))>0:
            a = Image.open(dc_path +"TWI.png")
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.TWI_ol = dark
        else:
            self.TWI_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"THI.png"))>0:
            a = Image.open(dc_path +"THI.png")
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.THI_ol = dark
        else:
            self.THI_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"STO2.png"))>0:
            a = Image.open(dc_path +"STO2.png")
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.STO2_ol = dark
        else:
            self.STO2_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"TLI.png"))>0:
            a = Image.open(dc_path +"TLI.png")
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.TLI_ol = dark
        else:
            self.TLI_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"OHI.png"))>0:
            a = Image.open(dc_path +"OHI.png")
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+a.shape[0]), (320-before_midy):(320-before_midy+a.shape[1]), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.OHI_ol = dark
        else:
            self.OHI_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if self.active_image is "RGB":
            self.__update_to_rgb()
        elif self.active_image is "STO2":
            self.__update_to_sto2()
        elif self.active_image is "NIR":
            self.__update_to_nir()
        elif self.active_image is "TWI":
            self.__update_to_twi()
        elif self.active_image is "THI":
            self.__update_to_thi()
        elif self.active_image is "OHI":
            self.__update_to_ohi()
        elif self.active_image is "TLI":
            self.__update_to_tli()
            
    def __update_selected_data_cube_ol_main(self, event=None):
        dc_path = self.get_selected_data_cube_path_ol()[0:-33] + "/"
        if self.current_dc_path_ol is not self.selection_listbox_ol.curselection()[0]:
            if len(self.selection_listbox_ol.curselection())>0:
                self.current_dc_path_ol = self.selection_listbox_ol.curselection()[0]
        
        a = Image.open(glob.glob(dc_path +"*RGB-Image.png")[0])
        a = np.asarray(a)
        a = a[30:510, 3:643, :3]
        a = Image.fromarray(a)
        a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
        a = np.asarray(a)
        dark = np.zeros((480, 640,3))
        self.bark_ol = np.zeros((480, 640,3))
        mid_x = int(round(a.shape[0]/2))
        mid_y = int(round(a.shape[1]/2))
        before_midx = mid_x
        before_midy = mid_y
        if before_midx>240:
            before_midx = 240
        if before_midy>320:
            before_midy = 320
        dark[(240-before_midx):(240-before_midx+2*before_midx), (320-before_midy):(320-before_midy+2*before_midy), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
        self.bark_ol[(240-before_midx):(240-before_midx+2*before_midx), (320-before_midy):(320-before_midy+2*before_midy), 0:3] = 1
        dark = dark.astype("uint8")
        self.RGB_ol = dark
        self.bark_ol = self.bark_ol.astype("uint8")
        
        if len(glob.glob(dc_path +"*NIR-Perfusion.png"))>0:
            a = Image.open(glob.glob(dc_path +"*NIR-Perfusion.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+2*before_midx), (320-before_midy):(320-before_midy+2*before_midy), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.NIR_ol = dark
        else:
            self.NIR_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*TWI.png"))>0:
            a = Image.open(glob.glob(dc_path +"*TWI.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+2*before_midx), (320-before_midy):(320-before_midy+2*before_midy), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.TWI_ol = dark
        else:
            self.TWI_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*THI.png"))>0:
            a = Image.open(glob.glob(dc_path +"*THI.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+2*before_midx), (320-before_midy):(320-before_midy+2*before_midy), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.THI_ol = dark
        else:
            self.THI_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*Oxygenation.png"))>0:
            a = Image.open(glob.glob(dc_path +"*Oxygenation.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+2*before_midx), (320-before_midy):(320-before_midy+2*before_midy), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.STO2_ol = dark
        else:
            self.STO2_ol = np.zeros((480, 640,3)).astype("uint8")
            
        if len(glob.glob(dc_path +"*TLI.png"))>0:
            a = Image.open(glob.glob(dc_path +"*TLI.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            dark[(240-before_midx):(240-before_midx+2*before_midx), (320-before_midy):(320-before_midy+2*before_midy), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.TLI_ol = dark
        else:
            self.TLI_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if len(glob.glob(dc_path +"*OHI.png"))>0:
            a = Image.open(glob.glob(dc_path +"*OHI.png")[0])
            a = np.asarray(a)
            a = a[26:506, 4:644, :3]
            a = Image.fromarray(a)
            a = a.resize((int(a.size[0]*self.stretch_lr), int(a.size[1]*self.stretch_ud)))
            a = np.asarray(a)
            dark = np.zeros((480, 640,3))
            if before_midx>240:
                before_midx = 240
            if before_midy>320:
                before_midy = 320
            dark[(240-before_midx):(240-before_midx+2*before_midx), (320-before_midy):(320-before_midy+2*before_midy), 0:3] = a[(mid_x-before_midx):(mid_x-before_midx+2*before_midx), (mid_y-before_midy):(mid_y-before_midy+2*before_midy), 0:3]
            dark = dark.astype("uint8")
            self.OHI_ol = dark
        else:
            self.OHI_ol = np.zeros((480, 640,3)).astype("uint8")
        
        if self.active_image is "RGB":
            self.__update_to_rgb()
        elif self.active_image is "STO2":
            self.__update_to_sto2()
        elif self.active_image is "NIR":
            self.__update_to_nir()
        elif self.active_image is "TWI":
            self.__update_to_twi()
        elif self.active_image is "THI":
            self.__update_to_thi()
        elif self.active_image is "OHI":
            self.__update_to_ohi()
        elif self.active_image is "TLI":
            self.__update_to_tli()

    def __add_data_cube_dirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the data folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir)
        for sub_dir in sub_dirs:
            if os.path.exists(sub_dir +"/_hypergui_crops/") and self.hypergui_crops:
                self.__add_data_cube(sub_dir)
            elif not self.hypergui_crops:
               self.__add_data_cube(sub_dir) 
    
    def __add_data_cube_subdirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the OP folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir, True)
        for sub_dir in sub_dirs:
            if os.path.exists(sub_dir +"/_hypergui_crops/"):
                self.__add_data_cube(sub_dir)


    def __add_data_cube(self, sub_dir):
        contents = os.listdir(sub_dir)
        dc_path = [sub_dir + "/" + i for i in contents if ".dat" in i]  # takes first data cube it finds
        if len(dc_path) > 0:
            dc_path = dc_path[0]
            if dc_path in self.data_cube_paths:
                messagebox.showerror("Error", "That data has already been added.")
            else:
                # Add the new data to current class
                self.data_cube_paths.append(dc_path)

                # Display the data cube
                concat_path = os.path.basename(os.path.normpath(dc_path))
                self.selection_listbox.insert(END, concat_path)
                self.selection_listbox.config(width=18)
                self.selection_listbox_ol.insert(END, concat_path)
                self.selection_listbox_ol.config(width=18)

    def __get_path_to_dir(self, title):
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askdirectory(parent=self.root, title=title, initialdir=p)
        else:
            path = filedialog.askdirectory(parent=self.root, title=title)
        return path


    @staticmethod
    def __get_sub_folder_paths(path_to_main_folder, recursive = False): 
        sub_folders = sorted(glob.glob(path_to_main_folder+"/**/", recursive = recursive))
        return sub_folders
        
    def __input_info(self):
        info = self.listener.modules[INFO].input_info
        title = "Coordinate Input Information"
        make_info(title=title, info=info)
        
    def __shift_ol(self):
        pass

    def __next(self):
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(sel+1) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        #self.__remove_pt('all')
    
    def __update_img(self):
        if self.active_image is "RGB":
            self.__update_to_rgb()
        elif self.active_image is "STO2":
            self.__update_to_sto2()
        elif self.active_image is "NIR":
            self.__update_to_nir()
        elif self.active_image is "TWI":
            self.__update_to_twi()
        elif self.active_image is "THI":
            self.__update_to_thi()
        elif self.active_image is "OHI":
            self.__update_to_ohi()
        elif self.active_image is "TLI":
            self.__update_to_tli()
    
    def __shift_up(self, event =None):
        self.shift_ud = self.shift_ud-1
        self._build_inputs()
        self.__update_img()
    def __shift_down(self, event =None):
        self.shift_ud = self.shift_ud+1
        self._build_inputs()
        self.__update_img()
    def __shift_right(self, event =None):
        self.shift_lr = self.shift_lr-1
        self._build_inputs()
        self.__update_img()
    def __shift_left(self, event =None):
        self.shift_lr = self.shift_lr+1
        self._build_inputs()
        self.__update_img()
    def __tilt_1(self, event =None):
        self.tilt = self.tilt+1
        self._build_inputs()
        self.__update_img()
    def __tilt_2(self, event =None):
        self.tilt = self.tilt-1
        self._build_inputs()
        self.__update_img()
    def __stretch_lr_min(self, event =None):
        self.stretch_lr = self.stretch_lr-0.05
        self._build_inputs()
        self.__update_selected_data_cube_ol()
        self.__update_img()
    def __stretch_ud_min(self, event =None):
        self.stretch_ud = self.stretch_ud-0.05
        self._build_inputs()
        self.__update_selected_data_cube_ol()
        self.__update_selected_data_cube()
        self.__update_img()
    def __stretch_lr_plu(self, event =None):
        self.stretch_lr = self.stretch_lr+0.05
        self._build_inputs()
        self.__update_selected_data_cube_ol()
        self.__update_selected_data_cube()
        self.__update_img()
    def __stretch_ud_plu(self, event =None):
        self.stretch_ud = self.stretch_ud+0.05
        self._build_inputs()
        self.__update_selected_data_cube_ol()
        self.__update_selected_data_cube()
        self.__update_img()
    
    def __update_trans(self, event = None):
        self.stretch_ud = float(self.entry_stretch_ud.get())
        self.stretch_lr = float(self.entry_stretch_lr.get())
        self.shift_ud = int(self.entry_shift_ud.get())
        self.shift_lr = int(self.entry_shift_lr.get())
        self.tilt = int(self.entry_tilt.get())
        self.stretch_ud_2 = float(self.entry_stretch_ud_2.get())
        self.stretch_lr_2 = float(self.entry_stretch_lr_2.get())
        self.shift_ud_2 = int(self.entry_shift_ud_2.get())
        self.shift_lr_2 = int(self.entry_shift_lr_2.get())
        self.tilt_2 = int(self.entry_tilt_2.get())
        self.__update_selected_data_cube_ol()
        self.__update_selected_data_cube()
        self.__update_img()
        
    def __update_trans_slider(self, event = None):
        self.stretch_ud = float(self.stretch_ud_slider.get())
        self.stretch_lr = float(self.stretch_lr_slider.get())
        self.shift_ud = int(self.shift_ud_slider.get())
        self.shift_lr = int(self.shift_lr_slider.get())
        self.tilt = int(self.tilt_slider.get())
        self.stretch_ud_2 = float(self.stretch_ud_slider_2.get())
        self.stretch_lr_2 = float(self.stretch_lr_slider_2.get())
        self.shift_ud_2 = int(self.shift_ud_slider_2.get())
        self.shift_lr_2 = int(self.shift_lr_slider_2.get())
        self.tilt_2 = int(self.tilt_slider_2.get())
        self.__update_selected_data_cube_ol()
        self.__update_selected_data_cube()
        self.__update_img()

    def __subtract(self, event = None):
        self.mode = "SUBTRACT"
        self.bool_ol = np.sum(self.ol_bool, axis = 2)
        self.booly = np.sum(self.bool, axis = 2)
        up_hsi = rgb_image_to_hsi_array(self.upimage)
        down_hsi = rgb_image_to_hsi_array(self.downimage)
        diff_hsi = (down_hsi - up_hsi)
        diff_hsi[np.where(diff_hsi < 0)]=0
        self.save_hsi = diff_hsi
        diff_hsi[np.where(self.bool_ol == 0)]=0
        diff_hsi[np.where(self.booly == 0)]=0
        self.fig, self.image, self.image_array =  make_image(self.root, np.rot90(np.rot90(np.rot90(diff_hsi))), row = 1, column = 6, columnspan= 10, rowspan = 25, lower_scale_value = 0, upper_scale_value=100, color_rgb=BACKGROUND,
               figwidth=9, figheight=7, original=False, gs=False, img = None, axs = None, figu = None)
        
    def __add(self, event = None):
        self.mode = "ADD"
        self.bool_ol = np.sum(self.ol_bool, axis = 2)
        self.booly = np.sum(self.bool, axis = 2)
        up_hsi = rgb_image_to_hsi_array(self.upimage)
        down_hsi = rgb_image_to_hsi_array(self.downimage)
        diff_hsi = (down_hsi + up_hsi)
        diff_hsi[np.where(diff_hsi < 0)]=0
        self.save_hsi = diff_hsi
        diff_hsi[np.where(self.bool_ol == 0)]=0
        diff_hsi[np.where(self.booly == 0)]=0
        self.fig, self.image, self.image_array =  make_image(self.root, np.rot90(np.rot90(np.rot90(diff_hsi))), row = 1, column = 6, columnspan= 10, rowspan = 25, lower_scale_value = 0, upper_scale_value=100, color_rgb=BACKGROUND,
               figwidth=9, figheight=7, original=False, gs=False, img = None, axs = None, figu = None)
        
    def __multiply(self, event = None):
        self.mode = "MULTIPLY"
        self.bool_ol = np.sum(self.ol_bool, axis = 2)
        self.booly = np.sum(self.bool, axis = 2)
        up_hsi = rgb_image_to_hsi_array(self.upimage)
        down_hsi = rgb_image_to_hsi_array(self.downimage)
        diff_hsi = (down_hsi * up_hsi)
        diff_hsi[np.where(diff_hsi < 0)]=0
        self.save_hsi = diff_hsi
        diff_hsi[np.where(self.bool_ol == 0)]=0
        diff_hsi[np.where(self.booly == 0)]=0
        self.fig, self.image, self.image_array =  make_image(self.root, np.rot90(np.rot90(np.rot90(diff_hsi))), row = 1, column = 6, columnspan= 10, rowspan = 25, lower_scale_value = 0, upper_scale_value=100, color_rgb=BACKGROUND,
               figwidth=9, figheight=7, original=False, gs=False, img = None, axs = None, figu = None)
        
    def __mean(self, event = None):
        self.mode = "MEAN"
        self.bool_ol = np.sum(self.ol_bool, axis = 2)
        self.booly = np.sum(self.bool, axis = 2)
        up_hsi = rgb_image_to_hsi_array(self.upimage)
        down_hsi = rgb_image_to_hsi_array(self.downimage)
        diff_hsi = (down_hsi + up_hsi)/2
        diff_hsi[np.where(diff_hsi < 0)]=0
        self.save_hsi = diff_hsi
        diff_hsi[np.where(self.bool_ol == 0)]=0
        diff_hsi[np.where(self.booly == 0)]=0
        self.fig, self.image, self.image_array =  make_image(self.root, np.rot90(np.rot90(np.rot90(diff_hsi))), row = 1, column = 6, columnspan= 10, rowspan = 25, lower_scale_value = 0, upper_scale_value=100, color_rgb=BACKGROUND,
               figwidth=9, figheight=7, original=False, gs=False, img = None, axs = None, figu = None)
    
    def __save_img(self, event = None):
        save_hsi = self.save_hsi[np.min(np.where(self.bool == 0)[0]): np.max(np.where(self.bool == 0)[0]), np.min(np.where(self.bool ==0 )[1]): np.max(np.where(self.bool == 0)[1])]
        plt.clf()
        cmap = 'jet'
        plt.imshow(np.flipud(save_hsi), origin='lower', cmap=cmap, vmin=float(0), vmax=float(100))
        plt.axis('off')
        
        folder_1 = self.selection_listbox.curselection()[0]
        path = os.path.dirname(self.data_cube_paths[folder_1])+"/_baseline_subtraction/"
        if not os.path.exists(path):
            os.mkdir(path)
        folder_2 = self.selection_listbox_ol.curselection()[0]
        name = "BS_" + self.mode+"_"+os.path.basename(os.path.abspath(self.data_cube_paths[folder_2])) + "_from_" + os.path.basename(os.path.abspath(self.data_cube_paths[folder_1]))+"_shiftLR_"+str(self.shift_lr)+"_shiftUD_"+str(self.shift_ud)+"_stretchLR_"+str(self.stretch_lr)+"_stretchUD_"+str(self.stretch_ud)+"_tilt_"+str(self.tilt)+".png"
        output_path = path +name
        plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0)
        plt.clf()
    
    def __trash_list(self):
        self.data_cube_paths = []
        self.selection_listbox.delete(0,'end')
        self.selection_listbox_ol.delete(0,'end')
        
    def __update_hypergui_crops_checkbox(self, event=None):
        self.hypergui_crops = not self.hypergui_crops
        self.__update_selected_data_cube()
        self.__update_selected_data_cube_ol()
        
    def __reset(self):
        self.shift_lr_slider.set(0)
        self.shift_ud_slider.set(0)
        self.tilt_slider.set(0)
        self.stretch_lr_slider.set(1)
        self.stretch_ud_slider.set(1)
        self.shift_lr_slider_2.set(0)
        self.shift_ud_slider_2.set(0)
        self.tilt_slider_2.set(0)
        self.stretch_lr_slider_2.set(1)
        self.stretch_ud_slider_2.set(1)
        
    

            
        
        
        
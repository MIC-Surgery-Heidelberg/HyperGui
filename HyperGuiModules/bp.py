#Added by Jan Odenthal, University of Heidelberg,  odenthal@stud.uni-heidelberg.de
#Commissioned by Universitätsklinikum Heidelberg, Klinik für Allgemein-, Viszeral- und Transplantationschirurgie

from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from skimage.draw import line_aa
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import numpy as np
import csv
import os
import glob
import math
import shutil
import copy


class BP:
    def __init__(self, bp_frame, listener):
        self.root = bp_frame

        # Listener
        self.listener = listener
        
        # Bools
        self.unfocus = False
        self.live = False
        self.automatic_names = True
        self.delete_content = True
        self.inherit = True
        self.grab = False
        self.move_mode = False
        self.start_move = False
        self.rotate_on = False
        self.stretch_on = False
        
        #Lists
        self.data_cube_paths = []
        self.sub_dirs = []
        self.labels = [None]*20
        self.remove = [None]*20
        self.title = [None for ii in range(1000)]
        self.title_x = [None for ii in range(1000)]
        self.title_y =[None for ii in range(1000)]
        self.input_pt_title_list = [None for ii in range(1000)] 
        self.input_pt_title_x_list = [None for ii in range(1000)] 
        self.input_pt_title_y_list = [None for ii in range(1000)] 
        self.input_pt_x_list = [None for ii in range(1000)]  
        self.input_pt_y_list = [None for ii in range(1000)]  
        self.coords_list = [(None, None) for _ in range(1000000)]
        self.coords_list_copy = [(None, None) for _ in range(1000000)]
        
        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.render_data_cube_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None
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
        self.checkbox_value = IntVar(value=1)
        self.checkbox_value_2 = IntVar(value=0)
        self.save_label = None
        self.live_folder = None

        self.eudis_text = None
        
        self.pt1_label = None
        self.pt1_remove = None

        self.pt2_label = None
        self.pt2_remove = None

        self.pt3_label = None
        self.pt3_remove = None

        self.pt4_label = None
        self.pt4_remove = None

        self.pt5_label = None
        self.pt5_remove = None

        self.pt6_label = None
        self.pt6_remove = None

        self.pt7_label = None
        self.pt7_remove = None

        self.pt8_label = None
        self.pt8_remove = None
        
        self.pt9_label = None
        self.pt9_remove = None

        self.pt10_label = None
        self.pt10_remove = None

        self.all_points_remove = None

        self.instant_save_button = None
        self.input_coords_button = None

        self.coords_window = None
        self.input_points_title = None
        self.go_button = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None
        self.image_array = None

        self.pop_up_graph = None
        self.pop_up_window = None
        self.pop_up_image = None
        self.pop_up = False
        self.tif_save_path_end = None
        self.current_dc_path = None
        
        self.save_as_tif_checkbox_value = IntVar()
        
        self.mask_raw = None
        
        self.zoom_factor = 1
        self.rot = 0
        self.xstr = 1
        self.ystr = 1
        self.xsh = 0
        self.ysh = 0
        self.origin = (240, 320)
        self.color = (113,255,66)
        
        #Mouse
        self.mouse_x = 320
        self.mouse_y = 240
        self.bbox_x1 = 0
        self.bbox_x2 = 0
        self.bbox_y1 = 0
        self.bbox_y2 = 0
        self.view_mid = [240, 320]      
        self.move_start_x = None
        self.move_start_y = None
        self.xsh_last = 0
        self.ysh_last = 0
        self.xstr_last = 1
        self.ystr_last = 1
        self.rot_last = 0
        
        # Labelling
        self.labelling_name = "*"
        self.idx_dict = dict({0:0})
        
        self._init_widget()


    # ---------------------------------------------- UPDATER AND GETTERS ----------------------------------------------
        

    def get_selected_data_cube_path(self):
        if len(self.selection_listbox.curselection())>0:
            index = self.idx_dict[self.selection_listbox.curselection()[0]]
        else: 
            index = self.current_dc_path
        return self.data_cube_paths[index]

    def get_selected_data_paths(self):
        selection = self.selection_listbox.curselection()
        selected_data_paths = [self.data_cube_paths[self.idx_dict[i]] for i in selection]
        return selected_data_paths

    def update_original_image(self, original_image_data):
        self.original_image_data = original_image_data
        self._build_original_image(self.original_image_data)
        self._draw_points()
    
    def update_saved(self, key, value):
        assert type(value) == bool
        self.saves[key] = value
        
    def __update_selected_data_cube(self, event):
        if not self.inherit:
            self.__remove_pt("all")
        if len(self.selection_listbox.curselection())>0:
            dc_path = self.get_selected_data_cube_path()[0:-12]
            if self.current_dc_path is not self.selection_listbox.curselection()[0]:
                if len(self.selection_listbox.curselection())>0:
                    self.current_dc_path = self.selection_listbox.curselection()[0]
                self._update_tif_save_path()
        else:
            dc_path = self.data_cube_paths[0][0:-12]
            self.current_dc_path = 0
            self._update_tif_save_path()
        
        a = Image.open(dc_path +"RGB-Image.png")
        a = np.asarray(a)
        if a.shape[0] == 550:
            a = a[50:530, 20:660, :3]
        else:
            a = a[30:510, 3:643, :3]
        self.RGB = a
        
        if os.path.exists(dc_path +"NIR-Perfusion.png"):
            b = Image.open(dc_path +"NIR-Perfusion.png")
            b = np.asarray(b)
            if b.shape[0] == 550:
                b = b[50:530, 50:690, :3]
            else:
                b = b[26:506, 4:644, :3]
            self.NIR = b
        else:
            self.NIR = np.zeros((480, 680,3)).astype("uint8")
        
        if os.path.exists(dc_path +"TWI.png"):
            c = Image.open(dc_path +"TWI.png")
            c = np.asarray(c)
            if c.shape[0] == 550:
                c = c[50:530, 50:690, :3]
            else:
                c = c[26:506, 4:644, :3]
            self.TWI = c
        else:
            self.TWI = np.zeros((480, 680,3)).astype("uint8")
        
        if os.path.exists(dc_path +"THI.png"):
            d = Image.open(dc_path +"THI.png")
            d = np.asarray(d)
            if d.shape[0] == 550:
                d = d[50:530, 50:690, :3]
            else:
                d = d[26:506, 4:644, :3]
            self.THI = d
        else:
            self.THI  = np.zeros((480, 680,3)).astype("uint8")
        
        if os.path.exists(dc_path +"Oxygenation.png"):
            e = Image.open(dc_path +"Oxygenation.png")
            e = np.asarray(e)
            if e.shape[0] == 550:
                e = e[50:530, 50:690, :3]
            else:
                e = e[26:506, 4:644, :3]
            self.STO2 = e
        else:
            self.STO2 = np.zeros((480, 680,3)).astype("uint8")
        
        if os.path.exists(dc_path +"TLI.png"):
            f = Image.open(dc_path +"TLI.png")
            f = np.asarray(f)
            if f.shape[0] == 550:
                f = f[50:530, 50:690, :3]
            else:
                f = f[26:506, 4:644, :3]
            self.TLI = f
        else:
            self.TLI = np.zeros((480, 680, 3)).astype("uint8")
        
        if os.path.exists(dc_path +"OHI.png"):
            g = Image.open(dc_path +"OHI.png")
            g = np.asarray(g)
            if g.shape[0] == 550:
                g = g[50:530, 50:690, :3]
            else:
                g = g[26:506, 4:644, :3]
            self.OHI = g
        else:
            self.OHI = np.zeros((480, 680,3)).astype("uint8")
        
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
        
        mask_path = os.path.dirname(dc_path) +'/'+self.listener.output_folder_hypergui +"/MASK_COORDINATES.csv"
        if os.path.exists(mask_path):
            self.__load_mask(mask_path)
        self.original_image.get_tk_widget().focus_force()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_selection_box()
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_tli()
        self._build_ohi()
        self._build_points()
        self._build_all_points()
        self._build_instant_save_button()
        self._build_original_image(self.original_image_data)
        #self._build_select_superdir_button()
        self._build_labelling_entry()
        self._build_select_all_subfolders_button()
        self._build_edit_coords_button()
        self._build_trash_button()
        self._build_tif_save_path_text()
        self._build_tif_save_path_input()
        self._build_save_tif()
        self._build_autonames_button()
        self._build_save_all_and_next()
        self._build_next_button()
        self._build_eudis_info()
        self._build_delete_content()
        self._build_live_button()
        self._build_info_label()
        self._build_delete_hypergui_button()
        self._build_counter(0)
        self._build_inherit_checkbox()
        
        self.rgb_button.config(foreground="red")

    # ---------------------------------------------- BUILDERS (DISPLAY) -----------------------------------------------

    def _build_rgb(self):
        self.rgb_button = make_button(self.root, text='RGB', width=3, command=self.__update_to_rgb, row=0, column=1,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='StO2', width=4, command=self.__update_to_sto2, row=0, column=2,
                                       columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=3, command=self.__update_to_nir, row=0, column=3,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    def _build_thi(self):
        self.thi_button = make_button(self.root, text='THI', width=3, command=self.__update_to_thi, row=0, column=4,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))

    def _build_twi(self):
        self.twi_button = make_button(self.root, text='TWI', width=3, command=self.__update_to_twi, row=0, column=5,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    def _build_tli(self):
        self.tli_button = make_button(self.root, text='TLI', width=3, command=self.__update_to_tli, row=0, column=6,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    def _build_ohi(self):
        self.ohi_button = make_button(self.root, text='OHI', width=3, command=self.__update_to_ohi, row=0, column=7,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))


    # ----------------------------------------------- BUILDERS (POINTS) -----------------------------------------------

    def _build_all_points(self):
        self.all_points_remove = make_button(self.root, text='x', width=1, command=lambda: self.__remove_pt('all'),
                                             row=2, column=12, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                                             highlightthickness=0)
        self.last_point_remove = make_button(self.root, text='undo last', width=10, command=lambda: self.__remove_pt('last'),
                                             row=2, column=11, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                                             highlightthickness=0)
        self.root.rowconfigure(24, weight=100)
                    
    def _build_points(self):
        self._build_pt1()
        self._build_pt2()
        self._build_pt3()
        self._build_pt4()
        self._build_pt5()
        self._build_pt6()
        self._build_pt7()
        self._build_pt8()
        self._build_pt9()
        self._build_pt10()
        self._build_pt11()
        self._build_pt12()
        self._build_pt13()
        self._build_pt14()
        self._build_pt15()
        self._build_pt16()
        self._build_pt17()
        self._build_pt18()
        self._build_pt19()
        self._build_pt20()

    def _build_ptn(self, num):
        if self.coords_list[num] == (None, None):
            self.labels[num] = make_text(self.root, content="Pt " + str(num) + ': ' + str(self.coords_list[num]),
                              bg=tkcolour_from_rgb(BACKGROUND), column=11, row=num + 4, width=18, columnspan=1,
                              padx=0, state=NORMAL, pady=0, text = self.labels[num])
        else:
            self.labels[num] = make_text(self.root,
                              content="Pt " + str(num) + ': ' + str(tuple(x + 1 for x in self.coords_list[num])),
                              bg=tkcolour_from_rgb(BACKGROUND), column=11, row=num + 4, width=18, columnspan=1, padx=0,
                              state=NORMAL, pady=0, text = self.labels[num])
        # remove
        self.remove[num] = make_button(self.root, text='x', width=1, command=lambda: self.__remove_pt(num+1), row=num + 4,
                             column=12, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                             highlightthickness=0, button = self.remove[num])

        return self.labels[num], self.remove[num]

    def _build_pt1(self):
        self.pt1_label, self.pt1_remove = self._build_ptn(0)

    def _build_pt2(self):
        self.pt2_label, self.pt2_remove= self._build_ptn(1)

    def _build_pt3(self):
        self.pt3_label, self.pt3_remove= self._build_ptn(2)

    def _build_pt4(self):
        self.pt4_label, self.pt4_remove= self._build_ptn(3)

    def _build_pt5(self):
        self.pt5_label, self.pt5_remove= self._build_ptn(4)

    def _build_pt6(self):
        self.pt6_label, self.pt6_remove= self._build_ptn(5)
        
    def _build_pt7(self):
        self.pt7_label, self.pt7_remove= self._build_ptn(6)

    def _build_pt8(self):
        self.pt8_label, self.pt8_remove= self._build_ptn(7)

    def _build_pt9(self):
        self.pt9_label, self.pt9_remove= self._build_ptn(8)

    def _build_pt10(self):
        self.pt10_label, self.pt10_remove= self._build_ptn(9)
        
    def _build_pt11(self):
        self.pt11_label, self.pt11_remove = self._build_ptn(10)

    def _build_pt12(self):
        self.pt12_label, self.pt12_remove= self._build_ptn(11)

    def _build_pt13(self):
        self.pt13_label, self.pt13_remove= self._build_ptn(12)

    def _build_pt14(self):
        self.pt14_label, self.pt14_remove= self._build_ptn(13)

    def _build_pt15(self):
        self.pt15_label, self.pt15_remove= self._build_ptn(14)

    def _build_pt16(self):
        self.pt16_label, self.pt16_remove= self._build_ptn(15)
        
    def _build_pt17(self):
        self.pt17_label, self.pt17_remove= self._build_ptn(16)

    def _build_pt18(self):
        self.pt18_label, self.pt18_remove= self._build_ptn(17)

    def _build_pt19(self):
        self.pt19_label, self.pt19_remove= self._build_ptn(18)

    def _build_pt20(self):
        self.pt20_label, self.pt20_remove= self._build_ptn(19)
        
        
    # ----------------------------------------------- BUILDERS (MISC) -----------------------------------------------
        
    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Batch Processing', command=self.__info, width=8)

    def _build_next_button(self):
        self.next_button = make_button(self.root, text='Next (wo. saving)', width=12, command=self.__next,
                                               row=26, column=10, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    def _build_instant_save_button(self):
        self.instant_save_button = make_button(self.root, text='Save coordinates\nand Next', width=12, command=self.__save_coords,
                                               row=26, column=4, columnspan=3, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    def _build_trash_button(self):
        self.trash_button = make_button(self.root, text='Clean List', width=9, command=self.__trash_list,
                                               row=26, column=1, columnspan=1, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))
    
    def _build_delete_hypergui_button(self):
        self.delete_hypergui_button = make_button(self.root, text='Delete\nhypergui-Folder', width=9, command=self.__delete_hg_folder,
                                               row=26, column=2, columnspan=2, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))


    def _build_select_superdir_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open OP\nFolder",
                                                   command=self.__add_data_cube_dirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=25, rowspan = 1, column=0, width=11, outer_pady=(5, 5))
    def _build_labelling_entry(self):
        labelling_text = make_text(self.root, content = "File-Filter:", row=24, column=0, width=14, bg=tkcolour_from_rgb((BACKGROUND)), padx=0, state=NORMAL, pady=0) 
        self.labelling_entry = make_entry(self.root, row=25, column=0, width=11)
        self.labelling_entry.bind("<KeyRelease>", self.__update_labelling)
    
    def _build_counter(self, n):
        self.lcounter_text = make_text(self.root, content = "N: " + str(n), row=23, column=0, width=14, bg=tkcolour_from_rgb((BACKGROUND)), padx=0, state=NORMAL, pady=0) 
        
    def _build_select_all_subfolders_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open Project\nFolder",
                                                   command=self.__add_data_cube_subdirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=26, rowspan=1, column=0, width=11, outer_pady=(5, 5))



    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, row=2, column=0, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, selectmode = "SINGLE", width = 32)
        self.selection_listbox.bind('<<ListboxSelect>>', self.__update_selected_data_cube)
        
    def _build_edit_coords_button(self):
        self.input_coords_button = make_button(self.root, text='Edit coords', width=9, command=self.__input_coords,
                                               row=26, column=11, columnspan=2, inner_pady=5, outer_padx=5,
                                               outer_pady=0, rowspan=1)
        
    def _build_inherit_checkbox(self):
        inherit_label = make_label(self.root, "inherit mask from previous", row=27, column=11, columnspan=1,
                                              outer_padx=(5, 5), outer_pady=(5, 5), inner_padx=10, inner_pady=5, wraplength=200)
        inherit_checkbox = make_checkbox(self.root, text="", row=27, column=12,
                                                    var=self.checkbox_value, sticky=NE, inner_padx=0,
                                                    inner_pady=0, outer_pady=(10, 0), outer_padx=(0, 20))
        inherit_checkbox.select()
        inherit_checkbox.bind('<Button-1>', self.__update_inherit_checkbox)
        
    def _build_tif_save_path_text(self, text = ""):
        self.tif_save_path_text =  make_text(self.root, content="Tif-Name: " + text, bg=tkcolour_from_rgb(BACKGROUND), column=10, row=0,
                                   width=65, columnspan=2, padx = 5)
        self.tif_save_path_text.configure(font=("Courier", 7, "italic"))
        
    def _build_tif_save_path_input(self):
        self.tif_save_path_input = make_entry(self.root, row=0, column=8, width=45, pady=(10, 10), columnspan=2)
        self.tif_save_path_input.bind('<Return>', self._update_tif_save_path_ext)
        
    
    def _build_save_tif(self):
        self.save_as_tif_label = make_button(self.root, "Save as Tif", row=26, column=9, outer_padx=(12, 0),
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5, rowspan = 1, columnspan=1, command = self.__save_tif)
        
    def _build_save_all_and_next(self):
        self.save_as_tif_label = make_button(self.root, "Save coordinates\n(w. Tif) and next", row=26, column=7, outer_padx=(12, 0), height= 2,
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5, rowspan = 1, columnspan=2, width = 15, command = self.__save_all)

    def _build_autonames_button(self):
        self.autonames_button = make_button(self.root, text='Auto', width=3, command=self.__switch_autoname,
                                               row=0, column=12, columnspan=1, inner_pady=0, outer_padx=5,
                                               outer_pady=1, rowspan=1)
    
    def _build_eudis_info(self):
        if self.move_mode:
            label = make_text(self.root, content="press m to toggle move-mode\nhold r for Rotation\nhold t for sTretch\npress o to Overwrite mask",
                                 bg=tkcolour_from_rgb((255,0,0)), column=11, row=24, width=28, columnspan=2,
                                 padx=0, state=NORMAL, pady=0, height = 5)
        else:
            label = make_text(self.root, content="press m to toggle move-mode\nhold r for Rotation\nhold t for sTretch\npress o to Overwrite mask",
                                     bg=tkcolour_from_rgb(BACKGROUND), column=11, row=24, width=28, columnspan=2,
                                     padx=0, state=NORMAL, pady=0, height = 5)
        
    def _build_live_button(self):
        self.live_button = make_button(self.root, text='Live', width=5, command=self.__update_live_checkbox,
                                               row=1, column=0, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=5, rowspan=1)
        self.live_button["bg"] = "white"
    
    def _build_delete_content(self):
        delete_content_label = make_label(self.root, "delete contents on save", row=1, column=11, columnspan=1,
                                              outer_padx=(35, 15), outer_pady=(10, 15), inner_padx=10, inner_pady=5, wraplength=140)
        delete_content_checkbox = make_checkbox(self.root, text="", row=1, column=12,
                                                    var=self.checkbox_value, sticky=NE, inner_padx=0,
                                                    inner_pady=0, outer_pady=(10, 0), outer_padx=(0, 20))
        delete_content_checkbox.select()
        delete_content_checkbox.bind('<Button-1>', self.__update_delete_content_checkbox)
        

    # ---------------------------------------------- IMAGE -----------------------------------------------
        
    def _build_original_image(self, data):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "Navigation:\n Mouse-Left or 'q' to place point\n '+' or 'w' to zoom in\n '-' or 's' to zoom out\n arrows to change image", row=1, column=1, rowspan=25,
                                             columnspan=10, inner_pady=300, inner_padx=400, outer_padx=(15, 10),
                                             outer_pady=(15, 10))
        else:
            #data = np.asarray(rgb_image_to_hsi_array(self.original_image_data)).reshape((480, 640))
            (self.original_image_graph, self.original_image, self.image_array) = \
                make_image(self.root, data, row=1, column=1, columnspan=10, rowspan=25, lower_scale_value=None,
                           upper_scale_value=None, color_rgb=BACKGROUND, original=True, figheight=7, figwidth=9, img = self.original_image, axs = self.original_image_graph, figu = self.original_image_graph)
            self.original_image.get_tk_widget().bind('<Button-2>', self.__pop_up_image)
            self.original_image.get_tk_widget().bind('<Button-1>', self.__click_event)
            self.original_image.get_tk_widget().bind('<ButtonRelease-1>', self.__end_move)
            self.original_image.get_tk_widget().bind('<+>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-minus>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-m>', self.__toggle_move_mode)
            self.original_image.get_tk_widget().bind('<Key-w>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-s>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-q>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Key-r>', self.__r_operation)
            self.original_image.get_tk_widget().bind('<Key-t>', self.__t_operation)
            self.original_image.get_tk_widget().bind('<Key-o>', self.__ov_mask)
            self.original_image.get_tk_widget().bind('<Key-f>', lambda event, arg = "all": self.__remove_pt(arg))
            self.original_image.get_tk_widget().bind('<KeyRelease-t>', self.__stop_stretch)
            self.original_image.get_tk_widget().bind('<KeyRelease-r>', self.__stop_rotation)
            self.original_image.get_tk_widget().bind('<Meta-L>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Alt-L>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Control_L>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Shift_L>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Caps_Lock>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<Leave>', self.__reset_mouse_position)
            self.original_image.get_tk_widget().bind('<Motion>', self.__update_mouse_position)
            self.original_image.get_tk_widget().bind('<MouseWheel>', self.__on_mousewheel)
            self.root.bind_all('<Left>', self.__prev)
            self.root.bind_all('<Right>', self.__next)
            self.root.bind_all('<Key-a>', self.__prev)
            self.root.bind_all('<Key-d>', self.__next)
            self.root.bind_all('<Up>', self.__first)
            self.root.bind_all('<Down>', self.__last)
            #self.original_image.get_tk_widget().bind('<Motion>', self.__update_cursor)
            self.original_image.get_tk_widget().focus_force()
            if self.pop_up:
                self.pop_up_graph = self.original_image_graph
                self.pop_up_graph.set_size_inches(8, 8)
                self.pop_up_image = FigureCanvasTkAgg(self.pop_up_graph, master=self.pop_up_window)
                self.pop_up_image.draw()
                self.pop_up_image.get_tk_widget().grid(column=0, row=0)
                self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
                
    def __on_mousewheel(self, event):
        if event.delta<0:
            self.__dezoom(event)
        else:
            self.__zoom(event)
            self.mouse_x = 320
            self.mouse_y = 240
            
    def __zoom(self, event):
        if self.zoom_factor < 16:
            self.zoom_factor = 2*self.zoom_factor
            self.view_mid[0] = round(self.view_mid[0] + self.mouse_y-240)*2
            self.view_mid[1] = round(self.view_mid[1] + self.mouse_x-320)*2
            max_x = self.zoom_factor*640-320
            max_y = self.zoom_factor*480 - 240
            if self.view_mid[0] < 240:
                self.view_mid[0] = 240
            if self.view_mid[1] < 320:
                self.view_mid[1] = 320
            if self.view_mid[0] > max_y:
                self.view_mid[0] = max_y
            if self.view_mid[1] > max_x:
                self.view_mid[1] = max_x
            self._draw_points()

        
        
    def __dezoom(self, event):
        if self.zoom_factor > 1:
            self.zoom_factor = round(0.5*self.zoom_factor)
            self.view_mid[0] = round((self.view_mid[0] + self.mouse_y-240)*0.5)
            self.view_mid[1] = round((self.view_mid[1] + self.mouse_x-320)*0.5)
            max_x = self.zoom_factor*640-320
            max_y = self.zoom_factor*480-240
            if self.view_mid[0] < 240:
                self.view_mid[0] = 240
            if self.view_mid[1] < 320:
                self.view_mid[1] = 320
            if self.view_mid[0] > max_y:
                self.view_mid[0] = max_y
            if self.view_mid[1] > max_x:
                self.view_mid[1] = max_x
            self._draw_points()
        
    def __update_mouse_position(self, event):
        pos = self.original_image_graph.axes[0].get_position()
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
        if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480:
            self.mouse_x = Xc
            self.mouse_y = Yc
            Xc = round((self.view_mid[1]+Xc-320)/self.zoom_factor)
            Yc = round((self.view_mid[0]+Yc-240)/self.zoom_factor)
        not_none = [i for i in self.coords_list if i != (None, None)]
        if not self.unfocus:
            self.original_image.get_tk_widget().focus_force()
        self.__update_cursor(event)
            
    def __reset_mouse_position(self, event):
        self.mouse_x = 320
        self.mouse_y = 240
    
    def __pop_up_image(self, event=None):
        (self.pop_up_window, self.pop_up_image) = make_popup_image(self.original_image_graph, interactive=True)
        self.pop_up = True
        self.pop_up_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
        self.pop_up_window.protocol("WM_DELETE_WINDOW", func=self.__close_pop_up)
        self.pop_up_window.attributes("-topmost", True)

    def __close_pop_up(self):
        self.pop_up = False
        self.pop_up_window.destroy()

    # --------------------------------------------------- DRAWING -----------------------------------------------------

    def _draw_points(self):
        if self.original_image_data is not None:
            copy_data = self.original_image_data.copy()
            not_none = [i for i in self.coords_list_copy if i != (None, None) ]
            for point in not_none:
                y = int(point[0])
                x = int(point[1])
                for xi in range(-4, 5):
                    copy_data[(x + xi) % 480, y, :3] = (100, 100, 100)
                for yi in range(-4, 5):
                    copy_data[x, (y + yi) % 640, :3] = (100, 100, 100)
                idx = not_none.index(point)
                self._draw_a_line(not_none[idx - 1], not_none[idx], copy_data, color = (100,100,100))   
                
            not_none = [i for i in self.coords_list if i != (None, None) ]
            for point in not_none:
                y = int(point[0])
                x = int(point[1])
                for xi in range(-4, 5):
                    copy_data[(x + xi) % 480, y, :3] = BRIGHT_GREEN_RGB
                for yi in range(-4, 5):
                    copy_data[x, (y + yi) % 640, :3] = BRIGHT_GREEN_RGB
                idx = not_none.index(point)
                self._draw_a_line(not_none[idx - 1], not_none[idx], copy_data, color = self.color)
 
            left = self.view_mid[1] - 320
            bottom = self.view_mid[0] - 240
            right = left + 640
            top = bottom + 480
            im = Image.fromarray(copy_data)
            im = im.resize((640*self.zoom_factor, 480*self.zoom_factor)) 
            im = im.crop((left, bottom, right, top))
            self._build_original_image(np.array(im))
            self.original_image.get_tk_widget().focus_force()
        
    @staticmethod
    def _draw_a_line(point1, point2, image, color = (113,255,66)):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i] % 480, cc[i] % 640] = (int(color[0] * val[i]), int(color[1] * val[i]), int(color[2] * val[i]))
        return image

    # --------------------------------------------- ADDING/REMOVING COORDS --------------------------------------------

    def __save_coords(self, save_tif = False):
        path = os.path.dirname(self.get_selected_data_cube_path())
        output_path1 = path + "/"+self.listener.output_folder_hypergui+"/mask" + '.csv'
        output_path2 = path + "/"+self.listener.output_folder_hypergui+"/MASK_COORDINATES" + '.csv'
        if os.path.exists(output_path1) or os.path.exists(output_path2):
            self.unfocus = True
            yn = messagebox.askquestion ('Verify','Are you sure you want to override mask.csv and MASK_CORDINATES.csv?',icon = 'warning')
            if yn == "yes":
                self.unfocus = False
                self.__save_points()
                self.__save_mask()
                if save_tif:
                    self.__save_tif()
        else:
            self.__save_points()
            self.__save_mask()
            if save_tif:
                self.__save_tif()
                
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(sel+1) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        #self.__remove_pt('all')

    def __get_coords(self, event):
        if not self.pop_up:
            pos = self.original_image_graph.axes[0].get_position()
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
            
            Xc = round((self.view_mid[1]+Xc-320)/self.zoom_factor)
            Yc = round((self.view_mid[0]+Yc-240)/self.zoom_factor)
            if Xc>=0 and Yc>=0 and Xc<=640 and Yc<=480:
                self.__add_pt((Xc, Yc))

        else:
            x = int((eventorigin.x - 17) * 640 / 770)
            y = int((eventorigin.y - 114) * 480 / 578)
            if 0 <= x < 640 and 0 <= y < 480:
                self.__add_pt((x, y))
                
    def __get_coords_list(self):
        point_coords = self.coords_list
        data = [[float(point_coords[i][0] + 1), float(point_coords[i][1] + 1)] for i in range(1000000) if
                point_coords[i] != (None, None)]
        return data
    
    def __input_coords(self):
        self.coords_window_frame = Toplevel()
        self.coords_window_frame.geometry("+0+0")
        self.coords_window_frame.configure(bg=tkcolour_from_rgb(BACKGROUND))
        
        self.frame_canvas = Frame(self.coords_window_frame)
        self.frame_canvas.grid(row=2, column=11, columnspan = 2, pady=(5, 0), sticky='nw', rowspan = 250)
        self.frame_canvas.grid_propagate(False)
        self.canvas = Canvas(self.frame_canvas, bg="yellow")
        self.canvas.grid(row=0, column=1, sticky="news")
        vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        vsb.grid(row=0, column=0, rowspan=5, sticky='ns')
        
        self.canvas.configure(yscrollcommand=vsb.set)
        self.coords_window = Frame(self.canvas, bg="blue")
        self.canvas.create_window((0, 0), window=self.coords_window, anchor='nw')
        


        # title
        self.input_points_title = make_label_button(self.coords_window, text='Coordinate Input',
                                                    command=self.__input_info, width=14)
        self.input_points_title.grid(columnspan=3)

        # points
        for ii in range(1000):
            self.input_pt_title_list[ii], self.input_pt_title_x_list[ii], self.input_pt_title_y_list[ii], self.input_pt_x_list[ii], self.input_pt_y_list[ii] = \
                self.__input_coord_n(ii)

        # go button
        self.go_button = make_button(self.coords_window, text='Go', width=2, command=self.__use_inputted_coords, row=201,
                                     column=3, columnspan=5, inner_pady=5, outer_padx=(15, 15), outer_pady=(7, 15))
        self.all_remove = make_button(self.coords_window, text='x', width=1, command=lambda: self.__remove_pt_n('all'),
                                         row=0, column=5, columnspan=1, inner_padx=3, inner_pady=0, outer_padx=10,
                                         highlightthickness=0)
        self.coords_window.update_idletasks()
        self.frame_canvas.config(width=1350,
                            height=900)
        self.canvas.config(width=1300,
                            height=900)
        
        
        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def __input_coord_n(self, num):
        rom = num % 200
        col = math.floor(num/200)*6
        self.title[num] = make_text(self.coords_window, content="Pt " + str(num) + ': ', bg=tkcolour_from_rgb(BACKGROUND),
                          column=col+0, row=rom + 1, width=6, pady=(0, 3), padx=(15, 0), text = self.title[num])
        self.title_x[num] = make_text(self.coords_window, content="x = ", bg=tkcolour_from_rgb(BACKGROUND), column=col+1, row=rom + 1,
                            width=4, pady=(0, 3), text = self.title_x[num])
        self.title_y[num] = make_text(self.coords_window, content="y = ", bg=tkcolour_from_rgb(BACKGROUND), column=col+3, row=rom + 1,
                            width=4, pady=(0, 3), padx=(5, 0), text = self.title_y[num])
        input_x = make_entry(self.coords_window, row=rom + 1, column=col+2, width=5, columnspan=1, pady=(0, 3))
        input_y = make_entry(self.coords_window, row=rom + 1, column=col+4, width=5, columnspan=1, padx=(0, 15),
                             pady=(0, 3))
        if self.coords_list[num] != (None, None):
            input_x.insert(END, str(self.coords_list[num][0] + 1))
            input_y.insert(END, str(self.coords_list[num][1] + 1))
            
        remove = make_button(self.coords_window, text='x', width=1, command=lambda: self.__remove_pt_n(num + 1), row=rom +1,
                         column=col+5, highlightthickness=0)
        return self.title[num], self.title_x[num], self.title_y[num], input_x, input_y
    
    def __use_inputted_coords(self):
        coords = []
        for ii in range(1000):
            coords.append([self.input_pt_x_list[ii].get(), self.input_pt_y_list[ii].get()])
        coords = [(int(i[0]) - 1, int(i[1]) - 1) for i in coords if i[0] != '' and i[1] != '']
        if len(coords) > 0:
            xs = [i[0] for i in coords]
            ys = [i[1] for i in coords]
            if min(xs) >= 0 and max(xs) < 640 and min(ys) >= 0 and max(ys) < 480:
                coords = coords + [(None,None) for ii in range(1000-len(coords))]
                self.coords_list = coords +self.coords_list[1000::]
                self._build_points()
                self._draw_points()
            else:
                messagebox.showerror("Error", "x values must be on the interval [1, 640] and y values must be on the "
                                              "interval \n[1, 480].")
        self.coords_window_frame.destroy()

    def __remove_pt(self, index):
        if index == 'all':
            self.coords_list = [(None, None) for _ in range(1000000)]
        elif index == 'last':
            counter = 0
            for element in self.coords_list:
                if element[0] is not None:
                    last_index = counter
                counter = counter + 1
            self.coords_list[last_index] = (None, None)
        else:
            self.coords_list[index - 1] = (None, None)
        self.coords_list_copy = self.coords_list[:]
        self._build_points()
        self._draw_points()
        
        
    def __remove_pt_n(self, index):
        if index == 'all':
            self.coords_list = [(None, None) for _ in range(1000000)]   
            for ii in range(1000):
                self.__input_coord_n(ii)
            self._build_points()
            self._draw_points()
        else:
            self.coords_list[index - 1] = (None, None)     
            self.__input_coord_n(index - 1)
            self._build_points()
            self._draw_points()

    def __add_pt(self, pt):
        if self.coords_list.count((None, None)) != 0:
            index = self.coords_list.index((None, None))
            if pt[0] <640 and pt[1] < 480:
                self.coords_list[index] = pt
                self.coords_list_copy = self.coords_list[:]
                self._build_points()
                self._draw_points()
                if self.coords_window is not None:
                    self.__input_coord_n(index)
                xChoords = [x[0] for x in self.coords_list if x[0] is not None]
                yChoords = [x[1] for x in self.coords_list if x[1] is not None]
                minX = min(xChoords)
                maxX = max(xChoords)
                minY = min(yChoords)
                maxY = max(yChoords)
                middleX = int((maxX - minX)/2 + minX)
                middleY = int((maxY - minY)/2 + minY)
                self.origin = (middleX, middleY)
                self.bbox_x1 = minX
                self.bbox_x2 = maxX
                self.bbox_y1 = minY
                self.bbox_y2 = maxY
        
                
    # ------------------------------------ Selection Listbox (add / remove datacubes) ----------------------------
    
 #   def __add_data_cube_dirs(self):
 #       super_dir = self.__get_path_to_dir("Please select folder containing all the data folders.")
 #       sub_dirs = self.__get_sub_folder_paths(super_dir)
 #       for sub_dir in sub_dirs:
 #           if len(glob.glob(sub_dir + "/*RGB-Image.png"))>=1:
 #               self.__add_data_cube(sub_dir)
 #               print("adding")
 #       self.__add_from_data_cube_paths()
            
    def __add_from_data_cube_paths(self, event = None):
        self.selection_listbox.delete(0,'end')
        ii = 0
        real_idx = []
        cc=0
        for dc_path in self.data_cube_paths:
            super_dir = os.path.dirname(os.path.abspath(dc_path))
            if len(glob.glob(super_dir + "/"+self.labelling_name))>0:
                concat_path = os.path.basename(os.path.normpath(dc_path)) 
                self.selection_listbox.insert(END, concat_path)
                self.selection_listbox.config(width=32)
                real_idx.append(ii)
                cc=cc+1
            ii = ii+1
        self.idx_dict = dict(zip(list(np.arange(0,len(real_idx),1)), real_idx))
        self._build_counter(cc)
        
    def __add_data_cube(self, sub_dir):
        contents = os.listdir(sub_dir)
        dc_path = [sub_dir + "/" + i for i in contents if "SpecCube.dat" in i]  # takes first data cube it finds
        if len(dc_path) > 0:
            dc_path = dc_path[0]
            if dc_path in self.data_cube_paths:
                messagebox.showerror("Error", "That data has already been added.")
            else:
                self.data_cube_paths.append(dc_path)
        
                
    
    def __add_data_cube_subdirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the OP folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir, True)
        for sub_dir in sub_dirs:
            if len(glob.glob(sub_dir + "/*RGB-Image.png"))>=1:
                self.__add_data_cube(sub_dir)
        self.__add_from_data_cube_paths()

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
    
    def _insert_data_cube_paths(self):
        for dc_path in self.data_cube_paths:
            concat_path = os.path.basename(os.path.normpath(dc_path))
            self.selection_listbox.insert(END, concat_path)
            self.selection_listbox.config(width=32)
        self._build_counter(len(self.data_cube_paths))
    
    def __trash_list(self):
        self.data_cube_paths = []
        self.selection_listbox.delete(0,'end')
        self.coords_list = [(None, None) for _ in range(1000000)]
        self.__remove_pt('all')
        self._build_counter(len(self.data_cube_paths))
    
    # ------------------------------------ Selection Listbox (control) ----------------------------
                
    def __next(self, event = None):
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(sel+1) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
            
    def __prev(self, event = None):
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        if sel is not 0:
            self.selection_listbox.selection_clear(0, END)
            self.selection_listbox.select_set(sel-1) #This only sets focus on the first item.
            self.selection_listbox.event_generate("<<ListboxSelect>>")
    
    def __first(self, event = None):
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(0) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        
    def __last(self, event = None):
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set("end") #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")

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
        self.update_original_image(self.RGB)

    def __update_to_sto2(self):
        self.active_image = "STO2"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="red")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.STO2)

    def __update_to_nir(self):
        self.active_image = "NIR"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="red")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.NIR)

    def __update_to_thi(self):
        self.active_image = "THI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="red")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.THI)

    def __update_to_twi(self):
        self.active_image = "TWI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="red")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.TWI)
        
    def __update_to_tli(self):
        self.active_image = "TLI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="red")
        self.ohi_button.config(foreground="black")
        self.update_original_image(self.TLI)
        
    def __update_to_ohi(self):
        self.active_image = "OHI"
        self.rgb_button.config(foreground="black")
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.tli_button.config(foreground="black")
        self.ohi_button.config(foreground="red")
        self.update_original_image(self.OHI)
        

    # ------------------------------------------------- Saving / Loading --------------------------------------------------
        
    def __save_mask(self):
        polygon = [point for point in self.coords_list if point != (None, None)]
        if len(polygon)>0:
            img = Image.new('L', (640, 480), 0)
            ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
            mask_array = np.array(img)
            path = os.path.dirname(self.get_selected_data_cube_path())
            if not os.path.exists(path + '/'+self.listener.output_folder_hypergui):
                os.mkdir(path + '/'+self.listener.output_folder_hypergui)
            output_path = path + '/'+self.listener.output_folder_hypergui + "/mask" + '.csv'
            np.savetxt(output_path, mask_array, delimiter=",", fmt="%d")
        else:
            pass
        
    def __save_points(self):
        data = self.__get_coords_list()
        if len(data)>0:
            path = os.path.dirname(self.get_selected_data_cube_path())
            if self.delete_content:
                if os.path.exists(path + '/'+self.listener.output_folder_hypergui):
                    shutil.rmtree(path + '/'+self.listener.output_folder_hypergui)
            if not os.path.exists(path + '/'+self.listener.output_folder_hypergui):
                os.mkdir(path + '/'+self.listener.output_folder_hypergui)
            output_path = path + '/'+self.listener.output_folder_hypergui + "/MASK_COORDINATES" + '.csv'
            np.savetxt(output_path, data, delimiter=",", fmt="%1.2f")
        else:
            pass
        
            
    def __save_tif(self):
            polygon = [point for point in self.coords_list if point != (None, None)]
            if len(polygon) >= 2:
                self._update_tif_save_path()
                path = os.path.dirname(self.get_selected_data_cube_path())
                if not os.path.exists(path + '/'+self.listener.output_folder_hypergui):
                    os.mkdir(path + '/'+self.listener.output_folder_hypergui)
                img = Image.new('L', (640, 480), 0)
                ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
                output_path = self.tif_save_path
                mask_img = Image.fromarray(((np.array(img)*-1+1)*255).astype("uint8"), 'L')
                mask_img.save(output_path)
            else:
                print("Draw a mask to save TIF.")
    
    def __delete_hg_folder(self, event = None):
        path = os.path.dirname(self.get_selected_data_cube_path())
        parent = path + '/'+self.listener.output_folder_hypergui
        if os.path.exists(parent):
            for filename in os.listdir(parent):
                file_path = os.path.join(parent, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        shutil.rmtree(parent)
        self.__remove_pt('all')
    
    def _update_tif_save_path(self, event = None):
        if self.get_selected_data_cube_path() is not None:
            path = os.path.dirname(self.get_selected_data_cube_path())
            self.tif_save_path_stem = path + '/' + self.listener.output_folder_hypergui +"/"
            if self.tif_save_path_end is None or self.automatic_names:
                self.tif_save_path_end = os.path.basename(path) + '_mask' + self.listener.output_folder_hypergui
            self.tif_save_path_input.delete(0,"end")
            self.tif_save_path_input.insert(0, self.tif_save_path_end)
            self.tif_save_path = self.tif_save_path_stem + self.tif_save_path_end + ".tif"
            self._build_tif_save_path_text(text  = self.tif_save_path_end)
            
    def _update_tif_save_path_ext(self, event = None):
        if self.get_selected_data_cube_path() is not None:
            self.automatic_names = False
            path = os.path.dirname(self.get_selected_data_cube_path())
            self.tif_save_path_stem = path + '/' + self.listener.output_folder_hypergui +"/"
            self.tif_save_path_end = self.tif_save_path_input.get()
            self.tif_save_path_input.delete(0,"end")
            self.tif_save_path_input.insert(0, self.tif_save_path_end)
            self.tif_save_path = self.tif_save_path_stem + self.tif_save_path_end + ".tif"
            self._build_tif_save_path_text(text = self.tif_save_path_end)  
            
    def __switch_autoname(self):
        self.automatic_names=True
        self._update_tif_save_path()
    
    def __save_all(self):
        self.__save_coords(True)
        
    def __load_mask(self, path):
        coords = []
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            for row in read_csv:
                coords.append(((int(float(row[0]) - 1)), (int(float(row[1]) - 1))))
            csvfile.close()
        for i in range(1000000 - len(coords)):
            coords.append((None, None))
        self.coords_list = coords
        self.coords_list_copy = self.coords_list[:]
        self._build_points()
        self._draw_points()
        self.original_image.get_tk_widget().focus_force()
        xChoords = [x[0] for x in self.coords_list if x[0] is not None]
        yChoords = [x[1] for x in self.coords_list if x[1] is not None]
        minX = min(xChoords)
        maxX = max(xChoords)
        minY = min(yChoords)
        maxY = max(yChoords)
        middleX = int((maxX - minX)/2 + minX)
        middleY = int((maxY - minY)/2 + minY)
        self.origin = (middleX, middleY)
        self.bbox_x1 = minX
        self.bbox_x2 = maxX
        self.bbox_y1 = minY
        self.bbox_y2 = maxY
    
    def __update_delete_content_checkbox(self, event = None):
        self.delete_content= not self.delete_content
        
    def __update_inherit_checkbox(self, event = None):
        self.inherit= not self.inherit
        
    
    #----------------------------- Live-Functions (Watchdog) ----------------------------------
    
    def __update_live_checkbox(self, event = None):
        self.live= not self.live
        if self.live:
            self.live_button["text"] = "Stop"
            self.live_button["bg"] = "red"
            self.live_folder= self.__get_path_to_dir("Please select folder to watch.")
        else:
            print("not watching... -_-")
            self.live_button["text"] = "Live"
            self.live_button["bg"] = "white"
        self.__start_watchdog()
        
    def __start_watchdog(self):
        if self.live:
            self.__watchdog()
            self.root.after(1000, self.__start_watchdog)
        else:
            pass
    
    def __watchdog(self):
        print("watching... O_O")
        super_dir = self.live_folder
        sub_dirs = self.__get_sub_folder_paths(super_dir, True)
        if not self.sub_dirs == sub_dirs:
                self.sub_dirs = sub_dirs 
                self.__trash_list()
                self.__watch_folder()
        
    def __watch_folder(self):
        if self.current_dc_path is None:
            self.current_dc_path = 0
        super_dir = self.live_folder
        sub_dirs = self.__get_sub_folder_paths(super_dir, True)
        for sub_dir in sub_dirs:
            if len(glob.glob(sub_dir + "/*RGB-Image.png"))==1:
                self.__add_data_cube(sub_dir)
        self.__add_from_data_cube_paths()
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set("end") 
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        
    #---------------------------------------- Info ---------------------------------
        
    def __input_info(self):
        info = self.listener.modules[INFO].input_info
        title = "Coordinate Input"
        make_info(title=title, info=info)
        
    
    def __info(self):
        info = self.listener.modules[INFO].bp_info
        title = "Batch Processing"
        make_info(title=title, info=info)
    
   #-------------------------------------- Transform -----------------------------
    
    def __ov_mask(self, event = None):
        self.coords_list = self.coords_list_copy[:]
        self._draw_points()
        xChoords = [x[0] for x in self.coords_list if x[0] is not None]
        yChoords = [x[1] for x in self.coords_list if x[1] is not None]
        minX = min(xChoords)
        maxX = max(xChoords)
        minY = min(yChoords)
        maxY = max(yChoords)
        middleX = int((maxX - minX)/2 + minX)
        middleY = int((maxY - minY)/2 + minY)
        self.origin = (middleX, middleY)
        self.bbox_x1 = minX
        self.bbox_x2 = maxX
        self.bbox_y1 = minY
        self.bbox_y2 = maxY
        self.xsh_last = 0
        self.ysh_last = 0
        self.rot_last = 0
        self.xstr_last = 1
        self.ystr_last = 1
        self.xsh = 0
        self.ysh= 0
        self.rot = 0
        self.xstr = 1
        self.ystr = 1
        

    def rotate(self, origin, point, angle):
        angle = angle * math.pi/180
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return (int(qx), int(qy))
    
    def stretch(self, origin, point, x, y):
        y_orig = origin[1]
        x_orig = origin[0]
        x_pt = point[0]
        y_pt = point[1]
        y_dist = y_pt - y_orig
        x_dist = x_pt - x_orig
        qx = x_orig + x*x_dist
        qy = y_orig + y*y_dist
        return (int(qx), int(qy))
        
    def __transfrom_coords(self):
        ii = 0
        for coord in self.coords_list:
            if coord[0] is not None:
                coord = self.rotate(self.origin, coord, self.rot)
                coord = self.stretch(self.origin, coord, self.xstr, self.ystr)
                coord = (coord[0]+self.xsh, coord[1]+self.ysh)
                if coord[0] < 0:
                    coord = (0,coord[1])
                if coord[1] < 0:
                    coord = (coord[0],0)
                if coord[0] >= 640:
                    coord = (639, coord[1])
                if coord[1] >= 480:
                    coord = (coord[0],479)
                self.coords_list_copy[ii] = coord
            ii = ii+1
        xChoords = [x[0] for x in self.coords_list_copy if x[0] is not None]
        yChoords = [x[1] for x in self.coords_list_copy if x[1] is not None]
        minX = min(xChoords)
        maxX = max(xChoords)
        minY = min(yChoords)
        maxY = max(yChoords)
        middleX = int((maxX - minX)/2 + minX)
        middleY = int((maxY - minY)/2 + minY)
        self.bbox_x1 = minX
        self.bbox_x2 = maxX
        self.bbox_y1 = minY
        self.bbox_y2 = maxY
        self._draw_points()
        
    def __update_cursor(self, event = None):
        if event is not None and self.move_mode:
            pos = self.original_image_graph.axes[0].get_position()
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
            if not self.start_move:
                if Xc>=self.bbox_x1 and Yc>=self.bbox_y1 and Xc<=self.bbox_x2 and Yc<=self.bbox_y2:
                    if not self.rotate_on and not self.stretch_on:
                        self.root.config(cursor="fleur")
                        self.grab = True
                else: 
                    self.root.config(cursor="")
                    self.grab = False
            else:
                if self.rotate_on:
                    self.rot = self.rot_last + int((Yc - self.move_start_y)/2)
                elif self.stretch_on:
                    self.xstr = self.xstr_last + (Xc - self.move_start_x)/100
                    self.ystr = self.ystr_last + (Yc - self.move_start_y)/100
                else:
                    self.xsh = self.xsh_last + (Xc - self.move_start_x) 
                    self.ysh = self.ysh_last + (Yc - self.move_start_y)
                self.__transfrom_coords()
    
    def __toggle_move_mode(self, event = None):
        self.move_mode = not self.move_mode
        if not self.move_mode:
            self.root.config(cursor="")
            self.color = (113,255,66)
            self.ysh = 0
            self.xsh = 0
            self.rot_last = 0
            self.xsh_last = 0
            self.ysh_last = 0
            self.xstr_last = 1
            self.ystr_last = 1
        else:
            self.color = (255,255,0)
        self._draw_points()
        self._build_eudis_info()
    
    def __click_event(self, event):
        if self.move_mode:
            self.__start_move(event)
        else:
            self.__get_coords(event)
    
    def __start_move(self, event):
        self.start_move = True
        pos = self.original_image_graph.axes[0].get_position()
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
        self.move_start_x = Xc
        self.move_start_y = Yc
    
    def __end_move(self, event):
        if self.start_move:
            self.start_move = False
            self.move_start_x = None
            self.move_start_y = None
            self.xsh_last = self.xsh
            self.ysh_last = self.ysh
            self.xstr_last = self.xstr
            self.ystr_last = self.ystr
            self.rot_last = self.rot
    
    def __r_operation(self, event):
        if self.move_mode:
            self.rotate_on = True
            self.root.config(cursor="exchange")
        else:
            self.__get_coords(event)
        
    def __stop_rotation(self, event = None):
        self.rotate_on = False
        self.root.config(cursor="")
        self.rot_last = self.rot
        
        
    def __t_operation(self, event):
        if self.move_mode:
            self.stretch_on = True
            self.root.config(cursor="sizing")
        
    def __stop_stretch(self, event = None):
        self.stretch_on = False
        self.root.config(cursor="")
        self.xstr_last = self.xstr
        self.ystr_last = self.ystr
        
###############  Labelling ##################
        
    def __update_labelling(self, event = None):
        self.labelling_name = self.labelling_entry.get()
        self.labelling_name = "*"+ self.labelling_name + "*"
        self.__add_from_data_cube_paths()
        
        
        
        
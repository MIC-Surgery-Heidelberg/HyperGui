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


class SpecInvest:
    def __init__(self, SI_frame, listener):
        self.root = SI_frame

        # Listener
        self.listener = listener
        
        # Bools
        self.unfocus = False
        self.live = False
        
        #Lists
        self.data_cube_paths = []
        self.sub_dirs = []
        
        # GUI
        self.select_data_cube_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.data_cube_path_label = None
        self.rgb_button = None
        self.sto2_button = None
        self.nir_button = None
        self.thi_button = None
        self.twi_button = None
        self.tli_button = None
        self.ohi_button = None
        self.active_image = "RGB"
        self.live_folder = None

        self.original_image_graph = None
        self.original_image_data = None
        self.original_image = None
        self.image_array = None

        self.current_dc_path = None
        
        self.zoom_factor = 1
        self.color = (113,255,66)
        
        self.choices2 = ['0. derivative', 
                        '1. derivative',
                        '2. derivative',
                        ]
        
        self.choices_dyn = ['static', 
                        'dynamic']
        
        self.gradient = "og"
        self.absorption_spec = None
        self.axes = None 
        self.drop_down_var2 = StringVar()
        self.drop_down_var_dyn = StringVar()
        
        self.y_high = 1
        self.y_low = 0
        
        self.dyn=True
        
        self.curve_sm = "curve"
        
        self.x_vals = np.arange(500, 1000, 5)
        
        self.interactive_absorption_spec_graph = None
        
        #Mouse
        self.mouse_x = 320
        self.mouse_y = 240
        self.view_mid = [240, 320]      
        
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
    
    def update_saved(self, key, value):
        assert type(value) == bool
        self.saves[key] = value
        
    def __update_selected_data_cube(self, event):
        if len(self.selection_listbox.curselection())>0:
            dc_path = self.get_selected_data_cube_path()[0:-12]
            self.data_cube = self.__read(self.get_selected_data_cube_path())
            if self.current_dc_path is not self.selection_listbox.curselection()[0]:
                if len(self.selection_listbox.curselection())>0:
                    self.current_dc_path = self.selection_listbox.curselection()[0]
        else:
            dc_path = self.data_cube_paths[0][0:-12]
            self.data_cube = self.__read(self.data_cube_paths[0])
            self.current_dc_path = 0
        
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
        self._build_original_image(self.original_image_data)
        #self._build_select_superdir_button()
        self._build_labelling_entry()
        self._build_select_all_subfolders_button()
        self._build_trash_button()
        self._build_next_button()
        self._build_live_button()
        self._build_info_label()
        self._build_curve_graph()
        self._build_drop_down2()
        self._build_drop_down_dyn()
        self._build_counter(0)
        
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

        
        
    # ----------------------------------------------- BUILDERS (MISC) -----------------------------------------------
        
    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Spectrum Calculation', command=self.__info, width=8)

    def _build_next_button(self):
        self.next_button = make_button(self.root, text='Next (wo. saving)', width=12, command=self.__next,
                                               row=26, column=10, columnspan=1, inner_pady=5, outer_padx=5,
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
      
    def _build_live_button(self):
        self.live_button = make_button(self.root, text='Live', width=5, command=self.__update_live_checkbox,
                                               row=1, column=0, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=5, rowspan=1)
        self.live_button["bg"] = "white"
        
    def _build_drop_down_dyn(self): 
        self.drop_down_var_dyn.set(self.choices_dyn[0])
        self.drop_down_menu_dyn = OptionMenu(self.root, self.drop_down_var_dyn, *self.choices_dyn, command=self.__change_dyn)
        self.drop_down_menu_dyn.configure(highlightthickness=0, width=10,
                                      anchor='w')
        self.drop_down_menu_dyn.grid(column=13, row=6, columnspan=2)
        
    def _build_drop_down2(self): 
        self.drop_down_var2.set(self.choices2[0])
        self.drop_down_menu2 = OptionMenu(self.root, self.drop_down_var2, *self.choices2, command=self.__set_der)
        self.drop_down_menu2.configure(highlightthickness=0, width=10,
                                      anchor='w')
        self.drop_down_menu2.grid(column=11, row=6, columnspan=2)
        
        self.lower_text = make_text(self.root, content="Lower: ", bg=tkcolour_from_rgb(BACKGROUND), column=11, row=8,
                                    width=7, columnspan=1, pady=(0, 5))
        self.lower_input = make_entry(self.root, row=8, column=12, width=5, columnspan=1)
        self.lower_input.bind('<Return>', self.__update_upper_lower)
        self.lower_input.insert(END, str(self.y_low))
        
        self.upper_text = make_text(self.root, content="Upper: ", bg=tkcolour_from_rgb(BACKGROUND), column=13, row=8,
                                    width=7, columnspan=1, pady=(0, 5))
        self.upper_input = make_entry(self.root, row=8, column=14, width=5, columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper_lower)
        self.upper_input.insert(END, str(self.y_high))
    

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
            self.original_image.get_tk_widget().bind('<+>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-minus>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-w>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-s>', self.__dezoom)
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
        if not self.unfocus:
            self.original_image.get_tk_widget().focus_force()
        self.absorption_spec = self.data_cube[int(Yc), int(Xc), :]
        self.absorption_spec_gradient1 = np.gradient(self.absorption_spec)
        self.absorption_spec_gradient2 = np.gradient(self.absorption_spec_gradient1)
        self._build_curve_graph()
            
    def __reset_mouse_position(self, event):
        self.mouse_x = 320
        self.mouse_y = 240



        
                
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
        
    
    def __info(self):
        info = self.listener.modules[INFO].spec_invest_info
        title = "Spectrum Investigation"
        make_info(title=title, info=info)
    
   #-------------------------------------- Labelling -----------------------------
        
    def __update_labelling(self, event = None):
        self.labelling_name = self.labelling_entry.get()
        self.labelling_name = "*"+ self.labelling_name + "*"
        self.__add_from_data_cube_paths()
        
    #-------------------------------------- Graph -----------------------------
        
    def __set_der(self, event = None):
        choice = self.drop_down_var2.get()[0]
        if choice == '0':
            self.gradient = "og"
        elif choice == '1':
            self.gradient = "first"
        elif choice == '2':
            self.gradient = "second"
        self._build_curve_graph()
            
    def __change_dyn(self, event):
        choice = self.drop_down_var_dyn.get()
        if choice == 'dynamic':
            self.dyn = True
        elif choice == 'static':
            self.dyn = False
        self._build_curve_graph()
        
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
        self.interactive_absorption_spec.get_tk_widget().grid(column=11, row=5, columnspan=4, rowspan=1)
 
    def __update_upper_lower(self, event):
        self.y_low = float(self.lower_input.get())
        self.y_high = float(self.upper_input.get())
        self._build_curve_graph()       
 
    @staticmethod   
    def __read(path):
        data = np.fromfile(path, dtype='>f')  # returns 1D array and reads file in big-endian binary format
        if data[3:].size == 38880000:
            data_cube = data[3:].reshape(720, 540, 100)
        else:        
            data_cube = data[3:].reshape(640, 480, 100)  # reshape to data cube and ignore first 3 values
        return np.rot90(data_cube)
    
    @staticmethod
    def format_axis(x, _):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 4))
        
        
        
        
#Added by Jan Odenthal, University of Heidelberg,  odenthal@stud.uni-heidelberg.de
#Commissioned by Universitätsklinikum Heidelberg, Klinik für Allgemein-, Viszeral- und Transplantationschirurgie

from HyperGuiModules.utility import *
from HyperGuiModules.constants import *
from AnalysisModules.analysis_recreated import RecreatedAnalysis
from skimage.draw import line_aa
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import os
import glob
import xlsxwriter
import pandas as pd
import shutil

class Progressions:
    def __init__(self, prog_frame, listener):
        self.root = prog_frame

        # Listener
        self.listener = listener
        
        # BOOLS & CHECKBOXES
        self.save_tif_bool = False
        self.first = True
        self.delete_content = True
        self.save_as_tif_checkbox_value = IntVar()
        self.var_keep = IntVar()
        self.var_load_recent = IntVar()
        self.keep = False
        self.load_recent = False
        
        # COORDS & MOUSE POSITION
        self.mouse_x = 320
        self.mouse_y = 240
        self.view_mid = [240, 320]
        self.measure_point = (None, None)
        self.coords_list = [(None, None) for _ in range(2)]
        
        # NUMERICAL
        self.counter = 0
        self.line_index = 0
        self.zoom_factor = 1
        self.name_unique = False
        
        self.y_low = 0
        self.y_high = 100
        self.dyn = False
        
        # LISTS  
        self.lines = [[(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)]
                      ]
        self.centers = [(None, None)]*100           
        self.data_cube_paths = []
        self.vals = {"RGB": [], "STO2": [], "NIR":[], "THI": [], "TWI":[], "TLI": [], "OHI": []}
        self.vals_fc = {"RGB": [], "STO2": [], "NIR":[], "THI": [], "TWI":[], "TLI": [], "OHI": []}
        # GUI
        self.select_data_cube_button = None
        self.select_output_dir_button = None
        self.render_data_cube_button = None
        self.selection_listbox = None
        self.data_cube_path_label = None
        self.output_dir_label = None
        self.delete_button = None
        self.title1 = None
        self.data_cube_path_label = None
        self.path_label = None
        self.rgb_button = None
        self.sto2_button = None
        self.nir_button = None
        self.thi_button = None
        self.twi_button = None
        self.tli_button = None
        self.ohi_button = None
        self.all_points_remove = None
        self.instant_save_button = None
        self.input_coords_button = None
        self.coords_window = None
        self.input_points_title = None
        self.go_button = None
        self.original_image_graph = None
        self.choices_dyn = ['static', 
                        'dynamic']
        self.drop_down_var = StringVar()
        self.choices = [ 
                        '1. STO2',
                        '2. NIR',
                        '3. THI',
                        '4. TWI',
                        '5. TLI',
                        '6. OHI',]
        self.drop_down_var_dyn = StringVar()
        self.curve_mode = "STO2"

        self.THI_render = None
        self.TLI_render = None
        self.TWI_render = None
        self.OHI_render = None
        self.NRI_render = None
        self.STO2_render = None
        
        # SAVING & LOADING
        self.filename = "_prog_results_1"
        self.image_to_save = None
        self.current_dc_path = None
        
        # IMAGE
        self.image_array = None
        self.active_image = "RGB"
        self.original_image_data = None
        self.original_image = None

        self._init_widget()

    # ---------------------------------------------- UPDATER AND GETTERS ----------------------------------------------
        

    def get_selected_data_cube_path(self):
        if len(self.selection_listbox.curselection())>0:
            index = self.selection_listbox.curselection()[0]
        else: 
            index = self.current_dc_path
        return self.data_cube_paths[index]

    def get_selected_data_paths(self):
        selection = self.selection_listbox.curselection()
        selected_data_paths = [self.data_cube_paths[i] for i in selection]
        return selected_data_paths
    
    def update_filename(self, event = None):
        self.counter = 0
        self.filename_unique = self.filename_entry.get()
        self.name_unique = True
        self._new_filename()
    
    def _insert_filename(self):
        self.filename_entry.delete(0,"end")
        self.filename_entry.insert(0, self.filename)

    def update_original_image(self, original_image_data):
        self.original_image_data = original_image_data
        self._build_original_image(self.original_image_data)
        self._draw_points()
    
    def update_saved(self, key, value):
        assert type(value) == bool
        self.saves[key] = value
        
    def update_conversion_factor(self, event = None):
        self.conversion_factor = float(self.input_conversion_factor.get())
        self.input_conversion_factor.delete(0,"end")
        self.input_conversion_factor.insert(0, str(self.conversion_factor))
        self.__update_all_listboxes()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_info_label()
        self._build_rgb()
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_tli()
        self._build_ohi()
        self._build_instant_save_button()
        self._build_original_image(self.original_image_data)
        self._build_select_superdir_button()
        self._build_select_all_subfolders_button()
        self._build_selection_box()
        self._build_line_box()
        self._build_centers_box()
        self._build_save_tif()
        self._build_next_button()
        self._build_trash_button()
        self._build_reset_lines_button()
        self._build_save_xlsx_button()
        self._build_filename_entry()
        self._build_keep_Checkbox()
        self._build_load_recent_Checkbox()
        self._build_delete_folder_button()
        self._build_drop_down()
        self._build_drop_down_dyn()
        self.__update_all_listboxes()
        self._build_titles()
        self._build_curve_graph()
        self._build_render_button()
        self.rgb_button.config(foreground="red")

    # ---------------------------------------------- BUILDERS (DISPLAY) -----------------------------------------------

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Measure Tool', command=self.__info, width=8)

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
        
    def _build_render_button(self):
        self.ohi_button = make_button(self.root, text='RENDER', width=3, command=self.__render, row=0, column=8,
                                      columnspan=1, inner_pady=5, outer_padx=(0, 5), outer_pady=(5, 0))
        
    # ----------------------------------------------- BUILDERS (MISC) -----------------------------------------------

    def _build_next_button(self):
        self.next_button = make_button(self.root, text='Next (wo. saving)', width=12, command=self.__next,
                                               row=28, column=10, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    def _build_curve_graph(self):
        self.interactive_absorption_spec_graph = Figure(figsize=(3.8, 3))
        self.axes_abs = self.interactive_absorption_spec_graph.add_subplot(111)
        self.interactive_absorption_spec_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        y_low = self.y_low
        y_high = self.y_high
        if not self.dyn:
            self.axes_abs.set_ylim(bottom=self.y_low, top=self.y_high)
        y_vals = self.vals_fc[self.curve_mode]
        self.axes_abs.plot(np.arange(len(y_vals)), y_vals, '-', lw=0.5)
            
            #commas and non-scientific notation
        self.axes_abs.ticklabel_format(style='plain')
        self.axes_abs.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
        self.axes_abs.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))          
        # draw figure
        self.interactive_absorption_spec = FigureCanvasTkAgg(self.interactive_absorption_spec_graph, master=self.root)
        self.interactive_absorption_spec.draw()
        self.interactive_absorption_spec.get_tk_widget().grid(column=13, row=2, columnspan=2)
        
    def __update_upper_lower(self, event):
        self.y_low = float(self.lower_input.get())
        self.y_high = float(self.upper_input.get())
        self._build_curve_graph()
        
    def _build_drop_down(self): 
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__set_prog)
        self.drop_down_menu.configure(highlightthickness=0, width=10,
                                      anchor='w')
        self.drop_down_menu.grid(column=13, row=1)
        
        self.lower_text = make_text(self.root, content="Lower: ", bg=tkcolour_from_rgb(BACKGROUND), column=13, row=3,
                                    width=7, columnspan=1, pady=(0, 5))
        self.lower_input = make_entry(self.root, row=3, column=14, width=5)
        self.lower_input.bind('<Return>', self.__update_upper_lower)
        self.lower_input.insert(END, str(self.y_low))
        
        self.upper_text = make_text(self.root, content="Upper: ", bg=tkcolour_from_rgb(BACKGROUND), column=13, row=4,
                                    width=7, columnspan=1, pady=(0, 5))
        self.upper_input = make_entry(self.root, row=4, column=14, width=5, columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper_lower)
        self.upper_input.insert(END, str(self.y_high))
        
    def __set_prog(self, event = None):
        self.curve_mode = self.drop_down_var.get()[3:]
        self._build_curve_graph()
        
    def __change_dyn(self, event):
        choice = self.drop_down_var_dyn.get()
        if choice == 'dynamic':
            self.dyn = True
        elif choice == 'static':
            self.dyn = False
        self._build_curve_graph()
            
    def _build_drop_down_dyn(self): 
        self.drop_down_var_dyn.set(self.choices_dyn[0])
        self.drop_down_menu_dyn = OptionMenu(self.root, self.drop_down_var_dyn, *self.choices_dyn, command=self.__change_dyn)
        self.drop_down_menu_dyn.configure(highlightthickness=0, width=10,
                                      anchor='w')
        self.drop_down_menu_dyn.grid(column=14, row=1)

    def _build_instant_save_button(self):
        self.instant_save_button = make_button(self.root, text='Save measurements\nand Next', width=12, command=self.__save_measure_and_next,
                                               row=28, column=4, columnspan=3, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    @staticmethod
    def format_axis(x, _):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 4))
        
    def _build_delete_folder_button(self):
        self.delete_folder_button = make_button(self.root, text='Delete folder', width=12, command=self.__delete_folder,
                                               row=28, column=3, columnspan=1, inner_pady=5, outer_padx=5,
                                               outer_pady=(10, 15), height= 2)
        
    def __delete_folder(self):
        path = os.path.dirname(self.get_selected_data_cube_path())
        if not os.path.exists(path + "/_prog"):
            os.mkdir(path + "/_prog")
        path = path + "/_prog"
        if os.path.exists(path):
            shutil.rmtree(path)
        self.__reset_lines()
        
    def _build_trash_button(self):
        self.trash_button = make_button(self.root, text='Clean List', width=9, command=self.__trash_list,
                                               row=28, column=1, columnspan=2, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))
        
    def _build_reset_lines_button(self):
        self.trash_button = make_button(self.root, text='Reset (r)', width=9, command=self.__reset_lines,
                                               row=28, column=11, columnspan=2, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))
    
    def _build_save_xlsx_button(self):
        self.trash_button = make_button(self.root, text='Save xlsx (x)', width=9, command=self.__save_xlsx,
                                               row=28, column=13, columnspan=1, inner_pady=5, outer_padx=0,
                                               outer_pady=(10, 15))


    def _build_select_superdir_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open OP\nFolder",
                                                   command=self.__add_data_cube_dirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=25, rowspan = 2, column=0, width=11, outer_pady=(5, 5))
        
    def _build_select_all_subfolders_button(self):
        self.select_data_cube_button = make_button(self.root, text="Open Project\nFolder",
                                                   command=self.__add_data_cube_subdirs, inner_padx=10, inner_pady=10,
                                                   outer_padx=15, row=28, rowspan=1, column=0, width=11, outer_pady=(5, 5))

    def _build_selection_box(self):
        self.selection_listbox = make_listbox(self.root, row=1, column=0, rowspan=24, padx=(0, 15), pady=(0, 15), height = 35, width = 18)
        self.selection_listbox.bind('<<ListboxSelect>>', self.__update_selected_data_cube)
        
    def _build_line_box(self):
        self.line_listbox = make_listbox(self.root, row=1, column=11, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, width = 8)
        self.line_listbox.bind('<<ListboxSelect>>', self.__update_selected_line)
        
    def _build_keep_Checkbox(self):
        self.cb_keep = Checkbutton(self.root, text='Keep', variable=self.var_keep)
        self.cb_keep.grid(row=28, column=14, columnspan = 1, sticky='nw')
        self.cb_keep.bind('<Button-1>', self.__update_keep_checkbox)
        
    def _build_load_recent_Checkbox(self):
        self.cb_load_recent = Checkbutton(self.root, text='Most recent', variable=self.var_load_recent)
        self.cb_load_recent.grid(row=25, column=11, columnspan = 2, sticky='nw')
        self.cb_load_recent.bind('<Button-1>', self.__update_load_recent_checkbox)
        
        
    def __update_load_recent_checkbox(self, event = None):
        self.load_recent = not self.load_recent
        print(self.load_recent)
        self.__read_file()
        
    def __update_keep_checkbox(self, event = None):
        self.keep = not self.keep
        
    def _build_titles(self):
            self.title1 = make_text(self.root, content="Coord", bg=tkcolour_from_rgb(BACKGROUND),
                              column=12, columnspan=1, row=0, width=8, text = self.title1)
    
    def _build_centers_box(self):
        self.centers_listbox = make_listbox(self.root, row=1, column=12, rowspan=21, padx=(0, 15), pady=(0, 15), height = 35, width = 12)
        
    def _build_filename_entry(self):
        title = make_text(self.root, content="Filename:", bg=tkcolour_from_rgb(BACKGROUND),
                          column=11, columnspan=2, row=26, width=15, pady=(5, 5), padx=(5, 5))
        self.filename_entry = make_entry(self.root, row=26, column=13, width=35, pady=(10, 10), columnspan=4)
        self.filename_entry.bind('<Return>', self.update_filename)
        self.filename_entry.delete(0,"end")
        self.filename_entry.insert(0, self.filename)
        
    def _build_save_tif(self):
        self.save_as_tif_label = make_button(self.root, "Save Image", row=28, column=9, outer_padx=(12, 0),
                                     outer_pady=(10, 15), inner_padx=10, inner_pady=5, rowspan = 1, columnspan=1, command = self.__save_image)
    


    # ---------------------------------------------- BUILDERS (IMAGE) -----------------------------------------------
        
    def _build_original_image(self, data):
        if data is None:
            # Placeholder
            self.original_image = make_label(self.root, "original image placeholder", row=1, column=1, rowspan=26,
                                             columnspan=10, inner_pady=300, inner_padx=400, outer_padx=(15, 10),
                                             outer_pady=(15, 10))
        else:
            #data = np.asarray(rgb_image_to_hsi_array(self.original_image_data)).reshape((480, 640))
            (self.original_image_graph, self.original_image, self.image_array) = \
                make_image(self.root, data, row=1, column=1, columnspan=10, rowspan=25, lower_scale_value=None,
                           upper_scale_value=None, color_rgb=BACKGROUND, original=True, figheight=7, figwidth=9, img = self.original_image, axs = self.original_image_graph, figu = self.original_image_graph)
            self.original_image.get_tk_widget().bind('<Button-1>', self.__get_coords)
            self.original_image.get_tk_widget().bind('<+>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-minus>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-w>', self.__zoom)
            self.original_image.get_tk_widget().bind('<Key-s>', self.__dezoom)
            self.original_image.get_tk_widget().bind('<Key-x>', self.__save_xlsx)
            self.original_image.get_tk_widget().bind('<Leave>', self.__reset_mouse_position)
            self.original_image.get_tk_widget().bind('<Motion>', self.__update_mouse_position)
            self.original_image.get_tk_widget().bind('<Key-r>', self.__reset_lines)
            self.original_image.get_tk_widget().bind('<BackSpace>', self.__del_last)
            self.original_image.get_tk_widget().focus_force()
   
    # --------------------------------------------- IMAGE (NAVIGATING) -----------------------------------------------
            
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
 
    # ---------------------------------------------  MOUSE POSITION ----------------------------------------      
               
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
        if len(not_none)>=1:             
            pt1 = not_none[-1]
            pt2 = (Xc, Yc)
            a = pt1[0]-pt2[0]
            b = pt1[1]-pt2[1]
            c = np.sqrt(a*a + b*b)
        self.original_image.get_tk_widget().focus_force()
            
    def __reset_mouse_position(self, event):
        self.mouse_x = 320
        self.mouse_y = 240

    # --------------------------------------------------- DRAWING -----------------------------------------------------

    def __del_last(self, event = None):
        self.line_index = self.line_index - 1
        if self.line_index == 0:
            self.line_index = 0
        self.centers[self.line_index] = (None, None)
        self._draw_points()
        self.__update_all_listboxes()

                        
        
        
    def _draw_points(self):
        self.vals = {"RGB": [], "STO2": [], "NIR":[], "THI": [], "TWI":[], "TLI": [], "OHI": []}
        self.vals_fc = {"RGB": [], "STO2": [], "NIR":[], "THI": [], "TWI":[], "TLI": [], "OHI": []}
        self.coordinates = []
        copy_data = self.original_image_data.copy()
        for ii in range(100):
            if self.centers[ii][0] is not None:#
                y = int(self.centers[ii][0])
                x = int(self.centers[ii][1])
                for xi in range(-4, 5):
                    copy_data[(x + xi) % 480, y, :3] = BRIGHT_BLUE_RGB
                for yi in range(-4, 5):
                    copy_data[x, (y + yi) % 640, :3] = BRIGHT_BLUE_RGB
             
            
            jj = ii +1
            if jj == 100:
                jj=0

            if self.centers[ii][0] is not None and self.centers[jj][0] is not None:
                not_none = [self.centers[ii], self.centers[jj]]
                for point in not_none:
                    y = int(point[0])
                    x = int(point[1])
                    for xi in range(-4, 5):
                        copy_data[(x + xi) % 480, y, :3] = BRIGHT_GREEN_RGB
                        for yi in range(-4, 5):
                            copy_data[x, (y + yi) % 640, :3] = BRIGHT_GREEN_RGB
                    idx = not_none.index(point)
                    self._draw_a_line_green(not_none[idx - 1], not_none[idx], copy_data)
                    self._add_vals(not_none[idx - 1], not_none[idx])
             
            if self.lines[ii][0][1] is not None and self.lines[ii][1][1] is not None:
                not_none = [self.lines[ii][0], self.lines[ii][1]]
                for point in not_none:
                    y = int(point[0])
                    x = int(point[1])
                    for xi in range(-4, 5):
                        copy_data[(x + xi) % 480, y, :3] = BRIGHT_GREEN_RGB
                        for yi in range(-4, 5):
                            copy_data[x, (y + yi) % 640, :3] = BRIGHT_GREEN_RGB
                    idx = not_none.index(point)
                    self._draw_a_line_blue(not_none[idx - 1], not_none[idx], copy_data)
        
        self.image_to_save = copy_data
        left = self.view_mid[1] - 320
        bottom = self.view_mid[0] - 240
        right = left + 640
        top = bottom + 480
        im = Image.fromarray(copy_data)
        im = im.resize((640*self.zoom_factor, 480*self.zoom_factor)) 
        im = im.crop((left, bottom, right, top))
        self._build_original_image(np.array(im))
        self.original_image.get_tk_widget().focus_force()
        self._build_curve_graph()
          
    @staticmethod
    def _draw_a_line_green(point1, point2, image):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i] % 480, cc[i] % 640] = (int(113 * val[i]), int(255 * val[i]), int(66 * val[i]))
        return image
    
    @staticmethod
    def _draw_a_line_blue(point1, point2, image):
        r0, c0 = point1
        r1, c1 = point2
        rr, cc, val = line_aa(c0, r0, c1, r1)
        for i in range(len(rr)):
            image[rr[i] % 480, cc[i] % 640] = (int(66 * val[i]), int(113 * val[i]), int(255 * val[i]))
        return image
    
    def _add_vals(self, point1, point2):
        if not self.STO2_render is None:
            r0, c0 = point1
            r1, c1 = point2
            rr, cc, val = line_aa(c0, r0, c1, r1)
            for mode in ["STO2", "THI", "TWI", "TLI", "OHI", "NIR"]:
                if mode == "STO2":
                    img = self.STO2_render
                    img_fc = self.STO2_render_fc
                elif mode == "THI":
                    img = self.THI_render
                    img_fc = self.THI_render_fc
                elif mode == "TWI":
                    img = self.TWI_render
                    img_fc = self.TWI_render_fc
                elif mode == "TLI":
                    img = self.TLI_render
                    img_fc = self.TLI_render_fc
                elif mode == "OHI":
                    img = self.OHI_render  
                    img_fc = self.OHI_render_fc
                elif mode == "NIR":
                    img = self.NIR_render 
                    img_fc = self.NIR_render_fc
                vals = []
                vals_fc = []
                coordinates = []
                if img is not None:
                    for i in range(len(rr)):
                        vals.append(img[rr[i] % 480, cc[i] % 640])  
                        coordinates.append((rr[i] % 480, cc[i] % 640))
                        vals_fc.append(img_fc[rr[i] % 480, cc[i] % 640])  
                self.vals[mode] = self.vals[mode] + vals
                self.vals_fc[mode] = self.vals_fc[mode] + vals_fc
                self.coordinates = self.coordinates + coordinates
        return
    
    @staticmethod
    def __process_data_cube(path):
        if path == '' or path is None:
            return None
        if path[-12:] != "SpecCube.dat":
            messagebox.showerror("Error", "That's not a .dat file!")
            return None
        else:
            data = np.fromfile(path, dtype='>f')  # returns 1D array and reads file in big-endian binary format
            print(data[3:].size)
            if data[3:].size == 38880000:
                data_cube = data[3:].reshape(720, 540, 100)
            else:        
                data_cube = data[3:].reshape(640, 480, 100)  # reshape to data cube and ignore first 3 values
            return data_cube
    
    def __render(self):
        self.STO2_render = np.reshape(np.array(rgb_image_to_jet_array(self.STO2)), (480,640))
        self.THI_render = np.reshape(np.array(rgb_image_to_jet_array(self.THI)), (480,640))
        self.TWI_render = np.reshape(np.array(rgb_image_to_jet_array(self.TWI) ), (480,640))
        self.NIR_render = np.reshape(np.array(rgb_image_to_jet_array(self.NIR) ), (480,640))
        self.TLI_render = np.reshape(np.array(rgb_image_to_jet_array(self.TLI) ), (480,640))
        self.OHI_render = np.reshape(np.array(rgb_image_to_jet_array(self.OHI) ), (480,640))
        rec_analysis = RecreatedAnalysis("", self.__process_data_cube(self.get_selected_data_cube_path()), (500,1000), [0.2, -0.03, -0.46, 0.45, 0.4, 1.55, 0.1, -0.5], self.listener, None)
        self.STO2_render_fc = rec_analysis.get_sto2().T*100
        self.NIR_render_fc = rec_analysis.get_nir().T*100
        self.THI_render_fc = rec_analysis.get_thi().T*100
        self.TWI_render_fc = rec_analysis.get_twi().T*100
        self.OHI_render_fc = rec_analysis.get_ohi().T*100
        self.TLI_render_fc = rec_analysis.get_tli().T*100
        self._draw_points()
        return

    # --------------------------------------------- ADDING/REMOVING COORDS --------------------------------------------

    def __get_coords(self, event):
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
                self.centers[self.line_index] = (Xc, Yc)
                self.line_index = self.line_index + 1
                if self.line_index == 100:
                    self.line_index = 0
                self.__update_all_listboxes()
        
        self._draw_points()
            
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


    # ------------------------------------------------- UPDATE MEASURMENTS & LINES --------------------------------------------------
        
    def __insert_lines(self):
        self.line_listbox.delete(0,'end')
        for ii in range(100):
            self.__add_line(ii)
        self.line_listbox.select_set(self.line_index)
        
    def __insert_centers(self):
        self.centers_listbox.delete(0,'end')
        for ii in range(100):
            self.__add_center(ii)
    
    def __update_selected_line(self, event):
        self.first = True
        self.line_index = self.line_listbox.curselection()[0]
    
    def __update_all_listboxes(self):
        self.__calc_centers()
        self.__insert_lines()
        self.__insert_centers()
    
    def __reset_lines(self, event = None):
        self.lines = [[(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)],
                      [(None, None), (None, None)]
                      ]
        self.centers = [(None, None)]*100                  
        self.line_index = 0
        self.first = True
        self.__update_all_listboxes()
        self._draw_points()
        
    def __calc_centers(self):
        for ii in range(100):
            if self.lines[ii][0][1] is not None and self.lines[ii][1][1] is not None:
                pt1 = self.lines[ii][0]
                pt2 = self.lines[ii][1]
                center1 = int(round((pt1[0] + pt2[0])/2))
                center2 = int(round((pt1[1] + pt2[1])/2))
                self.centers[ii] = (center1, center2)            
    
    def __add_line(self, index):
            not_none_idx = [x for x in range(100) if self.centers[x][0]]
            if index in not_none_idx:
                index_2 = not_none_idx.index(index)
                concat_path = "Point " + str(index_2+1)
                self.line_listbox.insert(END, concat_path)
    
    def __add_center(self, index):
            not_none_idx = [x for x in range(100) if self.centers[x][0]]
            if index in not_none_idx:
                concat_path = str(self.centers[index])
                self.centers_listbox.insert(END, concat_path)

    # -------------------------------------------------- SELECTION LISTBOX / LOADING DATACUBES -----------------------------------

    def __update_selected_data_cube(self, event):
        dc_path = self.get_selected_data_cube_path()[0:-12]
        if self.current_dc_path is not self.selection_listbox.curselection()[0]:
            if len(self.selection_listbox.curselection())>0:
                self.current_dc_path = self.selection_listbox.curselection()[0]
        
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
            self.NIR = np.zeros((480, 640,3)).astype("uint8")
        
        if os.path.exists(dc_path +"TWI.png"):
            c = Image.open(dc_path +"TWI.png")
            c = np.asarray(c)
            if c.shape[0] == 550:
                c = c[50:530, 50:690, :3]
            else:
                c = c[26:506, 4:644, :3]
            self.TWI = c
        else:
            self.TWI = np.zeros((480, 640,3)).astype("uint8")
        
        if os.path.exists(dc_path +"THI.png"):
            d = Image.open(dc_path +"THI.png")
            d = np.asarray(d)
            if d.shape[0] == 550:
                d = d[50:530, 50:690, :3]
            else:
                d = d[26:506, 4:644, :3]
            self.THI = d
        else:
            self.THI  = np.zeros((480, 640,3)).astype("uint8")
        
        if os.path.exists(dc_path +"Oxygenation.png"):
            e = Image.open(dc_path +"Oxygenation.png")
            e = np.asarray(e)
            if e.shape[0] == 550:
                e = e[50:530, 50:690, :3]
            else:
                e = e[26:506, 4:644, :3]
            self.STO2 = e
        else:
            self.STO2 = np.zeros((480, 640,3)).astype("uint8")
        
        if os.path.exists(dc_path +"TLI.png"):
            f = Image.open(dc_path +"TLI.png")
            f = np.asarray(f)
            if f.shape[0] == 550:
                f = f[50:530, 50:690, :3]
            else:
                f = f[26:506, 4:644, :3]
            self.TLI = f
        else:
            self.TLI = np.zeros((480, 640, 3)).astype("uint8")
        
        if os.path.exists(dc_path +"OHI.png"):
            g = Image.open(dc_path +"OHI.png")
            g = np.asarray(g)
            if g.shape[0] == 550:
                g = g[50:530, 50:690, :3]
            else:
                g = g[26:506, 4:644, :3]
            self.OHI = g
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
        self.original_image.get_tk_widget().focus_force()
        self.counter = 0
        self._new_filename()
        if not self.keep:
            self.__reset_lines()
            self.__read_file()
        

    def __add_data_cube_dirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the data folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir)
        for sub_dir in sub_dirs:
            if len(glob.glob(sub_dir + "/*RGB-Image.png"))>=1:
                self.__add_data_cube(sub_dir)
    
    def __add_data_cube_subdirs(self):
        super_dir = self.__get_path_to_dir("Please select folder containing all the OP folders.")
        sub_dirs = self.__get_sub_folder_paths(super_dir, True)
        for sub_dir in sub_dirs:
            if len(glob.glob(sub_dir + "/*RGB-Image.png"))>=1:
                self.__add_data_cube(sub_dir)


    def __add_data_cube(self, sub_dir):
        contents = os.listdir(sub_dir)
        dc_path = [sub_dir + "/" + i for i in contents if "SpecCube.dat" in i]  # takes first data cube it finds
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

    def __get_path_to_dir(self, title):
        if self.listener.dc_path is not None:
            p = os.path.dirname(os.path.dirname(self.listener.dc_path))
            path = filedialog.askdirectory(parent=self.root, title=title, initialdir=p)
        else:
            path = filedialog.askdirectory(parent=self.root, title=title)
        return path
    
    def __next(self):
        if len(self.selection_listbox.curselection())>0:
            sel = self.selection_listbox.curselection()[0]
        else:
            sel = self.current_dc_path
        self.selection_listbox.selection_clear(0, END)
        self.selection_listbox.select_set(sel+1) #This only sets focus on the first item.
        self.selection_listbox.event_generate("<<ListboxSelect>>")
        #self.__remove_pt('all')

    @staticmethod
    def __get_sub_folder_paths(path_to_main_folder, recursive = False): 
        #contents = os.listdir(path_to_main_folder)
        # Adds the path to the main folder in front for traversal
        #sub_folders = [path_to_main_folder + "/" + i for i in contents if bool(re.match('[\d/-_]+$', i))]
        sub_folders = sorted(glob.glob(path_to_main_folder+"/**/", recursive = recursive))
        return sub_folders
    
    def __trash_list(self):
        self.data_cube_paths = []
        self.selection_listbox.delete(0,'end')
        self.__remove_pt('all')
     
    # ------------------------------------------------ SAVING ---------------------------------------------------        
        
    def __save_image(self):
        path = os.path.dirname(self.get_selected_data_cube_path())
        if not os.path.exists(path + "/_prog"):
            os.mkdir(path + "/_prog")
        path = path + "/_prog"+"/"+ self.filename + '.png'
        img = Image.fromarray(self.image_to_save)
        img.save(path)
        
    def __save_xlsx(self, event = None):
        self.filename = self.filename_entry.get()
        path = os.path.dirname(self.get_selected_data_cube_path())
        if not os.path.exists(path + "/_prog"):
               os.mkdir(path + "/_prog")
        path = path + "/_prog"+"/" + self.filename + '_coords.xlsx'
        workbook = xlsxwriter.Workbook(path)
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'Point Coordinates', bold)
        cc = 0
        for ii in range(100):
                if self.centers[ii][1] is not None:
                    worksheet.write(cc+1, 0, str(self.centers[ii])) 
                cc = cc+1
        workbook.close()   
        
    def __save_xlsx_vals_from_png(self, event = None):
        self.filename = self.filename_entry.get()
        path = os.path.dirname(self.get_selected_data_cube_path())
        if not os.path.exists(path + "/_prog"):
               os.mkdir(path + "/_prog")
        path = path + "/_prog"+"/" + self.filename + '_values_from_png.xlsx'
        workbook = xlsxwriter.Workbook(path)
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'Coordinate', bold)
        worksheet.write(0, 1, 'STO2', bold)
        worksheet.write(0, 2, 'NIR', bold)
        worksheet.write(0, 3, 'THI', bold)
        worksheet.write(0, 4, 'TWI', bold)
        worksheet.write(0, 5, 'TLI', bold)
        worksheet.write(0, 6, 'OHI', bold)
        cc = 0
        for ii in range(len(self.vals["STO2"])):
            worksheet.write(cc+1, 0, str(self.coordinates[ii])) 
            worksheet.write(cc+1, 1, str(self.vals["STO2"][ii])) 
            worksheet.write(cc+1, 2, str(self.vals["NIR"][ii])) 
            worksheet.write(cc+1, 3, str(self.vals["THI"][ii])) 
            worksheet.write(cc+1, 4, str(self.vals["TWI"][ii])) 
            worksheet.write(cc+1, 5, str(self.vals["TLI"][ii])) 
            worksheet.write(cc+1, 6, str(self.vals["OHI"][ii])) 
            cc = cc+1
        workbook.close()
        
    def __save_xlsx_vals_from_cube(self, event = None):
        self.filename = self.filename_entry.get()
        path = os.path.dirname(self.get_selected_data_cube_path())
        if not os.path.exists(path + "/_prog"):
               os.mkdir(path + "/_prog")
        path = path + "/_prog"+"/" + self.filename + '_values_from_cube.xlsx'
        workbook = xlsxwriter.Workbook(path)
        bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'Coordinate', bold)
        worksheet.write(0, 1, 'STO2', bold)
        worksheet.write(0, 2, 'NIR', bold)
        worksheet.write(0, 3, 'THI', bold)
        worksheet.write(0, 4, 'TWI', bold)
        worksheet.write(0, 5, 'TLI', bold)
        worksheet.write(0, 6, 'OHI', bold)
        cc = 0
        for ii in range(len(self.vals["STO2"])):
            worksheet.write(cc+1, 0, str(self.coordinates[ii])) 
            worksheet.write(cc+1, 1, str(self.vals_fc["STO2"][ii])) 
            worksheet.write(cc+1, 2, str(self.vals_fc["NIR"][ii])) 
            worksheet.write(cc+1, 3, str(self.vals_fc["THI"][ii])) 
            worksheet.write(cc+1, 4, str(self.vals_fc["TWI"][ii])) 
            worksheet.write(cc+1, 5, str(self.vals_fc["TLI"][ii])) 
            worksheet.write(cc+1, 6, str(self.vals_fc["OHI"][ii])) 
            cc = cc+1
        workbook.close()
    
    def __read_file(self):
        self.__reset_lines()
        if self.load_recent:
            path = os.path.dirname(self.get_selected_data_cube_path())
            path = path + "/_prog/*_coords.xlsx"
            files = glob.glob(path)
            if len(files) >0:
                path = max(files, key=os.path.getctime)   
                dfs = pd.read_excel(path, sheet_name=None)
                df = dfs["Sheet1"]
                if "Point Coordinates" in df.columns:
                    coords = list(df["Point Coordinates"])
                    for ii, coord in enumerate(coords):
                        Xc = int(coord.replace("(", "").replace(")", "").split(", ")[0])
                        Yc = int(coord.replace("(", "").replace(")", "").split(", ")[1])
                        self.centers[self.line_index] = (Xc, Yc)
                        self.line_index = self.line_index + 1
                        if self.line_index == 100:
                            self.line_index = 0 
                        if np.any(np.isnan(df.iloc[ii, 1])):
                            self.line_index = self.line_index + 1
                            if self.line_index == 100:
                                self.line_index = 0 
                self.__update_all_listboxes()
                self._draw_points()
        else:
            path = os.path.dirname(self.get_selected_data_cube_path())
            path = path + "/_prog"+"/" + self.filename + '.xlsx'
            if os.path.exists(path):
                dfs = pd.read_excel(path, sheet_name=None)
                df = dfs["Sheet1"]
                if "Point Coordinates" in df.columns:
                    coords = list(df["Point Coordinates"])
                    for ii, coord in enumerate(coords):
                        Xc = int(coord.replace("(", "").replace(")", "").split(", ")[0])
                        Yc = int(coord.replace("(", "").replace(")", "").split(", ")[1])
                        self.centers[self.line_index] = (Xc, Yc)
                        self.line_index = self.line_index + 1
                        if self.line_index == 100:
                            self.line_index = 0 
                        if np.any(np.isnan(df.iloc[ii, 1])):
                            self.line_index = self.line_index + 1
                            if self.line_index == 100:
                                self.line_index = 0 
            self.__update_all_listboxes()
            self._draw_points()
                
        
    def _new_filename(self):
        self.counter = self.counter +1
        if not self.name_unique:
                self.filename = "_prog_results_"+str(self.counter)
        else:
                self.filename = self.filename_unique
        self._insert_filename()
    
    def __save_measure_and_next(self):
        self.__save_image()
        self.__save_xlsx()
        self.__save_xlsx_vals_from_png()
        self.__save_xlsx_vals_from_cube()
        self.__next()
             
    # --------------------------------------- MISC ----------------------------------
        
    def __info(self): 
        info = self.listener.modules[INFO].measure_info
        title = "Measure Tool"
        make_info(title=title, info=info)
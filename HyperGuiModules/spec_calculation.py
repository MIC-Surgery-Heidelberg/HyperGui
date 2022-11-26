from HyperGuiModules.utility import *
import matplotlib.pyplot as plt
import matplotlib
from tkinter import filedialog, messagebox
import csv
import logging
import os
matplotlib.use("TkAgg")


class SpecCalculation:
    def __init__(self, spec_calculation, listener):
        self.root = spec_calculation

        # Listener
        self.listener = listener

        self.output_path = None

        self.math = '-'

        self.hist1_button = None
        self.hist2_button = None
        self.calc_button = None

        self.data1_stats = [None, None, None, None]
        self.data2_stats = [None, None, None, None]
        self.data3_stats = [None, None, None, None]

        self.initial_data1 = None
        self.initial_data2 = None
        self.initial_data3 = None

        self.drop_down_var = StringVar()
        self.choices = ['-', '+', 'x', '/']

        self.bins = None
        self.contents = None
        self.graph0 = None
        self.graph2 = None
        self.graph4 = None
        self.axes = None

        self.info_label = None

        self._init_widget()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_buttons()
        self._build_reset_buttons()
        self._build_save_buttons()
        self._build_drop_down()
        self._build_equals()
        self._build_spec(None, None, 0, self.data1_stats)
        self._build_spec(None, None, 2, self.data2_stats)
        self._build_spec(None, None, 4, self.data3_stats)
        self._build_scale(self.data1_stats, 0)
        self._build_scale(self.data2_stats, 5)
        self._build_scale(self.data3_stats, 10)
        self._build_info_label()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_buttons(self):
        self.hist1_button = make_button(self.root, text="Choose First Optical Spectrum",
                                        command=self.__update_data1, row=1, column=0, outer_pady=(0, 5),
                                        outer_padx=15, width=23, height=1, columnspan=4)
        self.hist2_button = make_button(self.root, text="Choose Second Optical Spectrum",
                                        command=self.__update_data2, row=1, column=5, outer_pady=(0, 5),
                                        outer_padx=15, width=23, height=1, columnspan=4)
        self.calc_button = make_button(self.root, text="Calculate Optical Spectrum",
                                       command=self.__calculate, row=1, column=10, outer_pady=(0, 5),
                                       outer_padx=15, width=23, height=1, columnspan=4)

    def _build_reset_buttons(self):
        make_button(self.root, text="Reset", command=self.__reset_data1, row=7, column=0, outer_padx=15,
                    width=6, height=1, columnspan=4, outer_pady=15)
        make_button(self.root, text="Reset", command=self.__reset_data2, row=7, column=5, outer_padx=15,
                    width=6, height=1, columnspan=4, outer_pady=15)
        make_button(self.root, text="Reset", command=self.__reset_data3, row=7, column=10, outer_padx=15,
                    width=6, height=1, columnspan=4, outer_pady=15)

    def _build_save_buttons(self):
        make_button(self.root, text="Change Output Folder", command=self.__select_output, row=2, column=14,
                    outer_padx=15, width=15, height=1, columnspan=1, outer_pady=(35, 5), inner_pady=5)
        make_button(self.root, text="Save as CSV", command=self.__save_as_csv, row=3, column=14, outer_padx=15,
                    width=15, height=1, columnspan=1, outer_pady=(0, 5), inner_pady=5)
        make_button(self.root, text="Save as Image", command=self.__save_as_image, row=4, column=14, outer_padx=15,
                    width=15, height=1, columnspan=1, outer_pady=(0, 55), inner_pady=5)

    def _build_drop_down(self):
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__update_math)
        self.drop_down_menu.configure(highlightthickness=0, width=1, anchor='w', padx=15)
        self.drop_down_menu.grid(column=4, row=2, columnspan=1, padx=0, rowspan=3)

    def _build_scale(self, stats, col):
        if col == 0:
            (self.data1_minx, self.data1_maxx, self.data1_miny, self.data1_maxy) = self._build_scale_helper(stats, col)
        elif col == 5:
            (self.data2_minx, self.data2_maxx, self.data2_miny, self.data2_maxy) = self._build_scale_helper(stats, col)
        elif col == 10:
            (self.data3_minx, self.data3_maxx, self.data3_miny, self.data3_maxy) = self._build_scale_helper(stats, col)

    def _build_scale_helper(self, stats, col):
        bg = tkcolour_from_rgb(BACKGROUND)
        print(stats)
        # min x
        make_text(self.root, content="Min x: ", bg=bg, column=col, row=5, width=7, pady=(0, 10), padx=(25, 5))
        min_x_input = make_entry(self.root, row=5, column=col+1, width=7, pady=(0, 10), padx=(0, 30))
        min_x_input.bind('<Return>', lambda x: self.__update_scales(col))
        min_x_input.insert(END, str(stats[0]))
        # max x
        make_text(self.root, content="Max x: ", bg=bg, column=col+2, row=5, width=7, pady=(0, 10), padx=(0, 5))
        max_x_input = make_entry(self.root, row=5, column=col+3, width=7, pady=(0, 10), padx=(0, 25))
        max_x_input.bind('<Return>', lambda x: self.__update_scales(col))
        max_x_input.insert(END, str(stats[1]))
        # min y
        make_text(self.root, content="Min y: ", bg=bg, column=col, row=6, width=7, pady=(0, 10), padx=(25, 5))
        min_y_input = make_entry(self.root, row=6, column=col+1, width=7, pady=(0, 10), padx=(0, 30))
        min_y_input.bind('<Return>', lambda x: self.__update_scales(col))
        min_y_input.insert(END, str(stats[2]))
        # max x
        make_text(self.root, content="Max y: ", bg=bg, column=col+2, row=6, width=7, pady=(0, 10), padx=(0, 5))
        max_y_input = make_entry(self.root, row=6, column=col+3, width=7, pady=(0, 10), padx=(0, 25))
        max_y_input.bind('<Return>', lambda x: self.__update_scales(col))
        max_y_input.insert(END, str(stats[3]))
        return min_x_input, max_x_input, min_y_input, max_y_input

    def _build_equals(self):
        equals = make_text(self.root, content="=",  bg=tkcolour_from_rgb(BACKGROUND), column=9, row=2, width=3,
                           columnspan=1, padx=0, rowspan=3)
        equals.config(font=("Courier", 44))

    def get_graph(self, column):
        if column == 0:
            return self.graph0
        if column == 2:
            return self.graph2
        if column == 4:
            return self.graph4

    def _build_spec(self, x_vals, y_vals, column, stats):
        # create canvas
        graph = self.get_graph(column)
        graph = Figure(figsize=(3, 2))
        self.axes = graph.add_subplot(111)
        graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        # plot absorption spec
        if x_vals is not None:
            self.axes.plot(x_vals, y_vals, '-', lw=0.5)
            self.axes.grid(linestyle=':', linewidth=0.5)
        # set axes
        graph.set_tight_layout(True)
        y_low = stats[2]
        y_high = stats[3]
        if y_low is not None and y_high is not None:
            factor = (y_high - y_low) * 0.05
            y_low -= factor
            y_high += factor
        self.axes.set_xlim(left=stats[0], right=stats[1])
        self.axes.set_ylim(bottom=y_low, top=y_high)
        # commas and non-scientific notation
        self.axes.ticklabel_format(style='plain')
        self.axes.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
        self.axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
        # draw figure
        self.interactive_absorption_spec = FigureCanvasTkAgg(graph, master=self.root)
        self.interactive_absorption_spec.draw()
        self.interactive_absorption_spec.get_tk_widget().grid(column=int(2.5*column), row=2, columnspan=4, rowspan=3, ipady=5,
                                                              ipadx=0, pady=(0, 20), padx=0)
        self.interactive_absorption_spec.get_tk_widget().bind('<Button-2>', lambda x: self.__pop_up_image(graph))

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Optical Spectrum Calculation', command=self.__info, width=16)
        self.info_label.grid(columnspan=2, pady=(25, 30))

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __calculate(self):
        if self.x_vals1 is None or self.x_vals2 is None:
            messagebox.showerror("Error", "Please select two csv files.")
        elif self.x_vals1[0] != self.x_vals2[0] and self.x_vals1[-1] != self.x_vals2[-1]:
            messagebox.showerror("Error", "Please ensure your x axis is the same for each spectrum. Currently your "
                                          "first csv file begins at " + str(self.x_vals1[0]) + " and ends at "
                                          + str(self.x_vals1[-1]) + " while your second csv file begins at "
                                          + str(self.x_vals2[0]) + " and ends at " + str(self.x_vals2[-1]) + ".")
        else:
            self.x_vals3 = self.x_vals1
            if self.math == '-':
                self.y_vals3 = np.asarray(self.y_vals1) - np.asarray(self.y_vals2)
            elif self.math == '+':
                self.y_vals3 = np.asarray(self.y_vals1) + np.asarray(self.y_vals2)
            elif self.math == 'x':
                self.y_vals3 = np.asarray(self.y_vals1) * np.asarray(self.y_vals2)
            elif self.math == '/':
                if 0 in self.y_vals2 or 0.0 in self.y_vals2:
                    messagebox.showerror("Error", "Division by zero. Your second csv file contains zeros and thus "
                                                  "division cannot be completed.")
                    pass
                self.y_vals3 = np.asarray(self.y_vals1) / np.asarray(self.y_vals2)
            self.data3_stats = [np.min(self.x_vals3), np.max(self.x_vals3), np.min(self.y_vals3), np.max(self.y_vals3)]
            self.initial_data3 = [self.x_vals3, self.y_vals3]
            self.initial_stats3 = self.data3_stats
        self._build_spec(self.x_vals3, self.y_vals3, 4, self.data3_stats)
        self._build_scale(self.data3_stats, 10)


    @staticmethod
    def format_axis(x, p):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 2))

    def __update_data1(self):
        data1_path = filedialog.askopenfilename(parent=self.root, title="Please select a .csv file containing spectrum"
                                                                        "data.")
        if data1_path == '' or data1_path is None:
            return None
        if data1_path[-4:] != ".csv":
            messagebox.showerror("Error", "That's not a .csv file!")
        else:
            self.output_path = os.path.dirname(data1_path)
            self.x_vals1, self.y_vals1, self.data1_stats = self.__load_data(data1_path)
            self._build_spec(self.x_vals1, self.y_vals1, 0, self.data1_stats)
            self._build_scale(self.data1_stats, 0)
            self.initial_data1 = [self.x_vals1, self.y_vals1]
            self.initial_stats1 = self.data1_stats

    def __update_data2(self):
        data2_path = filedialog.askopenfilename(parent=self.root, title="Please select a .csv file containing optical "
                                                                        "spectrum data.")
        if data2_path == '' or data2_path is None:
            return None
        if data2_path[-4:] != ".csv":
            messagebox.showerror("Error", "That's not a .csv file!")
        else:
            self.x_vals2, self.y_vals2, self.data2_stats = self.__load_data(data2_path)
            self._build_spec(self.x_vals2, self.y_vals2, 2, self.data2_stats)
            self._build_scale(self.data2_stats, 5)
            self.initial_data2 = [self.x_vals2, self.y_vals2]
            self.initial_stats2 = self.data2_stats

    @staticmethod
    def __load_data(path):
        x_vals = []
        y_vals = []
        with open(path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            for row in read_csv:
                x_vals.append(float(row[0]))
                y_vals.append(float(row[1]))
        stats = [np.min(x_vals), np.max(x_vals), np.min(y_vals), np.max(y_vals)]
        return x_vals, y_vals, stats

    def __update_scales(self, col):
        if col == 0:
            print('updating')
            minx = float(self.data1_minx.get())
            maxx = float(self.data1_maxx.get())
            miny = float(self.data1_miny.get())
            maxy = float(self.data1_maxy.get())
            self.data1_stats = [minx, maxx, miny, maxy]
            self._build_spec(self.x_vals1, self.y_vals1, 0, self.data1_stats)
        elif col == 5:
            minx = float(self.data2_minx.get())
            maxx = float(self.data2_maxx.get())
            miny = float(self.data2_miny.get())
            maxy = float(self.data2_maxy.get())
            self.data2_stats = [minx, maxx, miny, maxy]
            self._build_spec(self.x_vals2, self.y_vals2, 2, self.data2_stats)
        elif col == 10:
            minx = float(self.data3_minx.get())
            maxx = float(self.data3_maxx.get())
            miny = float(self.data3_miny.get())
            maxy = float(self.data3_maxy.get())
            self.data3_stats = [minx, maxx, miny, maxy]
            self._build_spec(self.x_vals3, self.y_vals3, 4, self.data3_stats)

    def __reset_data1(self):
        print('resetting')
        self.data1_stats = self.initial_stats1
        self.x_vals1 = self.initial_data1[0]
        self.y_vals1 = self.initial_data1[1]
        self._build_spec(self.x_vals1, self.y_vals1, 0, self.data1_stats)
        self._build_scale(self.data1_stats, 0)

    def __reset_data2(self):
        self.data2_stats = self.initial_stats2
        self.x_vals2 = self.initial_data2[0]
        self.y_vals2 = self.initial_data2[1]
        self._build_spec(self.x_vals2, self.y_vals2, 2, self.data2_stats)
        self._build_scale(self.data2_stats, 5)

    def __reset_data3(self):
        self.data3_stats = self.initial_stats3
        self.x_vals3 = self.initial_data3[0]
        self.y_vals3 = self.initial_data3[1]
        self._build_spec(self.x_vals3, self.y_vals3, 4, self.data3_stats)
        self._build_scale(self.data3_stats, 10)

    def __update_math(self, event):
        self.math = self.drop_down_var.get()
        self.__calculate()

    def __info(self):
        info = self.listener.modules[INFO].spec_calc_info
        title = "Optical Spectrum Calculation Information"
        make_info(title=title, info=info)

    def __pop_up_image(self, graph):
        make_popup_image(graph)

    def __select_output(self):
        title = "Please select an output folder."
        self.output_path = filedialog.askdirectory(parent=self.root, title=title)

    def __save_as_csv(self):
        if self.output_path is None or self.output_path == '':
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        if self.x_vals1 is None:
            messagebox.showerror("Error", "Please generate a prediction to save.")
        else:
            (x_low, x_high, y_low, y_high) = self.data3_stats
            index1 = np.where(self.x_vals3 == x_low)[0][0]
            index2 = np.where(self.x_vals3 == x_high)[0][0]
            print(self.y_vals3)
            x_vals = self.x_vals3[index1:index2+1]
            y_vals = self.y_vals3[index1:index2+1]
            y_vals = np.clip(y_vals, a_min=y_low, a_max=y_high)
            print(y_vals)
            data = np.asarray([x_vals, y_vals]).T
            output_path = self.output_path + "/optical_spectrum_calculation" + self.__get_naming_info() + '.csv'
            logging.debug("SAVING DATA TO " + output_path)
            np.savetxt(output_path, data, delimiter=",", fmt="%.5f")

    def __save_as_image(self):
        if self.output_path is None or self.output_path == '':
            messagebox.showerror("Error", "Please select an output folder before saving data.")
        elif self.initial_data3 is None:
            messagebox.showerror("Error", "Please generate an optical spectrum to save.")
        else:
            (x_low, x_high, y_low, y_high) = self.data3_stats
            output_path = self.output_path + "/optical_spectrum_calculation" + self.__get_naming_info() + '.png'
            logging.debug("SAVING SPEC" + output_path)
            plt.clf()
            axes = plt.subplot(111)
            axes.plot(self.x_vals3, self.y_vals3, '-', lw=0.5)
            axes.grid(linestyle=':', linewidth=0.5)
            low = y_low
            high = y_high
            if low is not None and high is not None:
                factor = (high - low) * 0.05
                low -= factor
                high += factor
            axes.set_xlim(left=x_low, right=x_high)
            axes.set_ylim(bottom=low, top=high)
            # commas and non-scientific notation
            axes.ticklabel_format(style='plain')
            axes.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
            axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
            plt.savefig(output_path)
            plt.clf()

    def __get_naming_info(self):
        x_low = str(round(self.data3_stats[0], 5))
        x_high = str(round(self.data3_stats[1], 5))
        y_low = str(round(self.data3_stats[2], 5))
        y_high = str(round(self.data3_stats[3], 5))
        func = ''
        if self.math == '-':
            func = 'subtraction'
        if self.math == '+':
            func = 'addition'
        if self.math == 'x':
            func = 'multiplication'
        if self.math == '/':
            func = 'division'
        return '_' + func + '_(' + x_low + '-' + x_high + ")-(" + y_low + '-' + y_high + ')'

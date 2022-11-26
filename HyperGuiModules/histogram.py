from HyperGuiModules.utility import *
import numpy as np
import logging


class Histogram:
    def __init__(self, histogram_frame, listener):
        self.root = histogram_frame
        self.listener = listener

        self.flattened_data = None

        self.specs = (False, True, False)
        self.spec_number = 1
        self.old_spec_number = 1

        self.parametric = False
        self.non_parametric = False

        self.parametric_button = None
        self.mean_text = None
        self.mean_value = None
        self.sd_text = None
        self.sd_value = None
        self.non_parametric_button = None
        self.median_text = None
        self.median_value = None
        self.iqr_text = None
        self.iqr_value = None

        self.first_line = None
        self.min_x = None
        self.min_x_val = None
        self.min_y = None
        self.min_y_val = None
        self.second_line = None
        self.max_x = None
        self.max_x_val = None
        self.max_y = None
        self.max_y_val = None

        self.percent_negative_text = None
        self.percent_negative_value = None
        self.count_text = None
        self.count_value = None

        self.drop_down_var = StringVar()
        self.choices = ['1. Reflectance - Original',
                        '2. Reflectance - Original without Negative Values',
                        '3. Reflectance - Normalised',
                        '4. Reflectance - Normalised without Negative Values',
                        '5. Absorbance - Original',
                        '6. Absorbance - Original without Negative Values',
                        '7. Absorbance - Normalised',
                        '8. Absorbance - Normalised without Negative Values',
                        '9. Original Image',
                        '10. Original Image - Normalised',
                        '11. Recreated Image',
                        '12. Recreated Image - Normalised',
                        '13. New Image',
                        '14. New Image - Normalised']

        self.x_upper_scale_text = None
        self.y_upper_scale_text = None
        self.x_lower_scale_text = None
        self.y_lower_scale_text = None
        self.x_upper_scale_input = None
        self.y_upper_scale_input = None
        self.x_lower_scale_input = None
        self.y_lower_scale_input = None
        self.x_upper_scale_value = None
        self.y_upper_scale_value = None
        self.x_lower_scale_value = None
        self.y_lower_scale_value = None

        self.step_size_text = None
        self.step_size_input = None
        self.step_size_value = 0.01

        self.whole_stats = [None, None, None, None, None]  # [min_x, max_x, min_y, max_y, step]
        self.masked_stats = [None, None, None, None, None]

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value_iv = IntVar()
        self.save_checkbox_value = False
        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value_iv = IntVar()
        self.save_wo_scale_checkbox_value = False
        self.save_as_excel_label = None
        self.save_as_excel_checkbox = None
        self.save_as_excel_checkbox_value_iv = IntVar()
        self.save_as_excel_checkbox_value = False

        self.interactive_histogram_graph = None
        self.axes = None
        self.axes2 = None
        self.interactive_histogram = None

        self.upper_text = None
        self.upper_input = None
        self.upper_value = None
        self.lower_text = None
        self.lower_input = None
        self.lower_value = None

        self.info_label = None

        self._init_widgets()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def update_histogram(self, data):
        print("update hist")
        self.hist_data = data.flatten()
        self.flattened_data = data.flatten()
        if self.old_spec_number != self.spec_number:
            self.old_spec_number = self.spec_number
            self.masked_stats = [None, None, None, None, None]
            self.whole_stats = [None, None, None, None, None]
        if isinstance(self.hist_data, np.ma.MaskedArray):
            arr = np.ma.sort(self.hist_data)
            index = np.where(arr.mask)[0][0]
            self.flattened_data = arr[:index]
        self.flattened_data = self.flattened_data[self.flattened_data != np.array(None)]
        self.upper_value = np.ma.max(self.flattened_data)
        self.lower_value = np.ma.min(self.flattened_data)
        print("calc stats")
        self._calc_stats()
        if self.listener.is_masked:
            self.masked_stats = [self.min_x, self.max_x, self.min_y, self.max_y, self.step_size_value]
        else:
            self.whole_stats = [self.min_x, self.max_x, self.min_y, self.max_y, self.step_size_value]
        print("build scale")
        self._build_scale()
        self._build_step_size()
        self._build_interactive_histogram()
        
    def reset_histogram(self):
        self.hist_data = None
        self.flattened_data = None
        self._build_scale()
        self._build_step_size()
        self._build_interactive_histogram()

    def _init_widgets(self):
        self._build_scale()
        self._build_step_size()
        self._build_save()
        self._build_save_wo_scale()
        self._build_save_as_excel()
        self._build_info_label()
        self._build_reset_button()
        self._build_drop_down()
        self._build_interactive_histogram()
        self._build_stats()
        self._build_calc_button()

    # --------------------------------------------------- GETTERS ----------------------------------------------------

    def get_stats(self):
        if self.listener.is_masked:
            return self.masked_stats
        else:
            return self.whole_stats

    # ----------------------------------------------- BUILDERS (MISC) -------------------------------------------------

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Histogram', command=self.__info, width=8)

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=13, column=0, inner_padx=10, inner_pady=5,
                                     outer_padx=(15, 10), outer_pady=(0, 15))
        self.save_checkbox = make_checkbox(self.root, "", row=13, column=0, var=self.save_checkbox_value_iv, sticky=NE,
                                           inner_padx=0, inner_pady=0, outer_padx=(0, 10))
        self.save_checkbox.deselect()
        self.save_checkbox.bind('<Button-1>', self.__update_save_with_scale_check_status)

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=13, column=1, inner_padx=10,
                                              inner_pady=5, outer_padx=(10, 16), outer_pady=(0, 15))
        self.save_wo_scale_checkbox = make_checkbox(self.root, "", row=13, column=1,
                                                    var=self.save_wo_scale_checkbox_value_iv, sticky=NE, inner_padx=0,
                                                    inner_pady=0, outer_padx=(0, 7))
        self.save_wo_scale_checkbox.deselect()
        self.save_wo_scale_checkbox.bind('<Button-1>', self.__update_save_wo_scale_check_status)

    def _build_save_as_excel(self):
        self.save_as_excel_label = make_label(self.root, "Save as CSV", row=13, column=2, inner_padx=10, inner_pady=5,
                                              outer_padx=(5, 15), outer_pady=(0, 15))
        self.save_as_excel_checkbox = make_checkbox(self.root, "", row=13, column=2,
                                                    var=self.save_as_excel_checkbox_value_iv, sticky=NE, inner_padx=0,
                                                    inner_pady=0, outer_padx=(0, 25))
        self.save_as_excel_checkbox.deselect()
        self.save_as_excel_checkbox.bind('<Button-1>', self.__update_save_as_excel_check_status)

    def _build_reset_button(self):
        self.reset_button = make_button(self.root, "Reset", row=13, column=3, command=self.__reset, inner_padx=10,
                                        inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=2)
        
    def _build_calc_button(self):
        self.reset_button = make_button(self.root, "CALC", row=0, column=3, command=self.__calc, inner_padx=10,
                                        inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=2)


    def _build_drop_down(self):
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__update_data)
        self.drop_down_menu.configure(highlightthickness=0, width=1,
                                      anchor='w', padx=15)
        self.drop_down_menu.grid(column=1, row=0, columnspan=1, padx=(0, 15))

    # ----------------------------------------------- BUILDERS (DATA) -------------------------------------------------

    def _build_stats(self):
        print("Build stats")
        # parametric
        self.parametric_button = make_button(self.root, text='P:', width=4, command=self.__parametric, column=0, row=2,
                                             columnspan=1, outer_padx=(15, 0), highlightthickness=0, inner_padx=3,
                                             inner_pady=0, outer_pady=(0, 3))
        # mean
        self.mean_text = make_text(self.root, content="Mean = " + str(self.mean_value),
                                   bg=tkcolour_from_rgb(BACKGROUND), column=1, row=2, width=12, columnspan=1, padx=0,
                                   state=NORMAL)
        # standard deviation
        self.sd_text = make_text(self.root, content="SD = " + str(self.sd_value), bg=tkcolour_from_rgb(BACKGROUND),
                                 column=2, row=2, width=10, columnspan=1, padx=0, state=NORMAL)
        # non parametric
        self.non_parametric_button = make_button(self.root, text='NP:', width=4, command=self.__non_parametric,
                                                 column=0, row=3, columnspan=1, outer_padx=(15, 0),
                                                 highlightthickness=0, inner_padx=3, inner_pady=0)
        # median
        self.median_text = make_text(self.root, content="Median = " + str(self.median_value),
                                     bg=tkcolour_from_rgb(BACKGROUND), column=1, row=3, width=14, columnspan=1, padx=0,
                                     state=NORMAL)
        # IQR
        self.iqr_text = make_text(self.root, content="IQR = " + str(self.iqr_value), bg=tkcolour_from_rgb(BACKGROUND),
                                  column=2, row=3, width=22, columnspan=1, padx=(0, 10), state=NORMAL)
        # min and max
        first_line_text = "x min = " + str(self.min_x) + ', y val = ' + str(self.min_x_val) + '      y min = ' + \
                          str(self.min_y) + ', x val = ' + str(self.min_y_val)
        self.first_line = make_text(self.root, content=first_line_text, bg=tkcolour_from_rgb(BACKGROUND), column=1,
                                    row=4, width=60, columnspan=4, state=NORMAL, pady=(10, 0))
        second_line_text = "x max = " + str(self.max_x) + ', y val = ' + str(self.max_x_val) + '      y max = ' + \
                           str(self.max_y) + ', x val = ' + str(self.max_y_val)
        self.second_line = make_text(self.root, content=second_line_text, bg=tkcolour_from_rgb(BACKGROUND), column=1,
                                     row=5, width=60, columnspan=4, state=NORMAL, pady=(0, 20))

        # percent negative
        self.percent_negative_text = make_text(self.root, content="% Negative = " + str(self.percent_negative_value) +
                                                                  '%', bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                               row=2, width=25, columnspan=2, rowspan=1, padx=(10, 0), state=NORMAL,
                                               pady=0)
        if self.count_value is None:
            add = str(None)
        else:
            add = '{:,}'.format(self.count_value)
        self.count_text = make_text(self.root, content="Count = " + add, bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                    row=3, width=21, columnspan=2, rowspan=1, padx=0, state=NORMAL, pady=0)

    def _build_scale(self):
        # lower
        self.lower_text = make_text(self.root, content="Lower: ", 
                                    bg=tkcolour_from_rgb(BACKGROUND), column=3, row=7, width=7, columnspan=1,
                                    pady=(0, 10))
        self.lower_input = make_entry(self.root, row=7, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.lower_input.bind('<Return>', self.__update_upper_lower)
        self.lower_input.insert(END, str(self.min_x))

        # upper
        self.upper_text = make_text(self.root, content="Upper: ", 
                                    bg=tkcolour_from_rgb(BACKGROUND), column=3, row=8, width=7, columnspan=1,
                                    pady=(0, 10))
        self.upper_input = make_entry(self.root, row=8, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper_lower)
        self.upper_input.insert(END, str(self.max_x))

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="Min x: ", bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                            row=9, width=7, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=9, column=4, width=7, pady=(0, 10), padx=(0, 15),
                                              columnspan=1)
        self.x_lower_scale_input.bind('<Return>', self.__update_scales)
        self.x_lower_scale_input.insert(END, str(self.get_stats()[0]))

        # x upper
        self.x_upper_scale_text = make_text(self.root, content="Max x: ", bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                            row=10, width=7, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=10, column=4, width=7, pady=(0, 10), padx=(0, 15),
                                              columnspan=1)
        self.x_upper_scale_input.bind('<Return>', self.__update_scales)
        self.x_upper_scale_input.insert(END, str(self.get_stats()[1]))

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="Min y: ", bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                            row=11, width=7, columnspan=1, pady=(0, 10))
        self.y_lower_scale_input = make_entry(self.root, row=11, column=4, width=7, pady=(0, 10), padx=(0, 15),
                                              columnspan=1)
        self.y_lower_scale_input.bind('<Return>', self.__update_scales)
        self.y_lower_scale_input.insert(END, str(self.get_stats()[2]))

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="Max y: ", bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                            row=12, width=7, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=12, column=4, width=7, pady=(0, 10), padx=(0, 15),
                                              columnspan=1)
        self.y_upper_scale_input.bind('<Return>', self.__update_scales)
        self.y_upper_scale_input.insert(END, str(self.get_stats()[3]))

    def _build_step_size(self):
        self.step_size_text = make_text(self.root, content="Step: ", 
                                        bg=tkcolour_from_rgb(BACKGROUND), column=3, row=6, width=6, columnspan=1,
                                        pady=(0, 10))
        self.step_size_input = make_entry(self.root, row=6, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.step_size_input.bind('<Return>', self.__update_scales)
        self.step_size_input.insert(END, str(self.get_stats()[4]))

    # ---------------------------------------------- BUILDERS (GRAPH) ------------------------------------------------

    def _build_interactive_histogram(self):
        print("build int hist")
        # create canvas
        self.interactive_histogram_graph = Figure(figsize=(3.5, 2))
        self.axes = self.interactive_histogram_graph.add_subplot(111)
        self.interactive_histogram_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        if self.flattened_data is not None:
            # calc bins
            bins = np.arange(start=np.ma.min(self.flattened_data),
                             stop=np.ma.max(self.flattened_data) + self.get_stats()[4], step=self.get_stats()[4])
            # plot histogram
            self.axes.hist(self.flattened_data, bins=bins)
            if self.parametric:
                # plot error bar
                self.plot_parametric()
            elif self.non_parametric:
                # plot boxplot
                self.plot_non_parametric()
            # set axes
            self.interactive_histogram_graph.set_tight_layout(True)
            self.axes.set_xlim(left=self.get_stats()[0], right=self.get_stats()[1])
            self.axes.set_ylim(bottom=self.get_stats()[2], top=self.get_stats()[3])
            # commas and non-scientific notation
            self.axes.ticklabel_format(style='plain')
            self.axes.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))
            self.axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self.format_axis))

        # draw figure
        self.interactive_histogram = FigureCanvasTkAgg(self.interactive_histogram_graph, master=self.root)
        self.interactive_histogram.draw()
        self.interactive_histogram.get_tk_widget().grid(column=0, row=6, columnspan=3, rowspan=7, ipady=5, ipadx=0,
                                                        pady=0)
        self.interactive_histogram.get_tk_widget().bind('<Button-2>', self.__pop_up_image)

    def plot_parametric(self):
        self.axes2 = self.axes.twinx()
        self.axes2.plot([self.mean_value-self.sd_value, self.mean_value+self.sd_value], [1, 1], 'k-', lw=1)
        self.axes2.plot([self.mean_value-self.sd_value, self.mean_value-self.sd_value], [0.9, 1.1], 'k-', lw=1)
        self.axes2.plot([self.mean_value+self.sd_value, self.mean_value+self.sd_value], [0.9, 1.1], 'k-', lw=1)
        self.axes2.plot([self.mean_value, self.mean_value], [0.9, 1.1], '#F17E3A', lw=1)
        self.axes2.set_ylim(bottom=0, top=2)
        self.axes2.get_yaxis().set_visible(False)

    def plot_non_parametric(self):
        self.axes2 = self.axes.twinx()
        self.axes2.boxplot(self.flattened_data, vert=False, sym='')
        self.axes2.get_yaxis().set_visible(False)

    @staticmethod
    def format_axis(x, p):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 3))

    # ------------------------------------------------- CALCULATORS --------------------------------------------------

    def _calc_stats(self):
        # construct data list in proper range
        logging.debug("CONSTRUCTING RANGED DATA...")
        data = self.flattened_data[self.lower_value <= self.flattened_data]
        data = data[data <= self.upper_value]
        data = np.ma.sort(data)
        length = np.ma.count(data)
        # mean, sd, median, iqr
        logging.debug("CALCULATING STATS...")
        print("1")
        self.mean_value = np.round(np.ma.mean(data), 3)
        progress(0, 11)
        print("2")
        self.sd_value = np.round(np.ma.std(data), 3)
        progress(1, 11)
        print("3")
        self.median_value = np.round(data[int(length*1/2)], 3)
        progress(2, 11)
        print("4")
        self.iqr_value = (np.round(data[int(length*1/4)], 3), round(data[int(length*3/4)], 3))
        progress(3, 11)
        # generate bins
        print("5")
        if self.upper_value - self.lower_value > 10:
            self.step_size_value = 1
            if self.upper_value - self.lower_value > 1000:
                self.step_size_value = 100
        print(self.lower_value)
        print(self.upper_value)
        print(self.step_size_value)

        bins = np.arange(start=self.lower_value, stop=self.upper_value + self.step_size_value,
                         step=self.step_size_value)
        print(bins)
        progress(4, 11)
        # generate numpy histogram data
        print("6")
        histogram_data = np.histogram(data, bins=bins)
        progress(5, 11)
        print("7")
        # determine the minimum y value and at which x this occurs
        self.min_y = np.round(np.ma.min(np.histogram(data, bins=bins)[0]), 3)
        self.min_y_val = np.round(histogram_data[1][np.where(histogram_data[0] == self.min_y)[0][0]], 3)
        progress(6, 11)
        print("8")
        # determine the maximum y value and at which x this occurs
        self.max_y = np.round(np.ma.max(histogram_data[0]), 3)
        self.max_y_val = np.round(histogram_data[1][np.where(histogram_data[0] == self.max_y)[0][0]], 3)
        progress(7, 11)
        print("9")
        # determine the minimum x (bin) value and its size
        self.min_x = np.round(histogram_data[1][0], 3)
        self.min_x_val = np.round(histogram_data[0][0], 3)
        progress(8, 11)
        print("10")
        # determine the maximum x (bin) value and its size
        self.max_x = np.round(histogram_data[1][-1], 3)
        self.max_x_val = np.round(histogram_data[0][-1], 3)
        progress(9, 11)
        print("11")
        # percent negative
        percent = np.ma.sum(data < 0)/len(data) * 100
        self.percent_negative_value = round(percent, 3)
        progress(10, 11)
        print("12")
        self.count_value = round(len(self.flattened_data), 3)
        self._build_stats()

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].hist_info
        title = "Histogram Information"
        make_info(title=title, info=info)

    def __update_data(self, event):
        choice = self.drop_down_var.get()[:2]
        if choice in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.']:
            self.step_size_value = 0.01
            self.specs, self.spec_number = specs(choice=choice)
            self.listener.update_histogram_specs(self.specs)
        elif choice == '9.':
            data = self.listener.get_current_original_data()
            self.step_size_value = 1
            self.spec_number = 9
            self.update_histogram(data)
        elif choice == '10':
            data = self.listener.get_current_norm_original_data()
            self.step_size_value = 0.01
            self.spec_number = 10
            self.update_histogram(data)
        elif choice == '11':
            data = self.listener.get_current_rec_data()
            self.step_size_value = 0.01
            self.spec_number = 11
            self.update_histogram(data)
        elif choice == '12':
            data = self.listener.get_current_norm_rec_data()
            self.step_size_value = 0.01
            self.spec_number = 12
            self.update_histogram(data)
        elif choice == '13':
            data = self.listener.get_current_new_data()
            self.step_size_value = 0.01
            self.spec_number = 13
            self.update_histogram(data)
        elif choice == '14':
            data = self.listener.get_current_norm_new_data()
            self.step_size_value = 0.01
            self.spec_number = 14
            self.update_histogram(data)

    def __pop_up_image(self, event):
        make_popup_image(self.interactive_histogram_graph)

    def __parametric(self):
        if self.parametric:
            self.parametric = False
            self.parametric_button.config(foreground="black")
        else:
            self.parametric = True
            self.parametric_button.config(foreground="red")
            self.non_parametric = False
            self.non_parametric_button.config(foreground="black")
        self._build_interactive_histogram()

    def __non_parametric(self):
        if self.non_parametric:
            self.non_parametric = False
            self.non_parametric_button.config(foreground="black")
        else:
            self.non_parametric = True
            self.parametric = False
            self.non_parametric_button.config(foreground="red")
            self.parametric_button.config(foreground="black")
        self._build_interactive_histogram()

    def __reset(self):
        self.x_lower_scale_value = None
        self.x_upper_scale_value = None
        self.y_lower_scale_value = None
        self.y_upper_scale_value = None
        self.update_histogram(self.flattened_data)

    def __update_upper_lower(self, event):
        self.upper_value = float(self.upper_input.get())
        self.lower_value = float(self.lower_input.get())
        self._calc_stats()

    def __update_scales(self, event):
        self.x_upper_scale_value = float(self.x_upper_scale_input.get())
        self.y_upper_scale_value = float(self.y_upper_scale_input.get())
        self.x_lower_scale_value = float(self.x_lower_scale_input.get())
        self.y_lower_scale_value = float(self.y_lower_scale_input.get())
        self.step_size_value = float(self.step_size_input.get())
        if self.listener.is_masked:
            self.masked_stats = [self.x_lower_scale_value, self.x_upper_scale_value,
                                 self.y_lower_scale_value, self.y_upper_scale_value,
                                 self.step_size_value]
        else:
            self.whole_stats = [self.x_lower_scale_value, self.x_upper_scale_value,
                                self.y_lower_scale_value, self.y_upper_scale_value,
                                self.step_size_value]
        self._build_interactive_histogram()

    def __update_save_with_scale_check_status(self, event):
        self.save_checkbox_value = not self.save_checkbox_value
        self.listener.update_saved(HISTOGRAM_IMAGE, self.save_checkbox_value)

    def __update_save_wo_scale_check_status(self, event):
        self.save_wo_scale_checkbox_value = not self.save_wo_scale_checkbox_value
        self.listener.update_saved(HISTOGRAM_IMAGE_WO_SCALE, self.save_wo_scale_checkbox_value)

    def __update_save_as_excel_check_status(self, event):
        self.save_as_excel_checkbox_value = not self.save_as_excel_checkbox_value
        self.listener.update_saved(HISTOGRAM_EXCEL, self.save_as_excel_checkbox_value)
        
    def __calc(self):
        self.listener.calc_hist()

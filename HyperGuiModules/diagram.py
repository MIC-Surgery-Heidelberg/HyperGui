from HyperGuiModules.utility import *


class Diagram:
    def __init__(self, diagram_frame, listener):
        self.root = diagram_frame

        # Listener
        self.listener = listener

        self.whole_image_button = None
        self.whole_image_checkbox = None
        self.whole_image_checkbox_value_iv = IntVar()
        self.whole_image_checkbox_value = False

        self.masked_region_button = None
        self.masked_region_checkbox = None
        self.masked_region_checkbox_value_iv = IntVar()
        self.masked_region_checkbox_value = False

        self.is_masked = False
        self.info_label = None
        self._init_widget()

    # ------------------------------------------------ INITIALIZATION ------------------------------------------------

    def _init_widget(self):
        self._build_whole_image()
        self._build_masked_region()
        self._build_info_label()

    # --------------------------------------------------- BUILDERS ---------------------------------------------------

    def _build_whole_image(self):
        self.whole_image_button = make_button(self.root, "Whole Image", row=1, column=0,
                                              command=self.__use_whole_image, inner_padx=15, inner_pady=5,
                                              outer_padx=15, outer_pady=(0, 10))
        self.whole_image_button.config(foreground="red")
        self.whole_image_checkbox = make_checkbox(self.root, "", row=1, column=0, var=self.whole_image_checkbox_value_iv,
                                                  sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.whole_image_checkbox.bind('<Button-1>', self.__update_whole_image_check_status)
        self.whole_image_checkbox.select()
        self.listener.update_saved(WHOLE_IMAGE_SAVE, True)  # set whole image save to true by default

    def _build_masked_region(self):
        self.masked_region_button = make_button(self.root, "Masked Region", row=2, column=0,
                                                command=self.__use_masked_image, inner_padx=15, inner_pady=5,
                                                outer_padx=15, outer_pady=(0, 15))
        self.masked_region_checkbox = make_checkbox(self.root, "", row=2, column=0,
                                                    var=self.masked_region_checkbox_value_iv, sticky=NE, inner_padx=0,
                                                    inner_pady=0, outer_padx=(0, 5))
        self.masked_region_checkbox.deselect()
        self.masked_region_checkbox.bind('<Button-1>', self.__update_masked_region_check_status)

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Area', command=self.__info, width=5)
        self.info_label.grid(padx=(0, 65))

    # -------------------------------------------------- CALLBACKS ---------------------------------------------------

    def __info(self):
        info = self.listener.modules[INFO].diagram_info
        title = "Area Information"
        make_info(title=title, info=info)

    def __use_whole_image(self):
        self.is_masked = False
        self.whole_image_button.config(foreground="red")
        self.masked_region_button.config(foreground="black")
        self.listener.submit_is_masked(self.is_masked)

    def __use_masked_image(self):
        self.is_masked = True
        self.masked_region_button.config(foreground="red")
        self.whole_image_button.config(foreground="black")
        self.listener.submit_is_masked(self.is_masked)

    def __update_whole_image_check_status(self, event):
        self.whole_image_checkbox_value = not self.whole_image_checkbox_value
        self.listener.update_saved(WHOLE_IMAGE_SAVE, self.whole_image_checkbox_value)

    def __update_masked_region_check_status(self, event):
        self.masked_region_checkbox_value = not self.masked_region_checkbox_value
        self.listener.update_saved(MASKED_IMAGE_SAVE, self.masked_region_checkbox_value)

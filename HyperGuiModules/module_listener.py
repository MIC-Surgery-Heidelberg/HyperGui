from AnalysisModules.analysis_abs import AbsSpecAnalysis
from AnalysisModules.analysis_hist import HistogramAnalysis
from AnalysisModules.analysis_new import NewAnalysis
from AnalysisModules.analysis_recreated import RecreatedAnalysis
from AnalysisModules.analysis import Analysis
from HyperGuiModules.utility import *
import numpy as np
import logging


class ModuleListener:
    def __init__(self):
        # {module_name: module}
        self.modules = {}

        # SOURCE AND OUTPUT VALUES
        # {data_cube_path: analysis object}
        self.results = {}
        self.current_rendered_result_path = None
        self.selected_paths = []
        self.output_folder = None  # init with None intentionally
        self.output_folder_hypergui = '_hypergui_1'

        # NOTE: THE FOLLOWING ONLY CONTROLS WHAT TO RENDER, NOT WHAT IS SAVED

        self.data_cube = None
        self.dc_path = None
        
        self.segm = False
        self.recr = False
        self.live = False

        # ANALYSIS AND FORM
        self.normal = None
        self.absorbance = None
        self.wavelength = None
        self.index_number = None
        self.histogram_specs = None
        self.ab_spec_specs = None
        self.params = [0.2, -0.03, -0.46, 0.45, 0.4, 1.55, 0.1, -0.5]

        # ORIGINAL IMAGE
        self.mask = None

        # DIAGRAM
        self.is_masked = False

    # ------------------------------------------ INITIALIZATION OF DATA CUBE -----------------------------------------

    def submit_data_cube(self, data_cube, dc_path):
        self.data_cube = data_cube
        self.dc_path = dc_path
        self.results[dc_path] = ['hist', 'abs', 'rec', 'new', data_cube]

        if self.modules[ANALYSIS_AND_FORM]:
            self.wavelength = self.modules[ANALYSIS_AND_FORM].get_wavelength()
            self.index_number = self.modules[ANALYSIS_AND_FORM].index_selected
            self.mask = self.modules[ORIGINAL_COLOUR].mask_raw
            self.is_masked = self.modules[DIAGRAM].is_masked

            # specs = (absorbance/reflectance, original/norm, negatives yes/no)
            self.histogram_specs = self.modules[HISTOGRAM].specs
            self.ab_spec_specs = self.modules[ABSORPTION_SPEC].specs

            # update each based on inputs
            if not self.live:
                self._make_new_hist_analysis(dc_path, data_cube, self.wavelength, self.mask,
                                         self.histogram_specs)

            self._make_new_rec_analysis(dc_path, data_cube, self.wavelength, self.mask,
                                        self.params)
            self._make_new_new_analysis(dc_path, data_cube, self.wavelength, self.index_number, self.mask)
            if not self.live:
                self._make_new_abs_analysis(dc_path, data_cube, self.wavelength, self.mask, self.ab_spec_specs)
    
    def calc_abs(self):
        if self.get_result(self.current_rendered_result_path)[1] is "abs":
            self._make_new_abs_analysis(self.current_rendered_result_path, self.data_cube, self.wavelength, self.mask, self.ab_spec_specs)
        self.broadcast_to_absorption_spec()
        
    def calc_hist(self):
        if self.get_result(self.current_rendered_result_path)[0] is "hist":
            self._make_new_hist_analysis(self.current_rendered_result_path, self.data_cube, self.wavelength, self.mask, self.ab_spec_specs)
        self.broadcast_to_histogram()

    def set_data_cube(self, dc_path):
        self.current_rendered_result_path = dc_path
        self.broadcast_new_data()
    
    def set_output_folder_hypergui(self, string):
        self.output_folder_hypergui = '_hypergui_' + string

    def update_selected_paths(self, selected_paths):
        self.selected_paths = selected_paths

    def delete_analysis_result(self, path):
        logging.debug("DELETING DATA CUBE: " + path)
        del self.results[path]
    # ---------------------------------------------------- MISC ------------------------------------------------------

    def attach_module(self, module_name, mod):
        self.modules[module_name] = mod

    def instant_save_points(self):
        data = self.get_coords()
        self.modules[SAVE].instant_save_points(data, title="MASK_COORDINATES")

    def update_saved(self, saves_key, value):
        logging.debug("UPDATING " + saves_key + " TO " + str(value))
        self.modules[SAVE].update_saves(saves_key, value)

    # --------------------------------------------------- GETTERS ----------------------------------------------------

    def get_result(self, path):
        if self.results[path] is not None:
            return self.results[path]

    def get_mask(self):
        if self.mask is not None:
            return self.mask
        else:
            return np.asarray([[False for _ in range(self.data_cube.size[0])] for _ in range(self.data_cube.size[1])])

    def get_wl(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path)[3].get_wl_data_masked()
        else:
            return self.get_result(self.current_rendered_result_path)[3].get_wl_data()

    def get_idx(self):
        if self.is_masked:
            return self.get_result(self.current_rendered_result_path)[3].index_masked
        else:
            return self.get_result(self.current_rendered_result_path)[3].index

    def get_coords(self):
        point_coords = self.modules[ORIGINAL_COLOUR].coords_list
        data = [[float(point_coords[i][0] + 1), float(point_coords[i][1] + 1)] for i in range(1000000) if
                point_coords[i] != (None, None)]
        return data
    
    def get_segm(self):
        return self.segm

    # ------------------------------------------------- DATA GETTERS -------------------------------------------------

    def get_current_original_data(self):
        data = self.modules[ORIGINAL_COLOUR].original_image_data
        data = np.asarray(rgb_image_to_hsi_array(data))
        if not self.is_masked:
            return data
        else:
            mask = self.mask
            data = np.ma.array(data, mask=np.rot90(mask))
            return data

    def get_current_norm_original_data(self):
        data = self.modules[ORIGINAL_COLOUR].original_image_data
        data = np.asarray(rgb_image_to_hsi_array(data))
        # if np.ma.min(data) < 0:
        #     data = data + np.abs(np.ma.min(data))
        # if np.ma.min(data) > 0:
        #     data = data - np.abs(np.ma.min(data))
        data = data / np.ma.max(data)
        if not self.is_masked:
            return data
        else:            
            mask = self.mask
            return np.ma.array(data, mask=np.rot90(mask))

    def get_current_rec_data(self):
        data = self.modules[RECREATED_COLOUR].recreated_colour_image_data
        if not self.is_masked:
            return data
        else:
            if self.data_cube.shape[0] == 720:
                from PIL import Image
                mask = np.array(Image.fromarray(self.mask).resize((720, 540), resample=1))
            else:
                mask = self.mask
            return np.ma.array(data, mask=mask)

    def get_current_norm_rec_data(self):
        data = self.modules[RECREATED_COLOUR].recreated_colour_image_data
        if np.ma.min(data) < 0:
            data = data + np.abs(np.ma.min(data))
        if np.ma.min(data) > 0:
            data = data - np.abs(np.ma.min(data))
        data = data / np.ma.max(data)
        if not self.is_masked:
            return data
        else:
            if self.data_cube.shape[0] == 720:
                from PIL import Image
                mask = np.array(Image.fromarray(self.mask).resize((720, 540), resample=1))
            else:
                mask = self.mask
            return np.ma.array(data, mask=mask)

    def get_current_new_data(self):
        data = self.modules[NEW_COLOUR].new_colour_image_data
        if not self.is_masked:
            return data
        else:
            if self.data_cube.shape[0] == 720:
                from PIL import Image
                mask = np.array(Image.fromarray(self.mask).resize((720, 540), resample=1))
            else:
                mask = self.mask
            return np.ma.array(data, mask=mask)

    def get_current_norm_new_data(self):
        data = self.modules[NEW_COLOUR].new_colour_image_data
        if np.ma.min(data) < 0:
            data = data + np.abs(np.ma.min(data))
        if np.ma.min(data) > 0:
            data = data - np.abs(np.ma.min(data))
        data = data / np.ma.max(data)
        if not self.is_masked:
            return data
        else:
            if self.data_cube.shape[0] == 720:
                from PIL import Image
                mask = np.array(Image.fromarray(self.mask).resize((720, 540), resample=1))
            else:
                mask = self.mask
            return np.ma.array(data, mask=mask)

    # --------------------------------------------------- NAMING -----------------------------------------------------

    def get_csv_rec_info(self):
        # retrieve data: display, csv number
        display = self.modules[RECREATED_COLOUR].displayed_image_mode
        num = self.modules[RECREATED_COLOUR].spec_number
        info = '_' + str(display) + '_fromCSV' + str(num)
        return info

    def get_csv_new_info(self, mode):
        # retrieve data: display, csv number
        num = self.modules[NEW_COLOUR].spec_number
        mod = ''
        if mode == WL:
            mod = '_WL_' + str(self.wavelength[0] * 5 + 500) + '-' + str(self.wavelength[1] * 5 + 500)
        elif mode == IDX:
            mod = '_IDX' + str(self.index_number)
        info = str(mod) + '_fromCSV' + str(num)
        return info

    def get_csv_og_info(self):
        # retrieve data: display
        display = self.modules[ORIGINAL_COLOUR].displayed_image_mode
        info = '_original-' + str(display)
        return info

    def get_save_og_info(self, display, image):
        # e.g. og_image_RGB-cs_masked.png
        # e.g. og_image_THI_whole_data.csv
        grey = self.modules[ORIGINAL_COLOUR].gs
        colour = '-cs'
        if grey:
            colour = '-gs'
        if image:
            return 'og_image_' + display + colour
        else:
            return 'og_image_' + display + '_data'

    def get_save_rec_info(self, display, image, masked, path):
        # e.g. rec_image_fromCSV2_with-scale_STO2-gs-0.112341-30.122421_whole.png
        # e.g. rec_image_fromCSV2_wo-scale_STO2-0.112341-30.122421_masked_data.csv
        num = self.modules[RECREATED_COLOUR].spec_number
        (lower, upper) = self.generate_rec_values_for_saving(path, display)
        grey = self.modules[RECREATED_COLOUR].gs
        colour = '-cs'
        if grey:
            colour = '-gs'
        scale = '-' + str(lower) + '-' + str(upper)
        masked_mod = '_whole'
        if masked:
            masked_mod = '_masked'
        if image:
            return 'rec_image_fromCSV' + str(num), display + colour + scale + masked_mod
        else:
            return 'rec_image_fromCSV' + str(num) + '_' + display + scale + masked_mod + '_data'

    def generate_rec_values_for_saving(self, path, display):
        arr = []
        if display == STO2:
            arr = self.modules[RECREATED_COLOUR].sto2_stats
            if arr == [None, None]:
                data = self.results[path][2].sto2
                arr = [np.round(np.min(data), 4), np.round(np.max(data), 4)]
        if display == NIR:
            arr = self.modules[RECREATED_COLOUR].nir_stats
            if arr == [None, None]:
                data = self.results[path][2].nir
                arr = [np.round(np.min(data), 4), np.round(np.max(data), 4)]
        if display == THI:
            arr = self.modules[RECREATED_COLOUR].thi_stats
            if arr == [None, None]:
                data = self.results[path][2].thi
                arr = [np.round(np.min(data), 4), np.round(np.max(data), 4)]
        if display == TWI:
            arr = self.modules[RECREATED_COLOUR].twi_stats
            if arr == [None, None]:
                data = self.results[path][2].twi
                arr = [np.round(np.min(data), 4), np.round(np.max(data), 4)]
        if display == TLI:
            arr = self.modules[RECREATED_COLOUR].tli_stats
            if arr == [None, None]:
                data = self.results[path][2].tli
                arr = [np.round(np.min(data), 4), np.round(np.max(data), 4)]
        if display == OHI:
            arr = self.modules[RECREATED_COLOUR].ohi_stats
            if arr == [None, None]:
                data = self.results[path][2].ohi
                arr = [np.round(np.min(data), 4), np.round(np.max(data), 4)]
        return arr

    def get_save_new_info(self, display, image, masked, path):
        # e.g. new_image_fromCSV2_with-scale_IDX1-gs-0.112341-30.122421_masked.png
        # e.g. new_image_fromCSV2_with-scale_WL-500-560-0.112341-30.122421_whole_data.csv
        num = self.modules[NEW_COLOUR].spec_number
        (lower, upper) = self.generate_new_values_for_saving(path, display)
        mod = ''
        if display == 'WL':
            mod = 'WL-' + str(self.wavelength[0] * 5 + 500) + '-' + str(self.wavelength[1] * 5 + 500)
        elif display == 'IDX':
            mod = 'IDX' + str(self.index_number)
        grey = self.modules[NEW_COLOUR].gs
        colour = '-cs'
        if grey:
            colour = '-gs'
        scale = '-' + str(lower) + '-' + str(upper)
        masked_mod = '_whole'
        if masked:
            masked_mod = '_masked'
        if image:
            return 'new_image_fromCSV' + str(num), mod + colour + scale + masked_mod
        else:
            return 'new_image_fromCSV' + str(num) + '_' + mod + scale + masked_mod + '_data'

    def generate_new_values_for_saving(self, path, display):
        arr = []
        if display == IDX:
            arr = self.modules[NEW_COLOUR].idx_stats
            if arr == [None, None]:
                data = self.results[path][3].index
                arr = [np.round(np.min(data), 4), np.round(np.max(data), 4)]
        if display == WL:
            arr = self.modules[NEW_COLOUR].wl_stats
            if arr == [None, None]:
                data = self.results[path][3].get_wl_data()
                arr = [np.round(np.min(data), 4), np.round(np.max(data), 4)]
        return arr

    def get_save_hist_info(self, scale, image, masked, data):
        # e.g. histogram_fromCSV1_(0-3)-(0-200000)-0.01_with-scale_np.png
        # e.g. histogram_fromCSV9_(0-3)-(0-200000)-0.01_with-scale_np_STO2-csv7-cs-2.62299-0.22225.png
        # e.g. histogram_fromCSV12_(0-3)_(0-200000)-0.01_with-scale_np_IDX3-csv1-gs-2.62299-0.22225.png
        num = self.modules[HISTOGRAM].spec_number
        (xmin, xmax, ymin, ymax, step) = self.generate_hist_values_for_saving(masked, data)
        parametric = self.modules[HISTOGRAM].parametric
        non_parametric = self.modules[HISTOGRAM].non_parametric
        limits = '_(' + str(xmin) + '-' + str(xmax) + ')-(' + str(ymin) + '-' + str(ymax) + ')-' + str(step) + '_'
        scale_mod = 'wo-scale'
        if scale:
            scale_mod = 'with-scale'
        p_mod = ''
        if parametric:
            p_mod = 'p_'
        if non_parametric:
            p_mod = 'np_'
        if num == 9 or num == 10:
            data_mod = self.get_abbreviated_og_info()
        elif num == 11 or num == 12:
            data_mod = self.get_abbreviated_rec_info()
        elif num == 13 or num == 14:
            data_mod = self.get_abbreviated_new_info()
        else:
            data_mod = ['', '']
        masked_mod = 'whole_'
        if masked:
            masked_mod = 'masked_'
        if image:
            return 'histogram_fromCSV' + str(num) + limits + p_mod + data_mod[0] + masked_mod + scale_mod
        else:
            return 'histogram_fromCSV' + str(num) + limits + p_mod + data_mod[1] + masked_mod + 'data'

    def generate_hist_values_for_saving(self, masked, data):
        if not masked:
            arr = self.modules[HISTOGRAM].whole_stats
        else:
            arr = self.modules[HISTOGRAM].masked_stats

        if arr != [None, None, None, None, None]:
            return [round(float(arr[i]), 4) for i in range(5)]
        else:
            lower = np.ma.min(data)
            upper = np.ma.max(data)
            step = 0.01
            if self.modules[HISTOGRAM].spec_number == 9:
                step = 1
            bins = np.arange(start=lower, stop=upper + step, step=step)
            histogram_data = np.histogram(data, bins=bins)
            y_min = np.round(np.ma.min(histogram_data[0]), 4)
            y_max = np.round(np.ma.max(histogram_data[0]), 4)
            x_min = np.round(histogram_data[1][0], 4)
            x_max = np.round(histogram_data[1][-1], 4)
            return [x_min, x_max, y_min, y_max, step]

    def get_save_abs_info(self, scale, image, masked, data):
        # e.g. abspec_fromCSV1_(0-3)_(0-200000)_with-scale.png
        # e.g. abspec_fromCSV1_(0-3)_(0-200000)_with-scale_data.csv
        num = self.modules[ABSORPTION_SPEC].spec_number
        (xmin, xmax, ymin, ymax, normed) = self.generate_abs_values_for_saving(masked, data)
        norm = '_'
        if normed:
            norm = '-normed_'
        limits = '_(' + str(xmin) + '-' + str(xmax) + ')-(' + str(ymin) + '-' + str(ymax) + ')' + norm
        scale_mod = 'wo-scale'
        if scale:
            scale_mod = 'with-scale'
        masked_mod = 'whole_'
        if masked:
            masked_mod = 'masked_'
        if image:
            return 'spectrum_fromCSV' + str(num) + limits + masked_mod + scale_mod
        else:
            return 'spectrum_fromCSV' + str(num) + limits + masked_mod + 'data'

    def generate_abs_values_for_saving(self, masked, data):
        if not masked:
            arr = self.modules[ABSORPTION_SPEC].whole_stats
        else:
            arr = self.modules[ABSORPTION_SPEC].masked_stats
        if arr != [None, None, None, None, False]:
            a = [round(float(arr[i]), 4) for i in range(4)]
            a.append(arr[4])
            return a
        else:
            y_min = np.round(np.ma.min(data), 4)
            y_max = np.round(np.ma.max(data), 4)
            x_min = 500
            x_max = 995
            norm = False
            return [x_min, x_max, y_min, y_max, norm]

    def get_abbreviated_rec_info(self):
        # e.g. [0] = STO2-csv7-cs-2.62299-0.22225
        # e.g. [1] = STO2-csv7-2.62299-0.22225
        display = self.modules[RECREATED_COLOUR].displayed_image_mode
        num = self.modules[RECREATED_COLOUR].spec_number
        lower = round(float(self.modules[RECREATED_COLOUR].lower_scale_value), 4)
        upper = round(float(self.modules[RECREATED_COLOUR].upper_scale_value), 4)
        scale_mod = '-' + str(lower) + '-' + str(upper)
        grey = self.modules[RECREATED_COLOUR].gs
        norm = ''
        if self.modules[RECREATED_COLOUR].norm:
            norm = '-normed'
        colour = '-cs'
        if grey:
            colour = '-gs'
        image = display + '-csv' + str(num) + colour + scale_mod + norm + '_'
        csv = display + '-csv' + str(num) + scale_mod + norm + '_'
        return [image, csv]

    def get_abbreviated_new_info(self):
        # e.g. [0] = WL-500-500-csv7-cs-2.62299-0.22225
        # e.g. [1] = IDX4-csv7-2.62299-0.22225
        display = self.modules[NEW_COLOUR].displayed_image_mode
        num = self.modules[NEW_COLOUR].spec_number
        lower = round(float(self.modules[NEW_COLOUR].lower_scale_value), 4)
        upper = round(float(self.modules[NEW_COLOUR].upper_scale_value), 4)
        scale_mod = '-' + str(lower) + '-' + str(upper)
        grey = self.modules[NEW_COLOUR].gs
        norm = ''
        if self.modules[NEW_COLOUR].norm:
            norm = '-normed'
        colour = '-cs'
        if grey:
            colour = '-gs'
        if display == WL:
            mod = 'WL_' + str(self.wavelength[0] * 5 + 500) + '-' + str(self.wavelength[1] * 5 + 500)
        elif display == IDX:
            mod = 'IDX' + str(self.index_number)
        image = mod + '-csv' + str(num) + colour + scale_mod + norm + '_'
        csv = mod + '-csv' + str(num) + scale_mod + norm + '_'
        return [image, csv]

    def get_abbreviated_og_info(self):
        # e.g. [0] = original-STO2-cs
        # e.g. [1] = origianal-STO2-gs
        display = self.modules[ORIGINAL_COLOUR].displayed_image_mode
        grey = self.modules[ORIGINAL_COLOUR].gs
        colour = '-cs'
        if grey:
            colour = '-gs'
        image = 'original-' + str(display) + colour + '_'
        csv = 'original-' + str(display) + '_'
        return [image, csv]

    # ------------------------------------------------ CSV FUNCTIONS --------------------------------------------------

    def remove_masked_values(self, cube):
        logging.debug("DEALING WITH MASKED VALUES...")
        for i in range(len(cube)):
            for j in range(len(cube[i])):
                for k in range(len(cube[i][j])):
                    if cube[i][j][k] == '--' or cube[i][j][k] is None:
                        cube[i][j][k] = str('')
                    else:
                        cube[i][j][k] = str(float(cube[i][j][k]))
        return cube

    def ref_data_cube(self, path):
        # 1. Original reflectance
        # Data cube is originally same for all, use hist because its the first in the list
        # absorbance, original, non-neg
        obj = Analysis(path, self.get_result(path)[0].data_cube, self.wavelength, (False, True, False), mask=None)
        cube = obj.x1.tolist()
        return self.remove_masked_values(cube)

    def ref_non_neg_cube(self, path):
        # 2. Original reflectance without negative values --> 1 with spaces for
        # negative values
        obj = Analysis(path, self.get_result(path)[0].data_cube, self.wavelength, (False, True, True), mask=None)
        cube = obj.x1.tolist()
        return self.remove_masked_values(cube)

    def ref_norm_cube(self, path):
        # 3. Normalised reflectance --> 1 divded by max(1)
        obj = Analysis(path, self.get_result(path)[0].data_cube, self.wavelength, (False, False, False), mask=None)
        cube = obj.x1.tolist()
        return self.remove_masked_values(cube)

    def ref_norm_non_neg_cube(self, path):
        # 4. Normalised reflectance without negative values --> 3 with spaces
        # for negative values
        obj = Analysis(path, self.get_result(path)[0].data_cube, self.wavelength, (False, False, True), mask=None)
        cube = obj.x1.tolist()
        return self.remove_masked_values(cube)

    def ab_data_cube(self, path):
        # 5. Original absorbance --> -log() of 2
        obj = Analysis(path, self.get_result(path)[0].data_cube, self.wavelength, (True, True, False), mask=None)
        cube = obj.x2.tolist()
        return self.remove_masked_values(cube)

    def ab_non_neg_cube(self, path):
        # 6. Original absorbanve without negative values --> 5 with spaces for
        # negative values
        obj = Analysis(path, self.get_result(path)[0].data_cube, self.wavelength, (True, True, True), mask=None)
        cube = obj.x2.tolist()
        return self.remove_masked_values(cube)

    def ab_norm_cube(self, path):
        # 7. Normalised absorbance --> 5 divided by max(5)
        obj = Analysis(path, self.get_result(path)[0].data_cube, self.wavelength, (True, False, False), mask=None)
        cube = obj.x2.tolist()
        return self.remove_masked_values(cube)

    def ab_norm_non_neg_cube(self, path):
        # 8. Normalised absorbance without negative values --> 7 with spaces for
        # negative values
        obj = Analysis(path, self.get_result(path)[0].data_cube, self.wavelength, (True, False, True), mask=None)
        cube = obj.x2.tolist()
        return self.remove_masked_values(cube)

    # ------------------------------------------------- SUBMITTERS ---------------------------------------------------

    def submit_mask(self, new_mask):
        logging.debug("NEW MASK: [...]")
        self.mask = new_mask
        self.update_analysis(mask=self.mask)
        if self.is_masked:
            self.broadcast_new_data()

    def submit_wavelength(self, new_wavelength):
        logging.debug("NEW WAVELENGTH: " + str(new_wavelength))
        self.wavelength = new_wavelength
        self.update_analysis(wavelength=self.wavelength)
        self.broadcast_new_data()

    def submit_index(self, new_index_number):
        logging.debug("SETTING NEW INDEX: [...]")
        self.index_number = new_index_number
        self.update_analysis(index_number=self.index_number)
        self.broadcast_new_data()

    def submit_is_masked(self, new_is_masked):
        logging.debug("USING WHOLE IMAGE? " + str(new_is_masked))
        self.is_masked = new_is_masked
        self.broadcast_new_data()

    def submit_params(self):
        self.params = self.modules[PARAMETER].get_params()
        data_cube = self.get_result(self.current_rendered_result_path)[4]
        self._make_new_rec_analysis(self.current_rendered_result_path, data_cube, self.wavelength, self.mask,
                                    self.recreated_specs, self.params)
        self.broadcast_to_recreated_image()

    # ------------------------------------------------ BROADCASTERS --------------------------------------------------

    def broadcast_new_hypergui_folder_to_prediction(self):
        self.modules[PREDICTION].update_output_path()
        
    def broadcast_new_data(self):
        self.broadcast_to_prediction()
        self.broadcast_to_recreated_image()
        self.broadcast_to_new_image()
        self.broadcast_to_original_image()
        if not self.live:
            self.broadcast_to_histogram()
            self.broadcast_to_absorption_spec()
        else:
            self.reset_histogram()
            self.reset_absorption_spec()
    
    def reset_histogram(self):
        self.modules[HISTOGRAM].reset_histogram()
        
    def reset_absorption_spec(self):
        self.modules[ABSORPTION_SPEC].reset_absorption_spec()
        
    def broadcast_to_histogram(self):
        num = self.modules[HISTOGRAM].spec_number
        if num in [1, 2, 3, 4, 5, 6, 7, 8]:

            if self.is_masked:
                new_histogram_data = self.get_result(self.current_rendered_result_path)[0].histogram_data_masked
            else:
                new_histogram_data = self.get_result(self.current_rendered_result_path)[0].histogram_data
        elif num == 9:
            new_histogram_data = self.get_current_original_data()
        elif num == 10:
            new_histogram_data = self.get_current_norm_original_data()
        elif num == 11:
            new_histogram_data = self.get_current_rec_data()
        elif num == 12:
            new_histogram_data = self.get_current_norm_rec_data()
        elif num == 13:
            new_histogram_data = self.get_current_new_data()
        elif num == 14:
            new_histogram_data = self.get_current_norm_new_data()
        self.modules[HISTOGRAM].update_histogram(new_histogram_data)

    def broadcast_to_absorption_spec(self):
        if self.is_masked:
            new_absorption_spec = self.get_result(self.current_rendered_result_path)[1].absorption_roi_masked[:, 1]
        else:
            new_absorption_spec = self.get_result(self.current_rendered_result_path)[1].absorption_roi[:, 1]
        self.modules[ABSORPTION_SPEC].update_absorption_spec(new_absorption_spec)
        
    def broadcast_to_prediction(self): #JO
        self.modules[PREDICTION].update_cube()
        new_data = self.get_result(self.current_rendered_result_path)[3].get_rgb_og()
        self.modules[PREDICTION].update_RGB(new_data)
        
    def broadcast_to_prediction_2(self): #JO
        self.modules[PREDICTION2].update_cube(self.current_rendered_result_path)
        new_data = self.get_result(self.current_rendered_result_path)[3].get_rgb_og()
        self.modules[PREDICTION2].update_RGB(new_data)

    def broadcast_to_recreated_image(self):
        display_mode = self.modules[RECREATED_COLOUR].displayed_image_mode
        new_data = None
        if display_mode == STO2:
            new_data = self.get_result(self.current_rendered_result_path)[2].sto2
        elif display_mode == NIR:
            new_data = self.get_result(self.current_rendered_result_path)[2].nir
        elif display_mode == THI:
            new_data = self.get_result(self.current_rendered_result_path)[2].thi
        elif display_mode == TWI:
            new_data = self.get_result(self.current_rendered_result_path)[2].twi
        elif display_mode == TLI:
            new_data = self.get_result(self.current_rendered_result_path)[2].tli
        elif display_mode == OHI:
            new_data = self.get_result(self.current_rendered_result_path)[2].ohi
        self.modules[RECREATED_COLOUR].update_recreated_image(new_data)

    def broadcast_to_new_image(self):
        display_mode = self.modules[NEW_COLOUR].displayed_image_mode
        new_data = None
        if display_mode == WL:
            new_data = self.get_result(self.current_rendered_result_path)[3].get_wl_data()
        elif display_mode == IDX:
            new_data = self.get_result(self.current_rendered_result_path)[3].index
        self.modules[NEW_COLOUR].update_new_colour_image(new_data)

    def broadcast_to_original_image(self):
        # Use hist to get new images from the file as its the first in analysis list
        display_mode = self.modules[ORIGINAL_COLOUR].displayed_image_mode
        new_data = None
        if display_mode == RGB:
            logging.debug("GETTING RGB IMAGE")
            if not self.recr:
                new_data = self.get_result(self.current_rendered_result_path)[3].get_rgb_og(self.segm)
            else:
                new_data = self.get_result(self.current_rendered_result_path)[2].get_rgb()
        elif display_mode == STO2:
            logging.debug("GETTING STO2 IMAGE")
            if not self.recr:
                new_data = self.get_result(self.current_rendered_result_path)[3].get_sto2_og(self.segm)
            else:
                new_data = self.get_result(self.current_rendered_result_path)[2].get_sto2()
        elif display_mode == NIR:
            logging.debug("GETTING NIR IMAGE")
            if not self.recr:
                new_data = self.get_result(self.current_rendered_result_path)[3].get_nir_og(self.segm)
            else:
                new_data = self.get_result(self.current_rendered_result_path)[2].get_nir()
        elif display_mode == THI:
            logging.debug("GETTING THI IMAGE")
            if not self.recr:
                new_data = self.get_result(self.current_rendered_result_path)[3].get_thi_og(self.segm)
            else:
                new_data = self.get_result(self.current_rendered_result_path)[2].get_thi()
        elif display_mode == TLI:
            logging.debug("GETTING TLI IMAGE")
            if not self.recr:
                new_data = self.get_result(self.current_rendered_result_path)[3].get_tli_og(self.segm)
            else:
                new_data = self.get_result(self.current_rendered_result_path)[2].get_tli()
        elif display_mode == TWI:
            logging.debug("GETTING TWI IMAGE")
            if not self.recr:
                new_data = self.get_result(self.current_rendered_result_path)[3].get_twi_og(self.segm)
            else:
                new_data = self.get_result(self.current_rendered_result_path)[2].get_twi()
        elif display_mode == OHI:
            logging.debug("GETTING OHI IMAGE")
            if not self.recr:
                new_data = self.get_result(self.current_rendered_result_path)[3].get_ohi_og(self.segm)
            else:
                new_data = self.get_result(self.current_rendered_result_path)[2].get_ohi()
        self.modules[ORIGINAL_COLOUR].update_original_image(new_data)

    # ----------------------------------------------- MODULE UPDATERS ------------------------------------------------

    def update_analysis(self, mask=None, wavelength=None, index_number=None):
        for path, result_list in self.results.items():  # for each of the cubes
            if mask is not None:
                logging.debug("UPDATING MASK")
                for i in range(4):
                    result_list[i].update_mask(mask)
            if wavelength is not None:
                logging.debug("UPDATING WAVELENGTH TO: " + str(wavelength))
                for i in range(4):
                    result_list[i].update_wavelength(wavelength)
            if index_number is not None:
                logging.debug("UPDATING INDEX TO: " + str(index_number))
                result_list[3].update_index(index_number)

    def update_histogram_specs(self, spec_tup):
        path = self.current_rendered_result_path
        self.histogram_specs = spec_tup
        data_cube = self.get_result(self.current_rendered_result_path)[4]
        self._make_new_hist_analysis(path, data_cube, self.wavelength, self.mask, self.histogram_specs)
        self.broadcast_to_histogram()

    def update_abs_specs(self, spec_tup):
        path = self.current_rendered_result_path
        self.ab_spec_specs = spec_tup
        data_cube = self.get_result(self.current_rendered_result_path)[4]
        self._make_new_abs_analysis(path, data_cube, self.wavelength, self.mask, self.ab_spec_specs)
        self.broadcast_to_absorption_spec()

    def update_recreated_specs(self):
        path = self.current_rendered_result_path
        data_cube = self.get_result(self.current_rendered_result_path)[4]
        self._make_new_rec_analysis(path, data_cube, self.wavelength, self.mask, self.params)
        self.broadcast_to_recreated_image()

    def update_new_specs(self):
        path = self.current_rendered_result_path
        data_cube = self.get_result(self.current_rendered_result_path)[4]
        self._make_new_new_analysis(path, data_cube, self.wavelength, self.index_number, self.mask)
        self.broadcast_to_new_image()
        
    def update_segm(self, boole):
        self.segm = boole
    
    def update_recr(self, boole):
        self.recr = boole
        
    # -------------------------------------------- CREATE MODULE OBJECTS ---------------------------------------------

    # Use the path of the data cube as an identifier

    def _make_new_hist_analysis(self, path, data_cube, wavelength, mask, spec_tup):
        self.results[path][0] = HistogramAnalysis(path, data_cube, wavelength, spec_tup, ModuleListener(), mask)

    def _make_new_abs_analysis(self, path, data_cube, wavelength, mask, spec_tup):
        self.results[path][1] = AbsSpecAnalysis(path, data_cube, wavelength, spec_tup, ModuleListener(), mask)

    def _make_new_rec_analysis(self, path, data_cube, wavelength, mask, params):
        self.results[path][2] = RecreatedAnalysis(path, data_cube, wavelength, params, ModuleListener(), mask)

    def _make_new_new_analysis(self, path, data_cube, wavelength, index, mask):
        self.results[path][3] = NewAnalysis(path, data_cube, wavelength, index, ModuleListener(), mask)

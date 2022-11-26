import AnalysisModules
import importlib
import AnalysisModules.Indices.index_1
import AnalysisModules.Indices.index_2
import AnalysisModules.Indices.index_3
import AnalysisModules.Indices.index_4
import AnalysisModules.Indices.index_5
import AnalysisModules.Indices.index_6
import AnalysisModules.Indices.index_7
import AnalysisModules.Indices.index_8
import AnalysisModules.Indices.index_9
import AnalysisModules.Indices.index_10
import AnalysisModules.Indices.index_11
import AnalysisModules.Indices.index_12
import AnalysisModules.Indices.index_13
import AnalysisModules.Indices.index_14
import AnalysisModules.Indices.index_15
import AnalysisModules.Indices.index_16


class Index:
    def __init__(self, index_no, x_abs_or_ref, listener, wavelength=None):
        self.listener = listener

        self.index_no = index_no
        self.x_abs_or_ref = x_abs_or_ref
        assert index_no in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.wavelength = wavelength

        self.index = None

        self._calc_index()

    def get_index(self):
        return self.index

    """
    NOTE REGARDING INDICES
    In the original implementation, the index gradient calculation assumed there being 3 axis,
        and that wavelength is not yet bounded.
    That assumption was false, 
        as the index used to calculate the index gradient was ALREADY based on a subset of wavelengths.
    If you look at the implementation of the existant indices, 
        they are an average of a subset of the wavelengths.
    HOWEVER, that subset has nothing to do with the input wavelength, which is very odd.
    """
    
    def _calc_index(self):
        importlib.reload(AnalysisModules)
        importlib.reload(AnalysisModules.Indices.index_1)
        importlib.reload(AnalysisModules.Indices.index_2)
        importlib.reload(AnalysisModules.Indices.index_3)
        importlib.reload(AnalysisModules.Indices.index_4)
        importlib.reload(AnalysisModules.Indices.index_5)
        importlib.reload(AnalysisModules.Indices.index_6)
        importlib.reload(AnalysisModules.Indices.index_7)
        importlib.reload(AnalysisModules.Indices.index_8)
        importlib.reload(AnalysisModules.Indices.index_9)
        importlib.reload(AnalysisModules.Indices.index_10)
        importlib.reload(AnalysisModules.Indices.index_11)
        importlib.reload(AnalysisModules.Indices.index_12)
        importlib.reload(AnalysisModules.Indices.index_13)
        importlib.reload(AnalysisModules.Indices.index_14)
        importlib.reload(AnalysisModules.Indices.index_15)
        importlib.reload(AnalysisModules.Indices.index_16)
        from AnalysisModules.Indices.index_1 import get_index_1
        from AnalysisModules.Indices.index_2 import get_index_2
        from AnalysisModules.Indices.index_3 import get_index_3
        from AnalysisModules.Indices.index_4 import get_index_4
        from AnalysisModules.Indices.index_5 import get_index_5
        from AnalysisModules.Indices.index_6 import get_index_6
        from AnalysisModules.Indices.index_7 import get_index_7
        from AnalysisModules.Indices.index_8 import get_index_8
        from AnalysisModules.Indices.index_9 import get_index_9
        from AnalysisModules.Indices.index_10 import get_index_10
        from AnalysisModules.Indices.index_11 import get_index_11
        from AnalysisModules.Indices.index_12 import get_index_12
        from AnalysisModules.Indices.index_13 import get_index_13
        from AnalysisModules.Indices.index_14 import get_index_14
        from AnalysisModules.Indices.index_15 import get_index_15
        from AnalysisModules.Indices.index_16 import get_index_16
        if self.index_no == 1:
            self.index = get_index_1(self.x_abs_or_ref)
        elif self.index_no == 2:
            self.index = get_index_2(self.x_abs_or_ref)
        elif self.index_no == 3:
            self.index = get_index_3(self.x_abs_or_ref)
        elif self.index_no == 4:
            self.index = get_index_4(self.x_abs_or_ref)
        elif self.index_no == 5:
            self.index = get_index_5(self.x_abs_or_ref)
        elif self.index_no == 6:
            self.index = get_index_6(self.x_abs_or_ref)
        elif self.index_no == 7:
            self.index = get_index_7(self.x_abs_or_ref)
        elif self.index_no == 8:
            self.index = get_index_8(self.x_abs_or_ref)
        elif self.index_no == 9:
            self.index = get_index_9(self.x_abs_or_ref)
        elif self.index_no == 10:
            self.index = get_index_10(self.x_abs_or_ref, self.listener)
        elif self.index_no == 11:
            self.index = get_index_11(self.x_abs_or_ref)
        elif self.index_no == 12:
            self.index = get_index_12(self.x_abs_or_ref)
        elif self.index_no == 13:
            self.index = get_index_13(self.x_abs_or_ref, self.listener)
        elif self.index_no == 14:
            self.index = get_index_14(self.x_abs_or_ref, self.listener)
        elif self.index_no == 15:
            self.index = get_index_15(self.x_abs_or_ref, self.listener)
        elif self.index_no == 16:
            self.index = get_index_16(self.x_abs_or_ref)

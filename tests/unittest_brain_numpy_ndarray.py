# Copyright (c) 2017-2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the LGPL: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
# For details: https://github.com/PyCQA/astroid/blob/main/LICENSE
import unittest

try:
    import numpy  # pylint: disable=unused-import

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from astroid import builder


@unittest.skipUnless(HAS_NUMPY, "This test requires the numpy library.")
class NumpyBrainNdarrayTest(unittest.TestCase):
    """
    Test that calls to numpy functions returning arrays are correctly inferred
    """

    ndarray_returning_ndarray_methods = (
        "__abs__",
        "__add__",
        "__and__",
        "__array__",
        "__array_wrap__",
        "__copy__",
        "__deepcopy__",
        "__eq__",
        "__floordiv__",
        "__ge__",
        "__gt__",
        "__iadd__",
        "__iand__",
        "__ifloordiv__",
        "__ilshift__",
        "__imod__",
        "__imul__",
        "__invert__",
        "__ior__",
        "__ipow__",
        "__irshift__",
        "__isub__",
        "__itruediv__",
        "__ixor__",
        "__le__",
        "__lshift__",
        "__lt__",
        "__matmul__",
        "__mod__",
        "__mul__",
        "__ne__",
        "__neg__",
        "__or__",
        "__pos__",
        "__pow__",
        "__rshift__",
        "__sub__",
        "__truediv__",
        "__xor__",
        "all",
        "any",
        "argmax",
        "argmin",
        "argpartition",
        "argsort",
        "astype",
        "byteswap",
        "choose",
        "clip",
        "compress",
        "conj",
        "conjugate",
        "copy",
        "cumprod",
        "cumsum",
        "diagonal",
        "dot",
        "flatten",
        "getfield",
        "max",
        "mean",
        "min",
        "newbyteorder",
        "prod",
        "ptp",
        "ravel",
        "repeat",
        "reshape",
        "round",
        "searchsorted",
        "squeeze",
        "std",
        "sum",
        "swapaxes",
        "take",
        "trace",
        "transpose",
        "var",
        "view",
    )

    def _inferred_ndarray_method_call(self, func_name):
        node = builder.extract_node(
            f"""
        import numpy as np
        test_array = np.ndarray((2, 2))
        test_array.{func_name:s}()
        """
        )
        return node.infer()

    def _inferred_ndarray_attribute(self, attr_name):
        node = builder.extract_node(
            f"""
        import numpy as np
        test_array = np.ndarray((2, 2))
        test_array.{attr_name:s}
        """
        )
        return node.infer()

    def test_numpy_function_calls_inferred_as_ndarray(self):
        """
        Test that some calls to numpy functions are inferred as numpy.ndarray
        """
        licit_array_types = ".ndarray"
        for func_ in self.ndarray_returning_ndarray_methods:
            with self.subTest(typ=func_):
                inferred_values = list(self._inferred_ndarray_method_call(func_))
                self.assertTrue(
                    len(inferred_values) == 1,
                    msg=f"Too much inferred value for {func_:s}",
                )
                self.assertTrue(
                    inferred_values[-1].pytype() in licit_array_types,
                    msg=f"Illicit type for {func_:s} ({inferred_values[-1].pytype()})",
                )

    def test_numpy_ndarray_attribute_inferred_as_ndarray(self):
        """
        Test that some numpy ndarray attributes are inferred as numpy.ndarray
        """
        licit_array_types = ".ndarray"
        for attr_ in ("real", "imag", "shape", "T"):
            with self.subTest(typ=attr_):
                inferred_values = list(self._inferred_ndarray_attribute(attr_))
                self.assertTrue(
                    len(inferred_values) == 1,
                    msg=f"Too much inferred value for {attr_:s}",
                )
                self.assertTrue(
                    inferred_values[-1].pytype() in licit_array_types,
                    msg=f"Illicit type for {attr_:s} ({inferred_values[-1].pytype()})",
                )


if __name__ == "__main__":
    unittest.main()

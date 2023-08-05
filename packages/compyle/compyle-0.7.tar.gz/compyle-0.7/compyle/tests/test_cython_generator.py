"""Test code for Cython code generation.
"""
import unittest
from textwrap import dedent
from math import pi, sin
import sys


from ..config import get_config, set_config, use_config
from ..types import declare, KnownType, annotate
from ..cython_generator import (CythonGenerator, CythonClassHelper,
                                all_numeric, get_parallel_range)


class BasicEq:
    def __init__(self, hidden=None, rho=0.0, c=0.0):
        self.rho = rho
        self.c = c
        self._hidden = ['a', 'b']


class EqWithMethod(BasicEq):
    def func(self, d_idx=0, d_x=[0.0, 0.0]):
        tmp = abs(self.rho*self.c)*sin(pi*self.c)
        d_x[d_idx] = d_x[d_idx]*tmp


class EqWithReturn(BasicEq):
    def func(self, d_idx=0, d_x=[0.0, 0.0]):
        return d_x[d_idx]


class EqWithKnownTypes:
    def some_func(self, d_idx, d_p, WIJ, DWIJ, user, d_user, s_user):
        d_p[d_idx] = WIJ*DWIJ[0]


class EqWithMatrix:
    def func(self, d_idx, d_x=[0.0, 0.0]):
        mat = declare('matrix((2,2))')
        mat[0][0] = d_x[d_idx]
        vec, vec1 = declare('matrix(3, "float")', 2)
        vec[0] = d_x[d_idx]


class EqWithDeclare:
    def func(self, d_idx, d_x=[0.0, 0.0]):
        val, val1 = declare('float', 2)
        # val1 = declare('double')
        val = d_x[d_idx]
        index = declare('unsigned int')
        index = d_idx


def func_with_return(d_idx, d_x, x=0.0):
    x += 1
    return d_x[d_idx] + x


def simple_func(d_idx, d_x, x=0.0):
    d_x[d_idx] += x


@annotate(i='int', y='floatp', return_='float')
def annotated_f(i, y=[0.0]):
    x = declare('LOCAL_MEM matrix(64, "unsigned int")')
    return y[i]


class TestBase(unittest.TestCase):
    def assert_code_equal(self, result, expect):
        expect = expect.strip()
        result = result.strip()
        msg = 'EXPECTED:\n%s\nGOT:\n%s' % (expect, result)
        self.assertEqual(expect, result, msg)


class TestMiscUtils(TestBase):

    def test_all_numeric(self):
        x = [1, 2, 3.0]
        self.assertTrue(all_numeric(x))
        try:
            x = [0.0, 1, long(3)]
        except NameError:
            x = [0.0, 1, 3]
        self.assertTrue(all_numeric(x))
        x = [0.0, 1.0, '']
        self.assertFalse(all_numeric(x))

    def test_detect_type(self):
        cases = [
            (('d_something', None), 'double*'),
            (('s_something', None), 'double*'),
            (('d_idx', 0), 'long'),
            (('x', 1), 'long'),
            (('s', 'asdas'), 'str'),
            (('junk', 1.0), 'double'),
            (('y', [0.0, 1]), 'double*'),
            (('y', [0, 1, 0]), 'double*'),
            (('y', None), 'object'),
        ]
        cg = CythonGenerator()
        for args, expect in cases:
            msg = 'detect_type(*%r) != %r' % (args, expect)
            self.assertEqual(cg.detect_type(*args), expect, msg)

    def test_cython_class_helper(self):
        code = ('def f(self, x):',
                '        x += 1\n        return x+1')
        c = CythonClassHelper(name='A', public_vars={'x': 'double'},
                              methods=[code])
        expect = dedent("""
        cdef class A:
            cdef public double x
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            def f(self, x):
                x += 1
                return x+1
        """)
        self.assert_code_equal(c.generate().strip(), expect.strip())

    def test_get_parallel_range_without_openmp(self):
        with use_config(use_openmp=False):
            # Given/When
            res = get_parallel_range('NP')
            # Then
            self.assertEqual(res, 'range(0, NP, 1)')

            # Given/When
            res = get_parallel_range('START', 'NP')
            # Then
            self.assertEqual(res, 'range(START, NP, 1)')

            # Given/When
            res = get_parallel_range('NP', step=2)
            # Then
            self.assertEqual(res, 'range(0, NP, 2)')

            # Given/When
            res = get_parallel_range(1, 'NP+1', 2)
            # Then
            self.assertEqual(res, 'range(1, NP+1, 2)')

    def test_get_parallel_range_with_openmp(self):
        with use_config(use_openmp=True):
            cfg = get_config()
            sched, chunk = cfg.omp_schedule
            # Given/When
            res = get_parallel_range('NP')
            # Then
            expect = "prange(0, NP, 1, schedule='{}', chunksize={})".format(
                sched, chunk
            )
            self.assertEqual(res, expect)

            # Given/When
            res = get_parallel_range('START', 'NP', 2)
            # Then
            expect = (
                "prange(START, NP, 2, schedule='{}', chunksize={})".format(
                    sched, chunk
                )
            )
            self.assertEqual(res, expect)

            # Given/When
            res = get_parallel_range('NP', nogil=True)
            # Then
            expect = (
                "prange(0, NP, 1, schedule='{}', chunksize={}, "
                "nogil=True)".format(
                    sched, chunk
                )
            )
            self.assertEqual(res, expect)

            # Given/When
            res = get_parallel_range('NP', nogil=True, num_threads=4)
            # Then
            expect = (
                "prange(0, NP, 1, schedule='{}', chunksize={}, "
                "nogil=True, num_threads=4)".format(
                    sched, chunk
                )
            )
            self.assertEqual(res, expect)

        with use_config(use_openmp=True, omp_schedule=('static', 32)):
            # Given/When
            res = get_parallel_range('NP')
            # Then
            expect = "prange(0, NP, 1, schedule='{}', chunksize={})".format(
                'static', 32
            )
            self.assertEqual(res, expect)


class TestCythonCodeGenerator(TestBase):
    def setUp(self):
        get_config().use_openmp = False

    def tearDown(self):
        set_config(None)

    def test_simple_constructor(self):
        cg = CythonGenerator()
        cg.parse(BasicEq())
        expect = dedent("""
        cdef class BasicEq:
            cdef public list _hidden
            cdef public double c
            cdef public double rho
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_func_signature(self):
        # Given
        def f(x=1, y=[1.0]):
            pass

        cg = CythonGenerator()
        # When
        py_data, c_data = cg.get_func_signature(f)

        # Then
        self.assertEqual(py_data[0], ['long x', 'double[:] y'])
        self.assertEqual(py_data[1], ['x', '&y[0]'])
        self.assertEqual(c_data[0], ['long x', 'double* y'])
        self.assertEqual(c_data[1], ['x', 'y'])

    def test_function_with_annotation(self):
        # Given
        cg = CythonGenerator()
        # When
        cg.parse(annotated_f)

        # Then
        expect = dedent('''
        cdef inline float annotated_f(int i, float* y):
            cdef unsigned int x[64]
            return y[i]
        ''')
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    @unittest.skipIf(sys.version_info < (3, 4), reason='Requires Python3.')
    def test_python3_annotation(self):
        # Given
        from .py3_code import py3_f
        cg = CythonGenerator()

        # When
        cg.parse(py3_f)
        expect = dedent('''
        cdef inline int py3_f(int x):
            cdef int y
            y = x + 1
            return x*y
        ''')
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_simple_method(self):
        cg = CythonGenerator()
        cg.parse(EqWithMethod())
        expect = dedent("""
        cdef class EqWithMethod:
            cdef public list _hidden
            cdef public double c
            cdef public double rho
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            cdef inline void func(self, long d_idx, double* d_x):
                cdef double tmp
                tmp = abs(self.rho*self.c)*sin(pi*self.c)
                d_x[d_idx] = d_x[d_idx]*tmp
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_honors_use_openmp_setting(self):
        # When
        get_config().use_openmp = True
        # Then
        cg = CythonGenerator()
        cg.parse(EqWithMethod())
        expect = dedent("""
        cdef class EqWithMethod:
            cdef public list _hidden
            cdef public double c
            cdef public double rho
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            cdef inline void func(self, long d_idx, double* d_x) nogil:
                cdef double tmp
                tmp = abs(self.rho*self.c)*sin(pi*self.c)
                d_x[d_idx] = d_x[d_idx]*tmp
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_python_methods(self):
        cg = CythonGenerator(python_methods=True)
        cg.parse(EqWithMethod())
        expect = dedent("""
        cdef class EqWithMethod:
            cdef public list _hidden
            cdef public double c
            cdef public double rho
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            cdef inline void func(self, long d_idx, double* d_x):
                cdef double tmp
                tmp = abs(self.rho*self.c)*sin(pi*self.c)
                d_x[d_idx] = d_x[d_idx]*tmp

            cpdef py_func(self, long d_idx, double[:] d_x):
                self.func(d_idx, &d_x[0])
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

        cg.parse(EqWithReturn())
        expect = dedent("""
        cdef class EqWithReturn:
            cdef public list _hidden
            cdef public double c
            cdef public double rho
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            cdef inline double func(self, long d_idx, double* d_x):
                return d_x[d_idx]

            cpdef double py_func(self, long d_idx, double[:] d_x):
                return self.func(d_idx, &d_x[0])
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

        cg.parse(func_with_return)
        expect = dedent("""
        cdef inline double func_with_return(long d_idx, double* d_x, double x):
            x += 1
            return d_x[d_idx] + x

        cpdef double py_func_with_return(long d_idx, double[:] d_x, double x):
            return func_with_return(d_idx, &d_x[0], x)
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_method_with_return(self):
        cg = CythonGenerator()
        cg.parse(EqWithReturn())
        expect = dedent("""
        cdef class EqWithReturn:
            cdef public list _hidden
            cdef public double c
            cdef public double rho
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            cdef inline double func(self, long d_idx, double* d_x):
                return d_x[d_idx]
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_method_with_matrix(self):
        cg = CythonGenerator()
        cg.parse(EqWithMatrix())
        expect = dedent("""
        cdef class EqWithMatrix:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            cdef inline void func(self, long d_idx, double* d_x):
                cdef double mat[2][2]
                mat[0][0] = d_x[d_idx]
                cdef float vec[3], vec1[3]
                vec[0] = d_x[d_idx]
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_method_with_declare(self):
        cg = CythonGenerator()
        cg.parse(EqWithDeclare())
        expect = dedent("""
        cdef class EqWithDeclare:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            cdef inline void func(self, long d_idx, double* d_x):
                cdef float val, val1
                # val1 = declare('double')
                val = d_x[d_idx]
                cdef unsigned int index
                index = d_idx
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_method_with_known_types(self):  # noqa
        cg = CythonGenerator(
            known_types={'WIJ': 0.0, 'DWIJ': [0.0, 0.0, 0.0],
                         'user': KnownType('ndarray'),
                         'd_user': KnownType('long*'),
                         's_user': KnownType('int*')}
        )
        cg.parse(EqWithKnownTypes())
        expect = dedent("""
        cdef class EqWithKnownTypes:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            cdef inline void some_func(self, long d_idx, double* d_p, double WIJ, double* DWIJ, ndarray user, long* d_user, int* s_user):
                d_p[d_idx] = WIJ*DWIJ[0]
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

    def test_wrap_function(self):
        cg = CythonGenerator()
        cg.parse(func_with_return)
        expect = dedent("""
        cdef inline double func_with_return(long d_idx, double* d_x, double x):
            x += 1
            return d_x[d_idx] + x
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())

        cg.parse(simple_func)
        expect = dedent("""
        cdef inline void simple_func(long d_idx, double* d_x, double x):
            d_x[d_idx] += x
        """)
        self.assert_code_equal(cg.get_code().strip(), expect.strip())


if __name__ == '__main__':
    unittest.main()

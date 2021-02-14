# coding: utf-8
#------------------------------------------------------------------------------------------#
# This file is part of Pyccel which is released under MIT License. See the LICENSE file or #
# go to https://github.com/pyccel/pyccel/blob/master/LICENSE for full license details.     #
#------------------------------------------------------------------------------------------#

"""
This module provides us with functions and objects that allow us to compute
the arithmetic complexity a of a program.

Example
-------

"""

from collections import OrderedDict

from sympy import count_ops as sympy_count_ops
from sympy import Tuple
from sympy import summation
from sympy import Symbol
from sympy import Function

from pyccel.ast.literals import Literal
from pyccel.ast.core     import For, Assign, AugAssign, CodeBlock, Comment, EmptyNode
from pyccel.ast.core     import Allocate, Deallocate
from pyccel.ast.core     import FunctionDef, FunctionCall
from pyccel.ast.core     import Return
from pyccel.ast.core     import AddOp, SubOp, MulOp, DivOp
from pyccel.ast.numpyext import NumpyUfuncBase
from pyccel.ast.numpyext import ( NumpySin, NumpyCos, NumpyTan, NumpyArcsin,
                                  NumpyArccos, NumpyArctan, NumpyArctan2, NumpySinh, NumpyCosh, NumpyTanh,
                                  NumpyArcsinh, NumpyArccosh, NumpyArctanh )
from pyccel.ast.numpyext import ( NumpyMax, NumpyMin, NumpyFloor, NumpyAbs, NumpyFabs, NumpyExp, NumpyLog,
                                  NumpySqrt )

from pyccel.ast.internals import PyccelArraySize, Slice
from pyccel.ast.operators import PyccelAdd, PyccelMinus, PyccelDiv, PyccelMul, PyccelFloorDiv
from pyccel.ast.variable  import IndexedElement, Variable
from pyccel.ast.numpyext  import NumpyZeros, NumpyOnes
from pyccel.ast.operators import PyccelOperator, PyccelAssociativeParenthesis
from pyccel.ast.builtins  import PythonAbs
from pyccel.ast.sympy_helper import pyccel_to_sympy
from pyccel.complexity.basic import Complexity

__all__ = ["count_ops", "OpComplexity"]

ADD = Symbol('ADD')
SUB = Symbol('SUB')
MUL = Symbol('MUL')
DIV = Symbol('DIV')
IDIV = Symbol('IDIV')
ABS = Symbol('ABS')

op_registry = {
    AddOp(): ADD,
    SubOp(): SUB,
    MulOp(): MUL,
    DivOp(): DIV,
#    ModOp: MOD,
    }

SHAPE = Function('shape')

# ...
numpy_functions_registery = {
    #
    NumpySin:      'sin',
    NumpyCos:      'cos',
    NumpyTan:      'tan',
    NumpyArcsin:   'arcsin',
    NumpyArccos:   'arccos',
    NumpyArctan:   'arctan',
    NumpyArctan2:  'arctan2',
    NumpySinh:     'sinh',
    NumpyCosh:     'cosh',
    NumpyTanh:     'tanh',
    NumpyArcsinh:  'arcsinh',
    NumpyArccosh:  'arccosh',
    NumpyArctanh:  'arctanh',
    #
    NumpyMax:      'max',
    NumpyMin:      'min',
    #
    NumpyFloor:    'floor',
    NumpyAbs:      'abs',
    NumpyFabs:     'fabs',
    NumpyExp:      'exp',
    NumpyLog:      'log',
    NumpySqrt:     'sqrt',
}

# ...
# ==============================================================================
class OpComplexity(Complexity):
    """class for Operation complexity computation."""

    def cost(self, mode=None):
        """
        Computes the complexity of the given code.

        verbose: bool
            talk more

        mode: string
            possible values are (None, simple)
        """
        costs = OrderedDict()

        # ... first we treat declared functions
        if self.functions:
            for fname, d in self.functions.items():
                expr = count_ops(d, visual=True, costs=costs)

                if not(expr == 0) and (mode == 'simple'):
                    for i in ['ADD', 'SUB', 'DIV', 'MUL']:
                        expr = expr.subs(Symbol(i), 1)

                costs[fname] = expr
        # ...
#        print('*** ', costs)

        # ... then we compute the complexity for the main program
        expr = count_ops(self.ast, visual=True, costs=costs)

        if not(expr == 0) and (mode == 'simple'):
            for i in ['ADD', 'SUB', 'DIV', 'MUL']:
                expr = expr.subs(Symbol(i), 1)
        # ...

        # TODO use setter here
        self._costs = costs

        return expr

# ==============================================================================
# TODO move inside OpComplexity following the visiter algorithm
def count_ops(expr, visual=None, costs=None):

#    print('>>> ', expr)

    symbol_map = {}
    used_names = set()

    if isinstance(expr, Assign):
        if isinstance(expr.rhs, (NumpyZeros, NumpyOnes, Comment, EmptyNode)):
            return 0

        # ...
        op = 0
        if isinstance(expr, AugAssign):
            op = op_registry[expr.op]
        # ...

        # ...
        ntimes = 1
        if isinstance(expr.lhs, IndexedElement):
            indices = [(e,i) for e,i in enumerate(expr.lhs.indices) if isinstance(i, Slice)]
            for e,i in indices:
                # ...
                start = 0
                if not i.start == None:
                    start = i.start.python_value
                # ...

                # ...
                stop = SHAPE(expr.lhs.base, e)
                if not i.stop == None:
                    stop = i.stop.python_value
                # ...

                # ...
                step = 1
                if not i.step == None:
                    step = i.step.python_value
                # ...

                if not(step == 1):
                    raise NotImplementedError('only step == 1 is treated')

                # TODO uncomment this
                #      this was commented because we get floor(...)
                ntimes *= (stop - start) #// step
        # ...

        return ntimes * ( op + count_ops(expr.rhs, visual, costs=costs) )

    elif isinstance(expr, For):
        ops = sum(count_ops(i, visual, costs=costs) for i in expr.body.body)

        i = expr.target
        b = expr.iterable.start
        e = expr.iterable.stop
        i = pyccel_to_sympy(i, symbol_map, used_names)
        b = pyccel_to_sympy(b, symbol_map, used_names)
        e = pyccel_to_sympy(e, symbol_map, used_names)
        # TODO treat the case step /= 1
        return summation(ops, (i, b, e-1))

    elif isinstance(expr, (Tuple, tuple, list)):
        return sum(count_ops(i, visual, costs=costs) for i in expr)

    elif isinstance(expr, FunctionDef):
        return count_ops(expr.body, visual, costs=costs)

    elif isinstance(expr, FunctionCall):
        if costs is None:
            raise ValueError('costs dict is None')

        fname = expr.func_name

        if not fname in costs.keys():
            raise ValueError('Cannot find the cost of the function {}'.format(fname))

        return costs[fname]

    elif isinstance(expr, CodeBlock):
        return sum(count_ops(i, visual, costs=costs) for i in expr.body)

    elif isinstance(expr, (NumpyZeros, NumpyOnes, Comment, EmptyNode, Allocate, Deallocate)):
        return 0

    elif isinstance(expr, PyccelArraySize):
        return 0

    elif isinstance(expr, (Tuple, list)):
        return sum(count_ops(i, visual) for i in expr)

    elif isinstance(expr, Literal):
        return 0

    elif isinstance(expr, Variable):
        return 0

    elif isinstance(expr, IndexedElement):
        return 0

    elif expr is None:
        return 0

    elif isinstance(expr, Return):
        return sum(count_ops(i, visual, costs=costs) for i in [expr.stmt, expr.expr])

    elif isinstance(expr, PyccelAdd):
        ops = sum(count_ops(i, visual, costs=costs) for i in expr.args)
        return ops+ADD

    elif isinstance(expr, PyccelMinus):
        ops = sum(count_ops(i, visual, costs=costs) for i in expr.args)
        return ops+SUB

    elif isinstance(expr, PyccelDiv):
        ops = sum(count_ops(i, visual, costs=costs) for i in expr.args)
        return ops+DIV

    elif isinstance(expr, PyccelFloorDiv):
        ops = sum(count_ops(i, visual, costs=costs) for i in expr.args)
        return ops+IDIV

    elif isinstance(expr, PyccelMul):
        ops = sum(count_ops(i, visual, costs=costs) for i in expr.args)
        return ops+MUL

    elif isinstance(expr, PythonAbs):
        ops = sum(count_ops(i, visual, costs=costs) for i in expr.args)
        return ops+ABS

    elif isinstance(expr, PyccelOperator):
        return sum(count_ops(i, visual, costs=costs) for i in expr.args)

    elif isinstance(expr, NumpyUfuncBase):
        try:
            f = numpy_functions_registery[type(expr)]
        except:
            raise NotImplementedError('TODO count_ops for {}'.format(type(expr)))

        return Symbol(f.upper()) + sum(count_ops(i, visual, costs=costs) for i in expr.args)

    else:
        raise NotImplementedError('TODO count_ops for {}'.format(type(expr)))

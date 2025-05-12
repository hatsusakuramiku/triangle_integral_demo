from latex2sympy2 import latex2sympy
import sympy

latex_expr = "1"
sympy_expr = latex2sympy(latex_expr)

x, y = sympy.sympify("x"), sympy.sympify("y")
f = sympy.lambdify((x, y), sympy_expr, modules=["numpy", "math"])

result = f(2, 3)
print(result)  # 输出 -1

"""
Módulo de lógica matemática para la calculadora de derivadas e integrales.
Proporciona funciones para el cálculo simbólico usando SymPy.
"""
import sympy as sp
import numpy as np
import re
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class MathHelper:
    """
    Clase para realizar operaciones matemáticas simbólicas y numéricas.
    """
    def __init__(self):
        """Inicializa las variables simbólicas disponibles."""
        # Crear símbolo principal
        self.x_symbol = sp.Symbol('x')
        
        # Diccionario para almacenar la función actual y sus derivadas/integrales
        self.current = {
            'function': None,
            'derivative': None,
            'integral': None,
            'order': 1,
            'critical_points': None
        }
        
        # Configuración del parser para manejar expresiones más complejas
        self.transformations = standard_transformations + (implicit_multiplication_application,)
    
    def parse_function(self, func_str):
        """
        Convierte una cadena de función en una forma que SymPy pueda interpretar.
        
        Args:
            func_str (str): Cadena de texto con la función matemática.
            
        Returns:
            str: Cadena de texto procesada para ser usada por SymPy.
        """
        # Reemplazar notación amigable con notación de SymPy
        func_str = func_str.replace("^", "**")
        
        # Reemplazar casos como 2x con 2*x
        func_str = re.sub(r'([0-9])([a-zA-Z])', r'\1*\2', func_str)
        func_str = re.sub(r'(\))([a-zA-Z])', r'\1*\2', func_str)
        
        # Reemplazar funciones trigonométricas
        replacements = {
            'sen': 'sin',
            'tg': 'tan',
            'arctg': 'atan',
            'arcsen': 'asin',
            'arccos': 'acos',
            'cotg': 'cot',
            'sec': 'sec',
            'cosec': 'csc',
            'ln': 'log'
        }
        
        for old, new in replacements.items():
            func_str = func_str.replace(old, new)
        
        return func_str
    
    def set_function(self, func_str):
        """
        Establece la función actual para operar.
        
        Args:
            func_str (str): Cadena de texto con la función matemática.
            
        Returns:
            bool: True si la función se estableció correctamente, False en caso contrario.
        """
        try:
            # Parsear la función
            parsed_func = self.parse_function(func_str)
            
            # Intentar convertir a expresión SymPy usando parse_expr para mayor robustez
            try:
                expr = parse_expr(parsed_func, transformations=self.transformations)
            except:
                # Si falla, intentar el método tradicional
                expr = sp.sympify(parsed_func)
            
            self.current['function'] = expr
            
            # Limpiar derivadas y puntos críticos previos
            self.current['derivative'] = None
            self.current['integral'] = None
            self.current['critical_points'] = None
            
            return True
        except Exception as e:
            print(f"Error al establecer la función: {str(e)}")
            return False
    
    def calculate_derivative(self, order=1):
        """
        Calcula la derivada de la función actual.
        
        Args:
            order (int): Orden de la derivada (1, 2, etc.).
            
        Returns:
            sympy.Expr: Expresión simbólica de la derivada.
        """
        if self.current['function'] is None:
            raise ValueError("No hay función establecida")
        
        self.current['order'] = order
        
        try:
            # Calcular la derivada
            self.current['derivative'] = sp.diff(self.current['function'], self.x_symbol, order)
            
            # Intentar simplificar la expresión
            self.current['derivative'] = sp.simplify(self.current['derivative'])
            
            return self.current['derivative']
        except Exception as e:
            print(f"Error al calcular la derivada: {str(e)}")
            raise
    
    def calculate_integral(self, definite=False, lower=None, upper=None):
        """
        Calcula la integral de la función actual.
        
        Args:
            definite (bool): Si es True, calcula la integral definida.
            lower (float, optional): Límite inferior para integral definida.
            upper (float, optional): Límite superior para integral definida.
            
        Returns:
            sympy.Expr: Expresión simbólica de la integral.
        """
        if self.current['function'] is None:
            raise ValueError("No hay función establecida")
        
        try:
            if definite and lower is not None and upper is not None:
                self.current['integral'] = sp.integrate(self.current['function'], (self.x_symbol, lower, upper))
            else:
                self.current['integral'] = sp.integrate(self.current['function'], self.x_symbol)
            
            return self.current['integral']
        except Exception as e:
            print(f"Error al calcular la integral: {str(e)}")
            raise
    
    def find_critical_points(self):
        """
        Encuentra los puntos críticos de la función.
        
        Returns:
            list: Lista de puntos críticos en formato (x, tipo)
        """
        if self.current['function'] is None:
            raise ValueError("No hay función establecida")
        
        if self.current['derivative'] is None:
            self.calculate_derivative()
        
        # Si ya hemos calculado los puntos críticos, devolverlos
        if self.current['critical_points'] is not None:
            return self.current['critical_points']
        
        try:
            # Calcular la primera derivada si no existe
            if self.current['derivative'] is None:
                self.calculate_derivative()
            
            # Calcular la segunda derivada para clasificar los puntos
            second_derivative = sp.diff(self.current['function'], self.x_symbol, 2)
            
            # Resolver f'(x) = 0
            solutions = sp.solve(self.current['derivative'], self.x_symbol)
            
            critical_points = []
            
            for solution in solutions:
                # Verificar que la solución es real
                if isinstance(solution, sp.Number) and solution.is_real:
                    x_val = float(solution)
                    
                    # Evaluar la segunda derivada en el punto crítico
                    try:
                        second_deriv_val = float(second_derivative.subs(self.x_symbol, solution))
                        
                        # Clasificar el punto crítico
                        if second_deriv_val > 0:
                            point_type = "Mínimo"
                        elif second_deriv_val < 0:
                            point_type = "Máximo"
                        else:
                            point_type = "Punto de inflexión"
                    except:
                        point_type = "Indeterminado"
                    
                    # Evaluar la función en el punto
                    try:
                        y_val = float(self.current['function'].subs(self.x_symbol, solution))
                    except:
                        y_val = None
                    
                    critical_points.append({
                        'x': x_val,
                        'y': y_val,
                        'type': point_type
                    })
            
            # Ordenar los puntos por valor de x
            critical_points.sort(key=lambda p: p['x'])
            
            self.current['critical_points'] = critical_points
            return critical_points
        
        except Exception as e:
            print(f"Error al encontrar puntos críticos: {str(e)}")
            # En caso de error, devolver lista vacía
            self.current['critical_points'] = []
            return []
    
    def format_expression(self, expr, use_latex=False):
        """
        Formatea una expresión simbólica para su visualización.
        
        Args:
            expr (sympy.Expr): Expresión simbólica a formatear.
            use_latex (bool): Si es True, devuelve la expresión en formato LaTeX.
            
        Returns:
            str: Expresión formateada para mostrar al usuario.
        """
        if use_latex:
            return sp.latex(expr)
        
        # Convertir a cadena más legible
        expr_str = str(expr)
        
        # Reemplazar operaciones para mejor visualización
        expr_str = expr_str.replace("**", "^")
        expr_str = expr_str.replace("*", "·")  # Usando el punto medio para multiplicación
        
        # Reemplazar funciones comunes
        replacements = {
            'sin': 'sen',
            'log': 'ln',
            'asin': 'arcsen',
            'atan': 'arctg',
            'acos': 'arccos'
        }
        
        for new, old in replacements.items():
            expr_str = expr_str.replace(new, old)
        
        return expr_str
    
    def get_suitable_range(self, x_min=-10, x_max=10):
        """
        Determina un rango adecuado para graficar la función.
        
        Args:
            x_min (float): Valor mínimo predeterminado.
            x_max (float): Valor máximo predeterminado.
            
        Returns:
            tuple: (x_min, x_max) rango ajustado para la gráfica.
        """
        if self.current['function'] is None:
            return (x_min, x_max)
        
        try:
            # Intentar encontrar puntos críticos si aún no se han calculado
            if self.current['critical_points'] is None:
                self.find_critical_points()
            
            if self.current['critical_points'] and len(self.current['critical_points']) > 0:
                # Obtener los valores x de los puntos críticos
                x_values = [p['x'] for p in self.current['critical_points']]
                
                # Añadir un margen al rango
                new_x_min = min(x_values) - 2
                new_x_max = max(x_values) + 2
                
                # Limitar el rango para evitar gráficos muy extensos
                x_min = max(new_x_min, -20)
                x_max = min(new_x_max, 20)
                
                # Asegurar que el rango no sea demasiado pequeño
                if x_max - x_min < 5:
                    center = (x_min + x_max) / 2
                    x_min = center - 2.5
                    x_max = center + 2.5
        except:
            # En caso de error, usar el rango predeterminado
            pass
        
        return (x_min, x_max)
    
    def create_lambda_functions(self):
        """
        Crea funciones lambda para evaluación numérica.
        
        Returns:
            dict: Diccionario con funciones lambda para f(x), f'(x) e integral.
        """
        if self.current['function'] is None:
            raise ValueError("No hay función establecida")
        
        # Inicializar el diccionario
        lambda_funcs = {}
        
        # Función original
        lambda_funcs['function'] = sp.lambdify(self.x_symbol, self.current['function'], modules=['numpy', 'sympy'])
        
        # Derivada
        if self.current['derivative'] is None:
            self.calculate_derivative()
        lambda_funcs['derivative'] = sp.lambdify(self.x_symbol, self.current['derivative'], modules=['numpy', 'sympy'])
        
        # Integral (si está disponible)
        if self.current['integral'] is not None:
            lambda_funcs['integral'] = sp.lambdify(self.x_symbol, self.current['integral'], modules=['numpy', 'sympy'])
        
        return lambda_funcs
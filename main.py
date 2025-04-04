#!/usr/bin/env python3
"""
Calculadora de Derivadas e Integrales

Esta aplicación permite calcular derivadas, integrales y visualizar
gráficamente funciones matemáticas utilizando una interfaz moderna
con soporte para temas claros y oscuros, animaciones y múltiples
funcionalidades avanzadas.

Autor: Ilya
Versión: 2.0
"""
import sys
import os
import numpy as np
import sympy as sp
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

# Importar módulos propios
from gui import MainWindow
from logic import MathHelper

class DerivativeCalculator:
    """Clase principal de la aplicación."""
    
    def __init__(self):
        """Inicializa la aplicación."""
        # Crear aplicación PyQt
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Calculadora de Derivadas")
        self.app.setOrganizationName("Ilya")
        
        # Mostrar splash screen
        splash_pix = QPixmap("resources/icons/splash.png")
        if not splash_pix.isNull():
            splash = QSplashScreen(splash_pix)
            splash.show()
            splash.showMessage("Cargando calculadora...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
            self.app.processEvents()
        
        # Crear instancia de la lógica matemática
        self.math_helper = MathHelper()
        
        # Crear ventana principal
        self.main_window = MainWindow()
        
        # Conectar lógica con interfaz
        self.connect_logic()
        
        # Mostrar ventana con un pequeño retardo
        QTimer.singleShot(500, lambda: self._show_main_window(splash if 'splash' in locals() else None))
    
    def _show_main_window(self, splash=None):
        """Muestra la ventana principal y oculta el splash screen."""
        self.main_window.show()
        if splash:
            splash.finish(self.main_window)
    
    def connect_logic(self):
        """Conecta la lógica matemática con la interfaz gráfica."""
        # Conectar señal de cálculo
        self.main_window.input_page.calculate_requested.connect(self.process_calculation)
    
    def process_calculation(self, input_data):
        """
        Procesa el cálculo solicitado.
        
        Args:
            input_data (dict): Diccionario con los parámetros de cálculo.
        """
        try:
            # Extraer datos
            func_str = input_data.get('function', '')
            order = input_data.get('order', 1)
            calc_integral = input_data.get('integral_definida', False)
            lower_limit = input_data.get('lower_limit', '')
            upper_limit = input_data.get('upper_limit', '')
            
            # Establecer función en el helper
            if not self.math_helper.set_function(func_str):
                raise ValueError(f"No se pudo analizar la función: {func_str}")
            
            # Calcular derivada
            derivative = self.math_helper.calculate_derivative(order)
            
            # Buscar puntos críticos
            critical_points = self.math_helper.find_critical_points()
            
            # Calcular integral si es necesario
            integral = None
            if calc_integral:
                try:
                    # Determinar si es integral definida o indefinida
                    if lower_limit and upper_limit:
                        try:
                            lower = float(lower_limit)
                            upper = float(upper_limit)
                            integral = self.math_helper.calculate_integral(True, lower, upper)
                        except ValueError:
                            # Si hay error en los límites, calcular la indefinida
                            integral = self.math_helper.calculate_integral(False)
                    else:
                        integral = self.math_helper.calculate_integral(False)
                except Exception as e:
                    print(f"Error al calcular integral: {str(e)}")
            
            # Preparar resultados para mostrar
            results = {}
            
            # Formatear función
            func_formatted = self.math_helper.format_expression(self.math_helper.current['function'])
            results['function'] = f"f(x) = {func_formatted}"
            
            # Formatear derivada
            derivative_formatted = self.math_helper.format_expression(derivative)
            if order == 1:
                results['derivative'] = f"f'(x) = {derivative_formatted}"
            else:
                results['derivative'] = f"f^({order})(x) = {derivative_formatted}"
            
            # Incluir puntos críticos
            results['critical_points'] = critical_points
            
            # Formatear integral si está disponible
            if integral is not None:
                integral_formatted = self.math_helper.format_expression(integral)
                
                if calc_integral and lower_limit and upper_limit:
                    try:
                        # Valor numérico de la integral definida
                        int_value = float(integral)
                        results['integral'] = (
                            f"∫({func_formatted})dx "
                            f"desde {lower_limit} hasta {upper_limit} = {round(int_value, 6)}"
                        )
                    except:
                        results['integral'] = (
                            f"∫({func_formatted})dx "
                            f"desde {lower_limit} hasta {upper_limit} = {integral_formatted}"
                        )
                else:
                    results['integral'] = f"∫({func_formatted})dx = {integral_formatted} + C"
            
            # Obtener rango adecuado para gráfica
            x_range = self.math_helper.get_suitable_range()
            
            # Crear funciones lambda para evaluación numérica
            lambda_funcs = self.math_helper.create_lambda_functions()
            
            # Mostrar resultados
            self.main_window.results_page.set_results(results, lambda_funcs, x_range)
            self.main_window.show_results_page()
            
            # Añadir al historial
            self.main_window.input_page.add_to_history(input_data)
            
        except Exception as e:
            # Mostrar error
            QMessageBox.critical(
                self.main_window,
                "Error en el cálculo",
                f"Se produjo un error al procesar la función:\n{str(e)}"
            )
    
    def run(self):
        """Ejecuta la aplicación."""
        sys.exit(self.app.exec_())


def main():
    """Función principal."""
    # Iniciar aplicación
    calculator = DerivativeCalculator()
    calculator.run()


if __name__ == "__main__":
    main()
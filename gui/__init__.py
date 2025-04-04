"""
Paquete de interfaz gráfica para la calculadora de derivadas.
"""
from .main_window import MainWindow
from .canvas import MathPlotCanvas
from .themes import Themes
from .widgets import FunctionInputWidget, ResultWidget, HistoryWidget, AnimatedWidget

__all__ = [
    'MainWindow',
    'MathPlotCanvas',
    'Themes',
    'FunctionInputWidget',
    'ResultWidget',
    'HistoryWidget',
    'AnimatedWidget'
]
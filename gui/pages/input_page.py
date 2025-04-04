"""
Página de entrada para la calculadora de derivadas.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from ..widgets import FunctionInputWidget, HistoryWidget

class InputPage(QWidget):
    """Página para entrada de funciones y visualización de historial."""
    
    # Señales
    calculate_requested = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        """Inicializa la página de entrada."""
        super(InputPage, self).__init__(parent)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("Calculadora de Derivadas de Ilya - Versión Mejorada")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("titleLabel")
        title_label.setMinimumHeight(50)
        
        # Añadir título
        main_layout.addWidget(title_label)
        
        # Crear splitter para dividir la pantalla
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo: entrada de función
        self.function_input = FunctionInputWidget()
        
        # Panel derecho: historial
        self.history_widget = HistoryWidget()
        
        # Añadir widgets al splitter
        splitter.addWidget(self.function_input)
        splitter.addWidget(self.history_widget)
        
        # Establecer proporciones (60% entrada, 40% historial)
        splitter.setSizes([600, 400])
        
        # Añadir splitter al layout principal
        main_layout.addWidget(splitter)
        
        # Conectar señales
        self.function_input.calculate_clicked.connect(self._on_calculate_clicked)
        self.history_widget.history_selected.connect(self._on_history_selected)
    
    def _on_calculate_clicked(self):
        """Maneja el clic en el botón de calcular."""
        # Obtener los datos de entrada
        input_data = self.function_input.get_function_input()
        
        # Emitir señal con los datos
        self.calculate_requested.emit(input_data)
    
    def _on_history_selected(self, entry_data):
        """
        Maneja la selección de un elemento del historial.
        
        Args:
            entry_data (dict): Datos de la entrada seleccionada.
        """
        # Establecer los datos en el formulario
        self.function_input.set_function_input(entry_data)
    
    def add_to_history(self, entry_data):
        """
        Añade una entrada al historial.
        
        Args:
            entry_data (dict): Datos de la entrada para añadir.
        """
        self.history_widget.add_to_history(entry_data)
    
    def clear_inputs(self):
        """Limpia los campos de entrada."""
        empty_data = {
            'function': '',
            'order': 1,
            'integral_definida': False,
            'lower_limit': '',
            'upper_limit': ''
        }
        self.function_input.set_function_input(empty_data)
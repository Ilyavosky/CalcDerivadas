"""
Módulo con widgets personalizados para la interfaz de la calculadora.
"""
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
                           QSpinBox, QHBoxLayout, QVBoxLayout, QFormLayout,
                           QGroupBox, QListWidget, QListWidgetItem, QSplitter,
                           QFrame, QFileDialog, QMessageBox, QAction, QMenu,
                           QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette

class AnimatedWidget(QWidget):
    """Base para widgets con animaciones de aparición/desaparición."""
    
    def __init__(self, parent=None):
        """Inicializa el widget animado."""
        super(AnimatedWidget, self).__init__(parent)
        self.animation = None
        self.setAutoFillBackground(True)
    
    def fade_in(self, duration=300):
        """
        Anima la aparición gradual del widget.
        
        Args:
            duration (int): Duración de la animación en milisegundos.
        """
        self.setVisible(True)
        self.setMaximumHeight(0)
        
        # Crear animación
        self.animation = QPropertyAnimation(self, b"maximumHeight")
        self.animation.setDuration(duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.sizeHint().height())
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
    
    def fade_out(self, duration=300):
        """
        Anima la desaparición gradual del widget.
        
        Args:
            duration (int): Duración de la animación en milisegundos.
        """
        # Crear animación
        self.animation = QPropertyAnimation(self, b"maximumHeight")
        self.animation.setDuration(duration)
        self.animation.setStartValue(self.height())
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.finished.connect(lambda: self.setVisible(False))
        self.animation.start()


class FunctionInputWidget(QGroupBox):
    """Widget para entrada de función matemática con validación."""
    
    function_changed = pyqtSignal(str, int)  # Emite: función, orden derivada
    calculate_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """Inicializa el widget de entrada de función."""
        super(FunctionInputWidget, self).__init__("Entrada de la Función", parent)
        
        # Configurar layout
        layout = QFormLayout(self)
        layout.setVerticalSpacing(10)
        
        # Widgets para entrada de función
        self.function_label = QLabel("Ingrese la función f(x):")
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ejemplos: sin(x), x^2, e^x, ln(x), 2*x+3")
        
        # Widgets para orden de derivada
        self.order_label = QLabel("Orden de derivada:")
        self.order_spin = QSpinBox()
        self.order_spin.setRange(1, 10)
        self.order_spin.setValue(1)
        
        # Widgets para integral definida
        self.integral_group = QGroupBox("Integral Definida")
        self.integral_group.setCheckable(True)
        self.integral_group.setChecked(False)
        
        integral_layout = QFormLayout(self.integral_group)
        
        self.lower_label = QLabel("Límite inferior:")
        self.lower_input = QLineEdit()
        self.upper_label = QLabel("Límite superior:")
        self.upper_input = QLineEdit()
        
        integral_layout.addRow(self.lower_label, self.lower_input)
        integral_layout.addRow(self.upper_label, self.upper_input)
        
        # Botón para calcular
        self.calc_button = QPushButton("Calcular")
        self.calc_button.setMinimumHeight(40)
        
        # Ejemplos de uso
        self.examples_label = QLabel("Puedes usar: sin(x), cos(x), tan(x), exp(x)/e^x, ln(x), etc.")
        self.examples_label.setStyleSheet("color: #666666;")
        
        # Añadir widgets al layout
        layout.addRow(self.function_label, self.function_input)
        layout.addRow(self.order_label, self.order_spin)
        layout.addRow(self.integral_group)
        layout.addRow(self.calc_button)
        layout.addRow(self.examples_label)
        
        # Conectar señales
        self.function_input.textChanged.connect(self._on_input_change)
        self.order_spin.valueChanged.connect(self._on_input_change)
        self.calc_button.clicked.connect(self.calculate_clicked)
    
    def _on_input_change(self):
        """Maneja los cambios en la entrada de función."""
        func = self.function_input.text()
        order = self.order_spin.value()
        
        self.function_changed.emit(func, order)
    
    def get_function_input(self):
        """
        Obtiene la entrada de función actual.
        
        Returns:
            dict: Diccionario con los valores de entrada.
        """
        return {
            'function': self.function_input.text(),
            'order': self.order_spin.value(),
            'integral_definida': self.integral_group.isChecked(),
            'lower_limit': self.lower_input.text(),
            'upper_limit': self.upper_input.text()
        }
    
    def set_function_input(self, function_data):
        """
        Establece los valores de entrada de función.
        
        Args:
            function_data (dict): Diccionario con valores para establecer.
        """
        if 'function' in function_data:
            self.function_input.setText(function_data['function'])
        
        if 'order' in function_data:
            self.order_spin.setValue(function_data['order'])
        
        if 'integral_definida' in function_data:
            self.integral_group.setChecked(function_data['integral_definida'])
        
        if 'lower_limit' in function_data:
            self.lower_input.setText(function_data['lower_limit'])
        
        if 'upper_limit' in function_data:
            self.upper_input.setText(function_data['upper_limit'])


class ResultWidget(AnimatedWidget):
    """Widget para mostrar los resultados del cálculo."""
    
    def __init__(self, parent=None):
        """Inicializa el widget de resultados."""
        super(ResultWidget, self).__init__(parent)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Grupo para resultados
        self.results_group = QGroupBox("Resultados")
        results_layout = QFormLayout(self.results_group)
        
        # Etiquetas para mostrar resultados
        self.function_result = QLabel("")
        self.derivative_result = QLabel("")
        self.integral_result = QLabel("")
        
        # Estilo para los resultados
        result_style = """
            font-weight: bold;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 4px;
        """
        
        self.function_result.setStyleSheet(result_style)
        self.derivative_result.setStyleSheet(result_style)
        self.integral_result.setStyleSheet(result_style)
        
        self.function_result.setWordWrap(True)
        self.derivative_result.setWordWrap(True)
        self.integral_result.setWordWrap(True)
        
        # Añadir etiquetas al layout
        results_layout.addRow("Función f(x):", self.function_result)
        results_layout.addRow("Derivada f'(x):", self.derivative_result)
        results_layout.addRow("Integral:", self.integral_result)
        
        # Añadir grupo al layout principal
        layout.addWidget(self.results_group)
        
        # Tabla de puntos críticos
        self.critical_points_group = QGroupBox("Puntos Críticos")
        critical_points_layout = QVBoxLayout(self.critical_points_group)
        
        self.critical_points_table = QTableWidget(0, 3)
        self.critical_points_table.setHorizontalHeaderLabels(["Valor x", "Valor f(x)", "Tipo"])
        self.critical_points_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        critical_points_layout.addWidget(self.critical_points_table)
        
        layout.addWidget(self.critical_points_group)
        
        # Opciones para exportar resultados
        self.export_group = QGroupBox("Exportar Resultados")
        export_layout = QHBoxLayout(self.export_group)
        
        self.export_image_btn = QPushButton("Guardar Gráfica")
        self.export_image_btn.setIcon(QIcon.fromTheme("document-save"))
        
        export_layout.addWidget(self.export_image_btn)
        
        layout.addWidget(self.export_group)
    
    def set_dark_mode(self, enable=True):
        """
        Cambia el estilo entre modo claro y oscuro.
        
        Args:
            enable (bool): Si es True, activa el modo oscuro.
        """
        if enable:
            result_style = """
                font-weight: bold;
                padding: 8px;
                background-color: #252526;
                border-radius: 4px;
                color: #e0e0e0;
            """
            table_style = """
                QTableWidget {
                    background-color: #252526;
                    color: #e0e0e0;
                    border: 1px solid #3e3e42;
                }
                QHeaderView::section {
                    background-color: #2d2d30;
                    color: #e0e0e0;
                    border: 1px solid #3e3e42;
                }
            """
        else:
            result_style = """
                font-weight: bold;
                padding: 8px;
                background-color: #f8f9fa;
                border-radius: 4px;
                color: #2c3e50;
            """
            table_style = """
                QTableWidget {
                    background-color: #ffffff;
                    color: #333333;
                    border: 1px solid #cccccc;
                }
                QHeaderView::section {
                    background-color: #e0e0e0;
                    color: #333333;
                    border: 1px solid #cccccc;
                }
            """
        
        self.function_result.setStyleSheet(result_style)
        self.derivative_result.setStyleSheet(result_style)
        self.integral_result.setStyleSheet(result_style)
        self.critical_points_table.setStyleSheet(table_style)
    
    def set_results(self, results):
        """
        Establece y muestra los resultados del cálculo.
        
        Args:
            results (dict): Diccionario con los resultados a mostrar.
        """
        # Actualizar textos
        if 'function' in results:
            self.function_result.setText(results['function'])
        else:
            self.function_result.setText("")
        
        if 'derivative' in results:
            self.derivative_result.setText(results['derivative'])
        else:
            self.derivative_result.setText("")
        
        if 'integral' in results:
            self.integral_result.setText(results['integral'])
        else:
            self.integral_result.setText("")
        
        # Actualizar tabla de puntos críticos
        if 'critical_points' in results and results['critical_points']:
            self.update_critical_points(results['critical_points'])
        else:
            # Limpiar tabla
            self.critical_points_table.setRowCount(0)
        
        # Animar la aparición
        self.fade_in()
    
    def update_critical_points(self, critical_points):
        """
        Actualiza la tabla de puntos críticos.
        
        Args:
            critical_points (list): Lista de diccionarios con información de puntos críticos.
        """
        # Limpiar tabla
        self.critical_points_table.setRowCount(0)
        
        # Añadir filas para cada punto crítico
        for i, point in enumerate(critical_points):
            self.critical_points_table.insertRow(i)
            
            # Crear y configurar celdas
            x_item = QTableWidgetItem(f"{point['x']:.4f}")
            x_item.setTextAlignment(Qt.AlignCenter)
            
            if point['y'] is not None:
                y_item = QTableWidgetItem(f"{point['y']:.4f}")
            else:
                y_item = QTableWidgetItem("Indefinido")
            y_item.setTextAlignment(Qt.AlignCenter)
            
            type_item = QTableWidgetItem(point['type'])
            type_item.setTextAlignment(Qt.AlignCenter)
            
            # Colorear según el tipo de punto
            if point['type'] == "Máximo":
                type_item.setBackground(QColor(255, 200, 200))  # Rojo claro
            elif point['type'] == "Mínimo":
                type_item.setBackground(QColor(200, 255, 200))  # Verde claro
            elif point['type'] == "Punto de inflexión":
                type_item.setBackground(QColor(200, 200, 255))  # Azul claro
            
            # Añadir celdas a la tabla
            self.critical_points_table.setItem(i, 0, x_item)
            self.critical_points_table.setItem(i, 1, y_item)
            self.critical_points_table.setItem(i, 2, type_item)


class HistoryWidget(QGroupBox):
    """Widget para mostrar el historial de cálculos."""
    
    history_selected = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        """Inicializa el widget de historial."""
        super(HistoryWidget, self).__init__("Historial de Cálculos", parent)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Lista de historial
        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)
        self.history_list.setObjectName("historyList")
        
        # Botones de acción
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Limpiar Historial")
        
        button_layout.addWidget(self.clear_btn)
        
        # Añadir widgets al layout
        layout.addWidget(self.history_list)
        layout.addLayout(button_layout)
        
        # Conectar señales
        self.history_list.itemClicked.connect(self._on_item_clicked)
        self.clear_btn.clicked.connect(self.clear_history)
    
    def add_to_history(self, entry):
        """
        Añade una entrada al historial.
        
        Args:
            entry (dict): Diccionario con información de la entrada.
        """
        # Crear texto para mostrar
        func_str = entry.get('function', '')
        order = entry.get('order', 1)
        
        # Crear cadena de visualización
        if order > 1:
            display_text = f"{func_str} (Derivada orden {order})"
        else:
            display_text = f"{func_str}"
        
        # Añadir a la lista
        item = QListWidgetItem(display_text)
        item.setData(Qt.UserRole, entry)  # Almacenar datos completos
        
        self.history_list.insertItem(0, item)  # Añadir al principio
    
    def _on_item_clicked(self, item):
        """
        Maneja el clic en un elemento del historial.
        
        Args:
            item (QListWidgetItem): Elemento seleccionado.
        """
        # Obtener datos almacenados
        entry_data = item.data(Qt.UserRole)
        
        # Emitir señal con los datos
        self.history_selected.emit(entry_data)
    
    def clear_history(self):
        """Limpia el historial de cálculos."""
        self.history_list.clear()
    
    def get_history_items(self):
        """
        Obtiene todos los elementos del historial.
        
        Returns:
            list: Lista de diccionarios con entradas del historial.
        """
        items = []
        for i in range(self.history_list.count()):
            item = self.history_list.item(i)
            items.append(item.data(Qt.UserRole))
        
        return items
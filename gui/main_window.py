"""
Ventana principal para la aplicación de calculadora de derivadas.
"""
import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QStackedWidget, 
                           QStatusBar, QMenuBar, QMenu, QAction, QToolBar, 
                           QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QSize, QSettings, QPropertyAnimation, QTimer, pyqtSlot
from PyQt5.QtGui import QIcon, QFont

from .themes import Themes
from .pages import InputPage, ResultsPage

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        """Inicializa la ventana principal."""
        super(MainWindow, self).__init__()
        
        # Configurar ventana
        self.setWindowTitle("Calculadora de Derivadas de Ilya - Versión Mejorada")
        self.setMinimumSize(1024, 768)
        
        # Crear configuración para guardar preferencias
        self.settings = QSettings("Ilya", "DerivativesCalculator")
        
        # Tema actual
        self.dark_mode = self.settings.value("darkMode", False, type=bool)
        
        # Configurar estilo inicial
        self.apply_theme()
        
        # Crear widgets centrales
        self.setup_ui()
        
        # Restaurar geometría guardada
        self.restore_geometry()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear stack para páginas
        self.stack = QStackedWidget()
        
        # Crear páginas
        self.input_page = InputPage()
        self.results_page = ResultsPage()
        
        # Añadir páginas al stack
        self.stack.addWidget(self.input_page)
        self.stack.addWidget(self.results_page)
        
        # Añadir stack al layout principal
        main_layout.addWidget(self.stack)
        
        # Crear barra de estado
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Listo")
        
        # Crear menús
        self.create_menus()
        
        # Conectar señales de las páginas
        self.input_page.calculate_requested.connect(self.calculate_derivative)
        self.results_page.back_requested.connect(self.show_input_page)
        
        # Mostrar página inicial
        self.show_input_page()
    
    def create_menus(self):
        """Crea la estructura de menús de la aplicación."""
        # Menú Archivo
        file_menu = self.menuBar().addMenu("&Archivo")
        
        new_action = QAction("&Nuevo cálculo", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_calculation)
        
        save_action = QAction("&Guardar gráfica", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_graph)
        
        exit_action = QAction("&Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Menú Ver
        view_menu = self.menuBar().addMenu("&Ver")
        
        theme_action = QAction("Cambiar &tema", self)
        theme_action.triggered.connect(self.toggle_theme)
        
        fullscreen_action = QAction("&Pantalla completa", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        
        view_menu.addAction(theme_action)
        view_menu.addAction(fullscreen_action)
        
        # Menú Ayuda
        help_menu = self.menuBar().addMenu("A&yuda")
        
        about_action = QAction("&Acerca de", self)
        about_action.triggered.connect(self.show_about)
        
        help_menu.addAction(about_action)
    
    def apply_theme(self):
        """Aplica el tema actual (claro u oscuro)."""
        if self.dark_mode:
            self.setStyleSheet(Themes.get_dark_theme())
        else:
            self.setStyleSheet(Themes.get_light_theme())
        
        # Si la página de resultados ya está creada, actualizar su tema
        if hasattr(self, 'results_page'):
            self.results_page.dark_mode = self.dark_mode
            if self.results_page.plot_canvas:
                self.results_page.plot_canvas.set_dark_mode(self.dark_mode)
            if self.results_page.result_widget:
                self.results_page.result_widget.set_dark_mode(self.dark_mode)
    
    def toggle_theme(self):
        """Alterna entre tema claro y oscuro."""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        
        # Guardar preferencia
        self.settings.setValue("darkMode", self.dark_mode)
    
    def toggle_fullscreen(self):
        """Alterna entre modo normal y pantalla completa."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def show_input_page(self):
        """Muestra la página de entrada de funciones."""
        self.stack.setCurrentWidget(self.input_page)
        self.statusBar.showMessage("Ingrese una función para calcular su derivada")
    
    def show_results_page(self):
        """Muestra la página de resultados."""
        self.stack.setCurrentWidget(self.results_page)
        self.statusBar.showMessage("Resultados del cálculo")
    
    @pyqtSlot(dict)
    def calculate_derivative(self, input_data):
        """
        Calcula la derivada según los datos de entrada.
        
        Args:
            input_data (dict): Diccionario con los datos de entrada.
        """
        # Verificar si hay una función para calcular
        if not input_data.get('function', ''):
            QMessageBox.warning(
                self, 
                "Error de entrada", 
                "Por favor ingrese una función para calcular su derivada."
            )
            return
        
        # Aquí se haría la llamada al módulo de lógica
        # Esto es un placeholder hasta que implementemos el módulo completo
        self.statusBar.showMessage("Calculando...")
        
        # Simular un breve retraso para mostrar la animación de transición
        QTimer.singleShot(500, lambda: self.process_calculation(input_data))
    
    def process_calculation(self, input_data):
        """
        Procesa el cálculo y muestra los resultados.
        
        Args:
            input_data (dict): Diccionario con los datos de entrada.
        """
        # En la implementación real, aquí llamaríamos a las funciones del módulo logic.py
        # Por ahora, solo mostraremos la página de resultados con datos de ejemplo
        
        # Añadir al historial
        self.input_page.add_to_history(input_data)
        
        # Mostrar la página de resultados
        self.show_results_page()
        
        # NOTA: Aquí se conectará con la lógica real cuando implementemos el módulo completo
    
    def new_calculation(self):
        """Inicia un nuevo cálculo."""
        self.input_page.clear_inputs()
        self.show_input_page()
    
    def save_graph(self):
        """Guarda la gráfica actual como imagen."""
        # Verificar que estamos en la página de resultados
        if self.stack.currentWidget() == self.results_page:
            self.results_page.export_image()
        else:
            QMessageBox.information(
                self, 
                "Guardar Gráfica", 
                "Primero debe calcular una derivada para poder guardar la gráfica."
            )
    
    def show_about(self):
        """Muestra información sobre la aplicación."""
        QMessageBox.about(
            self,
            "Acerca de Calculadora de Derivadas",
            """
            <h3>Calculadora de Derivadas - Versión Mejorada</h3>
            <p>Desarrollada por Ilya</p>
            <p>Esta aplicación permite calcular derivadas, integrales y visualizar
            gráficamente funciones matemáticas.</p>
            <p>Versión 2.0</p>
            """
        )
    
    def save_geometry(self):
        """Guarda la geometría de la ventana."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
    
    def restore_geometry(self):
        """Restaura la geometría guardada de la ventana."""
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        if self.settings.contains("windowState"):
            self.restoreState(self.settings.value("windowState"))
    
    def closeEvent(self, event):
        """
        Maneja el evento de cierre de la ventana.
        
        Args:
            event: Evento de cierre.
        """
        # Guardar geometría antes de cerrar
        self.save_geometry()
        event.accept()
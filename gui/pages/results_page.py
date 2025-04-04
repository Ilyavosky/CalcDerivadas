"""
Página de resultados para la calculadora de derivadas.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                           QPushButton, QFileDialog, QMessageBox, QLabel)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

from ..widgets import ResultWidget
from ..canvas import MathPlotCanvas

class ResultsPage(QWidget):
    """Página para mostrar los resultados y gráficas."""
    
    # Señales
    back_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        """Inicializa la página de resultados."""
        super(ResultsPage, self).__init__(parent)
        
        # Variables de estado
        self.dark_mode = False
        self.current_data = {
            'lambda_funcs': None,
            'x_range': (-10, 10),
            'critical_points': None
        }
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Barra de herramientas superior
        toolbar_layout = QHBoxLayout()
        
        # Botón para volver
        self.back_btn = QPushButton("« Volver")
        self.back_btn.setIcon(QIcon.fromTheme("go-previous"))
        
        # Botón para alternar modo oscuro
        self.theme_btn = QPushButton("Modo Oscuro")
        self.theme_btn.setIcon(QIcon.fromTheme("preferences-desktop-theme"))
        
        # Botón para pantalla completa
        self.fullscreen_btn = QPushButton("Pantalla Completa")
        self.fullscreen_btn.setIcon(QIcon.fromTheme("view-fullscreen"))
        
        # Añadir botones a la barra de herramientas
        toolbar_layout.addWidget(self.back_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.theme_btn)
        toolbar_layout.addWidget(self.fullscreen_btn)
        
        # Añadir barra de herramientas al layout principal
        main_layout.addLayout(toolbar_layout)
        
        # Crear splitter para dividir la pantalla
        splitter = QSplitter(Qt.Vertical)
        
        # Panel superior: gráficas
        self.plot_canvas = MathPlotCanvas(self, dark_mode=self.dark_mode)
        
        # Panel inferior: resultados
        self.result_widget = ResultWidget()
        
        # Añadir widgets al splitter
        splitter.addWidget(self.plot_canvas)
        splitter.addWidget(self.result_widget)
        
        # Establecer proporciones (70% gráficas, 30% resultados)
        splitter.setSizes([700, 300])
        
        # Añadir splitter al layout principal
        main_layout.addWidget(splitter)
        
        # Conectar señales
        self.back_btn.clicked.connect(self.back_requested)
        self.theme_btn.clicked.connect(self.toggle_dark_mode)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        self.result_widget.export_image_btn.clicked.connect(self.export_image)
    
    def set_results(self, results, lambda_funcs, x_range):
        """
        Establece y muestra los resultados del cálculo.
        
        Args:
            results (dict): Diccionario con los resultados a mostrar.
            lambda_funcs (dict): Funciones lambda para evaluación numérica.
            x_range (tuple): Rango para el eje X de las gráficas.
        """
        # Almacenar datos actuales
        self.current_data['lambda_funcs'] = lambda_funcs
        self.current_data['x_range'] = x_range
        
        if 'critical_points' in results:
            self.current_data['critical_points'] = results['critical_points']
        
        # Mostrar resultados
        self.result_widget.set_results(results)
        
        # Graficar funciones
        self.plot_canvas.plot_functions(lambda_funcs, x_range, 
                                       critical_points=self.current_data['critical_points'],
                                       dark_mode=self.dark_mode)
    
    def toggle_dark_mode(self):
        """Alterna entre modo claro y oscuro."""
        self.dark_mode = not self.dark_mode
        
        # Actualizar textos e iconos de botones
        if self.dark_mode:
            self.theme_btn.setText("Modo Claro")
        else:
            self.theme_btn.setText("Modo Oscuro")
        
        # Actualizar estilo de las gráficas
        self.plot_canvas.set_dark_mode(self.dark_mode)
        
        # Actualizar estilo de resultados
        self.result_widget.set_dark_mode(self.dark_mode)
        
        # Volver a graficar para aplicar estilo
        if self.current_data['lambda_funcs']:
            self.plot_canvas.plot_functions(
                self.current_data['lambda_funcs'],
                self.current_data['x_range'],
                critical_points=self.current_data['critical_points'],
                dark_mode=self.dark_mode
            )
    
    def toggle_fullscreen(self):
        """Alterna entre modo normal y pantalla completa."""
        if self.window().isFullScreen():
            self.window().showNormal()
            self.fullscreen_btn.setText("Pantalla Completa")
        else:
            self.window().showFullScreen()
            self.fullscreen_btn.setText("Restaurar")
    
    def export_image(self):
        """Exporta la gráfica actual como imagen."""
        # Abrir diálogo para guardar archivo
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar Gráfica", 
            "", 
            "Imágenes PNG (*.png);;Imágenes PDF (*.pdf);;Todos los archivos (*)"
        )
        
        if file_path:
            # Guardar la figura
            if self.plot_canvas.save_figure(file_path):
                QMessageBox.information(
                    self, 
                    "Exportación Exitosa", 
                    f"La gráfica se ha guardado correctamente en:\n{file_path}"
                )
            else:
                QMessageBox.warning(
                    self, 
                    "Error de Exportación", 
                    "No se pudo guardar la gráfica. Verifique la ruta y los permisos."
                )
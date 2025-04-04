"""
Módulo para el canvas personalizado de gráficas matemáticas.
Proporciona un widget para mostrar gráficas en la interfaz de PyQt5.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

class MathPlotCanvas(QWidget):
    """
    Widget para mostrar gráficas matemáticas con soporte para interacción y zoom.
    """
    
    def __init__(self, parent=None, dark_mode=False):
        """
        Inicializa el widget de canvas para gráficas.
        
        Args:
            parent (QWidget): Widget padre.
            dark_mode (bool): Si es True, usa un tema oscuro para las gráficas.
        """
        super(MathPlotCanvas, self).__init__(parent)
        
        # Crear layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear figura y subplots
        self.fig = Figure(tight_layout=True)
        
        # Crear subgráficas en una disposición 2x2
        self.axes = {}
        self.axes['function'] = self.fig.add_subplot(221)
        self.axes['derivative'] = self.fig.add_subplot(222)
        self.axes['integral'] = self.fig.add_subplot(223)
        self.axes['combined'] = self.fig.add_subplot(224)
        
        # Configurar títulos y rejillas
        self.axes['function'].set_title("Función f(x)")
        self.axes['derivative'].set_title("Derivada f'(x)")
        self.axes['integral'].set_title("Integral ∫f(x)dx")
        self.axes['combined'].set_title("Comparativa")
        
        for ax in self.axes.values():
            ax.grid(True, alpha=0.3)
        
        # Crear canvas
        self.canvas = FigureCanvasQTAgg(self.fig)
        
        # Añadir canvas al layout
        self.layout.addWidget(self.canvas)
        
        # Aplicar estilo según el modo
        self.set_dark_mode(dark_mode)
        
        # Variables para almacenar datos de las gráficas
        self.plotted_data = {
            'function': None,
            'derivative': None,
            'integral': None,
            'x_range': (-10, 10),
            'critical_points': None
        }
    
    def set_dark_mode(self, enable=True):
        """
        Cambia el tema de la gráfica entre claro y oscuro.
        
        Args:
            enable (bool): Si es True, activa el modo oscuro.
        """
        if enable:
            plt.style.use('dark_background')
            self.fig.patch.set_facecolor('#2D2D30')
            text_color = 'white'
            grid_color = '#555555'
            for ax in self.axes.values():
                ax.set_facecolor('#1E1E1E')
        else:
            plt.style.use('default')
            self.fig.patch.set_facecolor('#F5F5F5')
            text_color = 'black'
            grid_color = '#CCCCCC'
            for ax in self.axes.values():
                ax.set_facecolor('#FFFFFF')
        
        # Actualizar color del texto
        for ax in self.axes.values():
            ax.title.set_color(text_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.tick_params(colors=text_color)
            ax.grid(True, color=grid_color, alpha=0.3)
        
        self.canvas.draw_idle()
    
    def clear_all(self):
        """Limpia todas las gráficas."""
        for ax in self.axes.values():
            ax.clear()
            ax.grid(True, alpha=0.3)
        
        # Restaurar títulos
        self.axes['function'].set_title("Función f(x)")
        self.axes['derivative'].set_title("Derivada f'(x)")
        self.axes['integral'].set_title("Integral ∫f(x)dx")
        self.axes['combined'].set_title("Comparativa")
        
        self.canvas.draw_idle()
        
        # Reiniciar datos almacenados
        for key in self.plotted_data:
            if key != 'x_range':
                self.plotted_data[key] = None
    
    def plot_functions(self, lambda_funcs, x_range, critical_points=None, dark_mode=False):
        """
        Grafica las funciones, derivadas, integrales y puntos críticos.
        
        Args:
            lambda_funcs (dict): Diccionario con funciones lambda para evaluación.
            x_range (tuple): Tupla (x_min, x_max) con el rango para los ejes x.
            critical_points (list): Lista de puntos críticos para marcar.
            dark_mode (bool): Si es True, usa colores para modo oscuro.
        """
        # Almacenar datos para reutilizar
        self.plotted_data['x_range'] = x_range
        self.plotted_data['critical_points'] = critical_points
        self.plotted_data.update({k: v for k, v in lambda_funcs.items() if k in self.plotted_data})
        
        # Limpiar gráficas previas
        self.clear_all()
        
        # Crear puntos x para graficar
        x_min, x_max = x_range
        x_vals = np.linspace(x_min, x_max, 1000)
        
        # Colores según el modo
        if dark_mode:
            colors = {
                'function': '#5E97F6',    # Azul claro
                'derivative': '#F06292',  # Rosa
                'integral': '#4CAF50',    # Verde
                'max_point': '#FF6F00',   # Naranja oscuro
                'min_point': '#00BFA5',   # Verde azulado
                'inflection': '#BA68C8',  # Púrpura
                'grid': '#555555'         # Gris oscuro
            }
        else:
            colors = {
                'function': '#1565C0',    # Azul
                'derivative': '#C2185B',  # Rojo
                'integral': '#2E7D32',    # Verde
                'max_point': '#E65100',   # Naranja
                'min_point': '#00796B',   # Verde oscuro
                'inflection': '#8E24AA',  # Púrpura
                'grid': '#CCCCCC'         # Gris claro
            }
        
        # Función lambda para filtrar valores válidos
        def filter_values(x, y):
            valid_indices = np.isfinite(y)
            return x[valid_indices], y[valid_indices]
        
        # Graficar función original
        if 'function' in lambda_funcs:
            try:
                f_vals = lambda_funcs['function'](x_vals)
                x_valid, f_valid = filter_values(x_vals, f_vals)
                
                self.axes['function'].plot(x_valid, f_valid, '-', 
                                          color=colors['function'], 
                                          lw=2, 
                                          label='f(x)')
                self.axes['function'].set_xlabel('x')
                self.axes['function'].set_ylabel('f(x)')
                
                # Graficar en la vista combinada
                self.axes['combined'].plot(x_valid, f_valid, '-', 
                                          color=colors['function'], 
                                          lw=2, 
                                          label='f(x)')
            except Exception as e:
                print(f"Error al graficar función: {str(e)}")
        
        # Graficar derivada
        if 'derivative' in lambda_funcs:
            try:
                df_vals = lambda_funcs['derivative'](x_vals)
                x_valid, df_valid = filter_values(x_vals, df_vals)
                
                self.axes['derivative'].plot(x_valid, df_valid, '-', 
                                            color=colors['derivative'], 
                                            lw=2, 
                                            label="f'(x)")
                self.axes['derivative'].set_xlabel('x')
                self.axes['derivative'].set_ylabel("f'(x)")
                
                # Graficar en la vista combinada
                self.axes['combined'].plot(x_valid, df_valid, '-', 
                                          color=colors['derivative'], 
                                          lw=2, 
                                          label="f'(x)")
                
                # Añadir línea horizontal en y=0 para derivada
                self.axes['derivative'].axhline(y=0, color='gray', linestyle='--', alpha=0.7)
            except Exception as e:
                print(f"Error al graficar derivada: {str(e)}")
        
        # Graficar integral si está disponible
        if 'integral' in lambda_funcs:
            try:
                int_vals = lambda_funcs['integral'](x_vals)
                x_valid, int_valid = filter_values(x_vals, int_vals)
                
                self.axes['integral'].plot(x_valid, int_valid, '-', 
                                          color=colors['integral'], 
                                          lw=2, 
                                          label="∫f(x)dx")
                self.axes['integral'].set_xlabel('x')
                self.axes['integral'].set_ylabel("∫f(x)dx")
                
                # Graficar en la vista combinada
                self.axes['combined'].plot(x_valid, int_valid, '-', 
                                          color=colors['integral'], 
                                          lw=1.5, 
                                          label="∫f(x)dx")
            except Exception as e:
                print(f"Error al graficar integral: {str(e)}")
        
        # Marcar puntos críticos si están disponibles
        if critical_points:
            # Para cada tipo de punto crítico, usar un marcador diferente
            markers = {
                "Máximo": ("v", colors['max_point'], "Máximo"),
                "Mínimo": ("^", colors['min_point'], "Mínimo"),
                "Punto de inflexión": ("o", colors['inflection'], "Inflexión"),
                "Indeterminado": ("s", "gray", "Indeterminado")
            }
            
            for point in critical_points:
                x_val = point['x']
                
                # Verificar si el punto está en el rango visible
                if x_min <= x_val <= x_max:
                    try:
                        # Obtener el tipo de punto y su configuración de marcador
                        point_type = point['type']
                        marker, color, label = markers.get(point_type, markers["Indeterminado"])
                        
                        # Evaluar función en el punto
                        if 'function' in lambda_funcs and point['y'] is not None:
                            y_val = point['y']
                            
                            # Marcar en la gráfica de función
                            self.axes['function'].plot(x_val, y_val, marker, 
                                                     color=color, 
                                                     ms=8, 
                                                     label=label if label not in [l.get_label() for l in self.axes['function'].get_lines()] else "")
                            
                            # Marcar en la vista combinada
                            self.axes['combined'].plot(x_val, y_val, marker, 
                                                     color=color, 
                                                     ms=8)
                        
                        # Marcar en la gráfica de derivada (siempre en y=0)
                        if 'derivative' in lambda_funcs:
                            self.axes['derivative'].plot(x_val, 0, marker, 
                                                       color=color, 
                                                       ms=8)
                    except Exception as e:
                        print(f"Error al marcar punto crítico: {str(e)}")
        
        # Añadir leyendas
        for ax in self.axes.values():
            if len(ax.get_lines()) > 0:  # Solo añadir leyenda si hay líneas
                # Eliminar duplicados en la leyenda
                handles, labels = ax.get_legend_handles_labels()
                by_label = dict(zip(labels, handles))
                if by_label:  # Solo si hay elementos
                    ax.legend(by_label.values(), by_label.keys(), loc='best', fontsize='small')
        
        # Ajustar diseño y refrescar canvas
        self.fig.tight_layout()
        self.canvas.draw_idle()
    
    def save_figure(self, filename, dpi=300):
        """
        Guarda la figura actual en un archivo.
        
        Args:
            filename (str): Ruta y nombre del archivo para guardar.
            dpi (int): Resolución en puntos por pulgada.
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        try:
            self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
            return True
        except Exception as e:
            print(f"Error al guardar figura: {str(e)}")
            return False
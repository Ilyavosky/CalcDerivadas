"""
Módulo para graficación de funciones matemáticas.
Proporciona clases para visualizar funciones, derivadas e integrales.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MathCanvas(FigureCanvas):
    """
    Canvas personalizado para graficar funciones matemáticas en PyQt5.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100, dark_mode=False):
        """
        Inicializa el canvas para gráficas matemáticas.
        
        Args:
            parent (QWidget): Widget padre.
            width (int): Ancho de la figura en pulgadas.
            height (int): Alto de la figura en pulgadas.
            dpi (int): Resolución en puntos por pulgada.
            dark_mode (bool): Si es True, usa un tema oscuro para las gráficas.
        """
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        # Crear subgráficas
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
        
        # Aplicar estilo según el modo
        self.set_dark_mode(dark_mode)
        
        super(MathCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
        # Ajustar diseño
        self.fig.tight_layout()
    
    def set_dark_mode(self, enable=True):
        """
        Cambia el tema de la gráfica entre claro y oscuro.
        
        Args:
            enable (bool): Si es True, activa el modo oscuro.
        """
        if enable:
            plt.style.use('dark_background')
            text_color = 'white'
            self.fig.patch.set_facecolor('#2D2D30')
            for ax in self.axes.values():
                ax.set_facecolor('#1E1E1E')
        else:
            plt.style.use('default')
            text_color = 'black'
            self.fig.patch.set_facecolor('#F5F5F5')
            for ax in self.axes.values():
                ax.set_facecolor('#FFFFFF')
        
        # Actualizar color del texto
        for ax in self.axes.values():
            ax.title.set_color(text_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.tick_params(colors=text_color)
        
        self.draw_idle()
    
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
        
        self.draw_idle()
    
    def plot_functions(self, lambda_funcs, x_range, eval_point=None, dark_mode=False):
        """
        Grafica las funciones, derivadas e integrales.
        
        Args:
            lambda_funcs (dict): Diccionario con funciones lambda para evaluación.
            x_range (tuple): Tupla (x_min, x_max) con el rango para los ejes x.
            eval_point (float, optional): Punto en el que evaluar y marcar.
            dark_mode (bool): Si es True, usa colores para modo oscuro.
        """
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
                'point': '#FFD54F',       # Amarillo
                'grid': '#555555'         # Gris oscuro
            }
        else:
            colors = {
                'function': '#1565C0',    # Azul
                'derivative': '#C2185B',  # Rojo
                'integral': '#2E7D32',    # Verde
                'point': '#FF8F00',       # Naranja
                'grid': '#CCCCCC'         # Gris claro
            }
        
        # Función lambda para filtrar valores válidos
        def filter_values(x, y):
            valid_indices = np.isfinite(y)
            return x[valid_indices], y[valid_indices]
        
        # Graficar función original
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
                                          lw=2, 
                                          label="∫f(x)dx")
            except Exception as e:
                print(f"Error al graficar integral: {str(e)}")
        
        # Mostrar punto evaluado si se proporcionó
        if eval_point is not None:
            try:
                if x_min <= eval_point <= x_max:
                    # Calcular valores en el punto
                    point_y = lambda_funcs['function'](eval_point)
                    point_dy = lambda_funcs['derivative'](eval_point)
                    
                    # Marcar punto en la función
                    self.axes['function'].plot(eval_point, point_y, 'o', 
                                             color=colors['point'], 
                                             ms=8)
                    self.axes['function'].axvline(x=eval_point, 
                                                 color=colors['point'], 
                                                 linestyle='--', 
                                                 alpha=0.5)
                    
                    # Marcar punto en la derivada
                    self.axes['derivative'].plot(eval_point, point_dy, 'o', 
                                               color=colors['point'], 
                                               ms=8)
                    self.axes['derivative'].axvline(x=eval_point, 
                                                   color=colors['point'], 
                                                   linestyle='--', 
                                                   alpha=0.5)
                    
                    # Marcar en la vista combinada
                    self.axes['combined'].axvline(x=eval_point, 
                                                 color=colors['point'], 
                                                 linestyle='--', 
                                                 alpha=0.5)
                    
                    # Marcar en la integral si está disponible
                    if 'integral' in lambda_funcs:
                        point_int = lambda_funcs['integral'](eval_point)
                        self.axes['integral'].plot(eval_point, point_int, 'o', 
                                                  color=colors['point'], 
                                                  ms=8)
                        self.axes['integral'].axvline(x=eval_point, 
                                                     color=colors['point'], 
                                                     linestyle='--', 
                                                     alpha=0.5)
            except Exception as e:
                print(f"Error al marcar punto: {str(e)}")
        
        # Añadir leyendas
        for ax in self.axes.values():
            if len(ax.get_lines()) > 0:  # Solo añadir leyenda si hay líneas
                ax.legend(loc='best')
        
        # Ajustar diseño y refrescar canvas
        self.fig.tight_layout()
        self.draw_idle()
    
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
"""
Definiciones de temas para la interfaz de usuario.
Proporciona estilos para modos claro y oscuro.
"""

class Themes:
    """Clase para gestionar los temas de la aplicación."""
    
    @staticmethod
    def get_light_theme():
        """
        Obtiene el estilo para el tema claro.
        
        Returns:
            str: Hoja de estilos QSS para el tema claro.
        """
        return """
        QMainWindow, QDialog {
            background-color: #f5f5f5;
        }
        
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
            color: #333333;
        }
        
        QGroupBox {
            font-size: 11pt;
            font-weight: bold;
            border: 1px solid #cccccc;
            border-radius: 6px;
            margin-top: 14px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #4285f4;
        }
        
        QPushButton {
            background-color: #4a86e8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 10pt;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #3a76d8;
        }
        
        QPushButton:pressed {
            background-color: #2a66c8;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #888888;
        }
        
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 6px;
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
            selection-background-color: #4a86e8;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 1px solid #4a86e8;
        }
        
        QLabel {
            color: #333333;
        }
        
        QTabWidget::pane {
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: white;
        }
        
        QTabBar::tab {
            background-color: #e0e0e0;
            color: #333333;
            padding: 8px 12px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: 2px solid #4a86e8;
        }
        
        QScrollArea, QScrollBar {
            background-color: white;
            border-radius: 4px;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #f0f0f0;
            width: 12px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            min-height: 20px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }
        
        QListWidget, QTreeWidget, QTableWidget {
            background-color: white;
            alternate-background-color: #f9f9f9;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
        
        QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {
            background-color: #e0f0ff;
            color: #333333;
        }
        
        QHeaderView::section {
            background-color: #e0e0e0;
            padding: 4px;
            border: 1px solid #cccccc;
        }
        
        QMenuBar {
            background-color: white;
            border-bottom: 1px solid #cccccc;
        }
        
        QMenuBar::item {
            spacing: 5px;
            padding: 4px 10px;
            background: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #e0f0ff;
            border-radius: 4px;
        }
        
        QMenu {
            background-color: white;
            border: 1px solid #cccccc;
        }
        
        QMenu::item {
            padding: 6px 20px 6px 20px;
        }
        
        QMenu::item:selected {
            background-color: #e0f0ff;
            color: #333333;
        }
        
        QStatusBar {
            background-color: #f0f0f0;
            color: #333333;
        }
        
        QToolTip {
            background-color: #ffffcc;
            color: #333333;
            border: 1px solid #cccccc;
            padding: 4px;
        }
        
        /* Estilos específicos para la calculadora */
        #titleLabel {
            font-size: 16pt;
            font-weight: bold;
            color: #4285f4;
        }
        
        #resultLabel {
            font-weight: bold;
            color: #2c3e50; 
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        
        #historyList {
            background-color: white;
            alternate-background-color: #f0f8ff;
        }
        """
    
    @staticmethod
    def get_dark_theme():
        """
        Obtiene el estilo para el tema oscuro.
        
        Returns:
            str: Hoja de estilos QSS para el tema oscuro.
        """
        return """
        QMainWindow, QDialog {
            background-color: #2d2d30;
        }
        
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
            color: #e0e0e0;
        }
        
        QGroupBox {
            font-size: 11pt;
            font-weight: bold;
            border: 1px solid #3e3e42;
            border-radius: 6px;
            margin-top: 14px;
            background-color: #1e1e1e;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #5e97f6;
        }
        
        QPushButton {
            background-color: #3a76d8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 10pt;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #5e97f6;
        }
        
        QPushButton:pressed {
            background-color: #2a66c8;
        }
        
        QPushButton:disabled {
            background-color: #444444;
            color: #888888;
        }
        
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 6px;
            border: 1px solid #3e3e42;
            border-radius: 4px;
            background-color: #2d2d30;
            color: #e0e0e0;
            selection-background-color: #3a76d8;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 1px solid #5e97f6;
        }
        
        QLabel {
            color: #e0e0e0;
        }
        
        QTabWidget::pane {
            border: 1px solid #3e3e42;
            border-radius: 4px;
            background-color: #1e1e1e;
        }
        
        QTabBar::tab {
            background-color: #2d2d30;
            color: #e0e0e0;
            padding: 8px 12px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #1e1e1e;
            border-bottom: 2px solid #5e97f6;
        }
        
        QScrollArea, QScrollBar {
            background-color: #1e1e1e;
            border-radius: 4px;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #2d2d30;
            width: 12px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3e3e42;
            min-height: 20px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #5e5e60;
        }
        
        QListWidget, QTreeWidget, QTableWidget {
            background-color: #1e1e1e;
            alternate-background-color: #252526;
            border: 1px solid #3e3e42;
            border-radius: 4px;
            color: #e0e0e0;
        }
        
        QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {
            background-color: #2d5fb3;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #2d2d30;
            padding: 4px;
            border: 1px solid #3e3e42;
            color: #e0e0e0;
        }
        
        QMenuBar {
            background-color: #1e1e1e;
            border-bottom: 1px solid #3e3e42;
        }
        
        QMenuBar::item {
            spacing: 5px;
            padding: 4px 10px;
            background: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #2d5fb3;
            border-radius: 4px;
            color: white;
        }
        
        QMenu {
            background-color: #1e1e1e;
            border: 1px solid #3e3e42;
        }
        
        QMenu::item {
            padding: 6px 20px 6px 20px;
        }
        
        QMenu::item:selected {
            background-color: #2d5fb3;
            color: white;
        }
        
        QStatusBar {
            background-color: #1e1e1e;
            color: #e0e0e0;
        }
        
        QToolTip {
            background-color: #2d2d30;
            color: #e0e0e0;
            border: 1px solid #3e3e42;
            padding: 4px;
        }
        
        /* Estilos específicos para la calculadora */
        #titleLabel {
            font-size: 16pt;
            font-weight: bold;
            color: #5e97f6;
        }
        
        #resultLabel {
            font-weight: bold;
            color: #e0e0e0; 
            padding: 8px;
            background-color: #252526;
            border-radius: 4px;
        }
        
        #historyList {
            background-color: #1e1e1e;
            alternate-background-color: #252526;
        }
        """
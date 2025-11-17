import customtkinter as ctk

class FrameB(ctk.CTkFrame):
    """
    Frame base para mantener un diseño uniforme en toda la aplicación.
    Aquí se definen estilos de fondo, bordes, padding, etc.
    """

    def __init__(self, master=None, **kwargs):

        # Valores por defecto para todos los frames
        base_style = {
            "fg_color": "#1E1E1E",     # color base oscuro
            "corner_radius": 10,
            "border_width": 2,
            "border_color": "#3A3A3A",
        }

        # Permite que el usuario sobreescriba parámetros si los manda
        base_style.update(kwargs)

        super().__init__(master, **base_style)

    # Ejemplo de método que todos los frames pueden usar
    def limpiar(self):
        """Elimina todos los widgets dentro del frame."""
        for widget in self.winfo_children():
            widget.destroy()
            
class ButtonB(ctk.CTkButton):
    """
    Botón estandarizado para toda la app.
    """

    def __init__(self, master=None, **kwargs):

        base_style = {
            "fg_color": "#3C7DD9",        # azul suave
            "hover_color": "#2F64AE",
            "text_color": "white",
            "corner_radius": 8,
            "height": 35,
            "font": ("Arial", 14, "bold"),
        }

        base_style.update(kwargs)

        super().__init__(master, **base_style)

# mesa_widget.py
from __future__ import annotations
import customtkinter as ctk
from typing import Callable, Optional

from models import Mesa, EstadoMesa
from frame import ButtonB


def color_por_estado(estado: EstadoMesa) -> str:
    """Devuelve un color según el estado de la mesa."""
    if estado == EstadoMesa.LIBRE:
        return "#2E8B57"  # verde tipo 'sea green'
    elif estado == EstadoMesa.OCUPADA:
        return "#B22222"  # rojo fuerte
    elif estado == EstadoMesa.RESERVADA:
        return "#DAA520"  # dorado/amarillo
    return "#3A3A3A"      # gris por defecto


class MesaWidget(ButtonB):
    """
    Widget base para representar una mesa.
    Hereda de ButtonB para mantener el estilo global de la app.
    """

    def __init__(
        self,
        master,
        mesa: Mesa,
        on_click: Optional[Callable[[Mesa], None]] = None,
        **kwargs
    ):
        self.mesa = mesa
        self._on_click = on_click

        texto = f"Mesa {mesa.id}\n{mesa.sillas} sillas"
        fg_color = color_por_estado(mesa.estado)

        base_style = {
            "text": texto,
            "fg_color": fg_color,
            "hover_color": fg_color,  # luego si quieres diferenciamos el hover
            "command": self._handle_click,
        }

        base_style.update(kwargs)

        super().__init__(master, **base_style)

    # ---------------- Métodos de comportamiento ---------------- #

    def _handle_click(self):
        """Callback interno cuando se hace click en la mesa."""
        if self._on_click:
            self._on_click(self.mesa)

    def actualizar_estado(self, nuevo_estado: EstadoMesa):
        """Actualiza el estado de la mesa y refresca el color."""
        self.mesa.estado = nuevo_estado
        nuevo_color = color_por_estado(nuevo_estado)
        self.configure(fg_color=nuevo_color, hover_color=nuevo_color)

    def colocar_en_plano(self):
        """
        Coloca el widget usando las coordenadas de la mesa.
        (pos_x, pos_y, ancho, alto) vienen de la tabla 'mesas'.
        """
        self.place(
            x=self.mesa.pos_x,
            y=self.mesa.pos_y,
            width=self.mesa.ancho,
            height=self.mesa.alto,
        )


# ----------------------------------------------------------
# Subclases para polimorfismo visual (rectangular / circular)
# ----------------------------------------------------------

class MesaRectangular(MesaWidget):
    """
    Representación rectangular de una mesa.
    Por ahora solo hereda de MesaWidget, pero aquí
    podrías cambiar fuentes, bordes, etc.
    """
    pass


class MesaCircular(MesaWidget):
    """
    Representación circular de una mesa.
    CustomTkinter no dibuja círculos reales en botones, pero este
    hook es útil por si quieres cambiar el estilo (ej: corner_radius alto).
    """
    def __init__(self, master, mesa: Mesa, on_click=None, **kwargs):
        kwargs.setdefault("corner_radius", 999)  # parece más 'redondo'
        super().__init__(master, mesa, on_click=on_click, **kwargs)


# ----------------------------------------------------------
# Factory: elige la clase adecuada según mesa.forma
# ----------------------------------------------------------

class MesaWidgetFactory:
    @staticmethod
    def crear_widget(
        master,
        mesa: Mesa,
        on_click: Optional[Callable[[Mesa], None]] = None,
        **kwargs
    ) -> MesaWidget:
        """
        Crea un widget de mesa según el campo 'forma' de la entidad Mesa.
        Ejemplos esperados: "rectangulo", "circulo".
        """
        forma = (mesa.forma or "").lower()

        if forma == "rectangulo":
            return MesaRectangular(master, mesa, on_click=on_click, **kwargs)
        elif forma == "circulo":
            return MesaCircular(master, mesa, on_click=on_click, **kwargs)
        else:
            # Si viene algo raro, usa el widget genérico
            return MesaWidget(master, mesa, on_click=on_click, **kwargs)

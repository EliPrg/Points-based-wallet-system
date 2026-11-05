# Definición de costantes para el sistema
from dataclasses import dataclass
# Niveles de lealtad
Niveles = {"Bronce": (0, 1), "Plata": (1000, 1.25), "Oro": (5000, 1.5)}
# Puntos por u.m.
UM_puntos = 10


# Clase interna de la configuración para los premios
@dataclass(frozen=True)
class configPremios:
    id_premio: str
    nombre: str
    costo: int
    stockInicial: int = 10


# Catalogo de premios
Catalogo = [configPremios("P01", "Café de cortesía", 100),
            configPremios("P02", "Cupón de descuento 10%", 250),
            configPremios("P03", "Gift card de 50 u.m.", 800),
            configPremios("P04", "Audífonos inalámbricos", 1200),
            configPremios("P05", "Fin de semana en hotel", 4000)]

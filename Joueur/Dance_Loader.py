#représente un mouvement de la chorégraphie
class DanceStep:
    """Représente un mouvement de la chorégraphie."""

    def __init__(self, nb_pas: int, direction: str):
        self.nb_pas = nb_pas
        self.direction = direction  # "U", "D", "L", "R", "B"

    def __repr__(self):
        return f"DanceStep({self.nb_pas}{self.direction})"


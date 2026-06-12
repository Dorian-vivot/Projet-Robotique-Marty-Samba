from pathlib import Path


Valid_Directions = {"U", "D", "L", "R", "B"}
Valid_Arms = {"ALU", "ARU", "ALB", "ARB"}
Valid_Expressions = {"XNT", "XSD", "XNG", "XHP", "XDN"}




#représente un mouvement de la chorégraphie
class DanceStep:
    

    def __init__(self, nb_pas: int, direction: str):
        if direction not in Valid_Directions:
            raise ValueError(f"Direction invalide : {direction!r}. "
                             f"Valeurs acceptées : {Valid_Directions}")
        self.nb_pas = nb_pas
        self.direction = direction  # "U", "D", "L", "R", "B"
        self.arms: str = ""
        self.expression: str = ""

    def __repr__(self):
        return f"DanceStep({self.nb_pas}{self.direction})"

#lie une couleur à ses événements associés
class Action_By_Color:

    def __init__(self, color: str, arms: list[str], expression: str):
        self.color = color
        self.arms = arms
        self.expression = expression

    def get_arms_string(self):
        return "+".join(self.arms)
    
    def __repr__(self):
        return (f"ColorAction(color={self.color!r} "
                f"arms={self.get_arms_string()!r} "
                f"exp={self.expression!r})")
    

class Dance_Loader:
    def __init__(self):
        self.steps: list[DanceStep] = []
        self.action_by_color: dict[str, Action_By_Color]= {}
        self.loaded: bool = False
        self.file_path: str = ""
    
    def load_path(self, path: str):
        contenu = Path(path).read_text()
        self.file_path = path
        self.loaded = True
        print(f"[DanceLoader] Chargé : {path} | "
            f"{len(self.steps)} mouvements | "
            f"{len(self.action_by_color)} règles ACT")

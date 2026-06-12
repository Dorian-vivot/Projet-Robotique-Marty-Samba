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
        self.parse(contenu)
        self.file_path = path
        self.loaded = True
        print(f"[DanceLoader] Chargé : {path} | "
            f"{len(self.steps)} mouvements | "
            f"{len(self.action_by_color)} règles ACT")
        
    def parse(self, content: str):
        lines = [line.strip() for line in content.splitlines()]
        try:
            action_index = next(index for index, line in enumerate(lines) if line.upper() == "ACT")
        except StopIteration:
            action_index = len(lines)
        self.steps = self.parse_sequence(lines[:action_index])
        self.action_by_color = self.parse_act(lines[action_index + 1:])

    
    @staticmethod
    def parse_step_line(line: str):
        line = line.strip().upper()
        if not line:
            return None
        nombre_str = ""
        direction = ""
        for char in line:
            if char.isdigit():
                nombre_str += char
            else:
                direction = char
        if direction not in Valid_Directions:
            return None
        return DanceStep(int(nombre_str), direction)
    
    def parse_sequence(self, lines: list[str]):
        steps = []
        for line in lines:
            if not line or line.upper().startswith("SEQ"):
                continue
            step = self.parse_step_line(line)
            if step:
                steps.append(step)
        return steps
    
    def parse_act(self, lines: list[str]):
        color_actions = {}
        for line in lines:
            if not line:
                continue
            mouvements = line.strip().upper().split()
            if len(mouvements) < 2:
                continue
            color = mouvements[0]
            arms = []
            expression = ""
            for mouvement in mouvements[1:]:
                if mouvement in Valid_Arms:
                    arms.append(mouvement)
                elif mouvement in Valid_Expressions:
                    expression = mouvement
            color_actions[color] = Action_By_Color(color, arms, expression)
        return color_actions

    def get_action_for_color(self, color: str):
        return self.action_by_color.get(color.strip().upper())

    def get_sequence(self, max_steps: int):
        if not self.loaded or not self.steps:
            return []

        nb_definis = len(self.steps)
        sequence = []
        for i in range(max_steps):
            src = self.steps[i % nb_definis]
            sequence.append(DanceStep(src.nb_pas, src.direction))
        return sequence
    
    def apply_color_to_step(self, step: DanceStep, color: str) -> None:
        action = self.get_action_for_color(color)
        if action:
            step.arms = action.get_arms_string()
            step.expression = action.expression



    def get_summary(self) -> str:
        if not self.loaded:
            return "Aucun fichier .dance chargé"
        lines = [
            f"Fichier : {self.file_path}",
            f"{len(self.steps)} mouvement(s) défini(s)",
            "",
            "Séquence :"
        ]
        for index, step in enumerate(self.steps, 1):
            lines.append(f"  {index}. {step.nb_pas} pas => {step.direction}")
        lines += ["", "Règles ACT :"]
        if self.action_by_color:
            for color, action in self.action_by_color.items():
                lines.append(f"  [{color}] bras={action.get_arms_string()!r} "
                              f"expression={action.expression!r}")
        else:
            lines.append("  (aucune règle définie)")
        return "\n".join(lines)
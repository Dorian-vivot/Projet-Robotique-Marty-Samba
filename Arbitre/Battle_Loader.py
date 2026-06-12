
from pathlib import Path
import re


class Rule:
 
    def __init__(self, elements: list[str], operator: str, points: int):
        self.elements = elements
        self.operator = operator
        self.points = points

    def matches(self, move_elements : set[str]):
        if self.operator == "AND":
            for element in self.elements:
                if element not in move_elements:
                    return False
            return True
        else:
            for element in self.elements:
                if element in move_elements:
                    return True
            return False
            
 
    def __repr__(self):
        separator = "+" if self.operator == "AND" else ","
        return f"Rule({separator.join(self.elements)} → {self.points:+d})"

#Charge et parse un fichier .battle puis calcule les points d'un mouvement.
class BattleLoader:
 
    def __init__(self):
        self.max_steps: int = 10
        self.rules_by_color: dict = {}
        self.loaded: bool = False
        self.file_path: str = ""

    #Charge les règles depuis un fichier .battle
    def load_path(self, path : str):

        contenu = Path(path).read_text()
        self.parse(contenu)
        self.file_path = path
        self.loaded = True
        
    #Parse une ligne du fichier .battle
    @staticmethod
    def _parse_rule(line: str):
        if "=" not in line:
            print(f"Ligne ignorée : {line}")
            return None

        parts = line.split("=")

        if len(parts) < 2:
            print(f"Ligne ignorée : {line}")
            return None

        combination = parts[0].strip()
        points_str = parts[1].strip()

        try:
            points = int(points_str)
        except ValueError:
            print(f"Ligne ignorée : {line}")
            return None

        elements = []

    # cass OR avec virgule
        if "," in combination:
            morceaux = combination.split(",")

            for morceau in morceaux:
                elements.append(morceau.strip().upper())

            operator = "OR"

        # cas AND avec +
        elif "+" in combination:
            morceaux = combination.split("+")

            for morceau in morceaux:
                elements.append(morceau.strip().upper())

            operator = "AND"

        # cas un seul élément
        else:
            elements.append(combination.strip().upper())
            operator = "AND"

        return Rule(elements, operator, points)
    #Parse le contenu d'un fichier .battle
    def parse(self, content: str) -> None:
        self.max_steps = 10
        self.rules_by_color = {}
        current_color: str | None = None
 
        for raw_line in content.splitlines():
            line = raw_line.strip()
 
            if not line or line.startswith("#"):
                continue
 
            if line.upper().startswith("MVS"):
                parts = line.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    self.max_steps = int(parts[1])
                continue
 
            color_match = re.fullmatch(r"\[([A-Z])\]", line)
            if color_match:
                current_color = color_match.group(1)
                if current_color not in self.rules_by_color:
                    self.rules_by_color[current_color] = []
                continue

            if "=" in line and current_color is not None:
                rule = self._parse_rule(line)
                if rule:
                    self.rules_by_color[current_color].append(rule)
    #Construit l'ensemble des éléments d'un mouvementpour pouvoir le comparer aux règles.
    def build_move_elements(self, arms: str, expression: str) -> set[str]: 

        move_elements: set[str] = set() 
        
        for element in (arms or "").split("+"):
            mouvement = element.strip().upper()
            if mouvement:
                move_elements.add(mouvement)

        expression_element = (expression or "").strip().upper()
        if expression_element:
            move_elements.add(expression_element)
        
        return move_elements 

        
    def score(self, color: str, arms: str, expression: str):
        if not self.loaded:
            return 0
        color=(color or "").strip().upper()
        if color not in self.rules_by_color:
            return 0
        
        move_elements = self.build_move_elements(arms, expression) 

        total_points = 0
        for rule in self.rules_by_color[color]:
            if rule.matches(move_elements):
                total_points += rule.points

        return total_points
    #Retourne un résumé des règles chargées
    def summary(self):
        if not self.loaded:
            return "Aucun fichier .battle chargé."
        
        lines = [f"Fichier : {self.file_path}", f"Mouvements max (MVS) : {self.max_steps}"]
        for color, rules in self.rules_by_color.items():
            lines.append(f"  [{color}]")
            for rule in rules:
                lines.append(f"    {rule}")
        return "\n".join(lines)
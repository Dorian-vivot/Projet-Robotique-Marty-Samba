
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
                if element not in move_elements:
                    return True
                return False
            
 
    def __repr__(self):
        separator = "+" if self.operator == "AND" else ","
        return f"Rule({separator.join(self.elements)} → {self.points:+d})"


class BattleLoader:
 
    def __init__(self):
        self.max_steps: int = 10
        self._rules_by_color: dict = {}
        self.loaded: bool = False
        self._file_path: str = ""

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

        if not points_str.isdigit():
            print(f"Ligne ignorée : {line}")
            return None

        points = int(points_str)

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
 
    def parse(self, content: str) -> None:
        self.max_steps = 10
        self._rules_by_color = {}
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
                if current_color not in self._rules_by_color:
                    self._rules_by_color[current_color] = []
                continue

            if "=" in line and current_color is not None:
                rule = self._parse_rule(line)
                if rule:
                    self._rules_by_color[current_color].append(rule)
        
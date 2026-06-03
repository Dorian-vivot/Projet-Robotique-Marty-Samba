import re
 
 
class BattleLoader:
 
    def __init__(self):
        self.max_steps: int = 10
        self._rules_by_color: dict = {}
        self.loaded: bool = False
        self._file_path: str = ""
 
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

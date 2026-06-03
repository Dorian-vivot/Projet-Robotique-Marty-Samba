class BattleLoader:
 
    def __init__(self):
        self.max_steps: int = 10
        self._rules_by_color: dict = {}
        self.loaded: bool = False
        self._file_path: str = ""

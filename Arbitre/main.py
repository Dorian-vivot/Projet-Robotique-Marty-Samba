from Battle_Loader import BattleLoader
if __name__ == "__main__":
    loader = BattleLoader()
    loader.parse("[N]\nALB+ARB=1\nALU+ARU=-2")
    for rule in loader._rules_by_color["N"]:
        print(rule)
    loader.parse("[N]\nALB+ARB=1\nALU,ARU=-1\nXSD=2")
    for rule in loader._rules_by_color["N"]:
        print(rule)

    loader.parse("[N]\nALB,ARB=1\nALU+ARU=2")
    move = {"ALB", "ALU", "XSD"}
    for rule in loader._rules_by_color["N"]:
        print(f"{rule}->match={rule.matches(move)}")


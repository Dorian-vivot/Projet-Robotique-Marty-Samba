from Battle_Loader import BattleLoader
if __name__ == "__main__":
    loader = BattleLoader()
    loader.parse("[N]\nALB+ARB=1\nALU+ARU=-2")
    for rule in loader._rules_by_color["N"]:
        print(rule)
    loader.parse("[N]\nALB+ARB=1\nALU,ARU=-1") 
  
    move = loader.build_move_elements("ALB+ARB", "XSD") 
    print(f"code du mouvement : {move}") 



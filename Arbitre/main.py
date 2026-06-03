from Battle_Loader import BattleLoader
if __name__ == "__main__":
    loader = BattleLoader()
    loader.parse("MVS 10")
    print(f"max_steps = {loader.max_steps}")
    loader.parse("mvS 3")
    print(f"max_steps2 = {loader.max_steps}")

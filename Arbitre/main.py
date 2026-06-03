from Battle_Loader import BattleLoader
if __name__ == "__main__":
    loader = BattleLoader()
    loader.parse("MVS 10\n[N]\n[B]\n[R]")
    print(f"max_steps       = {loader.max_steps}")
    print(f"couleurs lues   = {list(loader._rules_by_color)}")
    loader.parse("")
    print(f"couleurs lues   = {list(loader._rules_by_color)}")


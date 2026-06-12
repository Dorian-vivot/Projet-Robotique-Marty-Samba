import sys
from PyQt6.QtWidgets import QApplication, QWidget
from mainWindow import MainWindow
import Dance_Loader

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    action_noir = Dance_Loader.Action_By_Color("N", ["ARU", "ALB"], "XNG")
    action_bleu = Dance_Loader.Action_By_Color("B", [], "XSD")
    action_rouge = Dance_Loader.Action_By_Color("R", ["ALU"], "")
    print(action_noir)
    print(action_bleu)
    print(action_rouge)

    print(f"\nBras Noir : {action_noir.get_arms_string()!r}")
    print(f"Bras Bleu : {action_bleu.get_arms_string()!r}")

    step = Dance_Loader.DanceStep(2, "B")
    step.arms = action_noir.get_arms_string()
    step.expression = action_noir.expression
    print(step)

    sys.exit()
    main()
import math

"""
Classe pour gérer la conversion d'une couleur hexadécimal et qui renvoie une couleur standard
"""
class ColorAlgorithm():
    def __init__(self):
        self.STANDARD_COLOURS = {
            "Rouge": (125, 23, 33),
            "Vert": (47, 44, 41),
            "Bleu": (64, 65, 90),
            "Jaune": (17, 103, 37),
            "Rose" : (143, 33, 57),
            "Blanc": (255, 255, 255),
            "Gris": (128, 128, 128),
            "Noir": (0, 0, 0)
        }

    def get_color_hex_to_standard(self, hexColorCode) -> str | None:
        red_color = int(hexColorCode[0:2], 16)
        green_color = int(hexColorCode[2:4], 16)
        blue_color = int(hexColorCode[4:6], 16)

        color_identified = "None"
        max_distance = float('inf')

        for color_name, (red_standard, green_standard, blue_standard) in self.STANDARD_COLOURS.items():
            distance = math.sqrt((red_standard - red_color) ** 2 + (green_standard - green_color) ** 2 + (blue_standard - blue_color) ** 2)

            if distance < max_distance:
                max_distance = distance
                color_identified = color_name

        return color_identified
    

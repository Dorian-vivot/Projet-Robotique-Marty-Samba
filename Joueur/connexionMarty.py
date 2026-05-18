import martypy
 
IP = "127.0.0.1"  # à remplacer par la bonne ip
 
def connecter():
    marty = martypy.Marty(f"wifi/{IP}")
    print("Connecté !")
    return marty
 
def deconnecter(marty):
    marty.close()
    print("Déconnecté.")
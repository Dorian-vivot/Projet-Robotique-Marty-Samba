import martypy
 
IP = "192.168.0.105"  # à remplacer par la bonne ip
 
def connecter():
    marty = martypy.Marty("wifi", "192.168.0.105")
    print("Connecté !")
    return marty
 
def deconnecter(marty):
    marty.close()
    print("Déconnecté.")
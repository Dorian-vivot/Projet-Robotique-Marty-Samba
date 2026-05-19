from connexionMarty import connecter, deconnecter
 
marty = connecter()
 
#marche
marty.walk(1)                   # 1 pas en avant
marty.walk(1, step_length=-40)  # 1 pas en arrière
 
# bouger les bras
# 0 bras normal
# 30 bras levé
# -30 bras baissé
marty.arms(50, 0, 1000)    # lever bras droit
marty.arms(0, 50, 1000)    # lever bras gauche
marty.arms(50, 50, 1000)   # lever les deux bras
marty.arms(-50, -50, 1000) # deux bras en bas
marty.arms(0, 0, 1000)     # bras normal
 
# expressions
marty.eyes("normal")  # neutre  
marty.eyes("excited") # triste  
marty.eyes("angry")   # colère 
 
deconnecter(marty)
# Rapport de projet  
- etudiant 1: Christian ZHUANG  
- etudiant 2: Kemo Sané  

## I - Comportements implémentés:
### **hateFriend**:  
    Eviter les robots de la même equipe,  
    Sinon avancer tout droit
### **stalker**:  suivre les adversaires (architecture de subsomption)
    1. Evite les robots de la même équipe s'il en voit un, sinon
    2. Aller vers les robots adverses, sinon
    3. eviter les murs, sinon
    4. aller tout droit
### **enter**: longer les murs (arbre de décision)
    1. s'éloigner du mur si le robot est trop près
    2. se rapprocher du mur si le robot est trop éloigné

## II - __Strategie comportementale__:
    - S'arrête, si un adversaire est derrière le robot
    - Eviter les robots de la même équipe
    
    Puis 3 comportements différents selon le robotId:
    - Suivre les adversaires , sinon longer ou eviter les murs
    - Longer ou eviter les murs
    - Suivre les adversaires, sinon eviter les murs

 __Remarque__:  
On choisit de longer ou d'éviter les murs, selon l'itération de la partie. On change de comportement tous les 250 itérations.




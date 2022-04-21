# Rapport de projet  
- etudiant 1: Christian ZHUANG  
- etudiant 2: Kemo Sané  

## Comportements implémentés:
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

## Strategie comportementale
    3 strategies différentes selon le robotId:
    - Suivre les adversaires (stalker), sinon longer (enter) ou eviter les murs
    - Longer (enter) ou eviter les murs
    - Suivre les adversaires (stalker), sinon eviter les murs

 __Remarque__:  
On choisit de longer ou d'éviter les murs, selon l'itération de la partie. On change de comportement tous les 250 itérations




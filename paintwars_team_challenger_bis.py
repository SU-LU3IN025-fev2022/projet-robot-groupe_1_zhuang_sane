# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: Christian ZHUANG 
#  Prénom Nom: Kemo  SANE 
# ================================================================
import numpy as np

from pyroborobo import Pyroborobo

def get_team_name():
    return "[ AaAaAaA ]"

def step(robotId, sensors):
    # Senseurs
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]

    # Variables utilisé
    left = sensors["sensor_front_left"]
    right = sensors["sensor_front_right"]
    front = sensors["sensor_front"]
    s_front_left = sensors["sensor_front_left"]["distance_to_wall"]
    s_front_right = sensors["sensor_front_right"]['distance_to_wall']
    s_back_right = sensors["sensor_back_right"]['distance_to_wall']
    s_back_left = sensors["sensor_back_left"]['distance_to_wall']
    s_left = sensors["sensor_left"]["distance_to_wall"]
    s_right = sensors["sensor_right"]["distance_to_wall"]
    s_front = front["distance_to_wall"] 

    # ===========  Comportements de braitenberg  ============================
    def hateAll():
        translation = min(front["distance_to_wall"], front["distance_to_robot"])
        rotation = (-1) * (left["distance_to_wall"] +  left["distance_to_robot"]) + (1) *(right["distance_to_wall"] +  right["distance_to_robot"]) 
        return translation, rotation
    
    def hateBot():
        translation = front["distance_to_robot"]
        rotation = (-1) * left["distance_to_robot"] + 1 * right["distance_to_robot"]
        return translation, rotation
    
    def hateWall():
        translation = front["distance_to_wall"]
        rotation = (-1) * left["distance_to_wall"] + 1 * right["distance_to_wall"]
        return translation, rotation
    
    def loveBot():
        translation = front["distance_to_robot"]
        rotation = 1 * left["distance_to_robot"] + (-1) *right["distance_to_robot"]
        return translation, rotation
    
    def loveWall():
        translation = front["distance_to_wall"]
        rotation = 1 * left["distance_to_wall"] + (-1) *right["distance_to_wall"]
        return translation, rotation

    # ===========  Comportement Complexe ============================
    # Comportement par defaut
    def default():
        translation = 1
        rotation = 0
        if sensors["sensor_front_right"]["distance"] < 1:
            rotation = -0.5
        elif sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
            rotation = 0.5
        return translation, rotation
    
    # Evite les robots alliés
    def hateFriend():
        if left["isSameTeam"] or right["isSameTeam"] or sensors["sensor_left"]["isSameTeam"] or sensors["sensor_right"]["isSameTeam"] or front["isSameTeam"]:
            if sensors["sensor_left"]["distance_to_robot"]<1: return  1, 0.3
            if sensors["sensor_right"]["distance_to_robot"]<1: return  1, -0.3
            if front["distance_to_robot"]<0.5: return 1, 0.3
            return hateAll()
        return 1, 0
    # Architecture de subsomption:
    # 1. aller vers les robots si detecte un robot,  sinon
    # 2. eviter les murs si detecte un mur, sinon
    # 3. aller tout droit
    def subsomption():
        if left["distance_to_robot"]<1 or right["distance_to_robot"]<1:
            return loveBot()
        elif left["distance_to_wall"]<1 or right["distance_to_wall"]<1:
            if left["distance_to_wall"] == right["distance_to_wall"]: return 1, 0.5
            return hateWall()
        else: return 1, 0
    # Arbre de subsomption:
    # 1. eviter les allies si detecte robot alliés, sinon
    # 2. effectue le comportement subsomption
    def stalker():
        if left["isSameTeam"] or right["isSameTeam"]: return hateFriend()
        return subsomption()
    
    # Arbre de décision: longer les murs
    def enter():
        def alea(a, b, va, vb):
            if np.random.random_sample() < 0.5:
                if a: return 1, va
                if b: return 1, vb
            else: 
                if b: return 1, vb
                if a: return 1, va
        # Mur en face et sur un des cotes
        d = 0.3
        if (s_front<d and s_left<d) or (s_front<d and s_right<d):
            l = s_front<d and s_left<d
            r = s_front<d and s_right<d
            return alea(l, r, 1, -1)
        d = 0.5
        # Couloir
        if s_front_right<1 and s_right<1 and s_front_left<1 and s_left<1:
            return 1, 0

        # Mur sur un des cotes ou les deux
        if s_front_left<1 or s_front_right<1:
            if s_front_left - s_front_right < 0.01 : return 1, 1
            if s_front_left<d or s_front_right<d: return hateWall()
            return loveWall()
        if s_left<1 or s_right<1:
            if s_left<1 and s_right <1 : return 1, 0
            l = s_left<1
            r = s_right<1
            return alea(l, r, -0.3, 0.3)
        d = 0.3
        # Mur derriere droite ou grauche
        if  s_back_right<1 or s_back_left<1:
            if s_back_right<1 and s_back_left<1: return 1, 0 
            l = s_back_left<1
            r = s_back_right<1
            return alea(l, r, -0.3, 0.3)
        # Mur en face
        if s_front < 1:
             if np.random.random_sample() < 0.5: return 1, 0.5
             else: return 1, -0.5
        return 1, 0

    # Differents strategie selon le robotId
    # stalker + ( enter / default)
    def strat1():
        if left["distance_to_robot"]<1 or right["distance_to_robot"]<1 or front["distance_to_robot"]<1: return subsomption()
        if np.random.random_sample()<0.99: return enter()
        else:
            if s_left<1 and s_right==1: return 1, 1
            if s_right<1 and s_left==1: return 1, -1
            return default()
    # ( enter / default)
    def strat2():
        if np.random.random_sample()<0.99: return enter()
        else: 
            if s_left<1 and s_right==1: return 1, 1
            if s_right<1 and s_left==1: return 1, -1
            return default()
    # stalker + default
    def strat3():
        if left["distance_to_robot"]<1 or right["distance_to_robot"]<1 or front["distance_to_robot"]<1: return subsomption()
        return default()

    def detect_back(s):
        return s["isRobot"] and (not s["isSameTeam"]) and s["distance"]<1
    # Detecte si il y a un enemie qui le poursuit
    if detect_back(sensors["sensor_back"]): 
        return 0,0
    if left["isSameTeam"] or right["isSameTeam"] or sensors["sensor_left"]["isSameTeam"] or sensors["sensor_right"]["isSameTeam"] or front["isSameTeam"]: translation, rotation = hateFriend()
    else:
        if robotId<2: return strat1()
        elif robotId<3: return strat2()
        else: return strat3()
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))
    return translation, rotation
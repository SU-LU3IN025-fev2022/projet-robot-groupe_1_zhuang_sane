# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: ZHUANG Christian
#  Prénom Nom: Sané Kemo

import numpy as np

def get_team_name():
    return "[ AaAaAaA ]"

def step(robotId, sensors):
    def get_extended_sensors(sensors):
        for key in sensors:
            sensors[key]["distance_to_robot"] = 1.0
            sensors[key]["distance_to_wall"] = 1.0
            if sensors[key]["isRobot"] == True:
                sensors[key]["distance_to_robot"] = sensors[key]["distance"]
            else:
                sensors[key]["distance_to_wall"] = sensors[key]["distance"]
        return sensors
    sensors = get_extended_sensors(sensors)

    # Variables utilisé
    s_front_left = sensors["sensor_front_left"]["distance_to_wall"]
    s_front_right = sensors["sensor_front_right"]['distance_to_wall']
    s_back_right = sensors["sensor_back_right"]['distance_to_wall']
    s_back_left = sensors["sensor_back_left"]['distance_to_wall']
    s_left = sensors["sensor_left"]["distance_to_wall"]
    s_right = sensors["sensor_right"]["distance_to_wall"]
    s_front = sensors["sensor_front"]["distance_to_wall"] 
    left = sensors["sensor_front_left"]
    right = sensors["sensor_front_right"]

    # ===========  Comportements de braitenberg  ============================
    def hateAll():
        translation = min(sensors["sensor_front"]["distance_to_wall"], sensors["sensor_front"]["distance_to_robot"])
        rotation = (-1) * (left["distance_to_wall"] +  left["distance_to_robot"]) + (1) *(right["distance_to_wall"] +  right["distance_to_robot"]) 
        return translation, rotation
    
    def hateBot():
        translation = sensors["sensor_front"]["distance_to_robot"]
        rotation = (-1) * left["distance_to_robot"] + 1 * right["distance_to_robot"]
        return translation, rotation
    
    def hateWall():
        translation = sensors["sensor_front"]["distance_to_wall"]
        rotation = (-1) * left["distance_to_wall"] + 1 * right["distance_to_wall"]
        return translation, rotation
    
    def loveBot():
        translation = sensors["sensor_front"]["distance_to_robot"]
        rotation = 1 * left["distance_to_robot"] + (-1) *right["distance_to_robot"]
        return translation, rotation
    
    def loveWall():
        translation = sensors["sensor_front"]["distance_to_wall"]
        rotation = 1 * left["distance_to_wall"] + (-1) *right["distance_to_wall"]
        return translation, rotation

    # ===========  Comportement Complexe ============================
    def hateFriend():
        if left["isSameTeam"] or right["isSameTeam"]:
            if sensors["sensor_front"]["distance_to_robot"]<0.: return 1, 0.5
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
        return subsomption.step(robotId, sensors)
    # Arbre de décision: longer les murs
    def enter():
        if left["isSameTeam"] or right["isSameTeam"]: return hateFriend()
        d = 0.3
        # Mur en face et sur un des cotes
        if s_front<d and s_left<d: return 1, 1
        if s_front<d and s_right<d: return 1, -1
        # Mur sur un des cotes ou les deux
        if s_front_left<1 or s_front_right<1:
            if s_front_left - s_front_right < 0.1 : return 1, 1
            if s_front_left<0.3 or s_front_right<0.3: return hateWall()
            return loveWall()
        d = 0.3
        # Mur derriere droite ou grauche
        if np.random.random_sample() < 0.5:
            if s_back_right<d or s_right<d: return 1, 0.3
            if s_back_left<d or s_left<d: return 1, -0.3
        else: 
            if d<s_back_left<1 or d<s_left<1: return 1, -0.3
            if d<s_back_right<1 or d<s_right<1: return 1, 0.3
        # Mur en face
        if s_front < 1: return 1, 0.3
        return 1, 0

    translation, rotation = enter()
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))
    return translation, rotation


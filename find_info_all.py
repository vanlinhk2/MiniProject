import pandas as pd

def find_aside_info(aside_info):
    ls_aside1 = []
    ls_aside2 = []
    for item in aside_info:
        item1 = item.split()[-1]
        item2 = item.replace(item1, '').strip()
        ls_aside1.append(item2)
        ls_aside2.append(item1)
    aside = pd.DataFrame([ls_aside2], columns=ls_aside1)
    return aside

def find_info_attacking(attacking):
    crossing, finishing, heading_accuracy, short_passing, volleys = [], [], [], [], []

    for elem in attacking:
        elems = elem.split(maxsplit = 1)
        if elems[1] == "Crossing":
            crossing.append(elems[0])
        elif elems[1] == "Finishing":
            finishing.append(elems[0])
        elif elems[1] == "Heading accuracy":
            heading_accuracy.append(elems[0])
        elif elems[1] == "Short passing":
            short_passing.append(elems[0])
        elif elems[1] == "Volleys":
            volleys.append(elems[0])
    info_attacking = pd.DataFrame({
    "Crossing": crossing,
    "Finishing": finishing,
    "Heading accuracy": heading_accuracy,
    "Short passing" :short_passing,
    "Volleys": volleys
    })
    return info_attacking

def find_info_skill(skill):
    dribbling, curve, fk_accuracy, long_passing, ball_control = [], [], [], [], []

    for elem in skill:
        elems = elem.split(maxsplit = 1)
        if elems[1] == "Dribbling":
            dribbling.append(elems[0])
        elif elems[1] == "Curve":
            curve.append(elems[0])
        elif elems[1] == "FK Accuracy":
            fk_accuracy.append(elems[0])
        elif elems[1] == "Long passing":
            long_passing.append(elems[0])
        elif elems[1] == "Ball control":
            ball_control.append(elems[0])
    info_skill = pd.DataFrame({
    "Dribbling": dribbling,
    "Curve": curve,
    "FK Accuracy": fk_accuracy,
    "Long passing" :long_passing,
    "Ball control": ball_control
    })
    return info_skill



def find_info_movement(movement):
    acceleration, sprint_speed, agility, reactions, balance = [], [], [], [], []

    for elem in movement:
        elems = elem.split(maxsplit = 1)
        if elems[1] == "Acceleration":
            acceleration.append(elems[0])
        elif elems[1] == "Sprint speed":
            sprint_speed.append(elems[0])
        elif elems[1] == "Agility":
            agility.append(elems[0])
        elif elems[1] == "Reactions":
            reactions.append(elems[0])
        elif elems[1] == "Balance":
            balance.append(elems[0])
    info_movement = pd.DataFrame({
    "Acceleration": acceleration,
    "Sprint speed": sprint_speed,
    "Agility": agility,
    "Reactions" :reactions,
    "Balance": balance
    })
    return info_movement

def find_info_power(power):
    shot_power, jumping, stamina, strength, long_shots = [], [], [], [], []

    for elem in power:
        elems = elem.split(maxsplit = 1)
        if elems[1] == "Shot power":
            shot_power.append(elems[0])
        elif elems[1] == "Jumping":
            jumping.append(elems[0])
        elif elems[1] == "Stamina":
            stamina.append(elems[0])
        elif elems[1] == "Strength":
            strength.append(elems[0])
        elif elems[1] == "Long shots":
            long_shots.append(elems[0])
    info_power = pd.DataFrame({
    "Shot power": shot_power,
    "Jumping": jumping,
    "Stamina": stamina,
    "Strength" :strength,
    "Long shots": long_shots
    })
    return info_power

def find_info_mentality(mentality):
    aggression, interceptions, att_position, vision, penalties, composure = [], [], [], [], [], []

    for elem in mentality:
        elems = elem.split(maxsplit=1)
        if elems[1] == "Aggression":
            aggression.append(elems[0])
        elif elems[1] == "Interceptions":
            interceptions.append(elems[0])
        elif elems[1] == "Att. Position":
            att_position.append(elems[0])
        elif elems[1] == "Vision":
            vision.append(elems[0])
        elif elems[1] == "Penalties":
            penalties.append(elems[0])
        elif elems[1] == "Composure":
            composure.append(elems[0])
    
    info_mentality = pd.DataFrame({
        "Aggression": aggression,
        "Interceptions": interceptions,
        "Att. Position": att_position,
        "Vision": vision,
        "Penalties": penalties,
        "Composure": composure
    })
    
    return info_mentality

def find_info_defending(defending):
    defensive_awareness, standing_tackle, sliding_tackle = [], [], []

    for elem in defending:
        elems = elem.split(maxsplit=1)
        if elems[1] == "Defensive awareness":
            defensive_awareness.append(elems[0])
        elif elems[1] == "Standing tackle":
            standing_tackle.append(elems[0])
        elif elems[1] == "Sliding tackle":
            sliding_tackle.append(elems[0])
    
    info_defending = pd.DataFrame({
        "Defensive awareness": defensive_awareness,
        "Standing tackle": standing_tackle,
        "Sliding tackle": sliding_tackle
    })
    
    return info_defending


def find_info_goalkeeping(goalkeeping):
    gk_diving, gk_handling, gk_kicking, gk_positioning, gk_reflexes = [], [], [], [], []

    for elem in goalkeeping:
        elems = elem.split(maxsplit=1)
        if elems[1] == "GK Diving":
            gk_diving.append(elems[0])
        elif elems[1] == "GK Handling":
            gk_handling.append(elems[0])
        elif elems[1] == "GK Kicking":
            gk_kicking.append(elems[0])
        elif elems[1] == "GK Positioning":
            gk_positioning.append(elems[0])
        elif elems[1] == "GK Reflexes":
            gk_reflexes.append(elems[0])
    
    info_goalkeeping = pd.DataFrame({
        "GK Diving": gk_diving,
        "GK Handling": gk_handling,
        "GK Kicking": gk_kicking,
        "GK Positioning": gk_positioning,
        "GK Reflexes": gk_reflexes
    })
    
    return info_goalkeeping

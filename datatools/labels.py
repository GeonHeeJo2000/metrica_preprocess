import os, sys
import pandas as pd

# Pass labeling
def pass_label(events):
    pass_event = events[(events["eventType"] == "PASS")].copy()

    pass_dict = {'PASS':['PASS','HEAD','GOAL KICK','DEEP BALL','THROUGH BALL-DEEP BALL', 'CLEARANCE', 'HEAD-CLEARANCE',
                         'HEAD-INTERCEPTION-CLEARANCE', 'OFFSIDE','DEEP BALL-OFFSIDE'],
                 'BALL LOST' : ['INTERCEPTION','GOAL KICK-INTERCEPTION', 'CLEARANCE', 'GOAL KICK', 
                                'DEEP BALL', 'CLEARANCE-INTERCEPTION','THROUGH BALL-DEEP BALL-INTERCEPTION'],
                 'BALL OUT' : ['CLEARANCE', 'GOAL KICK', 'DEEP BALL', 'THROUGH BALL-DEEP BALL']
                 }
    
    # TYPE이 'PASS'이고 SUBTYPE이 pass_dict['PASS']에 포함된 값은 성공한 패스로 간주
    # type == 'PASS'인 모든 유형X -> 헤딩으로 패스한 데이터는 제외하기 위함
    success_condition = (pass_event['type'] == 'PASS') & (pass_event['subtype'].isin(pass_dict['PASS']))

    pass_event.loc[success_condition, 'outcome'] = True
    
    return pass_event

# dribble labeling
def dribble_label(events):
    dribble_event = events[events['eventType']=='DRIBBLE'].copy()

    for idx, row in dribble_event.iterrows():
        # DRIBBLE-WON vs CARRY는 성공/실패 분석과정이 다름 -> metrica1, 2과 3의 회사가 달라서 그런가?...
        # DRIBBLE-WON은 다음 이벤트의 subtype에 따라 결정되고
        # CARRY는 CARRY구간내 이벤트의 type에 따라 결정됨
        if row["subtype"] == "DRIBBLE-WON":
            next_frame = events.at[idx + 1, "start_frame"]
            related_events = events[(events['start_frame'] == next_frame)
                                 &(events['game_id'] == row['game_id'])]

            related_event_subtype_list = list(related_events['subtype'].values)

            if not any(related_event_subtype in ["THEFT", "INTERCEPTION"] for related_event_subtype in related_event_subtype_list):
                dribble_event["outcome"] = True

            continue

        #event로 알아내기
        related_events = events[(events['start_frame'] >= row['start_frame'])
                                 &(events['start_frame'] <= row['end_frame'])
                                 &(events['game_id'] == row['game_id'])]
        
        related_event_type_list = list(related_events['type'].values)

        if not any(related_event_type in ["BALL LOST", "BALL OUT"] for related_event_type in related_event_type_list):
            dribble_event["outcome"] = True
    
    return dribble_event

# Shot labeling
def shot_label(events):
    shot_event = events[events['eventType']=='SHOT'].copy()

    # 자살골은 제외
    shot_event['outcome'] = shot_event['goal']

    return shot_event

# Cross labeling
def cross_label(events):
    cross_event = events[events['eventType']=='CROSS'].copy()

    cross_dict = {'PASS':['CROSS'],
                 'BALL LOST' : ['CROSS-INTERCEPTION','CROSS'],
                 'BALL OUT' : ['CROSS']
                 }
    
    success_condition = (cross_event['type'] == 'PASS') & (cross_event['subtype'].isin(cross_dict['PASS']))

    cross_event.loc[success_condition, 'outcome'] = True

    return cross_event

# events Concat
def unified_labels(events):
    events["outcome"] = False

    pass_event = pass_label(events)
    dribble_event = dribble_label(events)
    shot_event = shot_label(events)
    cross_event = cross_label(events)
    
    pass_dribble_shot_cross = pd.concat([pass_event, dribble_event, shot_event, cross_event], axis=0)
    
    return pass_dribble_shot_cross

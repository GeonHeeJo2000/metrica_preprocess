import numpy as np
import pandas as pd

# event_type를 통일된 형태로 변환 -> 너무 많은 이벤트 유형은 분석을 복잡하게 변환
# 연구에 사용할 이벤트 타입: 패스, 슛, 드리블, 크로스
def identify_event_type(row):
    # event-definition에 따라 정의된 모든 패스 이벤트들을 파악한 결과, 모든 패스의 유형들을 정리함
    # row['type']이 'PASS', 'BALL LOST', 'BALL OUT' 중 하나이고 
    # row['subtype']이 해당 key의 value 값 중 하나일 때 패스로 식별함
    pass_dict = {'PASS':['PASS','HEAD','GOAL KICK','DEEP BALL','THROUGH BALL-DEEP BALL', 'CLEARANCE', 'HEAD-CLEARANCE',
                         'HEAD-INTERCEPTION-CLEARANCE', 'OFFSIDE','DEEP BALL-OFFSIDE'],

                 'BALL LOST' : ['INTERCEPTION','GOAL KICK-INTERCEPTION', 'CLEARANCE', 'GOAL KICK', 
                                'DEEP BALL', 'CLEARANCE-INTERCEPTION','THROUGH BALL-DEEP BALL-INTERCEPTION'],

                 'BALL OUT' : ['CLEARANCE', 'GOAL KICK', 'DEEP BALL', 'THROUGH BALL-DEEP BALL']
                 }

    if (row['type'] in pass_dict.keys()) and (row['subtype'] in pass_dict[row['type']]):
        return "PASS"
    elif row["type"] == "SHOT":
        return "SHOT" 
    # metrica1, 2 : CARRY는 없고, DRIBBLE-WON이 존재함
    # metrica3    : CARRY가 있음(데이터 수집 회사 차이?..)
    elif row["type"] == "CARRY" or row["subtype"] == "DRIBBLE-WON":
        return "DRIBBLE"

    # 패스와 크로스를 같은 타입으로 분리해서 사용하고 싶으면 아래와 같은 코드 사용
    if "CROSS" in row['subtype']:
        return "CROSS"
    
    return row["subtype"]
    
# 득점 여부를 판단
def identify_goal(events):

    # identify goals and own goals
    events["goal"] = events.apply(
            lambda row: row["type"] == "SHOT" and "-GOAL" in row["subtype"], axis=1
        )
    
    events["ownGoal"] = events.apply(
        lambda row: row["type"] == "BALL OUT" and "-GOAL" in row["subtype"], axis=1
    )
    
    return events

# 공격 방향을 나타내는 컬럼 생성
def set_play_direction(events, game_id):
    # 각 game_id에 따른 switch_sides 설정 -> 추후 공격 방향을 통일하기 위함
    # True : 전반전 원정-홈, 후반전 홈-원정
    # False: 전반전 홈-원정, 후반전 원정-홈

    # game_id=1(False) -> 전반전 : home(A)-away(B) & 후반적 : away(B)-home(A)
    # game_id=2(True)  -> 전반전 : away(B)-home(A) & 후반적 : home(A)-away(B)
    # game_id=3(False) -> 전반전 : home(B)-away(A) & 후반적 : away(A)-home(B)
    switch_sides_dict = {1 : False, 2 : True, 3 : False}
    switch_sides = switch_sides_dict[game_id]

     # 이벤트가 왼쪽에서 오른쪽으로 공격하면 True, 아니면 False
    events['is_left_to_right'] = False

    if switch_sides:
        events.loc[(events['team'] == 'Away') & (events['session'] == 1), 'is_left_to_right'] = True
        events.loc[(events['team'] == 'Home') & (events['session'] == 2), 'is_left_to_right'] = True
    else:
        events.loc[(events['team'] == 'Home') & (events['session'] == 1), 'is_left_to_right'] = True
        events.loc[(events['team'] == 'Away') & (events['session'] == 2), 'is_left_to_right'] = True

    return events

def unified_features(events, game_id):

    events = set_play_direction(events, game_id)
    events = identify_goal(events)
    events["eventType"] = events.apply(identify_event_type, axis=1)

    return events
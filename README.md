# metrica_preprocess
Metrica데이터셋 전처리 작업

- Metrica Sports Sample Data를 전처리하는 작업
- 공개되어있는 tracking-data를 활용하여 EPV, Un-xPass, PitchControl, Intended-receiver Prediction등 다양한 연구에 활용하기 위해 사전에 전처리한 작업
- 활용 이유: 기존 Metrica데이터셋은 이벤트유형이 다양하고, 이벤트 성공여부가 저장이 되어있지 않기 때문에 바로 사용하기에는 제약이 있음

작업 순서
----------------
1. https://github.com/metrica-sports/sample-data에서 data전부 다운로드(용량 제한때문에 일부만 첨부함)
2. notebook순서대로 실행
* 4-analyze-Intended-receiver.ipynb : 실패한 패스의 경우 패스의 의도를 알 수 없기 때문에 Intended-receiver의 정보("to"라는 컬럼)가 Nan으로 설정되어있다. 이는 실패한 패스를 분석할 때 제약이 있기 때문에 패스의 의도를 추가로 레이블링하였다.
* 레이블링은 두명의 연구자가 제작하고, 교차검증하여 수행했다. @menguri

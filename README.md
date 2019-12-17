# RTSim for test
테스트를 위해 코드 수정했습니다

## 1. 준비
__input 폴더에 적절한 input 넣어주세요
````
python taskgen.py
python ga.py
python rtsim.py
````
위 커맨드를 입력해서 개별로 실행해서 CPU-메모리 전력 소모 비율을 적절하게 맞추어 주세요

## 2. 테스트
````
python all.py
````
위 커맨드를 입력해서 테스트 횟수를 지정하면 테스트 결과가 콘솔 출력 됩니다.

## 3. 추가
GA 모드 시뮬레이션이 안된다면, input_ga의 PENALTY_RATIO를 높여보세요.

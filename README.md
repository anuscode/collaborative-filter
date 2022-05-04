# Collaborative Filtering Engine

# Prerequisites
1. 본 리뷰는 item based 및 배치 작업을 통해 적절한 데이터를 가져 올 수 있다는 가정 하에 작성 함.
2. 쿼리로 가져와야 할 자료는 matrix 혹은 matrix_p 참조.
   1. 우리 서비스에선 `star_score` 가 아닌 `시청시간`으로 해야 할 듯.

# 해당 소스코드 문제점
1. 어떻게 적절하게 정보를 미리 가져올지? (배치작업)
2. 피어슨 지수 계산이 너무 느림

# HOW TO SOLVE?
1. 배치작업 솔루션
   1. 쿼리로 해결 할 수 있을 것으로 사료 됨.
   2. 적절한 시간을 정하는 것이 관건
   3. 필요 시 단순하게 쿼리하고 파이썬으로 계산 후 메모리 값만 바꿔치면 될 것으로 생각 됨.

2. 피어슨 지수 계산 Faster
   1. 해당 matrix 에 각각의 mean 값을 미리 빼둔 값을 준비
   2. 해당 matrix 에 square 를 때린 값을 준비.
   3. 추천 받고싶은 벡터를 찾고 그 값을 faiss 로 각각 2번 곱함.
   4. 그 값을 피어슨 콜러레이션 방식으로 곱함.
   5. 매우 빠를 것으로 예상 함.

# RESULT
다크나이트 삽입 시
```text
             title  ...                                             genres
0  The Dark Knight  ...                   [Drama, Action, Crime, Thriller]
1       Prom Night  ...                        [Horror, Mystery, Thriller]
2   Wild Wild West  ...  [Action, Adventure, Comedy, Science Fiction, W...
3     Blue Thunder  ...  [Science Fiction, Action, Thriller, Crime, Drama]
4            Topaz  ...                 [Action, Drama, Mystery, Thriller]
```

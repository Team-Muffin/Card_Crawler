# Card Crawler

작성자: 김시은
<br />

## 1.Introduction

### Target Website

- Website: [Naver Card](https://card-search.naver.com/list?sortMethod=qc&isRefetch=true&bizType=CPC)
- Section: Credit Card Products

### Objective

- Parse the top 100 credit card products based on search ranking from Naver.

### Data Format

```
# CARD_NM(카드 이름): '신한카드 Deep Dream'
# CARD_IMG(카드 이미지 링크): 'https://vertical.pstatic.net/vertical-cardad/creatives/SH/2225/SH_2225_20220504-183134_hor.png'

# SMY_NOTI(요약정보_공지): '전월실적 한도없이 포인트 적립' (nullable)
# SMY_ANNUAL_FEE(요약정보_연회비): '국내 8천원, 해외 1만원'
# SMY_REWARDS(요약정보_연회비_보상): '신규 회원 최대 1만원 지급' (nullable)
# SMY_BASE_RECORD(요약정보_기준실적): '직전 1개월  합계 30만원 이상'
# SMY_BENEFIT1(요약정보_혜택1): '전월실적·적립한도 없이 0.7% 적립'
# SMY_BENEFIT2(요약정보_혜택2): '기본0.7%~최대3.5% 알아서 적립'

# TAGS (주요혜택 태그): ['연회비지원', '포인트/캐시백', '언제나할인', '영화', '편의점']
# BENEFITS (상세 혜택): '당신에게 Deep, 속깊은 디지털 라이프!연회비지원신규 고객 연회비 100% 캐시백! ...'
# TERMS (부가혜택 및 통합할인한도, 유의사항): ['부가혜택 및 통합할인한도[Deep Dream 카드의 더해드림 서비스]자주 가는 DREAM영역은 기본의 3배(총 2.1%) 포인트 적립!...', ...]'
```

<br />

## 2. Usage Instrunctions

### Requirements

```
pip install -r requirements.txt
```

### Run

```
./main.py
```

### Output

Check the crawling result on 'card.csv'

# gummy AI


## GPT-4 VS Mistral 비교 분석
이 파트에서는 2가지 AI 모델. GPT-4 (gpt-4-1106-preview) 와 Mistral(PiVoT-10.7B-Mistral-v0.2-RP) 을 비교 분석합니다. 이 비교는 텍스트 기반 인공지능 추리 게임 설정에서의 대화 생성 품질에 초점을 맞추고 있습니다.

### GPT-4 (gpt-4-1106-preview) 모델

#### 요청 및 응답
- __요청 :__ 
```JSON
{
  "content": "안녕? 어젯밤 일어난 사건에 대해 아는거 있어?",
  "npc_name": "애쉬"
}
```

- __응답 :__ 
```JSON
{
  "answer": "안녕, 탐정님! 어젯밤 사건이라니, 참으로 끔찍한 일이죠. 잠이 모자라서 온 마을이 수군거리고 있어요. 제가 알기로는, 레오가 늦은 밤까지 연주하고 있었다고 해요. 아마 그 시간에 뭔가 이상한 소리나 움직임을 목격했을 수도 있을 것 같아요. 물론 저는 장난치러 다니느라 그다지 많은 걸 보진 못했지만요. 하하, 장난은 장난일 뿐, 사건에 대해선 진지하게 생각하고 있답니다. 어쨌든, 주변에는 다양한 소문이 돌고 있으니, 조금 더 살펴보시는 게 좋을 거예요."
}
```

#### 분석
- __문맥 :__ 문맥 상 응답이 자연스러움.
- __문법 :__ 문법적으로 잘 구성되어 있음.
- __프롬 :__ NPC "애쉬" 의 성격과 사건에 대한 게임의 흐름을 잘 반영하고 있음.

### Mistral (PiVoT-10.7B-Mistral-v0.2-RP) 모델

#### 요청 및 응답
- __요청 :__ 
```JSON
{
  "content": "안녕? 어젯밤 일어난 사건에 대해 아는거 있어?",
  "npc_name": "애쉬"
}
```

- __응답 :__ 
```JSON
{
  "answer": "애쉬 says: 밤 10시 30분 정도 밖에서 밖에서 소리가 들렸고 밖에서 밖에서 소리가 들렸고 밖에서 소리가 들렸고 밖에서 소리가 들렸고 밖에서 소리가 들렸고 "
}
```

#### 분석
- __문맥 :__ 응답이 반복적이고 불완전함.
- __문법 :__ 문법적으로 끝맺음되지도 않고 말이 안됨.
- __프롬 :__ 프롬프트에 따른 적절한 대화를 생성하지 못함.


### 결론
- __GPT-4 :__ 상황에 적절하고 자연스러운 대화를 생성하는데 뛰어난 성능을 보임. 플레이어의 몰입감을 높이고 게임 진행에 필요한 정보를 제공하는데 유용함.
- __Mistral :__ 현재 모델 자체의 문제인지 데이터양의 문제인지 확인은 못했으나 반복적이고 불완전한 응답을 보이므로 실 적용 어려움. 설정이나 추가적인 최적화가 필요함.
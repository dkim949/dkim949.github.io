---
layout: page
title: RAG와 LLM을 활용한 기업 지식 관리 시스템 PoC
---

# RAG와 LLM을 활용한 기업 지식 관리 시스템 PoC

> **Duration**: 2 months  
> **Role**: Lead Data Scientist  
> **Scope**: AWS 기반 RAG 아키텍처 설계 및 LLM 파이프라인 구축

## Project Overview

대규모 언어 모델(LLM)의 발전과 함께, 기업 내부 지식을 효과적으로 활용하는 방법에 대한 관심이 높아지고 있습니다. 이 프로젝트에서는 **Retrieval-Augmented Generation (RAG)** 기술을 활용하여 기업 문서에서 정확한 정보를 검색하고, LLM을 통해 자연스러운 답변을 생성하는 시스템의 PoC를 진행했습니다.

## Problem Statement

### 기존 시스템의 한계

1. **정보 검색의 비효율성**
   - 방대한 내부 문서에서 필요한 정보를 찾는 데 많은 시간 소요
   - 키워드 기반 검색의 한계로 의미적으로 관련된 문서 누락

2. **LLM 단독 사용의 문제점**
   - Hallucination: 사실과 다른 정보 생성 위험
   - 최신 정보 반영 불가 (학습 데이터 기준 시점 제한)
   - 기업 특화 도메인 지식 부족

3. **비즈니스 요구사항**
   - 고객 문의 응대 시간 단축
   - 내부 직원의 정보 접근성 향상
   - 정확하고 신뢰할 수 있는 답변 제공

## Architecture Design

### RAG Pipeline Overview

```
[User Query] 
    ↓
[Query Embedding] → Amazon Bedrock (Titan Embeddings)
    ↓
[Vector Search] → Amazon OpenSearch Serverless
    ↓
[Context Retrieval] → Top-K Relevant Documents
    ↓
[Prompt Construction] → Query + Retrieved Context
    ↓
[LLM Generation] → Amazon Bedrock (Claude)
    ↓
[Response]
```

### AWS 서비스 구성

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Document Storage | Amazon S3 | 원본 문서 저장 |
| Vector Database | Amazon OpenSearch Serverless | 임베딩 벡터 저장 및 검색 |
| Embedding Model | Amazon Bedrock (Titan) | 텍스트 임베딩 생성 |
| LLM | Amazon Bedrock (Claude) | 답변 생성 |
| Orchestration | AWS Lambda | 파이프라인 조율 |
| API Gateway | Amazon API Gateway | RESTful API 제공 |

## Implementation Details

### 1. Document Processing Pipeline

문서 처리는 RAG 시스템의 성능을 좌우하는 핵심 단계입니다.

**Chunking Strategy**:
- Recursive Character Text Splitter 적용
- Chunk size: 500 tokens (overlap: 100 tokens)
- 문서 구조를 고려한 semantic chunking 시도

**Metadata Enrichment**:
- 문서 출처, 작성일, 카테고리 등 메타데이터 추가
- 검색 시 필터링 및 랭킹에 활용

### 2. Embedding and Indexing

```python
# Pseudo-code for embedding pipeline
def process_document(document):
    chunks = chunk_document(document, chunk_size=500, overlap=100)
    
    for chunk in chunks:
        embedding = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body={"inputText": chunk.text}
        )
        
        opensearch.index(
            index="knowledge-base",
            body={
                "content": chunk.text,
                "embedding": embedding,
                "metadata": chunk.metadata
            }
        )
```

### 3. Retrieval Strategy

단순한 벡터 유사도 검색을 넘어 여러 기법을 실험했습니다:

- **Hybrid Search**: 키워드 검색(BM25)과 벡터 검색 결합
- **Re-ranking**: Cross-encoder를 활용한 검색 결과 재정렬
- **Query Expansion**: LLM을 활용한 쿼리 확장으로 검색 recall 향상

### 4. Prompt Engineering

효과적인 답변 생성을 위한 프롬프트 설계:

```
You are a helpful assistant for [Company Name]. 
Answer the question based ONLY on the provided context.
If the context doesn't contain enough information, say "I don't have enough information to answer this question."

Context:
{retrieved_documents}

Question: {user_query}

Answer:
```

**프롬프트 최적화 포인트**:
- 명확한 역할 정의 (Role)
- 환각 방지를 위한 제약 조건 명시
- 출처 명시 요청으로 답변 신뢰도 향상

## Evaluation and Results

### 평가 지표

| Metric | Description | Result |
|--------|-------------|--------|
| Retrieval Precision@5 | 상위 5개 검색 결과 중 관련 문서 비율 | 78% |
| Answer Relevancy | 질문에 대한 답변의 관련성 (LLM 평가) | 4.2/5.0 |
| Faithfulness | 검색된 문서 기반 답변 충실도 | 91% |
| Response Latency | 평균 응답 시간 | 2.3s |

### Key Findings

1. **Chunking의 중요성**
   - Chunk 크기가 너무 작으면 문맥 손실, 너무 크면 관련 없는 정보 포함
   - 500 tokens가 해당 도메인에서 최적

2. **Hybrid Search의 효과**
   - 순수 벡터 검색 대비 precision 12% 향상
   - 특히 고유명사, 제품명 검색에서 효과적

3. **프롬프트 최적화 효과**
   - 출처 명시 요청 추가 시 사용자 신뢰도 향상
   - Few-shot 예시 추가로 답변 형식 일관성 확보

## Challenges and Solutions

### Challenge 1: 긴 문서 처리

**문제**: 일부 문서가 LLM의 context window를 초과

**해결책**: 
- Map-Reduce 패턴 적용: 각 chunk별 요약 후 통합
- 검색 결과의 우선순위화 및 context window 내 최적 배치

### Challenge 2: 도메인 특화 용어

**문제**: 업계 전문 용어에 대한 임베딩 품질 저하

**해결책**:
- 도메인 용어 사전 구축 및 query expansion에 활용
- Fine-tuning 대신 프롬프트에 용어 설명 포함

### Challenge 3: 답변 품질 일관성

**문제**: 동일한 질문에 대해 답변 품질 변동

**해결책**:
- Temperature 조정 (0.1로 낮춤)
- 답변 품질 모니터링 대시보드 구축
- Human-in-the-loop 피드백 시스템 설계

## Lessons Learned

1. **RAG는 만능이 아니다**
   - 검색 품질이 최종 답변 품질의 상한선을 결정
   - "Garbage In, Garbage Out" 원칙이 그대로 적용

2. **평가 체계의 중요성**
   - 자동화된 평가 메트릭과 인간 평가의 균형 필요
   - A/B 테스트를 통한 지속적 개선 체계 구축

3. **비용 최적화**
   - 캐싱 전략으로 반복 쿼리 비용 절감
   - 모델 선택 시 성능과 비용의 trade-off 고려

## Future Directions

- **Multi-modal RAG**: 이미지, 표 등 비정형 데이터 지원
- **Agent 기반 확장**: 복잡한 질문에 대한 다단계 추론
- **Fine-tuning 검토**: 도메인 특화 임베딩 모델 학습
- **프로덕션 배포**: 보안, 확장성, 모니터링 강화

## Conclusion

이 PoC를 통해 RAG 기술이 기업 지식 관리에 실질적인 가치를 제공할 수 있음을 확인했습니다. 특히 검색 품질 개선, 프롬프트 최적화, 평가 체계 구축이 성공적인 RAG 시스템의 핵심 요소임을 경험했습니다.

LLM 기술의 빠른 발전과 함께 RAG 아키텍처도 계속 진화하고 있으며, 이러한 기술을 비즈니스 문제에 효과적으로 적용하는 것이 앞으로의 중요한 과제입니다.

[Back to Works](/works/)

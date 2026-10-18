---
layout: page
lang: en
title: Enterprise Knowledge Management PoC with RAG and LLMs
---

# Enterprise Knowledge Management PoC with RAG and LLMs

> **Duration**: 2 months  
> **Role**: Lead Data Scientist  
> **Scope**: Designing a RAG architecture and building an LLM pipeline on AWS

## Project Overview

Advances in large language models (LLMs) have increased interest in making better use of internal company knowledge. In this project, I developed a proof of concept using **Retrieval-Augmented Generation (RAG)** to retrieve accurate information from company documents and generate natural-language answers with an LLM.

## Problem Statement

### Limitations of Existing Systems

1. **Inefficient Information Retrieval**
   - Finding relevant information across large collections of internal documents took considerable time
   - Keyword-based search missed semantically related documents

2. **Limitations of Using an LLM Alone**
   - Hallucination: the risk of generating information that is factually incorrect
   - No access to information beyond the training data cutoff
   - Limited knowledge of company-specific domains

3. **Business Requirements**
   - Reduce response times for customer inquiries
   - Improve employees' access to information
   - Provide accurate, reliable answers

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

### AWS Service Configuration

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Document Storage | Amazon S3 | Store source documents |
| Vector Database | Amazon OpenSearch Serverless | Store and search embedding vectors |
| Embedding Model | Amazon Bedrock (Titan) | Generate text embeddings |
| LLM | Amazon Bedrock (Claude) | Generate answers |
| Orchestration | AWS Lambda | Coordinate the pipeline |
| API Gateway | Amazon API Gateway | Expose a RESTful API |

## Implementation Details

### 1. Document Processing Pipeline

Document processing is a key factor in the performance of a RAG system.

**Chunking Strategy**:
- Applied a Recursive Character Text Splitter
- Chunk size: 500 tokens (overlap: 100 tokens)
- Experimented with semantic chunking that accounts for document structure

**Metadata Enrichment**:
- Added metadata such as document source, creation date, and category
- Used this metadata for filtering and ranking during retrieval

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

I experimented with several techniques beyond basic vector similarity search:

- **Hybrid Search**: Combined keyword search (BM25) with vector search
- **Re-ranking**: Reordered search results using a cross-encoder
- **Query Expansion**: Used an LLM to expand queries and improve retrieval recall

### 4. Prompt Engineering

A prompt designed to support effective answer generation:

```
You are a helpful assistant for [Company Name]. 
Answer the question based ONLY on the provided context.
If the context doesn't contain enough information, say "I don't have enough information to answer this question."

Context:
{retrieved_documents}

Question: {user_query}

Answer:
```

**Prompt Optimization Priorities**:
- Define the assistant's role clearly
- Specify constraints to reduce hallucinations
- Request source citations to make answers more trustworthy

## Evaluation and Results

### Evaluation Metrics

| Metric | Description | Result |
|--------|-------------|--------|
| Retrieval Precision@5 | Share of relevant documents among the top 5 results | 78% |
| Answer Relevancy | Relevance of the answer to the question (LLM-evaluated) | 4.2/5.0 |
| Faithfulness | How faithfully the answer reflects the retrieved documents | 91% |
| Response Latency | Average response time | 2.3s |

### Key Findings

1. **The Importance of Chunking**
   - Chunks that are too small lose context; chunks that are too large include irrelevant information
   - 500 tokens worked best for this domain

2. **The Benefits of Hybrid Search**
   - Improved precision by 12% compared with vector-only search
   - Particularly effective for proper nouns and product names

3. **The Impact of Prompt Optimization**
   - Requesting source citations improved user trust
   - Adding few-shot examples made answer formatting more consistent

## Challenges and Solutions

### Challenge 1: Processing Long Documents

**Problem**: Some documents exceeded the LLM's context window.

**Solution**:
- Applied a Map-Reduce pattern: summarize each chunk, then combine the summaries
- Prioritized retrieval results and arranged them to make the best use of the context window

### Challenge 2: Domain-Specific Terminology

**Problem**: Embeddings were less effective for industry-specific terminology.

**Solution**:
- Built a domain glossary and used it for query expansion
- Included terminology explanations in prompts instead of fine-tuning

### Challenge 3: Consistent Answer Quality

**Problem**: Answer quality varied for the same question.

**Solution**:
- Lowered the temperature to 0.1
- Built a dashboard to monitor answer quality
- Designed a human-in-the-loop feedback system

## Lessons Learned

1. **RAG Is Not a Cure-All**
   - Retrieval quality sets the ceiling for answer quality
   - The principle of "Garbage In, Garbage Out" still applies

2. **The Importance of an Evaluation Framework**
   - Automated metrics need to be balanced with human evaluation
   - Established a process for continuous improvement through A/B testing

3. **Cost Optimization**
   - Used caching to reduce the cost of repeated queries
   - Considered the trade-off between performance and cost when selecting models

## Future Directions

- **Multimodal RAG**: Support images, tables, and other unstructured data
- **Agent-Based Extensions**: Use multi-step reasoning for complex questions
- **Exploring Fine-Tuning**: Train domain-specific embedding models
- **Production Deployment**: Strengthen security, scalability, and monitoring

## Conclusion

This proof of concept showed how RAG can bring practical value to enterprise knowledge management. The work highlighted retrieval quality, prompt optimization, and a sound evaluation framework as key elements of a successful RAG system.

RAG architectures continue to evolve alongside rapid advances in LLMs. Applying these technologies effectively to business problems remains an important challenge.

[Back to Works](/works/)

## AI Knowledge Platform :

An end-to-end AI knowledge platform built from first principles, combining RAG, hybrid retrieval, vector search, local LLM inference, multi-agent orchestration, and MCP.
A production-oriented AI engineering project that allows users to upload documents, build searchable knowledge bases, ask source-grounded questions, and perform multi-step research using custom AI agents.
The project focuses on understanding and implementing the internal components of modern AI systems rather than hiding them behind high-level frameworks such as LangChain or LangGraph.

##Why This Project?
This project was built to explore what happens inside an AI application, beyond simply calling an LLM API.

It covers the complete pipeline:

Document
   ↓
PDF Extraction
   ↓
Cleaning & Chunking
   ↓
Embeddings
   ↓
Vector Database
   ↓
Hybrid Retrieval
   ↓
Context Construction
   ↓
Local LLM
   ↓
Grounded Answer
   ↓
Citations

It also extends the RAG pipeline into a custom multi-agent research system:

User Question
      ↓
Planner
      ↓
Task Decomposition
      ↓
Researcher
      ↓
Retriever
      ↓
Writer
      ↓
Reviewer
      ↓
Reflection / Revision
      ↓
Final Answer


## Key Highlights:

-> Custom RAG pipeline built from scratch

-> Hybrid retrieval using pgvector + PostgreSQL full-text search

-> Retrieval evaluation with measurable Recall@5

-> Improved retrieval recall from 0.73 → 0.83

-> Reciprocal Rank Fusion (RRF) for result merging

-> Sentence Transformer embeddings

-> PostgreSQL + pgvector vector search

-> Local LLM inference using Ollama

-> Streaming LLM responses

-> Source and page-level citations

-> Configurable chunking strategies

-> Multi-agent research workflow

-> Planner → Researcher → Writer → Reviewer → Reflection

-> MCP integration for external tools

-> JWT authentication and user-level authorization

-> Unit, integration, and API testing

-> FastAPI backend + Next.js frontend

-> Evaluation-driven engineering rather than assumption-driven optimization

## System Architecture
                              USER
                                │
                                ▼
                        ┌──────────────┐
                        │   Next.js    │
                        │   Frontend   │
                        └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   FastAPI    │
                        │   Backend    │
                        └──────┬───────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
        Documents             RAG           AI Agents
             │                 │                 │
             ▼                 ▼                 ▼
        PDF Extraction    Hybrid Search       Planner
             │                 │                 │
          Cleaning        pgvector + FTS      Researcher
             │                 │                 │
          Chunking             │               Writer
             │                 │                 │
        Embeddings             │              Reviewer
             │                 │                 │
             └────────────┐    │            Reflection
                          │    │                 │
                          ▼    ▼                 │
                       PostgreSQL                │
                       + pgvector               │
                          │                     │
                          └──────────┬──────────┘
                                     ▼
                              Context Builder
                                     │
                                     ▼
                              Prompt Builder
                                     │
                                     ▼
                               Ollama / LLM
                                     │
                                     ▼
                          Streaming Grounded Answer
                                     │
                                     ▼
                              Sources / Citations

## RAG Pipeline
The core of the platform is a custom Retrieval-Augmented Generation pipeline.

The implementation separates ingestion, retrieval, context construction, and generation into independently testable services.

1) Document Ingestion
PDF
 ↓
Text Extraction
 ↓
Cleaning
 ↓
Normalization
 ↓
Chunking
 ↓
Embedding Generation
 ↓
PostgreSQL + pgvector

PDF Extraction
PDF text is extracted while preserving page information.

This is important because retrieved content can later be connected back to its original page for source attribution.

Text Cleaning
Extraction artifacts and unnecessary formatting are normalized before chunking.

Configurable Chunking
The system supports multiple chunking strategies:

Fixed-size sliding window

Sentence-aware chunking

Semantic chunking

The purpose is to experiment with how chunk boundaries affect retrieval quality.

Embeddings
Each chunk is converted into a vector using a Sentence Transformer model.

Document Chunk
      ↓
Sentence Transformer
      ↓
384-dimensional embedding

These embeddings allow semantically related content to be retrieved even when the exact wording differs.

2) Vector Storage
Document chunks and embeddings are stored in:

PostgreSQL + pgvector

Stored information includes:

User ownership

Knowledge base

Document metadata

Page number

Chunk content

Embedding vector

The vector database allows semantic similarity search directly inside PostgreSQL.

Question
   ↓
Query Embedding
   ↓
pgvector
   ↓
Cosine Similarity
   ↓
Relevant Chunks

3) Hybrid Retrieval
One of the major engineering improvements in the project was moving beyond pure vector search.

Initial Approach: Vector Search
The original retrieval system used cosine similarity between the query embedding and stored document embeddings.

Query
 ↓
Embedding
 ↓
pgvector
 ↓
Cosine Similarity
 ↓
Top-K

This worked well for conceptual questions but exposed a weakness:

semantic search is not always good at exact facts.

Examples include:

Names

Numbers

Identifiers

Technical terms

Short factual statements

## Evaluation-Driven Retrieval Optimization
Instead of changing retrieval based on intuition, a fixed evaluation set of 10 real questions was created.

Each question had verified expected terms from the source documents.

The evaluation measured whether expected information appeared in the Top-5 retrieved chunks.

Baseline
Vector-only retrieval

Average Recall@5 = 0.73

Several failures were identified, including:

Q6 → Plant Watering System
Recall = 0.33

Q8 → Internship Supervisor
Recall = 0.00

Q9 → Total Internship Hours
Recall = 0.00

This provided a measurable baseline before optimization.

---->>> Keyword + Vector Retrieval
To address exact-match failures, PostgreSQL Full-Text Search was added.

A generated tsvector column and GIN index were used for efficient keyword retrieval.

Query
 │
 ├───────────────┐
 ▼               ▼
Vector Search   Full-Text Search
 │               │
 │               │
 └───────┬───────┘
         ▼
      RRF Merge
         ▼
      Top-K

The keyword search complements semantic retrieval by directly matching important terms.

--->>  Reciprocal Rank Fusion
The two ranked result lists are combined using Reciprocal Rank Fusion (RRF).

Conceptually:

RRF score = Σ 1 / (k + rank)

A chunk that appears highly in both retrieval systems receives a stronger combined score.

This avoids directly comparing incompatible score scales such as:

cosine distance

PostgreSQL text-ranking score

Instead, the system combines the rank positions.

## Retrieval Results
The exact same evaluation set was run before and after the retrieval change.

Metric	Vector Search	Hybrid Search
Average Recall@5	0.73	0.83
Q8: Internship Supervisor	0.00	1.00
Q6: Plant Watering	0.33	0.33
Q9: Total Hours	0.00	0.00

Result
Recall improved from 0.73 → 0.83

That's approximately a 13.7% relative improvement.

More importantly, Q8 went from:

0.00 → 1.00

showing that keyword retrieval recovered an exact factual lookup that semantic retrieval had missed.

##  Failure Analysis
The evaluation also exposed problems that retrieval alone could not solve.

Q6 — Plant Watering System
The relevant information was located inside a large table/logbook chunk.

Because many unrelated rows were stored together:

The embedding became less focused.

Keyword relevance was diluted.

Important terms were harder to retrieve.

Root cause
Chunking strategy was not table-aware.

Q9 — Internship Hours
Investigation of the raw database content revealed a PDF extraction problem.

The source text contained:

Tot al Hours

instead of:

Total Hours

Therefore, even keyword search could not reliably match the expected phrase.

Root cause
PDF table extraction corrupted the source text.

This was documented rather than artificially hidden from the evaluation.

It demonstrates an important RAG engineering lesson:

Retrieval quality depends not only on the search algorithm, but also on the quality and structure of the indexed data.

## Other Retrieval Experiments
The project also evaluated several additional techniques.

Query Rewriting
A local Ollama model was used to rewrite vague queries before retrieval.

The experiment showed that:

Unconstrained rewriting could hallucinate unrelated context.

Additional domain instructions reduced hallucination.

Rewriting still produced no measurable retrieval improvement.

Decision
Implemented → Tested → No measurable benefit → Not deployed

This is an intentional engineering decision rather than assuming every RAG technique improves performance.

Metadata Filtering
Metadata filtering is implemented for:

User

Document

Knowledge base

This provides both retrieval precision and access isolation.

The mechanism has been tested, while broader retrieval evaluation is planned once the system contains multiple documents and knowledge bases.

Cross-Encoder Reranking
Cross-encoder reranking was considered as a second-stage retrieval optimization.

It was not added because:

Hybrid retrieval already produced a measurable improvement.

It adds additional inference cost and complexity.

Current project constraints favor a lightweight local architecture.


## Multi-Agent Research System
The platform extends beyond standard question-answering with a custom multi-agent workflow.

                     User Question
                           │
                           ▼
                       Planner
                           │
                  Task Decomposition
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
        Research Task 1             Research Task 2
             │                           │
             ▼                           ▼
        Researcher                  Researcher
             │                           │
             └─────────────┬─────────────┘
                           ▼
                     Research Results
                           │
                           ▼
                         Writer
                           │
                           ▼
                       Reviewer
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
               Accept             Reject
                  │                 │
                  ▼                 ▼
             Final Answer       Reflection
                                    │
                                    ▼
                                  Revision
                                    │
                                    └──────► Reviewer

1) Planner Agent

Breaks a complex question into smaller research tasks.

Responsibilities:

Understand the objective

Decompose the problem

Generate structured tasks

Validate the generated plan

Handle invalid LLM output

2) Researcher Agent
Executes research tasks using the same retrieval infrastructure as the RAG pipeline.

Research Task
      ↓
Retriever
      ↓
Relevant Chunks
      ↓
Local LLM
      ↓
Research Result

This prevents the agent system from maintaining a completely separate knowledge retrieval system.

3) Writer Agent
Combines research results into a coherent response.

The writer does not independently search the database; it operates on structured research context.

4) Reviewer Agent
Reviews generated responses for:

Missing information

Unsupported claims

Inconsistency

Incomplete reasoning

Poor answer quality

5) Reflection Loop
If the reviewer rejects the answer:

Draft
 ↓
Review
 ↓
Issues
 ↓
Reflection
 ↓
Revision
 ↓
Review

This creates an explicit iterative generation workflow rather than a single LLM call.

## Model Context Protocol
The platform also experiments with Model Context Protocol (MCP) for connecting AI workflows with external tools.

AI Agent
   ↓
MCP Client
   ↓
MCP Server
   ↓
Tool / Resource
   ↓
External System

Implemented MCP capabilities include:

Filesystem interaction

File and folder search

PostgreSQL interaction

Database schema exploration

GitHub repository interaction

This demonstrates how agents can be extended beyond the internal knowledge base.

## Local LLM Architecture
Instead of making every generation request to a hosted LLM API, the project supports local LLM inference using Ollama.

Application
     ↓
LLM Service
     ↓
Ollama
     ↓
Local Model
     ↓
Streaming Tokens
     ↓
FastAPI
     ↓
Frontend

Why local inference?
No per-request API cost during development

Reduced dependency on external services

Better control over development data

Ability to experiment with different local models

Useful for self-hosted AI experimentation

The LLM layer is isolated behind a service abstraction, allowing the underlying provider/model to be changed without redesigning the RAG pipeline.


## Streaming Generation
The application supports streaming responses.

User
 ↓
/chat/stream
 ↓
Retrieval
 ↓
Context Construction
 ↓
Ollama
 ↓
Token Stream
 ↓
Frontend

Instead of waiting for the entire answer to be generated, tokens are returned progressively to the client.

## Source Grounding
The system preserves the relationship between retrieved chunks and their original documents.

Generated Answer
      │
      ├── Document
      ├── Page
      └── Retrieved Chunk

This allows generated answers to be connected back to source material and reduces the risk of unsupported responses.

## Authentication & Authorization
The backend supports multi-user access using JWT authentication.

Features include:

User registration

Login

Password hashing

JWT access tokens

Protected endpoints

User-specific document access

Knowledge-base ownership

Document-level filtering

Retrieval is therefore not simply:

Query → Search Everything

but instead:

User
 ↓
Authorized Knowledge Base
 ↓
Metadata Filtering
 ↓
Retrieval

## Database Design
The main entities are:

User
 │
 ├── Knowledge Bases
 │       │
 │       └── Documents
 │              │
 │              └── Chunks
 │                    │
 │                    └── Embeddings
 │
 └── Conversations

PostgreSQL
Used for:

Application data

Users

Documents

Knowledge bases

Chat history

Metadata

pgvector
Used for:

Embedding storage

Cosine similarity search

Semantic retrieval

PostgreSQL Full-Text Search
Used for:

Keyword retrieval

Exact term matching

Hybrid search

Alembic
Used for database migrations.

## Testing Strategy
Testing covers the AI pipeline at multiple levels.

Unit Tests
Individual components are tested independently.

Component	   Tests
Text cleaning	1
Chunking	      2
PDF extraction	3
Embeddings	      3
Prompt builder	5
LLM service	      3
Planner agent	5
Researcher agent	5
Retrieval service	3
Vector search	4

All tests shown above passed.

Integration Tests
The project tests interactions between real components.

Retrieval Integration
RetrievalService
      ↓
Search
      ↓
Sentence Transformer
      ↓
PostgreSQL
      ↓
pgvector
      ↓
Retrieved Results

RAG Context Integration
Hybrid Search
      ↓
Retrieved Chunks
      ↓
Context Builder
      ↓
LLM Context

LLM Integration
The streaming LLM path is also integration-tested using the local Ollama setup.

API Tests
FastAPI endpoints are tested independently.

Current API coverage includes the application health endpoint.

python -m pytest app/test/api/test_health.py -v

## Test Results
The demonstrated test runs include:

Unit tests: cleaning, chunking, extraction, embeddings, prompting, LLM, agents, retrieval

Integration tests: retrieval, RAG context, LLM

API tests: health endpoint

Every test execution shown during development completed successfully.

Run the complete suite with:

python -m pytest -v



## Running Locally
Requirements
Python 3.12+

PostgreSQL

pgvector

Node.js + npm

Ollama for local LLM inference

Git

Backend
git clone https://github.com/Rishika70592/AI_knowledge_platform.git
cd AI_knowledge_platform

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r app/requirements.txt

Configure environment variables:

DATABASE_URL=postgresql://username:password@localhost:5432/ai_knowledge_platform
SECRET_KEY=your_secret_key
OLLAMA_BASE_URL=http://localhost:11434

Run migrations:

alembic upgrade head

Start the backend:

uvicorn app.main:app --reload

Backend:

http://localhost:8000

Swagger:

http://localhost:8000/docs

Frontend
cd frontend
npm install
npm run dev

Frontend:

http://localhost:3000

Tests
python -m pytest -v



## Engineering Decisions & Lessons
This project is intentionally built around measurement and experimentation.

1. Don't assume semantic search solves everything
Vector search is excellent for semantic similarity but can miss exact facts.

2. Retrieval methods have complementary failure modes
Semantic and keyword retrieval solve different problems.

Hybrid retrieval combines their strengths.

3. Evaluate before optimizing
The fixed evaluation set made it possible to measure:

0.73 → 0.83

rather than simply claiming that retrieval "felt better."

4. More complex does not automatically mean better
Query rewriting was implemented and evaluated but deliberately not deployed because it did not improve retrieval quality with the selected local model.

5. Data quality is part of AI system quality
The remaining retrieval failures were traced to:

Poor table chunking

PDF extraction corruption

This demonstrates that improving an AI system is not always about changing the model.

6. AI components should be independently testable
The project separates:

Ingestion
   ↓
Chunking
   ↓
Embeddings
   ↓
Storage
   ↓
Retrieval
   ↓
Context
   ↓
Generation
   ↓
Agents

This makes individual components easier to evaluate, replace, and debug.



## What This Project Demonstrates

The primary goal was not simply to build an application that can call an LLM.

It demonstrates the ability to design and reason about an AI system across multiple layers:

                 AI ENGINEERING
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Retrieval       Agents          LLM
        │              │              │
     Embeddings      Planning       Prompting
     Vector DB       State          Streaming
     Hybrid Search   Tools          Local Inference
     Evaluation      Reflection
        │              │
        └──────────────┼──────────────┘
                       ▼
                 AI Application
                       │
                 FastAPI + Next.js
                       │
                 PostgreSQL

The project demonstrates end-to-end AI engineering, from raw documents and retrieval infrastructure to LLM generation, multi-agent workflows, evaluation, testing, and tool integration.


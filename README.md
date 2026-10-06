# AI Knowledge Platform

> A custom AI knowledge platform built from first principles,
> featuring RAG, vector search, MCP, and multi-agent orchestration.

## Overview
AI Knowledge Platform

An AI-powered knowledge platform built from first principles to explore and implement modern AI engineering concepts.

The platform allows users to upload documents, process and embed their content, perform semantic and hybrid retrieval, and ask questions using a custom Retrieval-Augmented Generation (RAG) pipeline.

Beyond RAG, the project explores LLM integration, vector search, multi-agent orchestration, Model Context Protocol (MCP), authentication, evaluation, and backend engineering without relying on high-level AI orchestration frameworks such as LangChain or LangGraph for the core pipeline.

Overview
What This Project Demonstrates

Custom PDF document ingestion and text processing

Configurable document chunking

Embedding generation using Sentence Transformers

PostgreSQL with pgvector for vector storage and similarity search

Custom RAG pipeline built from scratch

Hybrid retrieval and metadata filtering

Context and prompt construction

LLM integration with streaming responses

Source-grounded answers and citations

JWT-based authentication and multi-user support

AI agent workflow with planning, research, writing, and review

Model Context Protocol (MCP) integration

Unit, integration, and API testing

Next.js frontend integrated with a FastAPI backend

## Architecture
                         User
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
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Documents         RAG         AI Agents
             │             │             │
             ▼             ▼             ▼
        PDF Extraction   Retrieval      MCP
             │             │             │
             ▼             ▼             ▼
         Chunking     PostgreSQL       Tools
             │          + pgvector
             ▼             │
       Embeddings          │
             │             ▼
             └──────►  Context
                          │
                          ▼
                         LLM
                          │
                          ▼
                    Final Answer

Testing

The project includes unit, integration, and API tests covering the core document processing, embedding, retrieval, RAG, LLM, and agent components.

All tests executed during development passed successfully.


## Key Features

LM-powered chat with streaming responses

PDF document ingestion with text extraction and preprocessing

Configurable document chunking for efficient retrieval

Semantic embeddings using Sentence Transformers

PostgreSQL + pgvector for vector storage and similarity search

Custom RAG pipeline built without LangChain or LangGraph

Hybrid retrieval combining semantic and keyword-based search

Top-k similarity search with document and user filtering

Context-aware prompt construction for grounded answers

Source/citation generation to connect answers with retrieved documents

Multi-agent research workflow with:

Planner Agent

Researcher Agent

Retriever

Writer

Reviewer/Reflection

MCP integration for connecting AI agents with external tools

JWT authentication and user-specific document access

Database migrations using Alembic

REST API built with FastAPI

Unit, integration, and API testing with pytest

Health-check endpoint for backend monitoring

Environment-based configuration for local development and deployment

## RAG Pipeline




RAG Pipeline

The platform implements a custom Retrieval-Augmented Generation (RAG) pipeline from the ground up. The retrieval, chunking, embedding, ranking, context construction, and prompt-building components are implemented as independent services rather than relying on high-level orchestration frameworks.

The pipeline is divided into three major stages:

Document Ingestion

Information Retrieval

Context Construction & Generation

Complete RAG Architecture
                           DOCUMENT INGESTION
                                  │
                                  ▼
                           PDF Upload
                                  │
                                  ▼
                          Text Extraction
                                  │
                                  ▼
                       Cleaning & Normalization
                                  │
                                  ▼
                         Document Chunking
                                  │
                                  ▼
                       Embedding Generation
                                  │
                                  ▼
                       PostgreSQL + pgvector
                                  │
                                  │
                                  ▼
                           USER QUESTION
                                  │
                                  ▼
                         Query Embedding
                                  │
                                  ▼
                         Hybrid Retrieval
                         ┌────────┴────────┐
                         ▼                 ▼
                  Semantic Search     Keyword Search
                         │                 │
                         └────────┬────────┘
                                  ▼
                          Result Combination
                                  │
                                  ▼
                         Similarity Ranking
                                  │
                                  ▼
                         Metadata Filtering
                                  │
                                  ▼
                         Top-K Relevant Chunks
                                  │
                                  ▼
                           Context Builder
                                  │
                                  ▼
                           Prompt Builder
                                  │
                                  ▼
                                LLM
                                  │
                                  ▼
                           Final Answer
                                  │
                                  ▼
                         Sources / Citations

1. Document Ingestion

The ingestion pipeline converts uploaded documents into searchable vector representations.

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
Vector Storage

PDF Upload

Users can upload PDF documents through the backend API.

The system receives the document and starts the ingestion pipeline.

Text Extraction

Text is extracted from the PDF while preserving page-level information.

This allows retrieved chunks to retain their original page references, which can later be used for source attribution.

Text Cleaning

Extracted text is cleaned and normalized before being divided into chunks.

The cleaning stage handles unnecessary whitespace, formatting artifacts, and other extraction-related noise.

Document Chunking

Large documents are divided into smaller chunks before embedding.

Chunking is important because:

LLMs have limited context windows.

Smaller sections provide more precise retrieval.

Embeddings represent focused pieces of information.

Retrieved context can be selectively constructed.

The chunking implementation is configurable so different chunk sizes and overlap strategies can be evaluated.

Embedding Generation

Each document chunk is converted into a numerical vector using a Sentence Transformer embedding model.

Document Chunk
      ↓
Embedding Model
      ↓
Vector Representation


The resulting vectors represent the semantic meaning of the chunks and allow questions to be compared against document content.

Vector Storage

Document chunks, metadata, and embeddings are stored in PostgreSQL with pgvector.

Stored information includes concepts such as:

Document information

User ownership

Chunk content

Page information

Embedding vectors

Metadata

2. Query Processing

When a user asks a question, the question goes through a similar embedding process.

User Question
      ↓
Query Embedding
      ↓
Vector Representation


The query vector is then used to search the document collection for semantically relevant content.

3. Retrieval

The retrieval layer identifies the document chunks that are most relevant to the user's question.

Query
 ↓
Query Embedding
 ↓
Search
 ↓
Filtering
 ↓
Ranking
 ↓
Top-K Results


The system supports retrieval using semantic similarity and keyword-oriented search techniques.

Semantic Retrieval

Semantic retrieval compares the query embedding with stored document embeddings.

This allows the system to retrieve conceptually related content even when the exact words used in the question do not appear in the document.

Query Vector
      ↓
Vector Similarity
      ↓
Relevant Chunks

Hybrid Retrieval

The retrieval system can combine semantic and keyword-based search.

                 User Query
                     │
            ┌────────┴────────┐
            ▼                 ▼
     Semantic Search     Keyword Search
            │                 │
            └────────┬────────┘
                     ▼
              Combined Results
                     │
                     ▼
                  Ranking


Hybrid retrieval helps balance semantic understanding with exact keyword matching.

This is particularly useful for technical terms, names, identifiers, and domain-specific terminology.

Metadata Filtering

Retrieval can be restricted using metadata such as:

User

Document

Other document-level attributes

This prevents users from retrieving content belonging to documents they should not have access to.

Top-K Retrieval

Instead of sending an entire document to the LLM, the system selects the most relevant chunks.

All Document Chunks
        ↓
    Retrieval
        ↓
   Ranking
        ↓
   Top-K Chunks


The value of K can be configured and evaluated to understand the trade-off between retrieval quality, context size, and latency.

4. Context Construction

After retrieval, the selected chunks are transformed into a structured context for the LLM.

Top-K Retrieved Chunks
          ↓
    Context Builder
          ↓
   Structured Context


The context builder combines the relevant information while preserving useful metadata such as document and page references.

The goal is to provide the LLM with the smallest useful set of relevant information rather than the entire document.

5. Prompt Construction

The retrieved context and the user's question are combined into an LLM prompt.

Retrieved Context
       +
User Question
       ↓
Prompt Builder
       ↓
LLM Messages


The prompt builder defines the instructions that guide the model to answer using the retrieved information.

This helps reduce hallucinations by grounding the generated response in the retrieved document content.

6. Answer Generation

The constructed prompt is sent to the configured LLM.

Question
   +
Retrieved Context
   ↓
Prompt
   ↓
LLM
   ↓
Generated Answer


The application supports streaming responses so that generated tokens can be returned progressively rather than waiting for the complete answer.

7. Source Grounding & Citations

The RAG pipeline maintains the relationship between retrieved chunks and their original documents.

Answer
  │
  ├── Source Document
  ├── Page Number
  └── Retrieved Chunk


This provides traceability between the generated answer and the information retrieved from the knowledge base.

8. RAG Design Principles

The implementation focuses on understanding each component of RAG rather than treating RAG as a single black-box operation.

Key principles include:

Retrieve before generating

Use focused chunks instead of entire documents

Ground LLM responses in retrieved context

Preserve document metadata

Filter results by ownership and document

Keep retrieval and generation as separate components

Make retrieval parameters configurable

Evaluate retrieval independently from generation

9. Retrieval Experiments

The retrieval system is designed to allow experimentation with different configurations.

Experiments can include:

Parameter	Examples
Chunk size	Small vs. large chunks
Chunk overlap	Different overlap percentages
Embedding model	Different embedding models
Top-K	Different numbers of retrieved chunks
Retrieval method	Semantic / keyword / hybrid
Metadata filters	User / document filtering
Ranking	Different ranking strategies

These experiments help analyze the relationship between retrieval quality, latency, and context size.

10. RAG Testing

The RAG implementation is tested at multiple levels.

Unit Tests

Individual components are tested independently, including:

Text cleaning

PDF extraction

Chunking

Embedding generation

Prompt construction

LLM streaming

Retrieval services

Search functionality

Agent components

Integration Tests

Integration tests verify that multiple components work together.

Examples include:

RetrievalService
      ↓
Search
      ↓
Embedding Model
      ↓
PostgreSQL
      ↓
pgvector
      ↓
Retrieved Results


The project also tests the RAG context construction and LLM integration.

API Tests

The FastAPI health endpoint and backend API behavior are tested separately.

RAG Implementation Philosophy

The primary goal of this project is not simply to use RAG, but to understand how a RAG system works internally.

The implementation therefore avoids hiding the core retrieval process behind high-level AI orchestration frameworks.

The system is built around independently testable components for:

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
Ranking
   ↓
Context Construction
   ↓
Prompt Construction
   ↓
LLM Generation




## AI Agents

AI Agents

The platform includes a custom multi-agent research workflow designed to demonstrate planning, task decomposition, retrieval, research, review, and reflection without relying on high-level agent orchestration frameworks such as LangGraph.

Agent Architecture
                         User Query
                              │
                              ▼
                        Planner Agent
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             Research Task 1     Research Task 2
                    │                   │
                    ▼                   ▼
              Researcher Agent    Researcher Agent
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       Retrieved Results
                              │
                              ▼
                         Writer Agent
                              │
                              ▼
                        Reviewer Agent
                              │
                       ┌──────┴──────┐
                       │             │
                    Approved      Needs Review
                       │             │
                       ▼             ▼
                  Final Answer   Reflection Loop
                                     │
                                     ▼
                                  Revision
                                     │
                                     └──────→ Reviewer

Agent Workflow

The system follows a structured workflow:

User Question
      ↓
Planner
      ↓
Task Decomposition
      ↓
Research
      ↓
Retrieval
      ↓
Research Results
      ↓
Writer
      ↓
Reviewer
      ↓
Reflection / Revision
      ↓
Final Answer

Planner Agent

The Planner Agent converts a complex user request into a structured research plan.

Responsibilities include:

Understanding the user's objective

Breaking complex questions into smaller tasks

Generating research tasks

Validating the generated plan

Providing fallback behavior when the LLM returns invalid output

Example:

Complex Question
      ↓
Planner Agent
      ↓
┌─────────────────────┐
│ Task 1: Research A  │
│ Task 2: Research B  │
│ Task 3: Compare     │
└─────────────────────┘

Researcher Agent

The Researcher Agent executes the research tasks generated by the planner.

It coordinates retrieval and LLM-based reasoning to produce research results that can later be consumed by the writer.

Research Task
     ↓
Retriever
     ↓
Relevant Information
     ↓
LLM Research
     ↓
Research Result


The agent also handles cases where a plan or retriever is unavailable and maintains the current workflow state.

Retriever

The agent workflow connects to the custom retrieval system rather than implementing a separate knowledge-retrieval mechanism.

Agent
  ↓
Retrieval Service
  ↓
Hybrid Search
  ↓
Relevant Chunks
  ↓
Agent Context


This allows the agent system to use the same document knowledge base as the standard RAG pipeline.

Writer Agent

The Writer Agent transforms the collected research results into a coherent response.

Research Results
      ↓
Writer Agent
      ↓
Structured Response


The writer receives the relevant research context instead of independently searching the knowledge base.

Reviewer Agent

The Reviewer evaluates the generated response before it is returned to the user.

The review stage is intended to identify problems such as:

Missing information

Unsupported claims

Poor reasoning

Incomplete answers

Inconsistencies with retrieved information

Generated Answer
      ↓
Reviewer
      ↓
┌───────────────┐
│   Accept      │
│      OR       │
│ Request Review│
└───────────────┘

Reflection Loop

When the reviewer identifies issues, the workflow can enter a reflection/revision cycle.

Draft Answer
     ↓
Reviewer
     ↓
Issues Identified
     ↓
Reflection
     ↓
Revision
     ↓
Reviewer
     ↓
Final Answer


The purpose of the reflection loop is to improve answer quality through iterative evaluation rather than generating the final response in a single LLM call.

Agent State

The workflow maintains shared state between agents.

The state can contain information such as:

User question

Research plan

Research tasks

Retrieved information

Research results

Draft response

Review feedback

Final response

This allows individual agents to perform focused responsibilities while participating in a single workflow.

Agent Design Principles

The agent architecture follows several principles:

Single responsibility — each agent performs a specific task.

Task decomposition — complex questions are divided into smaller research tasks.

Shared state — agents communicate through structured workflow state.

Tool usage — agents can use retrieval and external tools when required.

Validation — agent outputs are validated before continuing the workflow.

Fallback handling — invalid LLM outputs do not automatically terminate the workflow.

Iterative improvement — reviewer feedback can trigger reflection and revision.

Separation of concerns — planning, retrieval, research, writing, and reviewing are separate components.

Agent Testing

The agent components are tested independently.

Current unit tests cover:

Planner plan generation

Research task creation

LLM invocation

Invalid JSON fallback

Invalid task-count fallback

Researcher behavior without a plan

Researcher behavior without a retriever

Retriever invocation

LLM research invocation

Research result creation

This makes individual agent behavior testable without requiring the entire multi-agent workflow to run for every test.

Why Build Agents From Scratch?

Instead of using a framework to hide the orchestration logic, this project implements the agent workflow explicitly.

The goal is to understand:

Planning
   ↓
Task Decomposition
   ↓
Tool / Retrieval Usage
   ↓
State Management
   ↓
Generation
   ↓
Review
   ↓
Reflection
   ↓
Revision


This provides a deeper understanding of how multi-agent AI systems can be designed and orchestrated internally.

## MCP Integration

AI Agents

The platform includes a custom multi-agent research workflow designed to demonstrate planning, task decomposition, retrieval, research, review, and reflection without relying on high-level agent orchestration frameworks such as LangGraph.

Agent Architecture
                         User Query
                              │
                              ▼
                        Planner Agent
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             Research Task 1     Research Task 2
                    │                   │
                    ▼                   ▼
              Researcher Agent    Researcher Agent
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       Retrieved Results
                              │
                              ▼
                         Writer Agent
                              │
                              ▼
                        Reviewer Agent
                              │
                       ┌──────┴──────┐
                       │             │
                    Approved      Needs Review
                       │             │
                       ▼             ▼
                  Final Answer   Reflection Loop
                                     │
                                     ▼
                                  Revision
                                     │
                                     └──────→ Reviewer

Agent Workflow

The system follows a structured workflow:

User Question
      ↓
Planner
      ↓
Task Decomposition
      ↓
Research
      ↓
Retrieval
      ↓
Research Results
      ↓
Writer
      ↓
Reviewer
      ↓
Reflection / Revision
      ↓
Final Answer

Planner Agent

The Planner Agent converts a complex user request into a structured research plan.

Responsibilities include:

Understanding the user's objective

Breaking complex questions into smaller tasks

Generating research tasks

Validating the generated plan

Providing fallback behavior when the LLM returns invalid output

Example:

Complex Question
      ↓
Planner Agent
      ↓
┌─────────────────────┐
│ Task 1: Research A  │
│ Task 2: Research B  │
│ Task 3: Compare     │
└─────────────────────┘

Researcher Agent

The Researcher Agent executes the research tasks generated by the planner.

It coordinates retrieval and LLM-based reasoning to produce research results that can later be consumed by the writer.

Research Task
     ↓
Retriever
     ↓
Relevant Information
     ↓
LLM Research
     ↓
Research Result


The agent also handles cases where a plan or retriever is unavailable and maintains the current workflow state.

Retriever

The agent workflow connects to the custom retrieval system rather than implementing a separate knowledge-retrieval mechanism.

Agent
  ↓
Retrieval Service
  ↓
Hybrid Search
  ↓
Relevant Chunks
  ↓
Agent Context


This allows the agent system to use the same document knowledge base as the standard RAG pipeline.

Writer Agent

The Writer Agent transforms the collected research results into a coherent response.

Research Results
      ↓
Writer Agent
      ↓
Structured Response


The writer receives the relevant research context instead of independently searching the knowledge base.

Reviewer Agent

The Reviewer evaluates the generated response before it is returned to the user.

The review stage is intended to identify problems such as:

Missing information

Unsupported claims

Poor reasoning

Incomplete answers

Inconsistencies with retrieved information

Generated Answer
      ↓
Reviewer
      ↓
┌───────────────┐
│   Accept      │
│      OR       │
│ Request Review│
└───────────────┘

Reflection Loop

When the reviewer identifies issues, the workflow can enter a reflection/revision cycle.

Draft Answer
     ↓
Reviewer
     ↓
Issues Identified
     ↓
Reflection
     ↓
Revision
     ↓
Reviewer
     ↓
Final Answer


The purpose of the reflection loop is to improve answer quality through iterative evaluation rather than generating the final response in a single LLM call.

Agent State

The workflow maintains shared state between agents.

The state can contain information such as:

User question

Research plan

Research tasks

Retrieved information

Research results

Draft response

Review feedback

Final response

This allows individual agents to perform focused responsibilities while participating in a single workflow.

Agent Design Principles

The agent architecture follows several principles:

Single responsibility — each agent performs a specific task.

Task decomposition — complex questions are divided into smaller research tasks.

Shared state — agents communicate through structured workflow state.

Tool usage — agents can use retrieval and external tools when required.

Validation — agent outputs are validated before continuing the workflow.

Fallback handling — invalid LLM outputs do not automatically terminate the workflow.

Iterative improvement — reviewer feedback can trigger reflection and revision.

Separation of concerns — planning, retrieval, research, writing, and reviewing are separate components.

Agent Testing

The agent components are tested independently.

Current unit tests cover:

Planner plan generation

Research task creation

LLM invocation

Invalid JSON fallback

Invalid task-count fallback

Researcher behavior without a plan

Researcher behavior without a retriever

Retriever invocation

LLM research invocation

Research result creation

This makes individual agent behavior testable without requiring the entire multi-agent workflow to run for every test.

Why Build Agents From Scratch?

Instead of using a framework to hide the orchestration logic, this project implements the agent workflow explicitly.

The goal is to understand:

Planning
   ↓
Task Decomposition
   ↓
Tool / Retrieval Usage
   ↓
State Management
   ↓
Generation
   ↓
Review
   ↓
Reflection
   ↓
Revision


This provides a deeper understanding of how multi-agent AI systems can be designed and orchestrated internally.

## Authentication

Authentication
The backend implements JWT-based authentication to support multiple users and protect user-specific resources.

User registration and login

Password hashing

JWT access tokens

Protected API endpoints

User-specific document and knowledge-base access

Authorization checks for owned resources


## Tech Stack

Backend
Python

FastAPI

SQLAlchemy

Alembic

Pydantic

PostgreSQL

pgvector

AI / ML
OpenAI API / Ollama

Sentence Transformers

Embeddings

Retrieval-Augmented Generation (RAG)

Hybrid search

AI agents

Model Context Protocol (MCP)

Frontend
Next.js

React

TypeScript

Testing & Development
Pytest

Async testing

Git / GitHub

Python virtual environment

Infrastructure
PostgreSQL + pgvector

Docker configuration



## API Endpoints
API Endpoints

The backend is built with FastAPI and exposes REST APIs for authentication, document ingestion, knowledge retrieval, RAG-based question answering, and system health monitoring.

Base URL
http://localhost:8000


Interactive API documentation:

http://localhost:8000/docs


ReDoc documentation:

http://localhost:8000/redoc

Health & System
Method	Endpoint	Description
GET	/health	Check whether the API is running
Authentication
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	Authenticate a user and obtain a JWT token

Authentication uses JWT access tokens to protect user-specific resources.

Example:

POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}


Authenticated requests use:

Authorization: Bearer <access_token>

Document Management
Method	Endpoint	Description
POST	/documents/upload	Upload and ingest a document
GET	/documents	List available documents
GET	/documents/{document_id}	Retrieve document information
DELETE	/documents/{document_id}	Delete a document

The document upload pipeline performs:

Upload
  ↓
PDF Text Extraction
  ↓
Text Cleaning
  ↓
Text Normalization
  ↓
Chunking
  ↓
Embedding Generation
  ↓
Metadata Storage
  ↓
Vector Storage

Retrieval & Search
Method	Endpoint	Description
POST	/search	Search the knowledge base
POST	/retrieval/search	Perform semantic/hybrid retrieval

The retrieval system supports:

Query embedding

Vector similarity search

Top-k retrieval

User filtering

Document filtering

Metadata filtering

Hybrid retrieval

Context construction

RAG / Question Answering
Method	Endpoint	Description
POST	/chat	Ask a question using the RAG pipeline
POST	/chat/stream	Ask a question and receive a streamed response

The RAG pipeline follows:

User Question
      ↓
Query Embedding
      ↓
Vector / Hybrid Search
      ↓
Similarity Ranking
      ↓
Top-k Relevant Chunks
      ↓
Context Builder
      ↓
Prompt Builder
      ↓
LLM
      ↓
Generated Answer
      ↓
Citations / Sources

Streaming Responses

The streaming endpoint returns the generated answer incrementally instead of waiting for the complete response.

Client
  ↓
POST /chat/stream
  ↓
RAG Retrieval
  ↓
LLM
  ↓
Token-by-token Streaming
  ↓
Client


This improves the perceived response time for longer AI-generated answers.

Knowledge Base
Method	Endpoint	Description
POST	/knowledge-bases	Create a knowledge base
GET	/knowledge-bases	List knowledge bases
GET	/knowledge-bases/{knowledge_base_id}	Retrieve a knowledge base
DELETE	/knowledge-bases/{knowledge_base_id}	Delete a knowledge base

Knowledge bases allow documents and their embeddings to be logically grouped for retrieval.

Chat History
Method	Endpoint	Description
GET	/chat/history	Retrieve previous conversations
GET	/chat/history/{conversation_id}	Retrieve a specific conversation
DELETE	/chat/history/{conversation_id}	Delete a conversation
Agent APIs

The agent system provides an orchestration layer for research-oriented tasks.

The workflow is:

Planner
   ↓
Retriever
   ↓
Researcher
   ↓
Writer
   ↓
Reviewer
   ↓
Reflection
   ↓
Final Answer


Agent components include:

Planning

Task decomposition

Retrieval

Research

Answer generation

Review

Reflection

Memory/state management

MCP Integration

The project also includes Model Context Protocol (MCP) integration for connecting AI workflows with external tools and resources.

Implemented MCP capabilities include:

Filesystem interaction

File and folder search

PostgreSQL interaction

Database schema exploration

GitHub repository interaction

The MCP architecture follows:

AI Agent
   ↓
MCP Client
   ↓
MCP Server
   ↓
Tool / Resource
   ↓
External System

API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

http://localhost:8000/docs


ReDoc:

http://localhost:8000/redoc


These interfaces can be used to explore endpoints, inspect request/response schemas, authenticate requests, and test the API locally.


## Database Schema

The project uses PostgreSQL as the primary database and pgvector for storing and searching document embeddings.

The main data flow is:

User
 │
 ├── Knowledge Bases
 │       │
 │       └── Documents
 │              │
 │              └── Document Chunks
 │                     │
 │                     └── Embeddings
 │
 └── Chat / Conversation History

Core Entities
Users — Stores user accounts and authentication information.

Knowledge Bases — Groups documents into separate searchable collections.

Documents — Stores uploaded document information and metadata.

Document Chunks — Stores the text produced by the document chunking pipeline.

Embeddings — Stores vector representations of document chunks using pgvector.

Chat History — Stores conversations and generated responses.

Vector Search
Document chunks are converted into numerical embeddings during ingestion.

Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embedding Model
   ↓
Vector Embedding
   ↓
PostgreSQL + pgvector

During retrieval, the user's question is also converted into an embedding and compared against stored document vectors.

Question
   ↓
Query Embedding
   ↓
pgvector Similarity Search
   ↓
Relevant Chunks
   ↓
RAG Context

pgvector enables semantic similarity search directly inside PostgreSQL.

Database Migrations
Database schema changes are managed using Alembic.

Run migrations with:

alembic upgrade head

Create a new migration when the database models change:

alembic revision --autogenerate -m "describe your change"


## Running Locally
Prerequisites
Before running the project locally, install:

Python 3.12+

PostgreSQL

pgvector extension

Git

Node.js and npm for the frontend

Ollama if using local LLMs

1. Clone the Repository
git clone https://github.com/Rishika70592/AI_knowledge_platform.git
cd AI_knowledge_platform

2. Create a Python Virtual Environment
Windows PowerShell:

python -m venv venv

Activate the environment:

.\venv\Scripts\Activate.ps1

3. Install Backend Dependencies
pip install -r app/requirements.txt

4. Configure Environment Variables
Create a .env file and configure the required database and AI provider settings.

Example:

DATABASE_URL=postgresql://username:password@localhost:5432/ai_knowledge_platform
OPENAI_API_KEY=your_api_key
SECRET_KEY=your_secret_key
OLLAMA_BASE_URL=http://localhost:11434

5. Start PostgreSQL
Make sure PostgreSQL is running and the required database exists.

The database should also have the pgvector extension enabled.

6. Run Database Migrations
From the project root:

alembic upgrade head

7. Start the Backend
uvicorn app.main:app --reload

The FastAPI backend will be available at:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc

8. Start the Frontend
Open another terminal:

cd frontend
npm install
npm run dev

The frontend will normally be available at:

http://localhost:3000

9. Run Tests
Run the complete test suite:

python -m pytest -v

Run unit tests:

python -m pytest app/test/unit -v

Run integration tests:

python -m pytest app/test/integration -v

Run API tests:

python -m pytest app/test/api -v

10. Local Development Flow
Once the services are running:

Next.js Frontend
       │
       ▼
FastAPI Backend
       │
       ├── Authentication
       │
       ├── Document Ingestion
       │
       ├── RAG Pipeline
       │
       ├── AI Agents
       │
       └── MCP Integration
              │
              ▼
       PostgreSQL + pgvector
              │
              ▼
       AI / Embedding Models

The project is currently designed primarily as a local learning and experimentation environment for understanding LLM applications, RAG, retrieval systems, AI agents, MCP, and backend engineering.

## Testing
Testing

The project includes unit, integration, and API tests covering the core AI pipeline.

Test Coverage
Area	Tests	Status
Text Cleaning	1	✅ Passed
Text Chunking	2	✅ Passed
PDF Text Extraction	3	✅ Passed
Embeddings	3	✅ Passed
Prompt Builder	5	✅ Passed
LLM Service	3	✅ Passed
Planner Agent	5	✅ Passed
Researcher Agent	5	✅ Passed
Retrieval Service	3	✅ Passed
Vector Search	4	✅ Passed
Retrieval Integration	1	✅ Passed
RAG Context Integration	1	✅ Passed
LLM Integration	1	✅ Passed
Health API	1	✅ Passed
Testing Strategy

Unit Tests

Core components are tested independently, including:

Text cleaning

PDF text extraction

Document chunking

Embedding generation

Prompt construction

LLM streaming

Vector search

Retrieval service

Agent planning

Agent research

Integration Tests

Integration tests verify that multiple components work together:

RetrievalService
      ↓
Search Service
      ↓
SentenceTransformer
      ↓
PostgreSQL
      ↓
pgvector similarity search
      ↓
Retrieved Results


The RAG context pipeline is also tested to verify that retrieved documents are correctly transformed into context for the LLM.

API Tests

The FastAPI health endpoint is tested to verify that the application starts correctly and responds as expected.

Example Test Command
python -m pytest app/test/unit/test_chunking.py -v

Current Result

All tests executed during development passed successfully.
## Screenshots / Demo





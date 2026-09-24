# ARES-RAG X
## Enterprise RAG + SQL Hybrid AI System

ARES-RAG X is an enterprise AI system that combines Retrieval-Augmented
Generation (RAG), SQL-based data querying, and intelligent query routing
to answer questions from both structured company data and unstructured
company documents.

---

## 1. Project Overview

Enterprise organizations store information in different formats.

For example:

- Employee information is stored in databases.
- Sales information is stored in databases.
- Attendance and leave records are stored in databases.
- Company policies are stored in documents.

A normal RAG system is good at searching documents but is not designed
for accurate numerical database queries.

A normal SQL system can query structured data but cannot naturally answer
questions from policy documents.

ARES-RAG X solves this problem by combining both approaches.

The system automatically determines whether a question requires:

- SQL
- RAG
- Hybrid SQL + RAG

and generates a grounded answer.

---

## 2. Main Objective

The main objective of ARES-RAG X is to build an enterprise AI assistant
that can securely answer questions from:

1. Structured enterprise databases
2. Unstructured enterprise documents
3. Both sources simultaneously

The system focuses on:

- Accurate retrieval
- Reliable SQL generation
- Evidence verification
- Query routing
- Hallucination reduction
- Enterprise data security
- API accessibility
- Web-based interaction

---

## 3. System Architecture

```text
                    USER
                      |
                      v
              Web Frontend
                      |
                      v
                 FastAPI
                      |
                      v
            Hybrid Coordinator
                      |
          +-----------+-----------+
          |                       |
          v                       v
      SQL Agent               RAG Agent
          |                       |
          v                       v
     SQLite Database         Document Retriever
                                  |
                                  v
                              HyDE
                                  |
                                  v
                           Vector Database
                                  |
                                  v
                           CrossEncoder
                                  |
                                  v
                               CRAG
                                  |
                                  v
                             Self-RAG
                                  |
                                  v
                              Ollama
                                  |
                                  +------+
                                         |
                                         v
                                  Final Answer
## 4. Technology Stack

### Programming

- Python 3.12

### Backend

- FastAPI
- Uvicorn

### Database

- SQLite

### Vector Database

- ChromaDB

### Embeddings

- FastEmbed
- BAAI/bge-small-en-v1.5

### Reranking

- CrossEncoder
- ms-marco-MiniLM-L-6-v2

### LLM

- Ollama
- llama3.2:3b

### AI Techniques

- RAG
- HyDE
- CRAG
- Self-RAG
- Semantic Search
- Semantic Cache
- Query Routing
- Text-to-SQL
- Hybrid Retrieval

### Frontend

- HTML
- CSS
- JavaScript

### API

- REST API
- FastAPI

### Deployment

- Cloudflare Quick Tunnel

---

## 5. Enterprise Database

The project uses a SQLite database containing enterprise-style company information.

### Database Tables

- departments
- employees
- sales
- attendance
- leave_records
- performance
- projects
- customers

The database contains:

- 100 employees
- 6 departments

Example question:

How many employees are there?

The SQL Agent generates an appropriate SQL query and retrieves the result from the database.

---

## 6. Enterprise Documents

ARES-RAG X also uses enterprise policy documents.

Examples include:

- Annual Leave Policy
- Sick Leave Policy
- Casual Leave Policy
- Remote Access Policy
- Other company policies

The document ingestion pipeline divides documents into chunks and stores them in the vector database.

Current document index:

- 24 documents
- 143 chunks

---

## 7. RAG Pipeline

The RAG pipeline follows these major steps:

User Question  
↓  
Query Processing  
↓  
HyDE  
↓  
Vector Retrieval  
↓  
Keyword Matching  
↓  
CrossEncoder Reranking  
↓  
CRAG Verification  
↓  
Self-RAG Verification  
↓  
LLM  
↓  
Final Answer

---

## 8. SQL Pipeline

Structured questions are processed using the SQL Agent.

User Question  
↓  
SQL Agent  
↓  
Text-to-SQL  
↓  
SQLite Database  
↓  
Query Result  
↓  
Natural Language Answer

Example:

Question:

How many employees are there?

SQL Result:

100

Answer:

There are 100 employees.

---

## 9. Hybrid Query Processing

ARES-RAG X can handle questions that require both database information and document information.

Example:

How many employees are there and what is the annual leave policy?

The system separates the requirements.

Employee Count:

Question  
↓  
SQL Agent  
↓  
100 employees

Annual Leave Policy:

Question  
↓  
RAG Agent  
↓  
Company Policy Document

The two results are then combined into one final answer.

---

## 10. Intelligent Query Routing

The Hybrid Coordinator determines which processing method is required.

### SQL Query

Example:

How many employees are there?

Route:

SQL

### RAG Query

Example:

What is the annual leave policy?

Route:

RAG

### Hybrid Query

Example:

How many employees are there and what is the annual leave policy?

Route:

HYBRID

---
## 11. HyDE

HyDE stands for Hypothetical Document Embeddings.

HyDE improves retrieval by generating a hypothetical answer or document related to the user's question before performing semantic search.

Pipeline:

User Question
↓
HyDE
↓
Hypothetical Document
↓
Embedding
↓
Vector Search
↓
Relevant Documents

This helps the retriever find documents that are semantically related to the question.

---

## 12. CrossEncoder Reranking

After retrieving candidate documents, ARES-RAG X uses a CrossEncoder to rerank the results.

Model:

ms-marco-MiniLM-L-6-v2

The reranker evaluates the relevance between:

- User question
- Retrieved document

The most relevant documents are placed at the top before being sent to the LLM.

---

## 13. CRAG

CRAG stands for Corrective Retrieval-Augmented Generation.

CRAG checks whether the retrieved documents are relevant to the user's question.

### CRAG Process

Question
↓
Retrieve Documents
↓
Check Relevance
↓
Relevant?
↓
Yes → Continue
↓
No → Generate Corrective Query
↓
Retrieve Again

The system also uses evidence overlap to verify whether retrieved information contains meaningful information related to the question.

This helps reduce answers based on irrelevant documents.

---

## 14. Self-RAG

Self-RAG stands for Self-Reflective Retrieval-Augmented Generation.

Self-RAG verifies whether the retrieved evidence actually supports the generated answer.

The system checks:

- Whether evidence supports the answer
- Whether the answer is grounded
- Whether unsupported information is being generated

If the evidence is sufficient, the answer is accepted.

If the evidence is insufficient, the system can reject or regenerate the response.

This helps reduce hallucinations.

---

## 15. Guardrails

ARES-RAG X contains guardrails to protect the system from unsafe or inappropriate queries.

The guardrail layer checks user questions before processing them.

The system can block requests that attempt to:

- Bypass system security
- Access unauthorized information
- Perform harmful actions
- Extract protected information

Safe questions are allowed to continue through the normal processing pipeline.

---

## 16. Semantic Cache

ARES-RAG X uses a semantic cache to avoid unnecessary repeated processing.

If the same or a semantically similar question is asked again, the system can return the previously generated result.

### Cache Process

User Question
↓
Check Cache
↓
Exact Match?
↓
Yes → Return Cached Answer
↓
No
↓
Semantic Similarity Check
↓
Similar Question?
↓
Yes → Return Cached Answer
↓
No → Process Normally

This can reduce:

- Processing time
- LLM calls
- Computational cost

---

## 17. Unsupported Query Protection

The system is designed to avoid inventing information when the required information is not available.

Example:

Question:

What is the office location of the company?

If the available enterprise documents and database do not contain verified information about the office location, the system returns a safe response instead of creating an unsupported answer.

Example response:

The available enterprise documents do not provide enough verified information to answer this question reliably.

This provides protection against hallucination.

---
## 18. Evaluation

ARES-RAG X includes an automated evaluation system to test the major capabilities of the project.

The evaluation contains six test cases.

### Test Cases

1. Employee Count
2. Department Count
3. Annual Leave Policy
4. Sick Leave Policy
5. Hybrid Employee + Policy Query
6. Unsupported Query

The latest evaluation result:

- Total Tests: 6
- Passed: 6
- Failed: 0
- Accuracy: 100%

This result represents the six-case evaluation suite and should not be interpreted as 100% real-world accuracy.

---

## 19. Retrieval Evaluation

The retrieval system was evaluated using retrieval metrics.

Results:

- Top-1 Retrieval: 90%
- Top-3 Retrieval: 100%
- Top-5 Retrieval: 100%

These results show that relevant enterprise documents were generally retrieved within the top results.

---

## 20. REST API

ARES-RAG X provides a REST API using FastAPI.

### Main Endpoints

GET `/`

Checks whether the API is running.

GET `/health`

Checks the health of the service.

POST `/ask`

Accepts a user question and returns the generated answer.

Example request:

```json
{
  "question": "How many employees are there?"
}

21. Frontend

ARES-RAG X includes a web-based frontend.

The frontend provides:

Question input
Example questions
Ask button
Loading indicator
Answer display
Error handling
API status indicator
Ctrl + Enter shortcut

The frontend communicates with the FastAPI backend using JavaScript Fetch API.

22. Public Demo

The FastAPI backend was exposed through a Cloudflare Quick Tunnel for demonstration.

The public API can be accessed through the temporary Cloudflare tunnel URL configured during deployment.

The public endpoint was tested successfully using:

Health check
SQL question
RAG question
Hybrid question

Note:

Cloudflare Quick Tunnel URLs are temporary and can change when the tunnel is restarted.

23. Project Structure
Ares RAG/
│
├── app/
│   ├── main.py
│   ├── api.py
│   ├── rag_agent.py
│   ├── sql_agent.py
│   └── hybrid_coordinator.py
│
├── src/
│   ├── retriever.py
│   ├── llm.py
│   ├── self_rag.py
│   ├── CRAG/
│   ├── HyDE/
│   ├── Text2SQL/
│   ├── query_engine/
│   └── guardrails/
│
├── data/
│
├── database/
│   └── nova_corp.db
│
├── evaluation/
│   └── evaluate_hybrid.py
│
├── frontend/
│   └── index.html
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── start.bat
└── README.md
24. How to Run
Step 1 — Open the Project

Open the project folder in VS Code.

C:\Users\santh\OneDrive\Desktop\Ares RAG
Step 2 — Activate Virtual Environment
venv\Scripts\activate
Step 3 — Start Ollama

Make sure Ollama is running and the required model is available.

ollama list

The project uses:

llama3.2:3b
Step 4 — Start FastAPI
python -m uvicorn app.api:app --reload
Step 5 — Open the Frontend

Open:

frontend/index.html

using VS Code Live Server.

25. Key Features

ARES-RAG X provides the following features:

Enterprise RAG
SQL-based question answering
Hybrid SQL + RAG processing
Intelligent query routing
HyDE retrieval
Vector search
CrossEncoder reranking
CRAG
Self-RAG
Guardrails
Semantic caching
Unsupported-query protection
Automated evaluation
REST API
Web frontend
Public demonstration deployment
26. Limitations

The current system has some limitations.

LLM

The project currently uses a local llama3.2:3b model through Ollama.

A larger model may provide better reasoning for complex enterprise questions.

Public Deployment

The current Cloudflare Quick Tunnel is intended for demonstration.

It is not a permanent production deployment.

Evaluation

The current automated evaluation contains a small fixed test set.

More enterprise questions and datasets would be required for broader evaluation.

Database

The current database contains synthetic enterprise-style data for demonstration and development.

27. Future Improvements

Possible future improvements include:

Larger and stronger LLM
Production cloud deployment
Authentication
Role-based access control
User management
Conversation history
Advanced monitoring
Logging dashboard
More enterprise documents
Larger evaluation datasets
Improved SQL validation
Multi-database support
Streaming responses
Production vector database
Automated document ingestion
28. Conclusion

ARES-RAG X demonstrates how an enterprise AI assistant can combine structured and unstructured data processing.

The system can automatically route questions to SQL, RAG, or both depending on the information required.

It also incorporates modern retrieval and reliability techniques including:

HyDE
CrossEncoder reranking
CRAG
Self-RAG
Guardrails
Semantic caching

The project provides a complete workflow from data retrieval to API and web-based interaction.

It demonstrates the practical use of Generative AI, Retrieval-Augmented Generation, Text-to-SQL, and hybrid AI architectures for enterprise applications.
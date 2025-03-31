# Jamaica Travel Recommendation System (AI-Powered RAG Pipeline)

## 🌴 Overview
This project is an AI-powered recommendation system that suggests travel destinations in Jamaica based on user queries. It implements a **Retrieval-Augmented Generation (RAG)** pipeline:
1. **Retrieval**: Finds relevant Reddit posts using similarity search.
2. **Augmentation**: Enhances responses with contextual data.
3. **Generation**: Provides natural-language recommendations via LLM.

## 🛠️ Technical Stack
| Component | Technology |
|-----------|------------|
| **Frontend** | Angular |
| **Backend** | FastAPI (Python) |
| **Embeddings** | Sentence Transformers (`paraphrase-MiniLM-L3-v2`) |
| **Vector Database** | FAISS (Facebook AI Similarity Search) |
| **LLM** | Groq API (Llama-3-70b) |

## 🔍 Pipeline Architecture
```mermaid
graph TD
A[User Query] --> B(Embedding Model)
B --> C[FAISS Similarity Search]
C --> D[Top 3 Reddit Posts]
D --> E[LLM Prompt Engineering]
E --> F[Final Recommendation]

## Key Steps & Processes

### 1. Data Preparation
- **Data Collection**: I scraped Reddit posts through Reddit's API from subreddits.
- **Embedding Generation**: Transformed text into embeddings using Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Storage**: Stored embeddings in a FAISS index for efficient similarity search

### 2. Query Processing
- **User Input**: Converts natural language queries to embeddings
- **Similarity Search**: FAISS retrieves the top 3 most relevant Reddit posts based on:
  ```python
  _, indices = index.search(query_embedding, k=3)

  ### 3. LLM Prompt Engineering
  - **Prompting**: I sent the retreived posts and the user's query as context when prompting the LLM. 
  Therefore, the LLM implemented the final, refined output. 

  ### Here's a quick demo



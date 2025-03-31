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

[User Query] --> (Embedding Model) --> [FAISS Similarity Search] --> [Top 3 Reddit Posts] --> [LLM Prompt Engineering] --> F[Final Recommendation]

## 🔍 Key Steps

### 1. Data Preparation
- **Data Collection**: I scraped Reddit posts about travelling to Jamaica
- **Embedding Generation**: Transformed text into embeddings using Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Storage**: Stored embeddings in a FAISS index for efficient similarity search

### 2. Query Processing
- **User Input**: Converts natural language queries to embeddings
- **Similarity Search**: FAISS retrieves the top 3 most relevant Reddit posts based on user's query.

### 3. LLM Enhancement
- **Prompt Engineering**: I combined the user's query and the retreived posts from the FAISS database and prompted the LLM with that context.
- **Final Output**: The LLM provided the final, refined output.

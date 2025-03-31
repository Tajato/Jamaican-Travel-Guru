# Jamaican-Travel-Guru
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
graph LR
A[User Query] --> B(Embedding Model)
B --> C[FAISS Similarity Search]
C --> D[Top 3 Reddit Posts]
D --> E[LLM Prompt Engineering]
E --> F[Final Recommendation]
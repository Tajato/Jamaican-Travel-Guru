from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware  
from functools import lru_cache

#Intialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", # local link
                   "https://jarecsys-frontend.onrender.com"], # production link
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Allow GET, POST methods
    allow_headers=["Content-Type", "Authorization"],  # Required for JSON requests
    expose_headers=["*"],  # Allows all headers
)

# Initialize model
#model = SentenceTransformer('all-MiniLM-L6-v2')  # Embedding model that turns text into embeddings
#model = SentenceTransformer('paraphrase-albert-small-v2')  
@lru_cache(maxsize=1)
def load_model():
    """Cache the embedding model (loads only on first call) to reduce memory usage on Render"""
    return SentenceTransformer('paraphrase-albert-small-v2', device='cpu') # using a smaller model like albert.
@lru_cache(maxsize=1)
def load_data():
    # get absolute path because render could not find the csv file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "cleaned_jamaica_tourism_data.csv")
    ja_df = pd.read_csv(csv_path)  

# Generate embeddings. Embeddings are vector represetation of texts.
    model = load_model()
    ja_df['combined_text'] = ja_df['title'] + " " + ja_df['selftext'].fillna('') # combining title and selftext together
    embeddings = model.encode(ja_df['combined_text'].tolist()) # this is where I turn combined title and selftext into vectors
    embeddings = np.array(embeddings).astype('float32') #ensure data type of embeddings is float32

# Build FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1]) # create an index for the embeddings I created. 
    #We let FAISS know the dimensions of the vectors. Shape[1] signifes the dimenions of the vectors
    #Using L2 distance(IndexFlatL2) instead of something like cosine similarity
    index.add(embeddings) # add the embeddings to the FAISS index so we can perform similarity searches
    return ja_df, index
class Query(BaseModel):
    text: str

load_dotenv()  

@app.post("/recommend")
async def recommend(query: Query):
    ja_df, index = load_data()
    model = load_model()
    #Get similar posts using FAISS
    query_embedding = model.encode([query.text]) # turning the query text into an embedding
    _, indices = index.search(query_embedding, k=3)  # Performing a similarity search and getting top 3 matches
    matches = ja_df.iloc[indices[0]][['title', 'selftext']].to_dict('records')

    #Prepare LLM prompt so I can let the user get a natural language response. 
    # Previously, the model just returned reddit title and comments. 
    context = "\n".join(
        f"Post {i+1}: {match['title']}\n{match['selftext']}\n" 
        for i, match in enumerate(matches)
    )
    #context = "Negril is the best beach"
    prompt = f"""
    You are a Jamaica travel expert. Based on these posts, suggest 3 best options to answer the traveler's question.
    Start off wiht a greeting by saying "Wah Gwaan?"
     Whenever you're finished, say "big up yourself!".
    Traveler's question: {query}
    
    Relevant posts:
    {context}
    
    Provide recommendations in this format:
    1. [Place/Activity]: [Brief description - why it's good for what they asked]
    2. [Place/Activity]: [Description]
    3. [Place/Activity]: [Description]
    
    Add practical tips if available.
    """
    

    # 3. Call Groq API to get access to the LLM.
    # On local, I used llama locally but for production purposes, Groq API came in handy.
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                         "Content-Type": "application/json"
},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7  # Controls creativity
            }
        )
        

        response.raise_for_status()  # Raise HTTP errors
        
        llm_response = response.json()["choices"][0]["message"]["content"]
        
        return {
            #"matches": matches,  # Original FAISS results
            "llm_response": llm_response  # LLM answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"LLM API error: {str(e)}"
        )
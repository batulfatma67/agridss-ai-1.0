from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Initialize models and load DB ONCE at the top 
# (Taa ke jab Nauman app run kare toh DB baar baar load na ho)
print("Loading agricultural knowledge base...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "data/vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)
print("Knowledge base ready!")

# 2. Main Retrieval Function (Nauman will call this)
def get_agricultural_context(question, k=3):
    """
    Takes a farmer's question and returns relevant text from the PDFs.
    This text will be sent to the LLM to generate an explainable answer.
    """
    results = vectorstore.similarity_search(question, k=k)
    
    context_text = ""
    for chunk in results:
        source = chunk.metadata.get('source', 'Unknown')
        page = chunk.metadata.get('page', 'Unknown')
        
        # Format the chunk so the LLM knows the source for citations
        context_text += f"[Source: {source} | Page: {page}]\n{chunk.page_content}\n\n"
        
    return context_text

# 3. Quick Test Run
if __name__ == "__main__":
    test_question = "What are the common root diseases in maize caused by poor soil quality or poor aeration, and what are their symptoms?"
    
    print("\n--- RETRIEVED CONTEXT FOR LLM ---")
    retrieved_data = get_agricultural_context(test_question)
    print(retrieved_data)
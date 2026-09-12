import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load PDF from the new documents folder
pdf_path = "data/documents/wheat.pdf"
print(f"Loading {pdf_path}...")
loader = PyPDFLoader(pdf_path)
documents = loader.load()
print("PDF loaded successfully")
print("Pages:", len(documents))

# 2. Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
print("Chunks created:", len(chunks))

# 3. Create embeddings using Sentence Transformers
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("Creating embeddings... (This might take a moment if downloading the model)")

# 4. Create vector database using FAISS
vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)
print("Vector database created")

# 5. Save vector database safely inside the data folder
os.makedirs("data/vectorstore", exist_ok=True)
vectorstore.save_local("data/vectorstore")
print("Vector database saved successfully in data/vectorstore!")
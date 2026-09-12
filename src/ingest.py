import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load ALL PDFs from the documents folder
folder_path = "data/documents"
print(f"Loading all PDFs from {folder_path}...")
loader = PyPDFDirectoryLoader(folder_path)
documents = loader.load()
print("All PDFs loaded successfully!")
print("Total Pages:", len(documents))

# 2. Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
print("Total Chunks created:", len(chunks))

# 3. Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("Creating embeddings... (This might take a moment)")

# 4. Create vector database
vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)
print("Vector database created")

# 5. Save vector database
os.makedirs("data/vectorstore", exist_ok=True)
vectorstore.save_local("data/vectorstore")
print("Vector database saved successfully in data/vectorstore!")

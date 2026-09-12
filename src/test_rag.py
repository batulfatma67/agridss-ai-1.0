from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import csv
import os

# 1. Load the Embedding Model and Vector Database
print("Loading Database for Testing...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("data/vectorstore", embeddings, allow_dangerous_deserialization=True)

# 2. List of 20 Test Questions (5 for each crop)
questions = [
    # Wheat Questions
    "When should I irrigate my wheat crop?",
    "How much fertilizer should I apply to wheat at different growth stages?",
    "What are the most common weeds in wheat and how to control them?",
    "How does plant population density affect wheat lodging?",
    "What is the benchmark height for an extended wheat stem?",
    
    # Rice Questions
    "How to prepare land for lowland rice cultivation?",
    "What is the recommended seed rate for a wet bed rice nursery?",
    "How can I control the African rice gall midge insect?",
    "What are the symptoms of iron toxicity in rice?",
    "How to manage weeds using pre-emergence chemicals in direct-seeded rice?",
    
    # Maize Questions
    "What are the common root diseases in maize like Pythium and Rhizoctonia?",
    "What factors govern the ear size of maize?",
    "How does poor soil aeration and waterlogging affect maize roots?",
    "How to identify the presence of a hardpan in a maize field?",
    "What is the benchmark length for a maize ear in good condition?",
    
    # Cotton / General Crop-Livestock Questions (from the Burkina Faso document)
    "How does Conservation Agriculture help in crop-livestock integration?",
    "What is the process of making silage and salt-licks for livestock?",
    "How to control weeds using Mucuna as a cover crop?",
    "What are the benefits of zero tillage and direct seeding?",
    "How does crop diversification improve soil fertility and farm income?"
]

# 3. Test the RAG Pipeline and Save Results
output_file = "rag_test_report.csv"

print(f"\nRunning {len(questions)} questions through the RAG Pipeline...\n")

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the Header of the CSV
    writer.writerow(["Question", "Retrieved Document", "Page No", "Context Match?", "Retrieved Text Snippet"])
    
    for i, q in enumerate(questions, 1):
        # Search the database
        docs = vectorstore.similarity_search(q, k=1)
        
        if docs:
            doc = docs[0]
            source = os.path.basename(doc.metadata.get("source", "Unknown"))
            page = doc.metadata.get("page", "N/A")
            # Get a short snippet of the text
            snippet = doc.page_content.replace("\n", " ")[:200] + "..."
            
            # Write to CSV (Leaving 'Context Match' blank for you to quickly review)
            writer.writerow([q, source, page, "Yes", snippet])
            print(f"[{i}/20] Tested: {q} -> Found in {source} (Page {page})")
        else:
            writer.writerow([q, "None", "None", "No", "No context found"])
            print(f"[{i}/20] Tested: {q} -> NO MATCH FOUND")

print(f"\n✅ Testing Complete! Open '{output_file}' to see the full report.")
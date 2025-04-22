
from docling.document_converter import DocumentConverter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_community.vectorstores import FAISS  # Vector database
from langchain_huggingface import HuggingFaceEmbeddings  # For text embeddings
from langchain_ollama.llms import OllamaLLM  # Local LLM integration
from langchain.prompts import PromptTemplate  # For customizing LLM prompts
from langchain.chains import RetrievalQA  # For question-answering pipeline
import time



def getQuestionAnswerChain(vector_store):
    """
    Create question-answer chain using LLM and vector store
    """
    # Initialize local LLM using Ollama
    llm = OllamaLLM(model="llama3.1")
    
    # Define custom prompt template for better QA responses
    prompt_template = """
        Use the following pieces of context to answer the question at the end.
        
        Check context very carefully and reference and try to make sense of that before responding.
        If you don't know the answer, just say you don't know.
        Don't try to make up an answer.
        Answer must be to the point.
        Think step-by-step.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    qaChain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Combines all retrieved docs into single context
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),  # Retrieve top 3 relevant chunks
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,  # Include source documents in response
    )
    return qaChain


def createVectorStore(texts: List[str]) -> FAISS:
    """
    Create and initialize FAISS vector store using text embeddings
    """
    # Initialize sentence transformer model for text embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )
    vectorStore = FAISS.from_texts(texts, embeddings)
    return vectorStore

def extractPDFText(file_path) -> str:
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_markdown()

def setup():
    """
    Main function to setup the PDF processing and QA pipeline
    Workflow: Extract | Split_Chunks | Vector_Store_Embeddings_QAChain
    """
    
    file_path = "sample/sample-invoice.pdf"

    #Extract PDF Text
    extractedPDFText = extractPDFText(file_path)
    with open("output.txt", 'w') as file:
        file.write(extractedPDFText)
    
    # STEP 2: Split PDF text into smaller chunks for processing
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # Maximum chunk size in characters
        chunk_overlap=100,  # Overlap between chunks to maintain context
        is_separator_regex=False
    )
    textChunks = textSplitter.split_text(extractedPDFText)
    
    # STEP 3:  vector store with embeddings for search
    vectorStore = createVectorStore(textChunks)
    
    # STEP 4: Initialize QA chain for processing questions
    qaChain = getQuestionAnswerChain(vectorStore)

    questionsAnswers(qaChain)
    
   

def questionsAnswers(qaChain):
    start_time = time.time()
    question = "What is VAT No. ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is VAT% ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is Invoice No ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is the Invoice Period ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is the Invoice Address ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is the Invoice Name and Phone # ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is the total amount for Transaction Fee T3 ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "List  all the Query References from table?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

if __name__ == "__main__":
    setup()

from docling.document_converter import DocumentConverter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_community.vectorstores import FAISS  # Vector database
from langchain_huggingface import HuggingFaceEmbeddings  # For text embeddings
from langchain_ollama.llms import OllamaLLM  # Local LLM integration
from langchain.prompts import PromptTemplate  # For customizing LLM prompts
from langchain.chains import RetrievalQA  # For question-answering pipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import time



def createPrompts() -> PromptTemplate :
     # Define custom prompt template for responses
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
    
    return PROMPT

def configureLLM() -> OllamaLLM :
    # Initialize local LLM using Ollama
    llm = OllamaLLM(model="llama3.2")
    return llm

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
    
    # STEP 4: configure the LLM 
    llm = configureLLM()

    # STEP 5: Create Prompts 
    prompts = createPrompts()

     # STEP 6: Initialize QA chain for processing questions
    qaChain = (
    {
        "context": vectorStore.as_retriever(),
        "question": RunnablePassthrough()
    }
        | prompts
        | llm
        | StrOutputParser()
    )
    

    # # STEP 6: Initialize QA chain for processing questions
    # qaChain = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",  # Combines all retrieved docs into single context
    #     retriever=vectorStore.as_retriever(search_kwargs={"k": 3}),  # Retrieve top 3 relevant chunks
    #     chain_type_kwargs={"prompt": prompts},
    #     return_source_documents=True,  # Include source documents in response
    #     )
    questionsAnswers(qaChain)
       

def questionsAnswers(qaChain):
    start_time = time.time()
    question = "What is VAT No. ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke(question)
    print(f"\nAnswer: {response}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is VAT% ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke(question)
    print(f"\nAnswer: {response}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is Invoice No ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke(question)
    print(f"\nAnswer: {response}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is the Invoice Period ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke(question)
    print(f"\nAnswer: {response}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is the Invoice Address ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke(question)
    print(f"\nAnswer: {response}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is the Invoice Name and Phone # ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke(question)
    print(f"\nAnswer: {response}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "What is the total amount for Transaction Fee T3 ?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke(question)
    print(f"\nAnswer: {response}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

    start_time = time.time()
    question = "List down all the  Query References?"
    print(f"\nQuestion: {question}")
    response = qaChain.invoke(question)
    print(f"\nAnswer: {response}")
    end_time = time.time() - start_time
    print(f"Time taken : {end_time:.2f} seconds.")

if __name__ == "__main__":
    setup()
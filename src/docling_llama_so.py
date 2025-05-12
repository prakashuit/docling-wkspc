from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import SimpleJsonOutputParser, JsonOutputParser
from langchain_ollama.llms import OllamaLLM  # Local LLM integration
from invoice_pydantic import Invoice, Service
from docling.document_converter import DocumentConverter
from ollama import chat
import time
from langchain_ollama import ChatOllama

prompt = PromptTemplate.from_template("""
You are an expert in Invoice data parser. Parse data and collect the details from the user query input.

Use this Schema:

{schema}

Respond only as JSON based on above-mentioned schema.
Strictly follow JSON Schema use the description from each field, do not add extra fields.

If you don't know any field then set it to None.
                                      
Think Step-by-step 

{query}
""")
def extractPDFText(file_path) -> str:
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_markdown()

def method1() :
    print(Invoice.model_json_schema())
    llama3 = OllamaLLM(model="llama3.2")
    llm = prompt | llama3 | SimpleJsonOutputParser()
    response = llm.invoke({"query": extractPDFText("sample/sample-invoice.pdf"), 
            "schema": Invoice.model_json_schema()})
    print(response)
    ...

def method2() :
    content = extractPDFText("sample/sample-invoice.pdf")
    response = chat(
        model="llama3.2",
        messages=[
            {
                "role":"user",
                "content":content
            }
        ],
        format=Invoice.model_json_schema(),
    )
    invoice = Invoice.model_validate_json(response.message.content)
    print(invoice.model_dump_json())
    ...

def method3():
    llm = ChatOllama(model='llama3.2').with_structured_output(Invoice,method='json_schema')
    response = llm.invoke(extractPDFText("sample/sample-invoice.pdf"))
    print(response.model_dump_json())
    ...

if(__name__=='__main__'):
    start_time = time.time()
    # method1()
    # method2()
    method3()
    print(f"Time taken : {(time.time()-start_time):.2f} seconds.")
from pydantic import BaseModel, Field
from typing import List

class Service(BaseModel):
    ServiceDescription: str = Field(..., description=" Service Description from table ")
    AmountWithoutVAT: float = Field(..., description="Amount-without VAT")
    Quantity: int = Field(..., description="quantity")
    TotalAmount: float = Field(..., description=" Total Amount")

class Invoice(BaseModel):
    InvoiceNo: int = Field(..., description="Invoice number from the invoice")
    PersonName: str = Field(..., description="Name of the person designated in the invoice")
    PersonAddress: str = Field(..., description="Address of the person")
    CompanyName: str = Field(..., description="Name of the company generated the invoice")
    CompanyAddress: str = Field(..., description="Address of the company generated the invoice")
    CustomerNo: int = Field(..., description="Customer number from invoice")
    InvoicePeriod: str = Field(..., description="Period of the invoice")
    InvoiceDate: str = Field(..., description="Date of the invoice")
    GrossAmount: float = Field(..., description="Total Gross Amount including VAT")
    VATPercentage: float = Field(..., description="VAT ""%"" on the invoice ")
    VATNumber: str = Field(..., description="VAT Number")
    ServiceNamesList: List[Service] = Field(..., description="Extract Service line items from the table structure on the given markdown from first page") 

# Example usage
invoice_data = {
    "InvoiceNo": 0,
    "PersonName": "ABCDEFGHIJKLM",
    "PersonAddress": "ABCDEFGHIJKLMN",
    "CompanyName": "ABCDEFGHIJKLMNOPQRSTUV",
    "CompanyAddress": "ABCDEFGHIJKLMN",
    "CustomerNo": 0,
    "InvoicePeriod": "ABCDEFGHIJKLMNOPQRST",
    "InvoiceDate": "ABCDEFGHIJKLMNOPQRSTUVWX",
    "GrossAmount": 0,
    "VATPercentage":19.0,
    "VATNumber":"DE19",
    "ServiceNamesList": [
        {
            "ServiceDescription": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "AmountWithoutVAT": 0.0,
            "Quantity": 0,
            "TotalAmount": 0
        }
    ]
}

invoice = Invoice(**invoice_data)
# print(invoice.model_dump_json(indent=4))

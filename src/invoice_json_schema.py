INVOICE_SCHEMA ={
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "InvoiceNo": {
      "type": "integer",
      "description": "Invoice No"
    },
    "PersonName": {
      "type": "string",
      "description": "Person name on the invoice"      
    },
    "PersonAddress": {
      "type": "string",
      "description": "Person Address on the invoice" 
    },
    "CompanyName": {
      "type": "string",
      "description": "Name of the company in the invoice" 
    },
    "CompanyAddress": {
      "type": "string",
      "description": "Invoice company address" 
    },
    "CustomerNo": {
      "type": "integer",
      "description": "Customer Number of the the invoice " 
    },
    "InvoicePeriod": {
      "type": "string",
      "description": "Invoice Period" 
    },
    "InvoiceDate": {
      "type": "string",
      "description": "Invoice Date" 
    },
    "GrossAmount": {
      "type": "integer",
      "description": "Gross Amount from the invoice" 
    },
    "Services": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "ServiceDescription": {
              "type": "string",
              "description": "Service description from the table" 
            },
            "Amount": {
              "type": "number",
              "description": "Amount for the service provided" 
            },
            "Quantity": {
              "type": "integer",
              "description": "Quantity of the service from the table" 
              
            },
            "TotalAmount": {
              "type": "integer",
              "description": "Total Amount for the service in context" 
            }
          },
          "required": [
            "ServiceDescription",
            "Amount",
            "Quantity",
            "TotalAmount"
          ]
        }
      ]
    }
  },
  "required": [
    "InvoiceNo",
    "PersonName",
    "PersonAddress",
    "CompanyName",
    "CompanyAddress",
    "CustomerNo",
    "InvoicePeriod",
    "InvoiceDate",
    "GrossAmount",
    "Services"
  ]
}
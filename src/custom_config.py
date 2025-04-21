import json
import logging
import time
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
    TesseractOcrOptions
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend


_log = logging.getLogger(__name__)

def customExtractConfig() -> {}:
    logging.basicConfig(level=logging.INFO)

    # input_doc_path = Path("./tests/data/pdf/2206.01062.pdf")

    ###########################################################################

    # The following sections contain a combination of PipelineOptions
    # and PDF Backends for various configurations.
    # Uncomment one section at the time to see the differences in the output.

    # PyPdfium without EasyOCR
    # --------------------
    # pipeline_options = PdfPipelineOptions()
    # pipeline_options.do_ocr = False
    # pipeline_options.do_table_structure = True
    # pipeline_options.table_structure_options.do_cell_matching = False

    # doc_converter = DocumentConverter(
    #     formatOptions={
    #         InputFormat.PDF: PdfFormatOption(
    #             pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend
    #         )
    #     }
    # )

    # PyPdfium with EasyOCR
    # -----------------
    # pipeline_options = PdfPipelineOptions()
    # pipeline_options.do_ocr = True
    # pipeline_options.do_table_structure = True
    # pipeline_options.table_structure_options.do_cell_matching = True

    # formatOptions={
    #     InputFormat.PDF: PdfFormatOption(
    #         pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend
    #     )
    # }

    # Docling Parse without EasyOCR
    # -------------------------
    # pipeline_options = PdfPipelineOptions()
    # pipeline_options.do_ocr = False
    # pipeline_options.do_table_structure = True
    # pipeline_options.table_structure_options.do_cell_matching = True

    # formatOptions={
    #     InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    # }

    # Docling Parse with EasyOCR
    # ----------------------
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.ocr_options.lang = ["es"]
    pipeline_options.accelerator_options = AcceleratorOptions(
        num_threads=4, device=AcceleratorDevice.AUTO
    )
    formatOptions : list ={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }


    # doc_converter = DocumentConverter(
    #     format_options={
    #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    #     }
    # )

    # Docling Parse with EasyOCR (CPU only)
    # ----------------------
    # pipeline_options = PdfPipelineOptions()
    # pipeline_options.do_ocr = True
    # pipeline_options.ocr_options.use_gpu = False  # <-- set this.
    # pipeline_options.do_table_structure = True
    # pipeline_options.table_structure_options.do_cell_matching = True

    # doc_converter = DocumentConverter(
    #     format_options={
    #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    #     }
    # )

    # Docling Parse with Tesseract
    # ----------------------
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.ocr_options = TesseractOcrOptions()

    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }

    # Docling Parse with Tesseract CLI
    # ----------------------
    # pipeline_options = PdfPipelineOptions()
    # pipeline_options.do_ocr = True
    # pipeline_options.do_table_structure = True
    # pipeline_options.table_structure_options.do_cell_matching = True
    # pipeline_options.ocr_options = TesseractCliOcrOptions()

    # doc_converter = DocumentConverter(
    #     format_options={
    #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    #     }
    # )

    # Docling Parse with ocrmac(Mac only)
    # ----------------------
    # pipeline_options = PdfPipelineOptions()
    # pipeline_options.do_ocr = True
    # pipeline_options.do_table_structure = True
    # pipeline_options.table_structure_options.do_cell_matching = True
    # pipeline_options.ocr_options = OcrMacOptions()

    # doc_converter = DocumentConverter(
    #     format_options={
    #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    #     }
    # )

    ###########################################################################

    return formatOptions
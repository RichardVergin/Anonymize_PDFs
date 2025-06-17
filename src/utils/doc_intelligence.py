from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import base64
import os
from PIL import Image
from pypdf import PdfWriter
import io


def convert_to_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string
 
 
def apply_doc_intelligence(base64_encoded_file, endpoint, key, model_id="prebuilt-read", return_text_only=True):
    # do ocr
    analyze_request = {
        "base64Source": base64_encoded_file
    }
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
 
    # print('start analyizing document')
    poller = document_intelligence_client.begin_analyze_document(
        model_id=model_id,
        body=analyze_request
    )
    if return_text_only:
        extracted_text = poller.result()['content']
        return extracted_text
    else:
        return poller.result()['pages']
 
 
def extract_text(file_name, directory_path, endpoint, key):
    # construct path and load file as base64 encoded
    file_path = os.path.join(directory_path, file_name)
    base64_encoded_file= convert_to_base64(
        file_path=file_path
    )
 
    # extract text
    text = apply_doc_intelligence(
        base64_encoded_file=base64_encoded_file,
        endpoint=endpoint,
        key=key
    )
    return text
 
 
def extract_layout(file_name, directory_path, endpoint, key):
    # construct path and load file as base64 encoded
    file_path = os.path.join(directory_path, file_name)
    base64_encoded_file= convert_to_base64(
        file_path=file_path
    )
 
    # extract text
    layout = apply_doc_intelligence(
        base64_encoded_file=base64_encoded_file,
        endpoint=endpoint,
        key=key,
        model_id="prebuilt-layout",
        return_text_only=False
    )
    return layout
 

import json
import boto3
import base64
import tempfile
import os
from pdf2docx import Converter
from docx2pdf import convert as docx_to_pdf
import PyPDF2
from PIL import Image
import img2pdf
from openpyxl import Workbook
from pptx import Presentation

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('S3_BUCKET', 'pdf-converter-files')

def lambda_handler(event, context):
    """Main router for all PDF operations"""
    
    path = event.get('path', '')
    
    # Route to appropriate handler
    if '/convert/' in path:
        return handle_convert(event, context)
    elif '/organize/' in path:
        return handle_organize(event, context)
    elif '/optimize/' in path:
        return handle_optimize(event, context)
    elif '/security/' in path:
        return handle_security(event, context)
    elif '/edit/' in path:
        return handle_edit(event, context)
    else:
        return error_response('Invalid endpoint')

def handle_convert(event, context):
    """Handle conversion operations"""
    path = event['path']
    body = json.loads(event.get('body', '{}'))
    
    try:
        if 'pdf-to-word' in path:
            return pdf_to_word(body, context)
        elif 'word-to-pdf' in path:
            return word_to_pdf(body, context)
        elif 'pdf-to-excel' in path:
            return pdf_to_excel(body, context)
        elif 'excel-to-pdf' in path:
            return excel_to_pdf(body, context)
        elif 'pdf-to-jpg' in path:
            return pdf_to_jpg(body, context)
        elif 'jpg-to-pdf' in path:
            return jpg_to_pdf(body, context)
        else:
            return error_response('Conversion type not supported')
    except Exception as e:
        return error_response(str(e))

def handle_organize(event, context):
    """Handle PDF organization operations"""
    path = event['path']
    body = json.loads(event.get('body', '{}'))
    
    try:
        if 'merge' in path:
            return merge_pdfs(body, context)
        elif 'split' in path:
            return split_pdf(body, context)
        elif 'rotate' in path:
            return rotate_pdf(body, context)
        elif 'delete-pages' in path:
            return delete_pages(body, context)
        elif 'extract-pages' in path:
            return extract_pages(body, context)
        else:
            return error_response('Organization type not supported')
    except Exception as e:
        return error_response(str(e))

def handle_optimize(event, context):
    """Handle PDF optimization operations"""
    path = event['path']
    body = json.loads(event.get('body', '{}'))
    
    try:
        if 'compress' in path:
            return compress_pdf(body, context)
        elif 'repair' in path:
            return repair_pdf(body, context)
        elif 'optimize' in path:
            return optimize_pdf(body, context)
        else:
            return error_response('Optimization type not supported')
    except Exception as e:
        return error_response(str(e))

def handle_security(event, context):
    """Handle PDF security operations"""
    path = event['path']
    body = json.loads(event.get('body', '{}'))
    
    try:
        if 'protect' in path:
            return protect_pdf(body, context)
        elif 'unlock' in path:
            return unlock_pdf(body, context)
        else:
            return error_response('Security operation not supported')
    except Exception as e:
        return error_response(str(e))

def handle_edit(event, context):
    """Handle PDF editing operations"""
    path = event['path']
    body = json.loads(event.get('body', '{}'))
    
    try:
        if 'watermark' in path:
            return add_watermark(body, context)
        elif 'page-numbers' in path:
            return add_page_numbers(body, context)
        elif 'ocr' in path:
            return ocr_pdf(body, context)
        else:
            return error_response('Edit operation not supported')
    except Exception as e:
        return error_response(str(e))

# Conversion functions
def pdf_to_word(body, context):
    file_content = base64.b64decode(body['file0'])
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pdf_file:
        pdf_file.write(file_content)
        pdf_path = pdf_file.name
    
    docx_path = pdf_path.replace('.pdf', '.docx')
    
    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()
    
    with open(docx_path, 'rb') as docx_file:
        docx_content = docx_file.read()
    
    download_url = upload_to_s3(docx_content, 'converted.docx', context)
    
    os.remove(pdf_path)
    os.remove(docx_path)
    
    return success_response(download_url, 'converted.docx')

def merge_pdfs(body, context):
    merger = PyPDF2.PdfMerger()
    
    # Get all files
    file_count = 0
    while f'file{file_count}' in body:
        file_content = base64.b64decode(body[f'file{file_count}'])
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(file_content)
            merger.append(temp_file.name)
        file_count += 1
    
    output_path = tempfile.mktemp(suffix='.pdf')
    merger.write(output_path)
    merger.close()
    
    with open(output_path, 'rb') as output_file:
        merged_content = output_file.read()
    
    download_url = upload_to_s3(merged_content, 'merged.pdf', context)
    os.remove(output_path)
    
    return success_response(download_url, 'merged.pdf')

def compress_pdf(body, context):
    file_content = base64.b64decode(body['file0'])
    options = json.loads(body.get('options', '{}'))
    level = options.get('level', 'medium')
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as input_file:
        input_file.write(file_content)
        input_path = input_file.name
    
    output_path = tempfile.mktemp(suffix='.pdf')
    
    # Compression logic here (using ghostscript or similar)
    # For now, placeholder
    with open(input_path, 'rb') as f:
        compressed_content = f.read()
    
    download_url = upload_to_s3(compressed_content, 'compressed.pdf', context)
    
    os.remove(input_path)
    
    return success_response(download_url, 'compressed.pdf')

def protect_pdf(body, context):
    file_content = base64.b64decode(body['file0'])
    options = json.loads(body.get('options', '{}'))
    password = options.get('password', '')
    
    reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    writer = PyPDF2.PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    writer.encrypt(password)
    
    output_path = tempfile.mktemp(suffix='.pdf')
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    with open(output_path, 'rb') as f:
        protected_content = f.read()
    
    download_url = upload_to_s3(protected_content, 'protected.pdf', context)
    os.remove(output_path)
    
    return success_response(download_url, 'protected.pdf')

# Helper functions
def upload_to_s3(content, filename, context):
    file_key = f"processed/{context.request_id}/{filename}"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_key,
        Body=content
    )
    
    download_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': file_key},
        ExpiresIn=3600
    )
    
    return download_url

def success_response(download_url, filename):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'success': True,
            'download_url': download_url,
            'filename': filename
        })
    }

def error_response(message):
    return {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'success': False,
            'error': message
        })
    }

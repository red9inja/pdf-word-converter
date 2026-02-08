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
    elif '/resume/' in path:
        return handle_resume(event, context)
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

def handle_resume(event, context):
    """Handle resume building operations"""
    path = event['path']
    body = json.loads(event.get('body', '{}'))
    
    try:
        if 'build' in path:
            return build_resume(body, context)
        elif 'ats-check' in path:
            return check_ats_score(body, context)
        elif 'templates' in path:
            return get_resume_templates(body, context)
        elif 'cover-letter' in path:
            return generate_cover_letter(body, context)
        else:
            return error_response('Resume operation not supported')
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

# Resume building functions
def build_resume(body, context):
    """Build ATS-optimized resume from user data"""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    
    options = json.loads(body.get('options', '{}'))
    personal_info = options.get('personalInfo', {})
    template = options.get('template', 'modern')
    
    # Create PDF
    output_path = tempfile.mktemp(suffix='.pdf')
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # ATS-friendly formatting
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#000000',
        spaceAfter=12
    )
    
    # Add content
    story.append(Paragraph(personal_info.get('fullName', ''), title_style))
    story.append(Paragraph(f"{personal_info.get('email', '')} | {personal_info.get('phone', '')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Professional Summary
    if options.get('summary'):
        story.append(Paragraph('PROFESSIONAL SUMMARY', styles['Heading2']))
        story.append(Paragraph(options['summary'], styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Work Experience
    experience = options.get('experience', {})
    if experience.get('jobTitle'):
        story.append(Paragraph('WORK EXPERIENCE', styles['Heading2']))
        story.append(Paragraph(f"<b>{experience['jobTitle']}</b> - {experience.get('company', '')}", styles['Normal']))
        story.append(Paragraph(experience.get('duration', ''), styles['Normal']))
        
        responsibilities = experience.get('responsibilities', '').split('\n')
        for resp in responsibilities:
            if resp.strip():
                story.append(Paragraph(resp, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Education
    education = options.get('education', {})
    if education.get('degree'):
        story.append(Paragraph('EDUCATION', styles['Heading2']))
        story.append(Paragraph(f"<b>{education['degree']}</b>", styles['Normal']))
        story.append(Paragraph(f"{education.get('university', '')} - {education.get('year', '')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Skills
    if options.get('skills'):
        story.append(Paragraph('SKILLS', styles['Heading2']))
        story.append(Paragraph(options['skills'], styles['Normal']))
    
    doc.build(story)
    
    with open(output_path, 'rb') as f:
        resume_content = f.read()
    
    download_url = upload_to_s3(resume_content, 'resume.pdf', context)
    os.remove(output_path)
    
    return success_response(download_url, 'resume.pdf')

def check_ats_score(body, context):
    """Check ATS compatibility score of resume"""
    file_content = base64.b64decode(body['file0'])
    
    # Extract text from resume
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(file_content)
        temp_path = temp_file.name
    
    reader = PyPDF2.PdfReader(temp_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    # ATS scoring logic
    score = 0
    feedback = []
    
    # Check for standard sections
    sections = ['experience', 'education', 'skills', 'summary']
    for section in sections:
        if section.lower() in text.lower():
            score += 20
        else:
            feedback.append(f"Missing '{section}' section")
    
    # Check for contact info
    if '@' in text:
        score += 10
    else:
        feedback.append("Missing email address")
    
    # Check for phone number
    import re
    if re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', text):
        score += 10
    else:
        feedback.append("Missing phone number")
    
    os.remove(temp_path)
    
    result = {
        'score': min(score, 100),
        'feedback': feedback,
        'recommendations': [
            'Use standard section headings',
            'Include relevant keywords',
            'Keep formatting simple',
            'Use standard fonts'
        ]
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'success': True,
            'result': result
        })
    }

def generate_cover_letter(body, context):
    """Generate personalized cover letter"""
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from datetime import datetime
    
    options = json.loads(body.get('options', '{}'))
    
    output_path = tempfile.mktemp(suffix='.pdf')
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Date
    story.append(Paragraph(datetime.now().strftime('%B %d, %Y'), styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Greeting
    manager = options.get('manager', 'Hiring Manager')
    story.append(Paragraph(f"Dear {manager},", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Body
    company = options.get('company', 'your company')
    position = options.get('position', 'this position')
    
    intro = f"I am writing to express my strong interest in the {position} position at {company}."
    story.append(Paragraph(intro, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    if options.get('why'):
        story.append(Paragraph(options['why'], styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    skills = options.get('skills', '')
    if skills:
        skills_text = f"My key skills include {skills}, which align perfectly with your requirements."
        story.append(Paragraph(skills_text, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    closing = "I look forward to the opportunity to discuss how I can contribute to your team."
    story.append(Paragraph(closing, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Sincerely,", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(options.get('name', ''), styles['Normal']))
    
    doc.build(story)
    
    with open(output_path, 'rb') as f:
        letter_content = f.read()
    
    download_url = upload_to_s3(letter_content, 'cover_letter.pdf', context)
    os.remove(output_path)
    
    return success_response(download_url, 'cover_letter.pdf')

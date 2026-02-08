import json
import boto3
import base64
from pdf2docx import Converter
import tempfile
import os

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('S3_BUCKET', 'pdf-converter-files')

def lambda_handler(event, context):
    try:
        # Get file from request
        body = json.loads(event['body'])
        file_content = base64.b64decode(body['file'])
        
        # Create temp files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pdf_file:
            pdf_file.write(file_content)
            pdf_path = pdf_file.name
        
        docx_path = pdf_path.replace('.pdf', '.docx')
        
        # Convert PDF to Word
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
        
        # Read converted file
        with open(docx_path, 'rb') as docx_file:
            docx_content = docx_file.read()
        
        # Upload to S3
        file_key = f"converted/{context.request_id}.docx"
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=docx_content,
            ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
        # Generate presigned URL (valid for 1 hour)
        download_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_key},
            ExpiresIn=3600
        )
        
        # Cleanup
        os.remove(pdf_path)
        os.remove(docx_path)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'download_url': download_url
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }

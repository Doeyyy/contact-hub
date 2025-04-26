import os
import tempfile
import uuid
from django.conf import settings
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from django.core.exceptions import ValidationError

def upload_document_to_backblaze(file, existing_document=None, bucket_name=settings.AWS_STORAGE_BUCKET_NAME):
    """
    Upload a document file to Backblaze B2 and return the public URL.
    
    Args:
        file: The document file uploaded by the user
        existing_document: An existing document to replace (optional)
        bucket_name: The Backblaze B2 bucket name
            
    Returns:
        str: Public URL of the uploaded document in Backblaze B2
        
    Raises:
        ValidationError: If the file is not a valid document type
    """
    # Validate the file - check for document file types
    allowed_content_types = [
        'application/pdf',                 # PDF
        'application/msword',              # DOC
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # DOCX
        'text/plain'                       # TXT
    ]
    
    # If content_type is not available or reliable, check file extension
    file_ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.pdf', '.doc', '.docx', '.txt']
    
    if file.content_type not in allowed_content_types and file_ext not in valid_extensions:
        raise ValidationError("Only document files (PDF, DOC, DOCX, TXT) are allowed.")

    # Create a unique filename to prevent overwriting existing files
    # Use a folder structure in the bucket for better organization
    folder_name = "documents"
    unique_filename = f"{folder_name}/{uuid.uuid4()}{file_ext}"
    
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Authorize Backblaze account
        application_key_id = settings.AWS_ACCESS_KEY_ID
        application_key = settings.AWS_SECRET_ACCESS_KEY
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", application_key_id, application_key)

        # Upload the document to Backblaze
        bucket = b2_api.get_bucket_by_name(bucket_name)
        
        # Determine content type
        content_type = file.content_type
        if content_type not in allowed_content_types:
            if file_ext == '.pdf':
                content_type = 'application/pdf'
            elif file_ext == '.doc':
                content_type = 'application/msword'
            elif file_ext == '.docx':
                content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif file_ext == '.txt':
                content_type = 'text/plain'
        
        # Upload with content type and metadata
        uploaded_file = bucket.upload_local_file(
            local_file=temp_file_path,
            file_name=unique_filename,
            content_type=content_type,
            file_info={'original_filename': file.name}
        )

        # Clean up the temporary file
        os.remove(temp_file_path)

        # Construct the direct URL to the file
        # Format: https://[custom_domain]/[filename]
        # or: https://[bucket_name].s3.[region].backblazeb2.com/[filename]
        if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN') and settings.AWS_S3_CUSTOM_DOMAIN:
            document_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
        else:
            document_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.backblazeb2.com/{unique_filename}"
        
        return document_url
        
    except Exception as e:
        # Clean up temp file in case of error
        try:
            if 'temp_file_path' in locals():
                os.remove(temp_file_path)
        except:
            pass
        
        # Re-raise the exception with more context
        raise ValidationError(f"Document upload failed: {str(e)}")
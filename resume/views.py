import spacy
import re
import pdfplumber
import docx
import io
import pytesseract
from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer

# Load the spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

def extract_first_name_ner(text):
    """
    Use spaCy's Named Entity Recognition (NER) to extract the first name.
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            print(f"Detected entity: {ent.text}")  #  print
            return ent.text.split()[0]  # Extract the first word as the first name
    return None

def parse_text(text):
    first_name = None
    email = None
    mobile_number = None

    # Regular expressions for email and mobile number
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_regex = r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'

    # Split text into lines for easier parsing
    lines = text.split('\n')

    # Try to find the first name using spaCy NER (AI-based)
    if not first_name:
        first_name = extract_first_name_ner(text)
    
    # Fallback: If spaCy NER couldn't extract the first name, use regex as a backup
    if not first_name:
        for line in lines:
            line = line.strip()
            if len(line.split()) >= 2 and '@' not in line:
                first_name = line.split()[0]  # Get the first word as the first name
                break

    # Check for an email address
    for line in lines:
        if not email:
            email_match = re.search(email_regex, line)
            if email_match:
                email = email_match.group(0)

        # Check for a mobile number
        if not mobile_number:
            phone_match = re.search(phone_regex, line)
            if phone_match:
                mobile_number = phone_match.group(0)

    return first_name, email, mobile_number

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Try extracting text normally
            extracted_text = page.extract_text() or ""
            if not extracted_text:
                # Fall back to OCR if no text is found
                image = page.to_image().original  # Convert PDF page to an image
                extracted_text = pytesseract.image_to_string(image)
            text += extracted_text
    return text

def extract_text_from_docx(file):
    text = ""
    doc = docx.Document(io.BytesIO(file.read()))
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

class ResumeExtractionView(APIView):
    
    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return Response({"error": "No resume file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_extension = resume_file.name.split('.')[-1].lower()
        text = ""
        try:
            if file_extension == 'pdf':
                text = extract_text_from_pdf(resume_file)
            elif file_extension in ['doc', 'docx']:
                text = extract_text_from_docx(resume_file)
            else:
                return Response({"error": "Unsupported file type. Only PDF and DOC/DOCX are supported."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Print the extracted text for debugging
        print(f"Extracted text: {text}")

        first_name, email, mobile_number = parse_text(text)
        
        # Debug prints
        print(f"Extracted first name: {first_name}")
        print(f"Extracted email: {email}")
        print(f"Extracted mobile number: {mobile_number}")
        
        if not email:
            return Response({"error": "Email address not found in the resume."}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate, created = Candidate.objects.update_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'mobile_number': mobile_number
            }
        )
        
        if created:
            return Response({"message": "Candidate created successfully.", "candidate": CandidateSerializer(candidate).data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Candidate with this email already exists.", "candidate": CandidateSerializer(candidate).data}, status=status.HTTP_200_OK)

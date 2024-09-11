# # resume/services.py

# from pyresparser import ResumeParser
# import os

# def extract_resume_data(file_path):
#     # Ensure the file path is valid
#     if not os.path.isfile(file_path):
#         raise FileNotFoundError("The provided file path does not exist.")

#     # Use pyresparser to extract resume information
#     data = ResumeParser(file_path).get_extracted_data()

    
#     first_name = data.get('name', '').split()[0]  # Get first name from the full name
#     email = data.get('email', '')
#     mobile_number = data.get('mobile_number', '')

#     return {
#         'first_name': first_name,
#         'email': email,
#         'mobile_number': mobile_number
#     }

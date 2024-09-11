
# Resume Processor

Django project with a REST API endpoint that processes a resume to extract the candidate's first name, email ID, and mobile number.




## Project Setup
1) Install Django

```bash
  pip install Django
  pip install djangorestframework
```

2) Navigate to Your Project Directory

```bash
  cd ResumeProcessor
```

3)Run the Development Server
```bash
  python manage.py runserver
```


## Test API using Postman

- Set method to POST.

- URL: http://127.0.0.1:8000/api/extract_resume/

- Under the "Body" tab, select "form-data".

- Add a key named resume with type File, and choose a file to upload.




## Screenshots

![Screenshot 1](https://github.com/Khushi-Bhatia/ResumeProcessor/blob/master/Screenshots/Screenshot%201.jpg)


![Screenshot 2](https://github.com/Khushi-Bhatia/ResumeProcessor/blob/master/Screenshots/Screenshot%202.jpg)

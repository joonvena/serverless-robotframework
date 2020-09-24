# Serverless-Robotframework  
Purpose of this project is to run simple Robot Framework test cases using lambda functions. Currently it is possible to run tests with standard libraries including:

- Builtin
- String
- Dialogs
- DateTime
- Collections
- XML
- RequestsLibrary

# Run Project
If you want to run project locally using virtualenv:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
FRONTEND_URL=http://localhost:3000 REPORT_BUCKET=bucket_name chalice local --no-autoreload
```

I'm using Terraform to manage the infrastructure for the backend. Currently its using S3 as backend for tfstate files. If you want to use this template you have to create the bucket for tfstate files manually and update the bucket name in the tf/chalice.tf.json file. When you execute this template it will as you for AWS_REGION and FRONTEND_URL. FRONTEND_URL is used to define CORS rules.
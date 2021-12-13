@ECHO OFF
ECHO Starting CI/CD Pipeline for schemavalidatexmltojson serverless application.
call .venv\Scripts\activate.bat
ECHO Installing CDK dependencies for Pipeline.
call pip install -r requirements.txt
ECHO Installing CDK Unit Test dependencies.
call pip install -r requirements-dev.txt
ECHO Running test UNIT cases.
call pytest
ECHO Running CDK Synth to generate YAML Cloudformation.
call cdk synth
ECHO Running CDK Diff to get changeset.
call cdk diff
ECHO Running CDK Deploy to create Pipeline for schemavalidatexmltojson project.
call cdk deploy
call .venv\Scripts\deactivate.bat
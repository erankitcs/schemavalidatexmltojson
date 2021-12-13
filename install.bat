@ECHO OFF
ECHO Starting schemavalidatexmltojson serverless application.
call .venv\Scripts\activate.bat
ECHO Installing test dependencies schemavalidatexmltojson testing.
call pip install -r tests\requirements.txt
ECHO Running test UNIT cases.
call coverage run -m pytest tests\unit
ECHO Running SAM Build
call sam build
ECHO Running SAM Deployment in guided mode.
call sam deploy --guided
call .venv\Scripts\deactivate.bat
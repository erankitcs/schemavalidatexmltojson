sam init
sam build
sam deploy 
sam deploy --guided

-- unit test
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip 
pip install -r tests\requirements.txt
coverage run -m pytest tests\unit

--
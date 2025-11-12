## to create requirements.txt
pip list --format=freeze | findstr -v "pkg1 pkg2 ..." > requirements.txt

# to create a virtural environment
py -m venv venv

# to activeate
.\venv\Scripts\Activate
## this should show (venv) before the file in the command line


# to install requirements in venv
1. activate venv (See above)
2. run pip install -r requirements.txt
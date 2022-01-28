**Activate the virtual environment**

'''
source blockchain-env/bin/activate
blockchain-env.scripts/activate
'''

***install all packages**

'''
pip3 install -r requirements.txt
'''

**Run the tests**

Make sure to activate the virtual environment

'''
python3 -m pytest backend/tests
'''
***Run the Application and the API**

make sure to activat the virtual environment

' ' '
python3 backend.app

''

export PEER=True && python3 -m backend.app
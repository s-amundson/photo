import urllib
# import urllib
import ssl
import requests

import logging
logger = logging.getLogger(__name__)
BASE_ADDRESS = 'https://0.0.0.0:8080/'
GALLERY_ID = 1
UPLOAD_ADDRESS = BASE_ADDRESS + 'add_image/' + str(GALLERY_ID) + '/'
PATH_TO_LOGIN = 'accounts/login/'
SSL_VERIFY = False



# Login to the site
session = requests.session()
session.headers['Referer'] = BASE_ADDRESS + PATH_TO_LOGIN
session.verify = SSL_VERIFY
r = session.get(BASE_ADDRESS + PATH_TO_LOGIN)
csrf = r.cookies.get('csrftoken')
logging.warning(r.status_code)
logging.warning(r.content)
logging.warning(csrf)
auth = {'login': 'EmilyNConlan@einrot.com', 'password': 'Plus6494', 'csrfmiddlewaretoken': csrf}
r = session.post(BASE_ADDRESS + PATH_TO_LOGIN, data=auth)
logging.warning(r.status_code)
logging.warning(r.content)

# Upload a picture
r = session.get(UPLOAD_ADDRESS)
csrf = r.cookies.get('csrftoken')
logging.warning(csrf)
filepath = '/home/sam/Pictures/20210720/DSC_0141_cropped.JPG'
files = {'image': open(filepath,'rb')}
data = {'privacy_level': 'private', 'csrfmiddlewaretoken': csrf}
r = session.post(UPLOAD_ADDRESS, data, files=files)
logging.warning(r.status_code)
for line in r.content.splitlines()[:500]:
    logging.warning(line)
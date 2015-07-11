"""

Utils including:
 - login
 - issue browsing/article processing regex
 - database check and create

"""
from models import db_connect
import os
import pickle
import requests
import re
import settings

# Save pickle session to the same folder as login.py
session_name = 'caixin.p'
abs_path = os.path.realpath(__file__)
session_path = abs_path.replace(__file__, session_name)

def load_session_or_login():
    """

    :return: a requests.session() that available for crawling
    """
    try:
        session = pickle.load(open(session_path, 'rb'))
        # TODO: verify correctness, or raise error
        # - should contain cookies
        # - didn't timeout, get a new page to check
        return session
    except (TypeError, FileNotFoundError, ValueError):
        # TypeError: didn't use open(filename, 'rb')
        # FileNotFoundError: file not found
        # ValueError: didn't use python3, unsupported pickle protocol
        return login()


def login():
    url_in_login = re.compile('(?<=src=\").*?(?=\")')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/43.0.2357.81 Safari/537.36',
        'Referer': 'http://user.caixin.com/usermanage/login/',
        'Via': 'Copyright@2014 Caixin'
    }
    # TODO: check this `cookiestime`
    data = dict(
        backUrl='http://weekly.caixin.com/',
        cookietime='31536000',
    )

    data['username'] = settings.USERNAME
    data['password'] = settings.PASSWORD

    # Init cookies
    login_session = requests.session()
    login_session.get('http://user.caixin.com/usermanage/login/',
                      headers=headers)

    # Login
    j = login_session.post('http://user.caixin.com/usermanage/login/',
                           headers=headers,
                           data=data)

    # Finish login by GET each redirecting-urls
    urls = url_in_login.findall(j.text)
    for url in urls:
        _ = login_session.get(url, headers=headers)

    # Go to index
    logged_in = login_session.get('http://weekly.caixin.com/')

    # Dump to the same folder as login.py
    pickle.dump(logged_in, open(session_path, 'wb'))

    return logged_in


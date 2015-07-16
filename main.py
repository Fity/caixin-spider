"""

Skeleton yet.

"""

from spider import Spider
from utils import load_session_or_login


def main():
    # Get requests.session
    session = load_session_or_login()

    # Run actual spider code non-blockingly
    caixin_spider = Spider(session)
    caixin_spider.run()

    # Generate ebooks and push to subscribers' kindle

    return True


if __name__ == '__main__':
    main()

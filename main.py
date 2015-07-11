"""

Skeleton yet.

"""

from models import db_connect, create_engine, insert_item
from sqlalchemy.orm import sessionmaker
from utils import load_session_or_login

def main():
    # Get requests.session
    session = load_session_or_login()

    # Get database session for add and commit sql_item
    db_engine = db_connect()
    create_engine(db_engine)
    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    # Run actual spider code non-blockingly

    # Generate ebooks and push to subscribers' kindle

    return True


if __name__ == 'main':
    main()

#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add user to the database """
        _session = self._session
        user = User(email=email, hashed_password=hashed_password)
        _session.add(user)
        _session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Searches for a user baesd on the given key """
        _session = self._session
        try:
            user = _session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError()

        if user is None:
            raise NoResultFound()
        else:
            return user

    def update_user(self, user_id: str, **kwargs) -> None:
        """ Update details of a user """
        _session = self._session
        user = self.find_user_by(id=user_id)
        for attr, value in kwargs.items():
            # Checking if the attribute is valid
            if attr in vars(user):
                setattr(user, attr, value)
                _session.commit()
            else:
                raise ValueError()
        return None

    # def update_user(self, user_id, **kwargs: str) -> None:
    #     """ Update details of a user """
    #     _session = self._session
    #     try:
    #         user = self.find_user_by(id=user_id)
    #     except NoResultFound:
    #         # print("Not found")
    #         raise ValueError()
    #     for attr, value in kwargs.items():
    #         # Checking if the attribute is valid
    #         if vars(user).get(attr):
    #             setattr(user, attr, value)
    #             _session.commit()
    #         else:
    #             raise ValueError()
    #     return None

import logging
import threading
from contextlib import contextmanager
from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query, Session

from tracker.config import config
from tracker.models.enums import Sort
from tracker.models.model import Model

logger = logging.getLogger(__name__)


class DB:
    def __init__(self):
        self.__engine = None
        self.__session_class = None
        self.db_lock = threading.Lock()
        self.__message = None

    @property
    def engine(self):
        with self.db_lock:
            if self.__engine is None:
                self.__engine = create_engine(
                    config.db_url, connect_args={"check_same_thread": False}
                )
        return self.__engine

    @contextmanager
    def session(self) -> Session:
        """Create SQL Alchemy db session."""
        engine = self.engine
        with self.db_lock:
            if self.__session_class is None:
                self.__session_class = sessionmaker(bind=engine)

        session = self.__session_class()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def __save(session: Session, obj: Model) -> Model:
        session.add(obj)
        session.commit()
        return obj

    def save(self, obj: Model):
        with self.session() as session:
            return self.__save(session=session, obj=obj)

    def __query(
        self,
        session: Session,
        model: Model,
        filters: Optional[list] = None,
        sort_key: Optional = None,
        sort_order: Sort = Sort.ascending,
    ) -> Query:
        """Return a filtered and sorted query object.

        Args:
            session: SQLAlchemy session.
            model: Model class to query.
            filters: Other statements to filter on.
            sort_key: Sorting field.
            sort_order: Sort order.
        """
        query = session.query(model)
        # Apply filters
        if filters is not None:
            for f in filters:
                query = query.filter(f)

        # Apply sort
        if sort_key is not None:
            query = query.order_by(sort_order.func(sort_key))

        return query

    def get_by_id(self, model, obj_id: Optional[str]) -> Optional[Model]:
        """Get object by id.

        Args:
            model: Model class to query.
            obj_id: ID of the object.
        """
        if obj_id is None:
            return None

        with self.session() as session:
            return session.query(model).get(obj_id)

    def get_by_ids(self, model, obj_ids: List[str]) -> List[Model]:
        """Bulk get by ids.

        Args:
            model: Model class to query.
            obj_ids: List of object ids to search for.
        """
        with self.session() as session:
            return [
                obj
                for obj in self.__query(
                    session=session,
                    model=model,
                    filters=[
                        model.id.in_(
                            # Filter out the None ids
                            [oid for oid in obj_ids if oid is not None]
                        )
                    ],
                )
            ]

    def first(
        self,
        model,
        filters: Optional[list] = None,
        sort_key: Optional = None,
        sort_order: Sort = Sort.ascending,
    ) -> Model:
        """Get the first element.

        Args:
            model: Model class to query.
            filters: Other statements to filter on.
            sort_key: Sorting field.
            sort_order: Sort order.
        """
        with self.session() as session:
            return self.__query(
                session=session,
                model=model,
                filters=filters,
                sort_key=sort_key,
                sort_order=sort_order,
            ).first()

    def all(
        self,
        model,
        sort_key: Optional = None,
        sort_order: Sort = Sort.ascending,
    ) -> List[Model]:
        """Return all objects.

        Args:
            model: Model class to query.
            sort_key: Sorting field.
            sort_order: Sort order.
        """
        with self.session() as session:
            return [
                obj
                for obj in self.__query(
                    session=session,
                    model=model,
                    sort_key=sort_key,
                    sort_order=sort_order,
                )
            ]

    def filter(
        self,
        model,
        filters: Optional[list] = None,
        sort_key: Optional = None,
        sort_order: Sort = Sort.ascending,
    ) -> List[Model]:
        """Filter objects.

        Args:
            model: Model class to query.
            filters: Other statements to filter on.
            sort_key: Sorting field.
            sort_order: Sort order.
        """
        with self.session() as session:
            return [
                obj
                for obj in self.__query(
                    session=session,
                    model=model,
                    filters=filters,
                    sort_key=sort_key,
                    sort_order=sort_order,
                )
            ]

    def delete(self, obj: Model) -> bool:
        """Delete an object by id.

        Args:
            obj: Object to delete.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        with self.session() as session:
            try:
                session.query(obj.__class__).filter(
                    obj.__class__.id == obj.id
                ).delete()
                return True
            except Exception as e:
                logger.error(
                    "Failed to delete %s with id=%s. Error: %s",
                    obj.__class__.__name__,
                    obj.id,
                    e,
                )
                return False

    def count(self, model, filters: Optional[list] = None) -> int:
        """Count objects.

        Args:
            model: Model class to query.
            filters: Other statements to filter on.
        """
        with self.session() as session:
            return self.__query(
                session=session, model=model, filters=filters
            ).count()


db = DB()

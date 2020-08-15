import logging
from uuid import UUID
from typing import Type, Optional, List, Union

import databases
import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.engine import Engine

from traktor import errors
from traktor.config import config
from traktor.models import Model
from traktor.models.enums import Sort


logger = logging.getLogger(__name__)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class AsyncDB:
    def __init__(self):
        self.db = databases.Database(config.db_url)

    async def connect(self):
        return await self.db.connect()

    async def disconnect(self):
        return await self.db.disconnect()

    async def __query(
        self,
        model: Type[Model],
        filters: Optional[list] = None,
        sort_key: Optional = None,
        sort_order: Sort = Sort.ascending,
        first: bool = False,
    ) -> Union[Optional[Model], List[Model]]:
        """Return a filtered and sorted query object.

        Args:
            model: Model class to query.
            filters: Other statements to filter on.
            sort_key: Sorting field.
            sort_order: Sort order.
            first: Return only the first object.
        """
        if filters is None or len(filters) == 0:
            query = model.__table__.select()
        else:
            combined = filters[0]
            for f in filters[1:]:
                combined = sa.and_(combined, f)
            query = model.__table__.select(combined)

        # Apply sort
        if sort_key is not None:
            query = query.order_by(sort_order.func(sort_key))

        if first:
            obj = await self.db.fetch_one(query)
            if obj is None:
                return None
            return model.from_row(obj)
        else:
            return [
                model.from_row(row) for row in await self.db.fetch_all(query)
            ]

    async def get_by_id(self, model: Type[Model], obj_id: UUID) -> Model:
        """Get object by id.

        Args:
            model: Model class to query.
            obj_id: ID of the object.
        """
        objs = await self.__query(model=model, filters=[model.id == obj_id])
        if len(objs) == 0:
            raise errors.ObjectNotFound(model=model, query={"id": str(obj_id)})
        elif len(objs) > 1:
            raise errors.MultipleObjectsFound(
                model=model, query={"id": str(obj_id)}
            )
        else:
            return objs[0]

    async def first(
        self,
        model: Type[Model],
        filters: Optional[list] = None,
        sort_key: Optional = None,
        sort_order: Sort = Sort.ascending,
    ) -> Optional[Model]:
        """Get the first element.

        Args:
            model: Model class to query.
            filters: Other statements to filter on.
            sort_key: Sorting field.
            sort_order: Sort order.
        """
        return await self.__query(
            model=model,
            filters=filters,
            sort_key=sort_key,
            sort_order=sort_order,
            first=True,
        )

    async def get(self, model: Type[Model], filters: list) -> Model:
        """Get a specific element or raise an error.

        Args:
            model: Model class to query.
            filters: List of filter expressions.

        Raises:
            errors.ObjectNotFound: If the object is not found.
        """
        obj = await self.first(model=model, filters=filters)
        if obj is None:
            raise errors.ObjectNotFound(model=model, query={})
        return obj

    async def all(
        self,
        model: Type[Model],
        sort_key: Optional = None,
        sort_order: Sort = Sort.ascending,
    ) -> List[Model]:
        """Return all objects.

        Args:
            model: Model class to query.
            sort_key: Sorting field.
            sort_order: Sort order.
        """
        return await self.__query(
            model=model, sort_key=sort_key, sort_order=sort_order,
        )

    async def filter(
        self,
        model: Type[Model],
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
        return await self.__query(
            model=model,
            filters=filters,
            sort_key=sort_key,
            sort_order=sort_order,
        )

    async def update(self, obj: Model) -> Model:
        await self.db.execute(
            obj.__table__.update()
            .where(obj.__class__.id == obj.id)
            .values(**obj.column_dict())
        )
        return obj

    async def save(self, obj: Model) -> Model:
        await self.db.execute(
            obj.__table__.insert().values(**obj.column_dict())
        )
        return obj

    async def delete(self, obj: Model) -> bool:
        """Delete an object.

        Args:
            obj: Object to delete.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        try:
            await self.db.execute(
                obj.__table__.delete(obj.__class__.id == obj.id)
            )
            return True
        except Exception as e:
            logger.error(
                "Failed to delete %s with id=%s. Error: %s",
                obj.__class__.__name__,
                obj.id,
                e,
            )
            return False


async_db = AsyncDB()

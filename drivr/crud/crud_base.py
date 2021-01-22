from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from drivr.db.entity import Entity

ModelType = TypeVar("ModelType", bound=Entity)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """The generic implementation of CRUD actions."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Query for the entity by the PK value.

        Args:
            db: the database session.
            id: the value from the entity PK.

        Returns:
            The entity associated to the PK value provided if it exists,
            otherwise `None` is returned.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """
        Query for all entities.

        Args:
            db: the database session.
            skip: the offset value.
            limit: the max number of entities to query.

        Returns:
            A list of entities based on the query parameters provided.
            If no entity is found, an empty list is returned.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, schema: CreateSchemaType) -> ModelType:
        """
        Persist a new entity.

        Args:
            db: the database session.
            schema: the schema for create a new entity.

        Returns:
            The created entity.
        """
        entity = self.model(**jsonable_encoder(schema))
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def remove(self, db: Session, model: ModelType) -> ModelType:
        """
        Remove an existent entity.

        Args:
            db: the database session.
            model: the entity to remove.

        Returns:
            The removed entity.
        """
        db.delete(model)
        db.commit()
        return model

    def update(
        self,
        db: Session,
        model: ModelType,
        schema: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Update an existing entity.

        Args:
            db: the database session.
            model: the target entity to be updated.
            schema: the schema used to update the entity.

        Returns:
            The updated entity.
        """
        jsonable_entity = jsonable_encoder(model)

        if isinstance(schema, dict):
            update_data = schema
        else:
            update_data = schema.dict(exclude_unset=True)

        for field in jsonable_entity:
            if field in update_data:
                setattr(model, field, update_data[field])

        db.commit()
        db.refresh(model)

        return model

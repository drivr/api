from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from drivr.db.entity import Entity

ModelType = TypeVar("ModelType", bound=Entity)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, schema: CreateSchemaType) -> ModelType:
        entity = self.model(**jsonable_encoder(schema))
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def remove(self, db: Session, model: ModelType) -> ModelType:
        db.delete(model)
        db.commit()
        return model

    def update(
        self,
        db: Session,
        model: ModelType,
        schema: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:

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

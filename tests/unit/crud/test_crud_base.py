from drivr.crud.crud_base import CRUDBase

__TEST_FILE__ = "drivr.crud.crud_base"


class TestGet:
    def test_should_filter_the_entity_by_id_provided(self, faker, mocker):
        entity_id = faker.pyint()

        entity = mocker.MagicMock()
        model = mocker.MagicMock()
        model.id = faker.pyint()
        db = mocker.MagicMock()
        db.query().filter().first.return_value = entity

        crud = CRUDBase(model=model)
        assert entity == crud.get(db=db, id=entity_id)

        db.query.assert_called_with(model)
        db.query().filter.assert_called_with(model.id == entity_id)
        db.query().filter().first.assert_called_once()


class TestAll:
    def test_should_query_all_entities_using_offset_and_limit(
        self,
        faker,
        mocker,
    ):
        offset = faker.pyint(min_value=1, max_value=100)
        limit = faker.pyint(min_value=100, max_value=200)

        entities = [mocker.MagicMock()]
        model = mocker.MagicMock()
        db = mocker.MagicMock()
        db.query().offset().limit().all.return_value = entities

        crud = CRUDBase(model=model)
        assert entities == crud.all(db=db, skip=offset, limit=limit)

        db.query.assert_called_with(model)
        db.query().offset.assert_called_with(offset)
        db.query().offset().limit.assert_called_with(limit)
        db.query().offset().limit().all.assert_called_once()


class TestCreate:
    def test_create_should_add_then_commit_and_refresh_the_entity(
        self,
        mocker,
    ):
        model = mocker.MagicMock()
        entity = mocker.MagicMock()
        schema = mocker.MagicMock()
        db = mocker.MagicMock()
        jsonable_encoder_return = mocker.MagicMock()

        jsonable_encoder = mocker.patch(
            f"{__TEST_FILE__}.jsonable_encoder",
            return_value=jsonable_encoder_return,
        )

        model.return_value = entity

        crud = CRUDBase(model=model)
        assert entity == crud.create(db=db, schema=schema)

        jsonable_encoder.assert_called_once_with(schema)
        model.assert_called_once_with(**jsonable_encoder_return)
        db.add.assert_called_once_with(entity)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(entity)


class TestRemove:
    def test_should_delete_the_entity_then_commit_and_return(
        self,
        mocker,
    ):
        model = mocker.MagicMock()
        entity = mocker.MagicMock()
        db = mocker.MagicMock()

        crud = CRUDBase(model=model)
        assert entity == crud.remove(db=db, model=entity)

        db.delete.assert_called_with(entity)
        db.commit.assert_called_once()


class TestUpdate:
    def test_should_exclude_unset_when_schema_is_not_instanceof_dict(
        self,
        mocker,
    ):
        db = mocker.MagicMock()
        model = mocker.MagicMock()
        schema = mocker.MagicMock()

        jsonable_encoder = mocker.patch(f"{__TEST_FILE__}.jsonable_encoder")

        crud = CRUDBase(model=model)
        assert model == crud.update(db=db, model=model, schema=schema)
        jsonable_encoder.assert_called_once_with(model)
        schema.dict.assert_called_once_with(exclude_unset=True)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(model)

    def test_should_use_dict_to_update_the_entity(
        self,
        faker,
        mocker,
    ):
        db = mocker.MagicMock()
        model = mocker.MagicMock()
        schema = {"key": faker.word()}

        jsonable_encoder = mocker.patch(
            f"{__TEST_FILE__}.jsonable_encoder",
            return_value=schema,
        )

        crud = CRUDBase(model=model)
        assert model == crud.update(db=db, model=model, schema=schema)
        jsonable_encoder.assert_called_once_with(model)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(model)

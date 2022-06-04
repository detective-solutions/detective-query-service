# import standard modules
import logging
from typing import Any, List
from copy import deepcopy


# import third party modules
from pydantic import ValidationError

# import project related modules
from detective_query_service.pydataobject.dgraph_type import MaskingObject, ColumnMask, RowMask, DataBaseConfig
from detective_query_service.pydataobject.event_type import (
    Context,
    MaskingEvent,
    QueryEvent,
    QueryBody,
    MaskingBody,
    CaseFileEvent,
    CaseFileBody
)


class EventOperation:

    ERROR_MASKING_BODY = MaskingBody(**{
            "queryType": "error",
            "query": ["select * from myTable"],
            "tableId": ["00000000-0000-0000-0000-000000000000"],
            "groupId": ["00000000-0000-0000-0000-000000000000"]
        })

    ERROR_QUERY_BODY = QueryBody(**{
            "queryType": "sqlQuery",
            "query": ["select * from myTable"],
            "tableId": ["00000000-0000-0000-0000-000000000000"]
        })

    ERROR_MASKING_OBJECT = MaskingObject(**{
        "name": "ERROR",
        "table": "NoTable",
        "groups": [{"name": "NoGroup"}]
    })

    ERROR_DB_CONFIG = DataBaseConfig(**{
        "name": "error",
        "host": "0.0.0.0",
        "port": "0000",
        "user": "error",
        "password": "",
        "database": "error",
        "databaseSchema": "error",
        "connectorName": "error"
    })

    ERROR_CASEFILE_OBJECT = CaseFileBody(**{
        "queryType": "error",
        "query": ["placeholder"],
        "tableSchema": [{'headerName': "error", 'field': "error", 'sortable': True, 'filter': True}],
        "tableData": [{"error": "DataFrame could not be initialized"}]
    })

    @classmethod
    def read_masking_event(cls, message: dict) -> MaskingEvent:
        try:
            event = MaskingEvent(
                context=Context(**message.get("context", {})),
                body=MaskingBody(**message.get("body", {}))
            )
        except ValidationError:
            context = Context(**message.get("context", {}))
            context.valid = False
            event = MaskingEvent(
                context=context,
                body=cls.ERROR_MASKING_BODY
            )
            logging.error(f"InitializationError for MaskingEvent with {message} in {context.dict()}")

        return event

    @classmethod
    def read_query_event(cls, message: dict) -> QueryEvent:
        try:
            event = QueryEvent(
                context=Context(**message.get("context", {})),
                body=QueryBody(**message.get("body", {}))
            )
        except ValidationError:
            context = Context(**message.get("context", {}))
            context.valid = False
            event = QueryEvent(
                context=context,
                body=cls.ERROR_QUERY_BODY
            )
            logging.error(f"InitializationError for QueryEvent with {message} in {context.dict()}")
        return event

    @classmethod
    def create_query_event(cls, message: dict) -> QueryEvent:
        try:
            event = QueryEvent(
                context=message.get("context", {}),
                body=QueryBody(**message.get("body", {}))
            )
        except ValidationError:
            context = Context(**message.get("context", {}))
            context.valid = False
            event = QueryEvent(
                context=context,
                body=cls.ERROR_QUERY_BODY
            )
            logging.error(f"InitializationError for QueryEvent with {message} in {context.dict()}")

        return event

    @classmethod
    def create_class_list(cls, dict_obj: dict, class_obj: Any, keyword: str) -> dict:
        if keyword in dict_obj.keys():
            class_list = list()
            for obj in dict_obj.get(keyword, list()):
                try:
                    class_list.append(class_obj(**obj))
                except Exception as e:
                    logging.error(f"Class list of {keyword} with {type(class_obj)} could not be created for {dict_obj}")
            dict_obj[keyword] = class_list
        return dict_obj

    @classmethod
    def transform_masks_query(cls, query_object: dict) -> list:
        mask_list = query_object.get("result", {})
        result_list = list()

        for masking_object in mask_list:
            mask_obj = deepcopy(masking_object)
            mask_obj["table"] = mask_obj.get("tables", {"tableName": ""}).get("tableName")

            del mask_obj["tables"]

            mask_obj = cls.create_class_list(mask_obj, ColumnMask, "columns")
            mask_obj = cls.create_class_list(mask_obj, RowMask, "rows")
            result_list.append(MaskingObject(**mask_obj))

        return result_list

    @classmethod
    def read_database_config(cls, context: Context, config_list: list) -> List[DataBaseConfig]:
        configs = list()
        try:
            for config in config_list:
                configs.append(DataBaseConfig(**config))
            return configs
        except AttributeError:
            logging.error(f"InitializationError for DataBaseConfig with {config_list} in {context.dict()}")
            error_return = cls.ERROR_DB_CONFIG
            error_return.valid = False
            return [error_return]

    @classmethod
    def create_casefile_event(cls, message: dict) -> CaseFileEvent:
        try:
            event = CaseFileEvent(
                context=message.get("context", {}),
                body=CaseFileBody(**message.get("body", {}))
            )
        except ValidationError:
            context = message.get("context", {})
            context.valid = False
            event = CaseFileEvent(
                context=context,
                body=cls.ERROR_CASEFILE_OBJECT
            )
            logging.error(f"InitializationError for CaseFileEvent with {message} in {context.dict()}")

        return event

from sqlalchemy import and_, or_, not_, select, true
from sqlalchemy.sql import operators, Select, ClauseElement, ColumnElement
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.orm import DeclarativeMeta

OPERATOR_MAP = {
    "eq": operators.eq, 
    "ne": operators.ne, 
    "lt": operators.lt, 
    "lte": operators.le, 
    "gt": operators.gt, 
    "gte": operators.ge, 
    "like": operators.like_op, 
    "ilike": operators.ilike_op, 
    "in": operators.in_op, 
    "notin": operators.notin_op
}

def parse_filter(model: DeclarativeMeta, field: str, value) -> BinaryExpression:
    if '__' in field:
        # E.g.: (MyObj, {"age__gt": 30}) --> (MyObj.age > 30)
        field_name, op = field.split('__')
        column = getattr(model, field_name)
        return OPERATOR_MAP[op](column, value)
    else:
        # E.g.: (MyObj, {"age": 30}) --> (MyObj.age == 30)
        return getattr(model, field) == value

def build_where_clause(model: DeclarativeMeta, where_filter: dict) -> ClauseElement:
    if '_and' in where_filter:
        return and_(*(build_where_clause(model, condition) for condition in where_filter['_and']))
    elif '_or' in where_filter:
        return or_(*(build_where_clause(model, condition) for condition in where_filter['_or']))
    elif '_not' in where_filter:
        return not_(build_where_clause(model, where_filter['_not']))
    else:
        return and_(*(parse_filter(model, field, value) for field, value in where_filter.items()))

def parse_order_by_column(model: DeclarativeMeta, field: tuple) -> ColumnElement:
    column = field[0]
    order = field[1] if len(field) > 1 else 0
    return getattr(model, column).desc() if order == 1 else getattr(model, column)

def build_select_query(model: DeclarativeMeta, where_filter: dict = {}, order_by_cols: list[tuple] = []) -> Select:
    return select(model).\
        where(build_where_clause(model, where_filter) if where_filter else true()).\
            order_by(*(parse_order_by_column(model, field) for field in order_by_cols))
# Spork

**Spork** is a lightweight ORM-style query builder library inspired by SQLAlchemy and the PySpark DataFrame API. It enables programmatic generation of SQL query strings using an intuitive, chainable interface.

It is currently in its alpha stages - many SQL functions (`current_date`, `max`) and so forth are not yet implemented.

---

## Features

- Generate SQL queries programmatically with a familiar, PySpark-like API.
- Support for filtering, selecting, and chaining operations.
- Lightweight and easy to integrate into any Python project.

---

## Installation

```bash
pip install spork
```

The library is entirely native python, and has no dependencies as of right now.

## Example
```python
query = Query().select("SomeGreatColumn", col("BaseColumn").cast("int").alias("AliasedColumn"))\
    ._from("MyGreatTable")\
    .where(col("SomeFilter") > 1000)\
    .order_by(col("SomeOrdering").desc())

"""
select
SomeGreatColumn,
BaseColumn::int as AliasedColumn
from
MyGreatTable
where
SomeFilter > 1000
order by SomeOrdering desc
"""
```

## Future Improvements

- Support for different SQL dialects
- Query validation
- Query formatting/linting


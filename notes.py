# Use this file for notes and running examples...
# As expected, run it with `python3 -m notes`

from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

print(engine)
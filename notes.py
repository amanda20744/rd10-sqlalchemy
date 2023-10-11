# Use this file for notes and running examples...
# As expected, run it with `python3 -m notes`

from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

print(engine)

from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

# "commit as you go" style
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    # raise RuntimeError("oh no!")
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()

# begin once style of commiting
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 4})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
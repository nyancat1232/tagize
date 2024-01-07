from pyplus.sql.oopgplus import TableStructure
from pyplus.sql.oopgplus import get_table_list

compat = False
if compat:
    from pyplus.sql.pgplus import read_from_server
    from pyplus.sql.pgplus import expand_foreign_column
    from pyplus.sql.pgplus import get_identity
    from pyplus.sql.pgplus import get_columns

    from pyplus.sql.pgplus import upload_to_sql_by_id
    from pyplus.sql.pgplus import write_to_server
    from pyplus.sql.pgplus import create_empty_with_id_with_column

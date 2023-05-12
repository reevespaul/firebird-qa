#coding:utf-8

"""
ID:          issue-7569
ISSUE:       https://github.com/FirebirdSQL/firebird/issues/7569
TITLE:       Multi-level order by and offset/fetch ignored on parenthesized query expressions
NOTES:
    [12.05.2023] pzotov
    Confirmed problem on 5.0.0.1033. Checked on 5.0.0.1046 -- all fine.
"""

import pytest
from firebird.qa import *

db = db_factory()

test_script = """
    set list on;
    recreate table rowdata (id int generated by default as identity);
    insert into rowdata default values;
    insert into rowdata default values;
    insert into rowdata default values;
    insert into rowdata default values;
    insert into rowdata default values;
    insert into rowdata default values;
    insert into rowdata default values;
    insert into rowdata default values;
    insert into rowdata default values;
    commit;


    select id_a
    from
    (
      select id as id_a
      from rowdata
      order by id
      offset 2 rows fetch next 5 rows only
    )
    order by id_a desc
    offset 2 rows fetch next 2 rows only;

    (
      select id as id_b
      from rowdata
      order by id
      offset 2 rows fetch next 5 rows only
    )
    order by id_b desc
    offset 2 rows fetch next 2 rows only;
"""

act = isql_act('db', test_script)

expected_stdout = """
    ID_A                            5
    ID_A                            4
    ID_B                            5
    ID_B                            4
"""

@pytest.mark.version('>=5.0')
def test_1(act: Action):
    act.expected_stdout = expected_stdout
    act.execute()
    assert act.clean_stdout == act.clean_expected_stdout
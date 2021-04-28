#coding:utf-8
#
# id:           functional.exception.create.03
# title:        CREATE EXCEPTION - too long message
# decription:   CREATE EXCEPTION - too long message
#               
#               Dependencies:
#               CREATE DATABASE
#               Basic SELECT
# tracker_id:   
# min_versions: []
# versions:     3.0
# qmid:         functional.exception.create.create_exception_03

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('-At block line: [\\d]+, col: [\\d]+', '-At block line')]

init_script_1 = """"""

db_1 = db_factory(charset='UTF8', sql_dialect=3, init=init_script_1)

test_script_1 = """
    set autoddl off;
    commit;

    -- Updated 23-oct-2015: try to create in the SAME transaction exceptions with too long message and correct message (reduce its length with 1)
    -- after statement fails. Do that using both ascii and non-ascii characters in these exceptions messages.
    -- Expected result: no errors should occur on commit, exceptions should work fine. Taken from eqc ticket #12062.
    -- 13.06.2016: replaced 'show exception' with regular select from rdb$exception: output of SHOW commands
    -- is volatile in unstable FB versions.

    create exception boo_ascii
    'FOO!BAR!abcdefghijklmnoprstu012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345'
    ;

    create exception boo_ascii
    'FOOBAR!abcdefghijklmnoprstu012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345'
    ;


    create exception boo_utf8
    '32ηΣημείωσηΣημείωσηΣημεσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωση'
    ;

    create exception boo_utf8
    '3ηΣημείωσηΣημείωσηΣημεσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωση'
    ;

    commit;

    set list on;
    select rdb$exception_name, rdb$message from rdb$exceptions;

    set term ^;
    execute block as
    begin
      exception boo_ascii;
    end
    ^

    execute block as
    begin
      exception boo_utf8;
    end
    ^
    set term ;^  
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    RDB$EXCEPTION_NAME              BOO_ASCII                                                                                                                                                                                                                                                       
    RDB$MESSAGE                     FOOBAR!abcdefghijklmnoprstu012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345

    RDB$EXCEPTION_NAME              BOO_UTF8                                                                                                                                                                                                                                                        
    RDB$MESSAGE                     3ηΣημείωσηΣημείωσηΣημεσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωση
  """
expected_stderr_1 = """
    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE EXCEPTION BOO_ASCII failed
    -Name longer than database column size

    Statement failed, SQLSTATE = 42000
    unsuccessful metadata update
    -CREATE EXCEPTION BOO_UTF8 failed
    -Name longer than database column size

    Statement failed, SQLSTATE = HY000
    exception 1
    -BOO_ASCII
    -FOOBAR!abcdefghijklmnoprstu01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901...
    -At block line: 3, col: 7

    Statement failed, SQLSTATE = HY000
    exception 2
    -BOO_UTF8
    -3ηΣημείωσηΣημείωσηΣημεσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείωσηΣημείω...
    -At block line: 3, col: 7
  """

@pytest.mark.version('>=3.0')
def test_03_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr
    assert act_1.clean_expected_stdout == act_1.clean_stdout


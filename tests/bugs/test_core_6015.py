#coding:utf-8
#
# id:           bugs.core_6015
# title:        Segfault when using expression index with complex expression
# decription:   
#                    Test creates following objects:
#                    * table <T> with two columnad, with adding rows;
#                    * stored proc <P>, which does update one record in the table <T> and returns changed value of column;
#                    * computed-by index on table <T> which evaluates result of stored proc <P>.
#                    
#                    Procedure can either use:
#                    1) static PSQL code for updating record, or
#                    2) change it using ES,
#                    3) change it using ES+EDS.
#               
#                    Currently test checks cases "1" and "2" only.
#                    Check of case "3" if DEFERRED: ISQL will hang and, after it will be interrupted, Firebird process
#                    keeps database file opened infinitely because of alived EDS connect.
#                    Discussed with Vlad, letters 17.04.2021 09:52 and (reply from Vlad) 21.04.2021 10:40.
#               
#                    ::: NB :::
#                    Code for FB 3.x is separated from 4.x because content of STDERR differs: FB 3.x raises 'lock-conflict'
#                    for static PSQL code (instead of "Attempt to evaluate index expression recursively").
#                    Also, error messages differ because CORE-5606 was not backported to FB 3.x.
#               
#                    Test cause FB crash on builds 3.0.8.33445 and 4.0.0.2416.
#                    Checked on:
#                        * Windows only:      3.0.8.33452 (SS/CS);
#                        * Windows and Linux: 4.0.0.2436 (SS/CS)
#                    -- all fine, no crashes.
#                  
# tracker_id:   CORE-6015
# min_versions: ['3.0.8']
# versions:     3.0.8, 4.0
# qmid:         

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0.8
# resources: None

substitutions_1 = [('(-)?At procedure .*', '')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set bail on;
    set term ^;
    create procedure sp_eval_static_psql(a_id int) returns(x_changed int) as
    begin
       suspend;
    end^
    create procedure sp_eval_dynamic_sql(a_id int) returns(x_changed int) as
    begin
       suspend;
    end^
    set term ;^
    commit;

    create table test_static_psql(id int primary key, x int);
    create index test_static_psql_eval on test_static_psql computed by ( ( select x_changed from sp_eval_static_psql( id ) ) );

    create table test_dynamic_sql(id int primary key, x int);
    create index test_dynamic_sql_eval on test_dynamic_sql computed by ( ( select x_changed from sp_eval_dynamic_sql( id ) ) );
    commit;

    insert into test_static_psql(id, x) values(1, 111);
    insert into test_static_psql(id, x) values(2, 222);

    insert into test_dynamic_sql(id, x) values(1, 111);
    insert into test_dynamic_sql(id, x) values(2, 222);
    commit;

    -- connect 'localhost:c:	emp\\c6015.fdb' user 'SYSDBA' password 'masterkey';
    connect '$(DSN)' user 'SYSDBA' password 'masterkey';

    set term ^;
    alter procedure sp_eval_static_psql(a_id int) returns(x_changed int) as
    begin
       update test_static_psql set x = -x order by x rows 1 returning x into x_changed;
       suspend;
    end^

    alter procedure sp_eval_dynamic_sql(a_id int) returns(x_changed int) as
    begin
       execute statement 'update test_dynamic_sql set x = -x order by x rows 1 returning x' into x_changed;
       suspend;
    end^
    set term ;^
    commit;

    set transaction read committed NO wait;

    set bail off;
    set list on;

    -- case-1: check when procedure changes record using STATIC PSQL code:
    -- #######
    select
        t.id as id_case_1
        ,t.x as x_case_1
        ,( select x_changed from sp_eval_static_psql( t.id ) ) as x_changed_1
    from test_static_psql t
    order by id
    ;

    -- case-2: check when procedure changes record using EXECUTE STATEMENT mechanism:
    -- #######
    select
        t.id as id_case_2
        ,t.x as x_case_2
        ,( select x_changed from sp_eval_dynamic_sql( t.id ) ) as x_changed_2
    from test_dynamic_sql t
    order by id
    ;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stderr_1 = """
    Statement failed, SQLSTATE = 40001
    lock conflict on no wait transaction
    -At procedure 'SP_EVAL_STATIC_PSQL' line: 3, col: 8
    At procedure 'SP_EVAL_STATIC_PSQL' line: 3, col: 8

    Statement failed, SQLSTATE = 40001
    Attempt to evaluate index expression recursively
    -At procedure 'SP_EVAL_DYNAMIC_SQL' line: 3, col: 8
    -lock conflict on no wait transaction
  """

@pytest.mark.version('>=3.0.8,<4.0')
def test_core_6015_1(act_1: Action):
    act_1.expected_stderr = expected_stderr_1
    act_1.execute()
    assert act_1.clean_expected_stderr == act_1.clean_stderr

# version: 4.0
# resources: None

substitutions_2 = [('(-)?At procedure .*', '')]

init_script_2 = """"""

db_2 = db_factory(sql_dialect=3, init=init_script_2)

test_script_2 = """
    set bail on;
    set term ^;
    create procedure sp_eval_static_psql(a_id int) returns(x_changed int) as
    begin
       suspend;
    end^
    create procedure sp_eval_dynamic_sql(a_id int) returns(x_changed int) as
    begin
       suspend;
    end^
    set term ;^
    commit;

    create table test_static_psql(id int primary key, x int);
    create index test_static_psql_eval on test_static_psql computed by ( ( select x_changed from sp_eval_static_psql( id ) ) );

    create table test_dynamic_sql(id int primary key, x int);
    create index test_dynamic_sql_eval on test_dynamic_sql computed by ( ( select x_changed from sp_eval_dynamic_sql( id ) ) );
    commit;

    insert into test_static_psql(id, x) values(1, 111);
    insert into test_static_psql(id, x) values(2, 222);

    insert into test_dynamic_sql(id, x) values(1, 111);
    insert into test_dynamic_sql(id, x) values(2, 222);
    commit;

    -- connect 'localhost:c:	emp\\c6015.fdb' user 'SYSDBA' password 'masterkey';
    connect '$(DSN)' user 'SYSDBA' password 'masterkey';

    set term ^;
    alter procedure sp_eval_static_psql(a_id int) returns(x_changed int) as
    begin
       update test_static_psql set x = -x order by x rows 1 returning x into x_changed;
       suspend;
    end^

    alter procedure sp_eval_dynamic_sql(a_id int) returns(x_changed int) as
    begin
       execute statement 'update test_dynamic_sql set x = -x order by x rows 1 returning x' into x_changed;
       suspend;
    end^
    set term ;^
    commit;

    set transaction read committed NO wait;

    set bail off;
    set list on;

    -- case-1: check when procedure changes record using STATIC PSQL code:
    -- #######
    select
        t.id as id_case_1
        ,t.x as x_case_1
        ,( select x_changed from sp_eval_static_psql( t.id ) ) as x_changed_1
    from test_static_psql t
    order by id
    ;

    -- case-2: check when procedure changes record using EXECUTE STATEMENT mechanism:
    -- #######
    select
        t.id as id_case_2
        ,t.x as x_case_2
        ,( select x_changed from sp_eval_dynamic_sql( t.id ) ) as x_changed_2
    from test_dynamic_sql t
    order by id
    ;
  """

act_2 = isql_act('db_2', test_script_2, substitutions=substitutions_2)

expected_stderr_2 = """
    Statement failed, SQLSTATE = 42000
    Expression evaluation error for index "TEST_STATIC_PSQL_EVAL" on table "TEST_STATIC_PSQL"
    -Attempt to evaluate index expression recursively
    -At procedure 'SP_EVAL_STATIC_PSQL' line: 3, col: 8
    At procedure 'SP_EVAL_STATIC_PSQL' line: 3, col: 8

    Statement failed, SQLSTATE = 42000
    Expression evaluation error for index "TEST_DYNAMIC_SQL_EVAL" on table "TEST_DYNAMIC_SQL"
    -Attempt to evaluate index expression recursively
    -At procedure 'SP_EVAL_DYNAMIC_SQL' line: 3, col: 8
  """

@pytest.mark.version('>=4.0')
def test_core_6015_2(act_2: Action):
    act_2.expected_stderr = expected_stderr_2
    act_2.execute()
    assert act_2.clean_expected_stderr == act_2.clean_stderr


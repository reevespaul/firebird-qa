#coding:utf-8
#
# id:           bugs.core_6316
# title:        Unable to specify new 32k page size
# decription:
#                   NOTE. Issues remain for some kind of commands: parser should be more rigorous.
#                   Sent letter to Alex and Dmitry, 29.05.2020 12:28.
#                   Checked on 4.0.0.2006.
#
# tracker_id:   CORE-6316
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from pathlib import Path
from firebird.qa import db_factory, python_act, Action, temp_file
from firebird.driver import DatabaseError, ShutdownMode, ShutdownMethod

# version: 4.0
# resources: None

substitutions_1 = [('Token unknown.*line.*', 'Token unknown')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1, do_not_create=True)

# test_script_1
#---
#
#  import os
#  import sys
#  #import fdb
#  from fdb import services
#
#  DB_NAME=os.path.join(context['temp_directory'],'tmp_6316.fdb')
#  DB_USER=user_name
#  DB_PSWD=user_password
#  page_list= (
#     "9223372036854775809"
#    ,"9223372036854775808"
#    ,"9223372036854775807"
#    ,"4294967297"
#    ,"4294967296"
#    ,"4294967295"
#    ,"2147483649"
#    ,"2147483648"
#    ,"2147483647"
#    ,"65537"
#    ,"32769"
#    ,"32768"
#    ,"32767"
#    ,"16385"
#    ,"16384"
#    ,"16383"
#    ,"8193"
#    ,"8192"
#    ,"8191"
#    ,"4097"
#    ,"4096"
#    ,"4095"
#    ,"2049"
#    ,"2048"
#    ,"2047"
#    ,"1025"
#    ,"1024"
#    ,"1023"
#    ,"0"
#    ,"0x10000"
#    ,"0xFFFF"
#    ,"0x8000"
#    ,"0x7FFF"
#    ,"0x4000"
#    ,"0x3FFF"
#    ,"0x2000"
#    ,"0x1FFF"
#    ,"0x1000"
#    ,"0xFFF"
#    ,"0x800"
#    ,"0x7FF"
#    ,"0x400"
#    ,"0x3FF"
#    ,"default"
#    ,"null"
#    ,"qwerty"
#    ,"-32768"
#  )
#
#  sttm_proto="create database 'localhost:%(DB_NAME)s' user %(DB_USER)s password '%(DB_PSWD)s' page_size %(i)s"
#
#  svc = services.connect( user = DB_USER, password = DB_PSWD )
#  #k=0
#  for i in page_list:
#      for j in (1,2):
#          if os.path.isfile(DB_NAME):
#              os.remove(DB_NAME)
#
#          try:
#              # ::: NB ::: No error occured until we specify 'DEFAULT CHARACTER SET ....'
#              sttm_actual = sttm_proto % locals() + ( ' default character set win1251' if j==1 else '' )
#
#              #print('Try create with page_size=%(i)s, clause "DEFAULT CHARACTER SET": ' % locals() + (  'present' if 'default character set' in sttm_actual else 'absent' )  )
#              print('')
#              print(sttm_actual.replace("'localhost:%(DB_NAME)s'" % locals(), "...").replace("user %(DB_USER)s " % locals(), '').replace("password '%(DB_PSWD)s' " % locals(), ''))
#              con = None
#              con = fdb.create_database( sql = sttm_actual)
#
#              if con:
#                  con.execute_immediate('alter database set linger to 0')
#                  con.commit()
#                  cur = con.cursor()
#                  cur.execute('select mon$database_name,mon$page_size,left(cast(mon$creation_date as varchar(50)),24) from mon$database')
#                  for r in cur:
#                      print('DB created. Actual page_size:', r[1] )
#                  cur.close()
#                  con.close()
#
#              if os.path.isfile(DB_NAME):
#                  svc.shutdown( DB_NAME, services.SHUT_FULL, services.SHUT_FORCE, 0)
#                  os.remove(DB_NAME)
#
#          except Exception as e:
#              print(e[0])
#
#  svc.close()
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    create database ... page_size 9223372036854775809 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -9223372036854775809
    create database ... page_size 9223372036854775809
    DB created. Actual page_size: 32768
    create database ... page_size 9223372036854775808 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -9223372036854775808
    create database ... page_size 9223372036854775808
    DB created. Actual page_size: 32768
    create database ... page_size 9223372036854775807 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -9223372036854775807
    create database ... page_size 9223372036854775807
    DB created. Actual page_size: 32768
    create database ... page_size 4294967297 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -4294967297
    create database ... page_size 4294967297
    DB created. Actual page_size: 32768
    create database ... page_size 4294967296 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -4294967296
    create database ... page_size 4294967296
    DB created. Actual page_size: 32768
    create database ... page_size 4294967295 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -4294967295
    create database ... page_size 4294967295
    DB created. Actual page_size: 32768
    create database ... page_size 2147483649 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -2147483649
    create database ... page_size 2147483649
    DB created. Actual page_size: 32768
    create database ... page_size 2147483648 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -2147483648
    create database ... page_size 2147483648
    DB created. Actual page_size: 32768
    create database ... page_size 2147483647 default character set win1251
    DB created. Actual page_size: 32768
    create database ... page_size 2147483647
    DB created. Actual page_size: 32768
    create database ... page_size 65537 default character set win1251
    DB created. Actual page_size: 32768
    create database ... page_size 65537
    DB created. Actual page_size: 32768
    create database ... page_size 32769 default character set win1251
    DB created. Actual page_size: 32768
    create database ... page_size 32769
    DB created. Actual page_size: 32768
    create database ... page_size 32768 default character set win1251
    DB created. Actual page_size: 32768
    create database ... page_size 32768
    DB created. Actual page_size: 32768
    create database ... page_size 32767 default character set win1251
    DB created. Actual page_size: 16384
    create database ... page_size 32767
    DB created. Actual page_size: 16384
    create database ... page_size 16385 default character set win1251
    DB created. Actual page_size: 16384
    create database ... page_size 16385
    DB created. Actual page_size: 16384
    create database ... page_size 16384 default character set win1251
    DB created. Actual page_size: 16384
    create database ... page_size 16384
    DB created. Actual page_size: 16384
    create database ... page_size 16383 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 16383
    DB created. Actual page_size: 8192
    create database ... page_size 8193 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 8193
    DB created. Actual page_size: 8192
    create database ... page_size 8192 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 8192
    DB created. Actual page_size: 8192
    create database ... page_size 8191 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 8191
    DB created. Actual page_size: 4096
    create database ... page_size 4097 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 4097
    DB created. Actual page_size: 4096
    create database ... page_size 4096 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 4096
    DB created. Actual page_size: 4096
    create database ... page_size 4095 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 4095
    DB created. Actual page_size: 4096
    create database ... page_size 2049 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 2049
    DB created. Actual page_size: 4096
    create database ... page_size 2048 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 2048
    DB created. Actual page_size: 4096
    create database ... page_size 2047 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 2047
    DB created. Actual page_size: 4096
    create database ... page_size 1025 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 1025
    DB created. Actual page_size: 4096
    create database ... page_size 1024 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 1024
    DB created. Actual page_size: 4096
    create database ... page_size 1023 default character set win1251
    DB created. Actual page_size: 4096
    create database ... page_size 1023
    DB created. Actual page_size: 4096
    create database ... page_size 0 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0
    DB created. Actual page_size: 8192
    create database ... page_size 0x10000 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x10000
    DB created. Actual page_size: 8192
    create database ... page_size 0xFFFF default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0xFFFF
    DB created. Actual page_size: 8192
    create database ... page_size 0x8000 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x8000
    DB created. Actual page_size: 8192
    create database ... page_size 0x7FFF default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x7FFF
    DB created. Actual page_size: 8192
    create database ... page_size 0x4000 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x4000
    DB created. Actual page_size: 8192
    create database ... page_size 0x3FFF default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x3FFF
    DB created. Actual page_size: 8192
    create database ... page_size 0x2000 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x2000
    DB created. Actual page_size: 8192
    create database ... page_size 0x1FFF default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x1FFF
    DB created. Actual page_size: 8192
    create database ... page_size 0x1000 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x1000
    DB created. Actual page_size: 8192
    create database ... page_size 0xFFF default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0xFFF
    DB created. Actual page_size: 8192
    create database ... page_size 0x800 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x800
    DB created. Actual page_size: 8192
    create database ... page_size 0x7FF default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x7FF
    DB created. Actual page_size: 8192
    create database ... page_size 0x400 default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x400
    DB created. Actual page_size: 8192
    create database ... page_size 0x3FF default character set win1251
    DB created. Actual page_size: 8192
    create database ... page_size 0x3FF
    DB created. Actual page_size: 8192
    create database ... page_size default default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -default
    create database ... page_size default
    DB created. Actual page_size: 8192
    create database ... page_size null default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -null
    create database ... page_size null
    DB created. Actual page_size: 8192
    create database ... page_size qwerty default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    -qwerty
    create database ... page_size qwerty
    DB created. Actual page_size: 8192
    create database ... page_size -32768 default character set win1251
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    --
    create database ... page_size -32768
    Statement failed, SQLSTATE = 42000
    Dynamic SQL Error
    -SQL error code = -104
    -Token unknown
    --
"""

page_list= ['9223372036854775809',
            '9223372036854775808',
            '9223372036854775807',
            '4294967297',
            '4294967296',
            '4294967295',
            '2147483649',
            '2147483648',
            '2147483647',
            '65537',
            '32769',
            '32768',
            '32767',
            '16385',
            '16384',
            '16383',
            '8193',
            '8192',
            '8191',
            '4097',
            '4096',
            '4095',
            '2049',
            '2048',
            '2047',
            '1025',
            '1024',
            '1023',
            '0',
            '0x10000',
            '0xFFFF',
            '0x8000',
            '0x7FFF',
            '0x4000',
            '0x3FFF',
            '0x2000',
            '0x1FFF',
            '0x1000',
            '0xFFF',
            '0x800',
            '0x7FF',
            '0x400',
            '0x3FF',
            'default',
            'null',
            'qwerty',
            '-32768'
            ]


@pytest.mark.version('>=4.0')
def test_1(act_1: Action, capsys):
    with act_1.connect_server() as srv:
        for page_size in page_list:
            for charset in [' default character set win1251', '']:
                cmd = f"create database '{act_1.db.dsn}' user {act_1.db.user} password '{act_1.db.password}' page_size {page_size}{charset}"
                print(f'create database ... page_size {page_size}{charset}')
                act_1.reset()
                act_1.isql(switches=['-q', '-b'], input=f'{cmd}; ALTER DATABASE SET LINGER TO 0;',
                           combine_output=True, connect_db=False, credentials=False)
                print(act_1.stdout)
                #
                if act_1.db.db_path.is_file():
                    with act_1.db.connect() as con:
                        print('DB created. Actual page_size:', con.info.page_size)
                    srv.database.shutdown(database=act_1.db.db_path, mode=ShutdownMode.FULL,
                                          method=ShutdownMethod.FORCED, timeout=0)
                    srv.database.bring_online(database=act_1.db.db_path)
                    act_1.db.drop()
    #
    act_1.reset()
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    #
    act_1.db.create() # to ensure clean teardown
    assert act_1.clean_stdout == act_1.clean_expected_stdout
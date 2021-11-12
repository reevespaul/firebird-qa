#coding:utf-8
#
# id:           bugs.core_2115
# title:        Query plan is missing for the long query
# decription:
# tracker_id:   CORE-2115
# min_versions: []
# versions:     3.0
# qmid:         None

import pytest
from zipfile import Path
from firebird.qa import db_factory, python_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import sys
#  import subprocess
#  import zipfile
#  import filecmp
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  db_conn.close()
#
#  #-----------------------------------
#
#  def flush_and_close(file_handle):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      os.fsync(file_handle.fileno())
#
#      file_handle.close()
#
#  #--------------------------------------------
#
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if os.path.isfile( f_names_list[i]):
#              os.remove( f_names_list[i] )
#              if os.path.isfile( f_names_list[i]):
#                  print('ERROR: can not remove file ' + f_names_list[i])
#
#  #-------------------------------------------
#
#  zf = zipfile.ZipFile( os.path.join(context['files_location'],'core_2115.zip'), 'r' )
#  for name in zf.namelist():
#      zo=zf.open(name, 'rU')
#      fn=open( os.path.join(context['temp_directory'],name), 'w')
#      fn.write( zo.read().replace('\\r','') )
#      fn.close()
#
#  ### do NOT: preserves Carriage Return character from Windows: zf.extractall( context['temp_directory'] )
#  zf.close()
#
#  # Result: files
#  # 1. tmp_core_2115_queries_with_long_plans.sql and
#  # 2. tmp_core_2115_check_txt_of_long_plans.log
#  # -- have been extracted into context['temp_directory']
#  #
#  # These queries were created in AUTOMATED way using following batch scenario:
#  #
#  #    @echo off
#  #    setlocal enabledelayedexpansion enableextensions
#  #
#  #    set in_list_min_count=50
#  #    set in_list_max_count=1500
#  #
#  #    @rem -Implementation limit exceeded
#  #    @rem -Too many values (more than 1500) in member list to match against
#  #
#  #    set log=%~n0.log
#  #    set sql=%~n0.sql
#  #    del %sql% 2>nul
#  #    (
#  #      echo -- GENERATED AUTO, DO NOT EDIT.
#  #      echo.
#  #      echo recreate table t234567890123456789012345678901(
#  #      echo    f234567890123456789012345678901 smallint
#  #      echo    unique using index x234567890123456789012345678901
#  #      echo ^);
#  #      echo commit;
#  #      echo.
#  #      @rem echo set list on; select current_timestamp from rdb$database;
#  #      echo set planonly;
#  #    ) >> %sql%
#  #
#  #
#  #    for /l %%i in (%in_list_min_count%, 25, %in_list_max_count%) do (
#  #        @echo Generating query with IN-list of %%i elements.
#  #        call :make_query %sql% %%i
#  #    )
#  #
#  #    @echo Done.
#  #
#  #    goto end
#  #
#  #    :make_query
#  #
#  #        setlocal
#  #        set sql=%1
#  #        set in_elems=%2
#  #        set /a k=10000+%in_elems%
#  #        set suff=!k:~1,4!
#  #
#  #        (
#  #          echo.
#  #          echo -- Query with "IN"-list of %in_elems% elements:
#  #          echo select %in_elems% as c
#  #          echo from t234567890123456789012345678901 as
#  #          echo t__________________________!suff!
#  #          echo where f234567890123456789012345678901 in (
#  #        ) >>%sql%
#  #
#  #        set /a k=1
#  #        set s=
#  #        for /l %%i in (1,1,%in_elems%) do (
#  #            if .!s!.==.. (
#  #                set s=0
#  #            ) else (
#  #                set s=!s!,0
#  #            )
#  #            set /a m=!k! %% 50
#  #
#  #            if !m! equ 0 (
#  #              if .%%i.==.%in_elems%. ( echo !s!>>%sql% ) else ( echo !s!,>>%sql% )
#  #              set s=
#  #            )
#  #            set /a k=!k!+1
#  #        )
#  #
#  #
#  #        (
#  #          if not .!s!.==.. echo !s!
#  #          echo ^);
#  #        ) >>%sql%
#  #
#  #        endlocal & goto:eof
#  #
#  #    :end
#
#  sql_long_plans_qry=os.path.join(context['temp_directory'],'tmp_core_2115_queries_with_long_plans.sql')
#  sql_long_plans_chk=os.path.join(context['temp_directory'],'tmp_core_2115_check_txt_of_long_plans.log')
#
#  sql_long_plans_res=open( os.path.join(context['temp_directory'],'tmp_core_2115_current_txt_of_long_plans.log'), 'w')
#
#  subprocess.call( [context["isql_path"], dsn, "-i", sql_long_plans_qry], stdout=sql_long_plans_res, stderr=subprocess.STDOUT )
#  flush_and_close( sql_long_plans_res )
#
#  if filecmp.cmp( sql_long_plans_chk, sql_long_plans_res.name):
#      print("Current plans match to original ones.")
#  else:
#      print("Found at least one MISMATCH with original plans.")
#
#
#  # cleanup
#  ##########
#
#  f_list = [ sql_long_plans_qry, sql_long_plans_chk, sql_long_plans_res.name ]
#  cleanup( f_list )
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

@pytest.mark.version('>=3.0')
def test_1(act_1: Action):
    # Read script and expected stdout from zip file
    datafile = Path(act_1.vars['files'] / 'core_2115.zip',
                    at='tmp_core_2115_queries_with_long_plans.sql')
    act_1.script = datafile.read_text()
    datafile = Path(act_1.vars['files'] / 'core_2115.zip',
                    at='tmp_core_2115_check_txt_of_long_plans.log')
    act_1.expected_stdout = datafile.read_text()
    act_1.execute()
    assert act_1.clean_stdout == act_1.clean_expected_stdout

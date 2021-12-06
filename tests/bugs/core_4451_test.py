#coding:utf-8
#
# id:           bugs.core_4451
# title:        Allow output to trace explain plan form.
# decription:
#                   Checked on
#                       4.0.0.1685 SS: 7.985s.
#                       4.0.0.1685 CS: 8.711s.
#                       3.0.5.33206 SS: 7.281s.
#                       3.0.5.33206 CS: 8.278s.
#
# tracker_id:   CORE-4451
# min_versions: ['3.0.0']
# versions:     3.0
# qmid:         None

import pytest
import time
from threading import Thread, Barrier
from firebird.qa import db_factory, python_act, Action

# version: 3.0
# resources: None

substitutions_1 = [('[ \t]+', ' '), ('[ \t]+[\\d]+[ \t]+ms', '')]

init_script_1 = """
    recreate table test(x int);
"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
#
#  import os
#  import subprocess
#  from subprocess import Popen
#  import time
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#  fdb_file=db_conn.database_name
#  db_conn.close()
#
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
#  #--------------------------------------------
#
#
#
#  #####################################################################
#  # Prepare config for trace session that will be launched by call of FBSVCMGR:
#
#  txt = '''    database= # %[\\\\\\\\/]bugs.core_4451.fdb
#      {
#          enabled = true
#          time_threshold = 0
#          log_initfini = false
#          print_plan = true
#          explain_plan = true
#          log_statement_prepare = true
#          include_filter=%(from|join)[[:whitespace:]]test%
#      }
#  '''
#  f_trccfg=open( os.path.join(context['temp_directory'],'tmp_trace_4451.cfg'), 'w')
#  f_trccfg.write(txt)
#  flush_and_close( f_trccfg )
#
#  #####################################################################
#  # Async. launch of trace session using FBSVCMGR action_trace_start:
#
#  f_trclog=open( os.path.join(context['temp_directory'],'tmp_trace_4451.log'), 'w')
#
#  # Execute a child program in a new process, redirecting STDERR to the same target as of STDOUT:
#  p_svcmgr = Popen( [ context['fbsvcmgr_path'], "localhost:service_mgr",
#                      "action_trace_start",
#                      "trc_cfg", f_trccfg.name
#                    ],
#                    stdout=f_trclog,
#                    stderr=subprocess.STDOUT
#                  )
#
#  # Wait! Trace session is initialized not instantly!
#  time.sleep(2)
#
#  #####################################################################
#
#  # Determine active trace session ID (for further stop):
#
#  f_trclst=open( os.path.join(context['temp_directory'],'tmp_trace_4451.lst'), 'w')
#  subprocess.call([context['fbsvcmgr_path'], "localhost:service_mgr",
#                   "action_trace_list"],
#                   stdout=f_trclst, stderr=subprocess.STDOUT
#                 )
#  flush_and_close( f_trclst )
#
#  # Session ID: 5
#  #   user:
#  #   date:  2015-08-27 15:24:14
#  #   flags: active, trace
#
#  trcssn=0
#  with open( f_trclst.name,'r') as f:
#      for line in f:
#          i=1
#          if 'Session ID' in line:
#              for word in line.split():
#                  if i==3:
#                      trcssn=word
#                  i=i+1
#              break
#
#  # Result: `trcssn` is ID of active trace session.
#  # We have to terminate trace session that is running on server BEFORE we termitane process `p_svcmgr`
#  if trcssn==0:
#      print("Error parsing trace session ID.")
#      flush_and_close( f_trclog )
#  else:
#      #####################################################################
#
#      # Preparing script for ISQL:
#
#      sql_cmd='''select count(*) from test;'''
#
#      so=sys.stdout
#      se=sys.stderr
#
#      sys.stdout = open(os.devnull, 'w')
#      sys.stderr = sys.stdout
#
#      runProgram('isql',[dsn],sql_cmd)
#
#      sys.stdout = so
#      sys.stderr = se
#
#      # do NOT reduce this delay!
#      time.sleep(2)
#
#      #####################################################################
#
#      # Stop trace session:
#
#      f_trclst=open(f_trclst.name, "a")
#      f_trclst.seek(0,2)
#      subprocess.call( [ context['fbsvcmgr_path'], "localhost:service_mgr",
#                         "action_trace_stop",
#                         "trc_id",trcssn
#                       ],
#                       stdout=f_trclst,
#                       stderr=subprocess.STDOUT
#                     )
#      flush_and_close( f_trclst )
#
#      p_svcmgr.terminate()
#      flush_and_close( f_trclog )
#
#      # do NOT remove this delay:
#      time.sleep(1)
#
#      show_line = 0
#      with open(f_trclog.name) as f:
#          for line in f:
#              show_line = ( show_line + 1 if ('^' * 79) in line or show_line>0 else show_line )
#              if show_line > 1:
#                  print(line)
#
#  # cleanup:
#  ##########
#  time.sleep(1)
#  cleanup( [i.name for i in (f_trclst, f_trccfg, f_trclog) ] )
#
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

expected_stdout_1 = """
    Select Expression
    -> Aggregate
    -> Table "TEST" Full Scan
"""

def trace_session(act: Action, b: Barrier):
    cfg30 = ['# Trace config, format for 3.0. Generated auto, do not edit!',
             f'database=%[\\\\/]{act.db.db_path.name}',
             '{',
             '  enabled = true',
             '  time_threshold = 0',
             '  log_initfini = false',
             '  print_plan = true',
             '  explain_plan = true',
             '  log_statement_prepare = true',
             '  include_filter=%(from|join)[[:whitespace:]]test%',
             '}']
    with act.connect_server() as srv:
        srv.trace.start(config='\n'.join(cfg30))
        b.wait()
        for line in srv:
            print(line)

@pytest.mark.version('>=3.0')
def test_1(act_1: Action, capsys):
    b = Barrier(2)
    trace_thread = Thread(target=trace_session, args=[act_1, b])
    trace_thread.start()
    b.wait()
    # Trace ready, run tests
    act_1.isql(switches=[], input='select count(*) from test;')
    # Stop trace
    time.sleep(2)
    with act_1.connect_server() as srv:
        for session in list(srv.trace.sessions.keys()):
            srv.trace.stop(session_id=session)
        trace_thread.join(1.0)
        if trace_thread.is_alive():
            pytest.fail('Trace thread still alive')
    # Check
    show_line = 0
    for line in capsys.readouterr().out.splitlines():
        show_line = (show_line + 1 if ('^' * 79) in line or show_line>0 else show_line)
        if show_line > 1:
            print(line)
    act_1.expected_stdout = expected_stdout_1
    act_1.stdout = capsys.readouterr().out
    assert act_1.clean_stdout == act_1.clean_expected_stdout

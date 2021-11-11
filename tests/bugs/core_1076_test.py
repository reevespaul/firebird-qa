#coding:utf-8
#
# id:           bugs.core_1076
# title:        gsec truncate First.Middle.Last Name fields to 17 chars instead of 32 chars available in field definition
# decription:
#                  FB2.0 correctly saves First, Middle & Last Name fields in the security database to the available length of 32 characters.
#                  FB1.5.3 and still now FB1.5.4RC1 truncates these field lengths to 17 chars.
#                  ---
#                  11.01.2016: refactored for 3.0: use FBSVCMGR instead of GSEC. This was agreed with Alex, see his reply 11.01.2015 17:57.
#
#
# tracker_id:   CORE-1076
# min_versions: []
# versions:     3.0
# qmid:

import pytest
from firebird.qa import db_factory, python_act, Action, user_factory, User

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# import os
#  import time
#  import subprocess
#  from subprocess import Popen
#  from fdb import services
#
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#
#
#  #--------------------------------------------
#
#  def flush_and_close(file_handle):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f,
#      # first do f.flush(), and
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb'):
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
#      file_handle.close()
#
#  #--------------------------------------------
#
#  def cleanup( f_names_list ):
#      global os
#      for i in range(len( f_names_list )):
#         if os.path.isfile( f_names_list[i]):
#              os.remove( f_names_list[i] )
#
#  #--------------------------------------------
#
#  db_name=db_conn.database_name
#  db_conn.close()
#
#  svc = services.connect(host='localhost')
#  security_db_name = svc.get_security_database_path()  # path+name of security DB
#  svc.close()
#
#  check_login="Nebuchadnezzar2_King_of_Babylon"
#
#  f_svc_log=open( os.path.join(context['temp_directory'],'tmp_1076_fbsvc.log'), 'w')
#  f_svc_err=open( os.path.join(context['temp_directory'],'tmp_1076_fbsvc.err'), 'w')
#
#  f_svc_log.write("Try to add user.")
#  f_svc_log.write("\\n")
#  f_svc_log.seek(0,2)
#
#  subprocess.call( [ context['fbsvcmgr_path']
#                     ,"localhost:service_mgr"
#                     ,"action_add_user"
#                     ,"dbname",       security_db_name
#                     ,"sec_username", check_login
#                     ,"sec_password", "Nebu_King_of_Babylon"
#                    ]
#                    ,stdout=f_svc_log, stderr=f_svc_err
#                 )
#
#  f_svc_log.seek(0,2)
#  f_svc_log.write("\\n")
#  f_svc_log.write("Try to modify user: change password and some attributes.")
#  f_svc_log.write("\\n")
#  f_svc_log.seek(0,2)
#
#  subprocess.call( [ context['fbsvcmgr_path']
#                     ,"localhost:service_mgr"
#                     ,"action_modify_user"
#                     ,"dbname",         security_db_name
#                     ,"sec_username",   check_login
#                     ,"sec_firstname",  "Nebuchadnezzar3_King_of_Babylon"
#                     ,"sec_middlename", "Nebuchadnezzar4_King_of_Babylon"
#                     ,"sec_lastname",   "Nebuchadnezzar5_King_of_Babylon"
#                    ]
#                    ,stdout=f_svc_log, stderr=f_svc_err
#                 )
#
#  f_svc_log.seek(0,2)
#  f_svc_log.write("\\n")
#  f_svc_log.write("All done.")
#  f_svc_log.write("\\n")
#
#  flush_and_close( f_svc_log )
#  flush_and_close( f_svc_err )
#
#  isql_txt='''    set list on;
#      select sec$user_name, sec$first_name, sec$middle_name, sec$last_name from sec$users
#      where upper(sec$user_name) = upper('%s');
#      commit;
#      drop user %s;
#  ''' % (check_login, check_login)
#
#  f_sql_txt=open( os.path.join(context['temp_directory'],'tmp_1076_isql.sql'), 'w')
#  f_sql_txt.write(isql_txt)
#  flush_and_close( f_sql_txt )
#
#  f_sql_log=open( os.path.join(context['temp_directory'],'tmp_1076_isql.log'), 'w')
#  f_sql_err=open( os.path.join(context['temp_directory'],'tmp_1076_isql.err'), 'w')
#
#  subprocess.call( [ context['isql_path'], dsn, "-i", f_sql_txt.name ]
#                   ,stdout=f_sql_log
#                   ,stderr=f_sql_err
#                 )
#
#  flush_and_close( f_sql_log )
#  flush_and_close( f_sql_err )
#
#  with open( f_svc_log.name,'r') as f:
#    l = [l for l in f.readlines() if l.strip()]
#
#  for line in l:
#     print("SVC STDOUT: "+line )
#
#  with open( f_svc_err.name,'r') as f:
#    l = [l for l in f.readlines() if l.strip()]
#
#  for line in l:
#     print("SVC STDERR: "+line )
#
#  with open( f_sql_log.name,'r') as f:
#    l = [l for l in f.readlines() if l.strip()]
#
#  for line in l:
#     print("SQL STDOUT: "+line )
#
#  with open( f_sql_err.name,'r') as f:
#    l = [l for l in f.readlines() if l.strip()]
#
#  for line in l:
#     print("SQL STDERR: "+line )
#
#  #############################################
#
#  # Cleanup.
#  time.sleep(1)
#  cleanup( [i.name for i in (f_svc_log, f_svc_err, f_sql_log, f_sql_err, f_sql_txt)] )
#
#---

act_1 = python_act('db_1', substitutions=substitutions_1)

user_1 = user_factory(name="Nebuchadnezzar2_King_of_Babylon",
                      password="Nebu_King_of_Babylon")

expected_stdout_1 = """
SEC$USER_NAME                   NEBUCHADNEZZAR2_KING_OF_BABYLON
SEC$FIRST_NAME                  Nebuchadnezzar3_King_of_Babylon
SEC$MIDDLE_NAME                 Nebuchadnezzar4_King_of_Babylon
SEC$LAST_NAME                   Nebuchadnezzar5_King_of_Babylon
"""

@pytest.mark.version('>=3.0')
def test_1(act_1: Action, user_1: User):
   user_1.update(first_name="Nebuchadnezzar3_King_of_Babylon",
                 middle_name="Nebuchadnezzar4_King_of_Babylon",
                 last_name="Nebuchadnezzar5_King_of_Babylon")
   #
   act_1.script = f"""set list on;
select sec$user_name, sec$first_name, sec$middle_name, sec$last_name from sec$users
where upper(sec$user_name) = upper('{user_1.name}');
"""
   act_1.expected_stdout = expected_stdout_1
   act_1.execute()
   assert act_1.clean_stdout == act_1.clean_expected_stdout


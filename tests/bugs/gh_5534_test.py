#coding:utf-8
#
# id:           bugs.gh_5534
# title:        String truncation exception on UPPER/LOWER functions, UTF8 database and some multibyte characters [CORE5255]
# decription:   
#                   https://github.com/FirebirdSQL/firebird/issues/5534
#               	
#               	Test verifies work of predicates, functions for string handling and comparison.
#               	::: NOTE :::
#               	Test does not verify `CONTAINING`! This will be done in separate test, after gh-6851 will be fixed
#               	(see note by Adriano in this ticket, date: 14.06.2021)
#               	
#               	None of them must raise exception, and result of actions is not displayed via suspend.
#                   Thus 'expected-' sections must be empty.
#               	If some character leads to error, apropriate repord ID is included into the list of problematic
#               	unicode characters (see variables 'vchr_id_problem_list' and 'blob_id_problem_list').
#               	This is performed for VARCHAR and BLOB datatypes.
#               	Bug was detected with BLOBs, see https://github.com/FirebirdSQL/firebird/issues/6858
#               	(fixed 17.06.2021)
#               	
#               	Confirmed problem on 5.0.0.75; 4.0.0.2508 (handling of all characters from this test raise error).
#               	Checked on: 5.0.0.79; 4.0.1.2517 - all OK.
#                
# tracker_id:   
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
	set bail on;
	set list on;

	recreate table test(
	   id int generated by default as identity constraint pk_txt primary key
	  ,txt varchar(1) character set utf8
	  ,blb blob character set utf8
	);

	-- https://github.com/FirebirdSQL/firebird/issues/5534
	insert into test(txt) values('Ⱥ'); -- U+023A
	insert into test(txt) values('Ⱥ'); -- U+023A
	insert into test(txt) values('Ⱦ'); -- U+023E
	insert into test(txt) values('ȿ'); -- U+023F
	insert into test(txt) values('ɀ'); -- U+0240
	insert into test(txt) values('ɐ'); -- U+0250
	insert into test(txt) values('ɑ'); -- U+0251
	insert into test(txt) values('ɒ'); -- U+0252

	insert into test(txt) values('ɜ'); -- U+025C // Latin Small Letter Reversed Open E
	-- Upper: U+A7AB // Latin Capital Letter Reversed Open E

	insert into test(txt) values('ɡ'); -- U+0261
	insert into test(txt) values('ɥ'); -- U+0265
	insert into test(txt) values('ɦ'); -- U+0266
	insert into test(txt) values('ɪ'); -- U+026A
	insert into test(txt) values('ɫ'); -- U+026B
	insert into test(txt) values('ɬ'); -- U+026C
	insert into test(txt) values('ɱ'); -- U+0271
	insert into test(txt) values('ɽ'); -- U+027D
	insert into test(txt) values('ʇ'); -- U+0287
	insert into test(txt) values('ʝ'); -- U+029D
	insert into test(txt) values('ʞ'); -- U+029E

	update test set blb = txt;
	commit;

	set term ^;
	execute block returns(
		vchr_id_problem_list varchar(32760) character set none
		,blob_id_problem_list varchar(32760) character set none
	) as
		declare x varchar(10) character set utf8;
		declare y blob character set utf8;
		declare b boolean;
		declare n bigint;
		declare v varbinary(64);
		declare k_prv varbinary(16384);
		declare k_pub varbinary(8192);
		declare text_encrypted varchar(256) character set octets;
		declare text_decrypted varchar(10) character set utf8;
	begin
		vchr_id_problem_list = '';
		blob_id_problem_list = '';
		k_prv = rsa_private(256);
		k_pub = rsa_public(k_prv);
		
		for select id, txt, blb from test as cursor c
		do begin
			begin
				n = bit_length(c.txt);
				n = char_length(c.txt);
				x = left(c.txt,1);
				x = lower(c.txt);
				x = lpad(c.txt,2,c.txt);
				n = octet_length(c.txt);
				x = overlay(c.txt placing c.txt from 1);
				n = position(c.txt in c.txt);
				x = reverse(c.txt);
				x = replace(c.txt, c.txt, c.txt);
				x = right(c.txt,1);
				x = rpad(c.txt,2,c.txt);
				x = substring(c.txt from 1 for 1);
				x = trim(c.txt);
				x = upper(c.txt);
				-------------------
				x = minvalue('ɡ','ɥ','ɦ','ɪ','ɫ','ɬ','ɱ','ɽ','ʇ','ʝ','ʞ');
				x = maxvalue('ɡ','ɥ','ɦ','ɪ','ɫ','ɬ','ɱ','ɽ','ʇ','ʝ','ʞ');
				n = hash(c.txt);
				-------------------
				b = c.txt = 'Ⱥ';
				b = c.txt < 'Ⱥ';
				b = c.txt > 'Ⱥ';
				b = c.txt <> 'Ⱥ';
				b = c.txt between 'Ⱥ' and 'ʞ';
				b = c.txt is distinct from 'ʞ';
				b = c.txt is not distinct from 'ʞ';
				b = c.txt starts with 'ʞ';
				b = c.txt similar to 'ʞ{0,1}';
				b = c.txt in ('ɡ','ɥ','ɦ','ɪ','ɫ','ɬ','ɱ','ɽ','ʇ','ʝ','ʞ');
				n = hash(c.txt);
				v = crypt_hash(c.txt using md5);
				v = crypt_hash(c.txt using sha1);
				v = crypt_hash(c.txt using sha256);
				v = crypt_hash(c.txt using sha512);
				
				-- 
				text_encrypted = rsa_encrypt(c.txt key k_pub hash md5);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash md5);
				text_encrypted = rsa_encrypt(c.txt key k_pub hash md5);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash md5);
				text_encrypted = rsa_encrypt(c.txt key k_pub hash sha1);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash sha1);
				text_encrypted = rsa_encrypt(c.txt key k_pub hash sha256);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash sha256);
				text_encrypted = rsa_encrypt(c.txt key k_pub hash sha512);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash sha512);			

			when any do
				begin
					vchr_id_problem_list = vchr_id_problem_list || c.id || '; ' ;
					--exception;
				end
			end

			begin
				n = bit_length(c.blb);
				n = char_length(c.blb);
				y = left(c.blb,1);
				y = lower(c.blb);
				y = lpad(c.blb,2,c.blb);
				n = octet_length(c.blb);
				y = overlay(c.blb placing c.blb from 1);
				n = position(c.blb in c.blb);
				y = reverse(c.blb);
				y = replace(c.blb, c.blb, c.blb);
				y = right(c.blb,1);
				y = rpad(c.blb,2,c.blb);
				y = substring(c.blb from 1 for 1);
				y = trim(c.blb);
				y = upper(c.blb);
				-------------------
				y = minvalue('ɡ','ɥ','ɦ','ɪ','ɫ','ɬ','ɱ','ɽ','ʇ','ʝ','ʞ');
				y = maxvalue('ɡ','ɥ','ɦ','ɪ','ɫ','ɬ','ɱ','ɽ','ʇ','ʝ','ʞ');
				-------------------
				b = c.blb = 'Ⱥ';
				b = c.blb < 'Ⱥ';
				b = c.blb > 'Ⱥ';
				b = c.blb <> 'Ⱥ';
				b = c.blb between 'Ⱥ' and 'ʞ';
				b = c.blb is distinct from 'ʞ';
				b = c.blb is not distinct from 'ʞ';
				b = c.blb starts with 'ʞ';
				b = c.blb similar to 'ʞ{0,1}';
				b = c.blb in ('ɡ','ɥ','ɦ','ɪ','ɫ','ɬ','ɱ','ɽ','ʇ','ʝ','ʞ');

				v = crypt_hash(c.blb using md5);
				v = crypt_hash(c.blb using sha1);
				v = crypt_hash(c.blb using sha256);
				v = crypt_hash(c.blb using sha512);
				
				-- Following statements were commented out because of bug
				-- described in https://github.com/FirebirdSQL/firebird/issues/6858
				-- They are uncommented because bug was fixed 17.06.2021.
				-- Checked on intermediate builds
				-- 4.0.1.2517 (17.06.2021 15:12) and 5.0.0.79 (17.06.2021 14:44).
				-- /*
				text_encrypted = rsa_encrypt(c.blb key k_pub hash md5);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash md5);
				text_encrypted = rsa_encrypt(c.blb key k_pub hash md5);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash md5);
				text_encrypted = rsa_encrypt(c.blb key k_pub hash sha1);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash sha1);
				text_encrypted = rsa_encrypt(c.blb key k_pub hash sha256);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash sha256);
				text_encrypted = rsa_encrypt(c.blb key k_pub hash sha512);
				text_decrypted = rsa_decrypt(text_encrypted key k_prv hash sha512);			
				-- */

			when any do
				begin
					blob_id_problem_list = blob_id_problem_list || c.id || '; ' ;
					--exception;
				end
			end


		end
		vchr_id_problem_list = trim(vchr_id_problem_list);
		blob_id_problem_list = trim(blob_id_problem_list);

		if ( vchr_id_problem_list > '' or blob_id_problem_list > '' ) then
			suspend;
	end
	^
	set term ;^
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)


@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    act_1.execute()
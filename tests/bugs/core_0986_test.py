#coding:utf-8

"""
ID:          issue-1393
ISSUE:       1393
TITLE:       Non-ASCII quoted identifiers are not converted to metadata (UNICODE_FSS) charset
DESCRIPTION:
JIRA:        CORE-986
"""

import pytest
from firebird.qa import *
from pathlib import Path

db = db_factory()

act = python_act('db', substitutions=[('in file .*', 'in file XXX')])

expected_stdout_a = """create collation "Циферки" for utf8 from unicode case insensitive 'NUMERIC-SORT=1';"""

expected_stderr_a_40 = """
Statement failed, SQLSTATE = 22018
arithmetic exception, numeric overflow, or string truncation
-Cannot transliterate character between character sets
After line 4 in file non_ascii_ddl.sql
"""

expected_stderr_a_30 = """
Statement failed, SQLSTATE = 22000
unsuccessful metadata update
-CREATE COLLATION Циферки failed
-Malformed string
After line 4 in file non_ascii_ddl.sql
"""

non_ascii_ddl='''
     set bail on;

     set echo on;

     create collation "Циферки" for utf8 from unicode case insensitive 'NUMERIC-SORT=1';
     create collation "Испания" for iso8859_1 from es_es_ci_ai 'SPECIALS-FIRST=1';;
     commit;

     create domain "ИД'шники" int;
     create domain "Группы" varchar(30) check( value in ('Электрика', 'Ходовая', 'Арматурка', 'Кузовщина') );
     create domain "Артикулы" varchar(12) character set utf8 check( value = upper(value) )
     collate "Циферки" -- enabled since core-5220 was fixed (30.04.2016)
     ;
     create domain "Комрады" varchar(40) character set iso8859_1
     collate "Испания" -- enabled since core-5220 was fixed (30.04.2016)
     ;
     create domain "Кол-во" numeric(12,3) not null;

     create sequence generilka;
     create sequence "Генерилка";

     create role "манагер";
     create role "начсклд";

     -- TEMPLY COMMENTED UNTIL CORE-5209 IS OPEN:
     -- ISQL -X ignores connection charset for text of EXCEPTION message (restoring it in initial charset when exception was created)
     recreate exception "Невзлет" 'Запись обломалась, ваши не пляшут. Но не стесняйтесь и обязательно заходите еще, мы всегда рады видеть вас. До скорой встречи, товарищ!';
     commit;

     -------------------------------------------------
     recreate table "склад" (
          "ИД'шник" "ИД'шники"
         ,"Откудова" "Группы"
         ,"Номенклатура" "Артикулы"
         ,"ИД'родителя" "ИД'шники"
         ,"сколько там" "Кол-во"
         ,constraint "ПК-ИД'шник" primary key ("ИД'шник") using index "склад_ПК"
         ,constraint "ФК-на-родока" foreign key("ИД'родителя") references "склад" ("ИД'шник")  using index "склад_ФК"
         ,constraint "остаток >=0" check ("сколько там" >= 0)
     );

     recreate view "Электрика"("ид изделия", "Название", "Запас") as
     select
          "ИД'шник"
         ,"Номенклатура"
         ,"сколько там"
     from "склад"
     where "Откудова" = 'Электрика'
     ;

     set term ^;
     create or alter trigger "склад би" for "склад" active before insert as
     begin
         --new."ИД'шник" = coalesce( new."ИД'шник", gen_id(generilka, 1) );
         -- not avail up to 2.5.6:
         new."ИД'шник" = coalesce( new."ИД'шник", gen_id("Генерилка", 1) );
     end
     ^

     create or alter procedure "Доб на склад"(
          "Откудова" varchar(30)
         ,"Номенклатура" varchar(30)
         ,"ИД'родителя" int
         ,"сколько там" numeric(12,3)
     ) returns (
         "код возврата" int
     ) as
     begin
         insert into "склад"(
              "Откудова"
             ,"Номенклатура"
             ,"ИД'родителя"
             ,"сколько там"
         ) values (
              :"Откудова"
             ,:"Номенклатура"
             ,:"ИД'родителя"
             ,:"сколько там"
         );

     end
     ^
     create or alter procedure "Удалить" as
     begin
      /*
             Антон Павлович Чехов. Каштанка

             1. Дурное поведение

              Молодая рыжая собака - помесь такса с дворняжкой - очень похожая мордой
         на лисицу, бегала взад и вперед по тротуару  и  беспокойно  оглядывалась  по
         сторонам. Изредка она останавливалась и, плача, приподнимая то одну  озябшую
         лапу, то другую, старалась дать себе отчет: как это могло случиться, что она
         заблудилась?
      */
     end
     ^
     set term ;^

     grant select on "склад" to "манагер";
     grant select, insert, update, delete on "склад" to "начсклд";
     -- no avail in 2.0: grant execute procedure "Доб на склад" to "начсклд";


     comment on sequence "Генерилка" is 'Генератор простых идей';
     comment on table "склад" is 'Это всё, что мы сейчас имеем в наличии';
     comment on view "Электрика" is 'Не суй пальцы в розетку, будет бо-бо!';
     comment on procedure "Доб на склад" is 'Процедурка добавления изделия на склад';
     comment on parameter "Доб на склад"."Откудова" is 'Группа изделия, которое собираемся добавить';

     comment on parameter "Доб на склад"."ИД'родителя"  is '
         Федор Михайлович Достоевский

         Преступление и наказание

         Роман в шести частях с эпилогом


         Часть первая

         I
        В начале июля, в чрезвычайно жаркое время, под вечер, один молодой человек вышел из своей каморки, которую нанимал от жильцов в С -- м переулке, на улицу и медленно, как бы в нерешимости, отправился к К -- ну мосту.
        Он благополучно избегнул встречи с своею хозяйкой на лестнице. Каморка его приходилась под самою кровлей высокого пятиэтажного дома и походила более на шкаф, чем на квартиру. Квартирная же хозяйка его, у которой он нанимал эту каморку с обедом и прислугой, помещалась одною лестницей ниже, в отдельной квартире, и каждый раз, при выходе на улицу, ему непременно надо было проходить мимо хозяйкиной кухни, почти всегда настежь отворенной на лестницу. И каждый раз молодой человек, проходя мимо, чувствовал какое-то болезненное и трусливое ощущение, которого стыдился и от которого морщился. Он был должен кругом хозяйке и боялся с нею встретиться.
        Не то чтоб он был так труслив и забит, совсем даже напротив; но с некоторого времени он был в раздражительном и напряженном состоянии, похожем на ипохондрию. Он до того углубился в себя и уединился от всех, что боялся даже всякой встречи, не только встречи с хозяйкой. Он был задавлен бедностью; но даже стесненное положение перестало в последнее время тяготить его. Насущными делами своими он совсем перестал и не хотел заниматься. Никакой хозяйки, в сущности, он не боялся, что бы та ни замышляла против него. Но останавливаться на лестнице, слушать всякий вздор про всю эту обыденную дребедень, до которой ему нет никакого дела, все эти приставания о платеже, угрозы, жалобы, и при этом самому изворачиваться, извиняться, лгать, -- нет уж, лучше проскользнуть как-нибудь кошкой по лестнице и улизнуть, чтобы никто не видал.
        Впрочем, на этот раз страх встречи с своею кредиторшей даже его самого поразил по выходе на улицу.
        "На какое дело хочу покуситься и в то же время каких пустяков боюсь! -- подумал он с странною улыбкой. -- Гм... да... всё в руках человека, и всё-то он мимо носу проносит, единственно от одной трусости... это уж аксиома... Любопытно, чего люди больше всего боятся? Нового шага, нового собственного слова они всего больше боятся... А впрочем, я слишком много болтаю. Оттого и ничего не делаю, что болтаю. Пожалуй, впрочем, и так: оттого болтаю, что ничего не делаю. Это я в этот последний месяц выучился болтать, лежа по целым суткам в углу и думая... о царе Горохе. Ну зачем я теперь иду? Разве я способен на это? Разве это серьезно? Совсем не серьезно. Так, ради фантазии сам себя тешу; игрушки! Да, пожалуй что и игрушки!"
        На улице жара стояла страшная, к тому же духота, толкотня, всюду известка, леса, кирпич, пыль и та особенная летняя вонь, столь известная каждому петербуржцу, не имеющему возможности нанять дачу, -- всё это разом неприятно потрясло и без того уже расстроенные нервы юноши. Нестерпимая же вонь из распивочных, которых в этой части города особенное множество, и пьяные, поминутно попадавшиеся, несмотря на буднее время, довершили отвратительный и грустный колорит картины. Чувство глубочайшего омерзения мелькнуло на миг в тонких чертах молодого человека. Кстати, он был замечательно хорош собою, с прекрасными темными глазами, темно-рус, ростом выше среднего, тонок и строен. Но скоро он впал как бы в глубокую задумчивость, даже, вернее сказать, как бы в какое-то забытье, и пошел, уже не замечая окружающего, да и не желая его замечать. Изредка только бормотал он что-то про себя, от своей привычки к монологам, в которой он сейчас сам себе признался. В эту же минуту он и сам сознавал, что мысли его порою мешаются и что он очень слаб: второй день как уж он почти совсем ничего не ел.
        Он был до того худо одет, что иной, даже и привычный человек, посовестился бы днем выходить в таких лохмотьях на улицу. Впрочем, квартал был таков, что костюмом здесь было трудно кого-нибудь удивить. Близость Сенной, обилие известных заведений и, по преимуществу, цеховое и ремесленное население, скученное в этих серединных петербургских улицах и переулках, пестрили иногда общую панораму такими субъектами, что странно было бы и удивляться при встрече с иною фигурой. Но столько злобного презрения уже накопилось в душе молодого человека, что, несмотря на всю свою, иногда очень молодую, щекотливость, он менее всего совестился своих лохмотьев на улице. Другое дело при встрече с иными знакомыми или с прежними товарищами, с которыми вообще он не любил встречаться... А между тем, когда один пьяный, которого неизвестно почему и куда провозили в это время по улице в огромной телеге, запряженной огромною ломовою лошадью, крикнул ему вдруг, проезжая: "Эй ты, немецкий шляпник!" -- и заорал во всё горло, указывая на него рукой, -- молодой человек вдруг остановился и судорожно схватился за свою шляпу. Шляпа эта была высокая, круглая, циммермановская, но вся уже изношенная, совсем рыжая, вся в дырах и пятнах, без полей и самым безобразнейшим углом заломившаяся на сторону. Но не стыд, а совсем другое чувство, похожее даже на испуг, охватило его.
        "Я так и знал! -- бормотал он в смущении, -- я так и думал! Это уж всего сквернее! Вот эдакая какая-нибудь глупость, какая-нибудь пошлейшая мелочь, весь замысел может испортить! Да, слишком приметная шляпа... Смешная, потому и приметная... К моим лохмотьям непременно нужна фуражка, хотя бы старый блин какой-нибудь, а не этот урод. Никто таких не носит, за версту заметят, запомнят... главное, потом запомнят, ан и улика. Тут нужно быть как можно неприметнее... Мелочи, мелочи главное!.. Вот эти-то мелочи и губят всегда и всё..."

     ';
     --------------------------------------------------
     commit;
     --/*
     --TEMPLY COMMENTED UNTIL CORE-5221 IS OPEN:
     set echo on;
     show collation;
     show domain;
     show exception; -- <<<<<<<<<<<<<
     show sequence;
     show table;
     show trigger;
     show view;
     show procedure;
     show role;
     --*/
     set list on;
     set echo off;
     select 'Metadata created OK.' as msg from rdb$database;
 '''


tmp_file = temp_file('non_ascii_ddl.sql')

@pytest.mark.version('>=3.0')
def test_1(act: Action, tmp_file: Path):
    tmp_file.write_bytes(non_ascii_ddl.encode('cp1251'))
    # run without specifying charset
    act.expected_stdout = expected_stdout_a
    act.expected_stderr = expected_stderr_a_40 if act.is_version('>=4.0') else expected_stderr_a_30
    act.isql(switches=['-q'], input_file=tmp_file, charset=None, io_enc='cp1251')
    assert (act.clean_stdout == act.clean_expected_stdout and
            act.clean_stderr == act.clean_expected_stderr)
    # run with charset
    act.reset()
    act.isql(switches=['-q'], input_file=tmp_file, charset='win1251', io_enc='cp1251')
    assert act.clean_stdout.endswith('Metadata created OK.')



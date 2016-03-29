# coding: utf-8
from django.shortcuts import render
from django.db.models import *
from demo.models import *

# Create your views here.
def query(request):
    # -- 1、 查询Student表中的所有记录的Sname、Ssex和classno列。
    # SELECT sname,ssex,class FROM student;
    # result = Student.objects.values('sname', 'ssex', 'classno')

    # -- 2、 查询教师所有的单位即不重复的Depart列。
    # SELECT DISTINCT(depart) FROM teacher;
    # result = Teacher.objects.values('depart').distinct()

    # -- 3、 查询Student表的所有记录。
    # SELECT * FROM student;
    # result = Student.objects.all()

    # -- 4、 查询Score表中成绩在60到80之间的所有记录。
    # SELECT * FROM score WHERE grade BETWEEN 60 AND 80;
    # SELECT * FROM score WHERE grade>=60 AND grade<=80;
    # result = Score.objects.filter(grade__range=(60, 80))
    # result = Score.objects.filter(grade__gte=60, grade__lte=80)
    # -- 5、 查询Score表中成绩为85，86或88的记录。
    # SELECT * FROM score WHERE grade IN (85,86,88);
    # result = Score.objects.filter(grade__in=(85,86,88))
    # Q F
    # result = Score.objects.filter(Q(grade=85) | Q(grade=86) | Q(grade=88))

    # -- 6、 查询Student表中“95031”班或性别为“女”的同学记录。
    # SELECT * FROM student WHERE class='95031' OR ssex='女';
    # result = Student.objects.filter(Q(classno='95031') | Q(ssex=u'女'))
    # -- 7、 以Class降序查询Student表的所有记录。
    # SELECT * FROM student ORDER BY class DESC;
    # result = Student.objects.order_by('-classno')
    # -- 8、 以Cno升序、grade降序查询Score表的所有记录。
    # SELECT * FROM score ORDER BY cno ASC,grade DESC;
    # result = Score.objects.order_by('cno', '-grade')
    # -- 9、 查询“95031”班的学生人数。
    # SELECT COUNT(*) AS total_sum FROM student GROUP BY class HAVING class='95031';
    # SELECT COUNT(*) AS total_sum FROM student where class='95031'
    # result = len(Student.objects.filter(classno='95031')) # 错误
    # result = Student.objects.filter(classno='95031').aggregate(Count('sname'))
    # result = Student.objects.filter(classno="95031").count()
    # -- 10、查询Score表中的最高分的学生学号和课程号。
    # SELECT sno,cno FROM score ORDER BY grade DESC LIMIT 1;
    # result = Score.objects.values('sno', 'cno').order_by('-grade')[:1]
    # -- 11、查询‘3-105’号课程的平均分。
    # SELECT ROUND(AVG(grade),2) AS avg_grade FROM score
    # GROUP BY cno HAVING cno='3-105';
    # result = Score.objects.filter(cno='3-105').aggregate(Avg('grade'))
    # -- 12、查询Score表中至少有5名学生选修的并以3开头的课程的平均分数。
    # SELECT ROUND(AVG(grade),2) AS avg_grade FROM score
    # GROUP BY cno HAVING COUNT(sno)>=5 AND cno LIKE '3%';
    # result = Score.objects.filter(cno__cno__startswith='3').values('cno').\
    #     annotate(grade_avg=Avg('grade'), sno_count=Count('sno')).filter(sno_count__gt=5)
    # -- 13、查询最低分大于70，最高分小于90的Sno列。
    # SELECT sno FROM score GROUP BY sno HAVING MAX(grade)<90 AND MIN(grade)>70;
    # result = Score.objects.values('sno').annotate(grade_max=Max('grade'), grade_min=Min('grade'))\
    #     .filter(grade_min__gt=70, grade_max__lt=90)
    # -- 14、查询所有学生的Sname、Cno和grade列。
    # SELECT s.sname,c.cno,c.grade FROM student AS s
    # JOIN score AS c ON s.sno=c.sno;
    # result = Score.objects.all()
    # result = Score.objects.values('sno__sname', 'cno', 'grade')
    # -- 15、查询所有学生的Sno、Cname和grade列。
    # SELECT c.sno,l.cname,c.grade FROM score AS c
    # JOIN lesson AS l ON c.cno=l.cno;
    # result = Score.objects.values('sno', 'cno__cname', 'grade')
    # -- 16、查询所有学生的Sname、Cname和grade列。
    # SELECT s.sname,l.cname,c.grade FROM student AS s
    # JOIN score AS c ON s.sno=c.sno
    # JOIN lesson AS l ON c.cno=l.cno;
    # result = Score.objects.values('sno__sname', 'cno__cname', 'grade')
    # 17、查询“95033”班所选课程的平均分。
    # select c.cname,avg(defree)
    # from score sc ,course c,student st
    # where c.cno = sc.cno
    # and  sc.sno = st.sno
    # and st.class='95033'
    # group by sc.cno
    # result = Score.objects.filter(sno__classno='95033').values('cno__cname').annotate(Avg('grade'))
    # -- 18、假设使用如下命令建立了一个grade表：
    # CREATE TABLE grade(
    # low DOUBLE(4,1),
    # upp DOUBLE(4,1),
    # rank CHAR(1)
    # );
    # INSERT INTO grade VALUES(90,100,'A'),
    # (80,89,'B'),
    # (70,79,'C'),
    # (60,69,'D'),
    # (0,59,'E');
    # COMMIT;
    #
    # -- 19、查询选修“3-105”课程的成绩高于“9”号同学成绩的所有同学的记录。
    # select * from demo_student where sno in (
    # select sno from
    # demo_score sc
    # where sc.cno_id='3-105'
    # and  sc.grade >(select grade from demo_score
    # where sno_id = 9
    # and cno_id='3-105'))
    # result = Student.objects.filter(sno__in=Score.objects.filter(cno='3-105', grade__gt=Score.objects.filter(sno='9', cno='3-105').values('grade')).values_list('sno'))

    # -- 20、查询score中选学一门以上课程的同学中分数为非最高分成绩的记录。
    # select * from demo_score a
    # where sno_id in (select sno_id from demo_score group by sno_id having COUNT(*)>1)
    # and
    # (grade not in (select MAX(grade) from demo_score b where a.cno_id=b.cno_id group by cno_id))
    # 原生sql
    # result = Score.objects.raw('select * from demo_score a where '
    #                            'sno_id in (select sno_id from demo_score group by sno_id having COUNT(*)>1) '
    #                   'and '
    #                   '(grade not in (select MAX(grade) from demo_score b where a.cno_id=b.cno_id group by cno_id))')
    # for i in result:
    #     print i
    # -- 21、查询成绩高于学号为“9”、课程号为“3-105”的成绩的所有记录。
    # select *
    # from score sc,student st
    # where sc.defree >(select defree from score
    # where sno = 9
    # and cno='3-105')
    # and sc.cno = '3-105'
    # and sc.sno = st.sno;
    # result = Score.objects.filter(grade__gt=Score.objects.filter(sno=9, cno='3-105'),
                         # cno='3-105').select_related('sno')
    # -- 22、查询和学号为8的同学同年出生的所有学生的Sno、Sname和Sbirthday列。
    # SELECT sno,sname,sbirthday FROM student WHERE YEAR(sbirthday)=
    # (SELECT YEAR(sbirthday) FROM student WHERE sno=8);
    # result = Student.objects.filter(sbirthday__year=Student.objects.get(sno=9).sbirthday.year)
    # -- 23、查询“张旭“教师任课的学生成绩。
    # SELECT grade FROM score AS s
    # JOIN lesson AS l ON s.cno=l.cno
    # JOIN teacher AS t ON l.tno=t.tno
    # WHERE t.tname='张旭';
    # result = Score.objects.filter(cno__tno__tname=u'张旭').values('grade')

    # -- 24、查询选修某课程的同学人数多于5人的教师姓名。
    # -- 第一种，子查询方式查询：
    # SELECT tname FROM teacher WHERE tno IN
    # (SELECT tno FROM lesson WHERE cno IN
    # (SELECT cno FROM score GROUP BY cno HAVING COUNT(*)>5));
    # result = Teacher.objects.filter(tno__in=
    #                                Course.objects.filter(cno__in=Score.objects.values('cno').
    #                                                      annotate(cno_count=Count('cno')).filter(cno_count__gt=5).
    #                                                      values('cno')).values('tno'))
    # -- 第二种，表连接方式查询：
    # SELECT tname FROM teacher AS t
    # JOIN lesson AS l ON t.tno=l.tno
    # JOIN score AS s ON s.cno=l.cno
    # GROUP BY s.cno HAVING COUNT(s.sno)>5;
    # result = Score.objects.values('cno__tno__tname').annotate(cno_count=Count('cno')).filter(cno_count__gt=5).values('cno__tno__tname')
    # -- 25、查询95033班和95031班全体学生的成绩记录。
    # SELECT s.sname,c.grade,c.cno FROM score AS c
    # JOIN student AS s ON c.sno=s.sno
    # WHERE s.class IN ('95033','95031');
    # result = Score.objects.filter(sno__classno__in=('95033', '95031')).select_related('sno')
    # -- 26、查询存在有85分以上成绩的课程Cno.
    # SELECT cno FROM score GROUP BY cno HAVING MAX(grade)>85;
    # result = Score.objects.values('cno').annotate(grade_max=Max('grade')).filter(grade_max__gt=85)
    # -- 27、查询出“计算机系“教师所教课程的成绩表。
    # SELECT c.sno,c.grade,c.cno,l.cname FROM score AS c
    # JOIN lesson AS l ON c.cno=l.cno
    # JOIN teacher AS t ON t.tno=l.tno
    # WHERE t.depart='计算机系';
    # result = Score.objects.filter(cno__tno__depart=u'计算机系')
    # -- 28、查询“计算机系”与“电子工程系“不同职称的教师的Tname和depart。
    # select
    #     t.tname,t.depart
    # from
    #     teacher t,course c
    # where c.tno = t.tno
    #     and (c.cname= '计算机系' or c.cname= '电子工程系' )
    # result = Teacher.objects.filter(Q(course__cname=u'计算机系') | Q(course__cname=u'电子工程系') )
    # -- 29、查询选修编号为“3-105“课程且成绩至少高于选修编号为“3-245”的同学的
    # --     Cno、Sno和grade,并按grade从高到低次序排序。
    # select cno_id ,sno_id ,grade
    # from demo_score
    # where grade >(
    # select min(grade)
    # from demo_score
    # where cno_id = '3-245'
    # )
    # order by grade desc;
    # result = Score.objects.filter(grade__gt=Score.objects.filter(cno='3-245').aggregate(grade_min=Min('grade')).values()[0]).order_by('-grade')
    # -- 30、查询选修编号为“3-105”且成绩高于选修编号为“3-245”课程最高分的同学的成绩记录
    # --     Cno、Sno和grade.
    # select cno ,sno ,defree
    # from score
    # where defree >(
    # select max(defree)
    # from score
    # where cno = '3-245'
    # ) and cno='3-105'
    # result = Score.objects.filter(grade__gt=Score.objects.filter(cno='3-245').aggregate(grade_max=Max('grade')).values()[0],
    #                               cno='3-105')

    # -- 31、查询所有教师和同学的name、sex和birthday.
    # SELECT sname AS name,ssex AS sex,sbirthday AS birthday FROM student
    # UNION ALL
    # SELECT tname,tsex,tbirthday FROM teacher;
    # import itertools
    # students = Student.objects.values('sname', 'ssex', 'sbirthday')
    # teachers = Teacher.objects.values('tname', 'tsex', 'tbirthday')
    # result = itertools.chain(students, teachers)
    # for r in result:
    #     print r
    # -- 32、查询所有“女”教师和“女”同学的name、sex和birthday.
    # SELECT sname AS name,ssex AS sex,sbirthday AS birthday FROM student WHERE ssex='女'
    # UNION ALL
    # SELECT tname,tsex,tbirthday FROM teacher WHERE tsex='女';
    # import itertools
    # students = Student.objects.filter(ssex='女').values('sname', 'ssex', 'sbirthday')
    # teachers = Teacher.objects.filter(tsex='女').values('tname', 'tsex', 'tbirthday')
    # result = itertools.chain(students, teachers)
    # for r in result:
    #     print r
    # -- 33、查询成绩比该课程平均成绩低的同学的成绩表。
    # SELECT grade,sno FROM score GROUP BY cno
    # HAVING grade<AVG(grade);
    # result = Score.objects.values('cno').annotate(grade_avg=Avg('grade')).filter(grade_avg__gt=F('grade'))
    # -- 34、查询所有任课教师的Tname和Depart.
    # SELECT tname,depart FROM teacher WHERE tno IN
    # (SELECT tno FROM lesson);
    # result = Teacher.objects.filter(tno__in=Course.objects.values('tno'))
    # -- 35 查询所有未讲课的教师的Tname和Depart.
    # SELECT tname,depart FROM teacher WHERE tno NOT IN
    # (SELECT tno FROM lesson);
    # result = Teacher.objects.filter(~Q(tno__in=Course.objects.values('tno')))
    # -- 36、查询至少有2名男生的班号。
    # SELECT class FROM student GROUP BY ssex
    # HAVING COUNT(*)>2 AND ssex='男';
    # result = Student.objects.filter(ssex=u'男').values('ssex').annotate(sex_count=Count('ssex')).filter(sex_count__gte=2)
    # -- 37、查询Student表中不姓“王”的同学记录。
    # SELECT * FROM student WHERE SUBSTRING(sname,1,1)!='王';
    # result = Student.objects.filter(~Q(sname__istartswith=u'王'))
    # -- 38、查询Student表中每个学生的姓名和年龄。
    # SELECT sname,(YEAR(CURRENT_DATE())-YEAR(sbirthday)) AS age FROM student;
    # orm和sql混用的方式
    # result = Student.objects.extra(select={'age':'year(CURRENT_DATE())-year(sbirthday)'}).values('sname', 'age')  #mysql下有效
    # result = Student.objects.extra(select={'age':'substr(date("now"),1,4)-substr(sbirthday,1,4)'}).values('sname', 'age')  #sqlite下有效
    # -- 39、查询Student表中最大和最小的Sbirthday日期值。
    # SELECT MAX(sbirthday),MIN(sbirthday) FROM student;
    # result = Student.objects.aggregate(sbirthday_max=Max('sbirthday'), sbirthday_min=Min('sbirthday'))
    # -- 40、以班号和年龄从大到小的顺序查询Student表中的全部记录。
    # SELECT * FROM student ORDER BY class DESC,sbirthday ASC;
    # result = Student.objects.order_by('-classno', '-sbirthday')
    # -- 41、查询“男”教师及其所上的课程。
    # SELECT l.cname,t.tname FROM lesson AS l
    # JOIN teacher AS t ON l.tno=t.tno
    # WHERE t.tsex='男';
    # result = Course.objects.filter(tno__tsex='男')
    # -- 42、查询最高分同学的Sno、Cno和grade列。
    # SELECT sno,cno,grade FROM score WHERE grade=
    # (SELECT MAX(grade) FROM score);
    # result = Score.objects.filter(grade=Score.objects.aggregate(grade_max=Max('grade'))['grade_max'])
    # -- 43、查询和“李军”同性别的所有同学的Sname.
    # SELECT sname FROM student WHERE ssex=
    # (SELECT ssex FROM student WHERE sname='李军');
    # result = Student.objects.filter(ssex=Student.objects.filter(sname=u'李军').values('ssex'))
    # -- 44、查询和“李军”同性别并同班的同学Sname.
    # SELECT sname FROM student WHERE ssex=
    # (SELECT ssex FROM student WHERE sname='李军')
    # AND class=(SELECT class FROM student WHERE sname='李军');
    # result = Student.objects.filter(ssex=Student.objects.filter(sname=u'李军').values('ssex'),
    #                                 classno=Student.objects.filter(sname=u'李军').values('classno'))
    # -- 45、查询所有选修“计算机导论”课程的“男”同学的成绩表
    # SELECT s.sname,c.cno,l.cname,c.grade FROM student AS s
    # JOIN score AS c ON s.sno=c.sno
    # JOIN lesson AS l ON l.cno=c.cno
    # WHERE l.cname='计算机导论' AND s.ssex='男';
    # result = Score.objects.filter(cno__cname=u'计算机导论', sno__ssex=u'男')
    # 46、查询韩梅梅选修了哪些课程
    # result = OptionalCourse.objects.filter(sno__sname=u'韩梅梅')
    # result = Student.objects.get(sname=u'韩梅梅').optionalcourse_set.all()
    return render(request, 'query.html', locals())
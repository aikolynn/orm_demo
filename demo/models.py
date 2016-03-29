# coding: utf-8
from django.db import models

# Create your models here.
# 学生
class Student(models.Model):
    sno = models.IntegerField(primary_key=True, verbose_name=u'学号')
    sname = models.CharField(max_length=20, verbose_name=u'姓名')
    ssex = models.CharField(max_length=4, choices=((1, u'男'), (2, u'女'), (3, u'保密')),
                            default=u'保密', verbose_name=u'姓名')
    sbirthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    classno = models.CharField(max_length=5, verbose_name=u'班级')

    class Meta:
        verbose_name = u'学生'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sname

# 老师
class Teacher(models.Model):
    tno = models.IntegerField(primary_key=True, verbose_name=u'编号')
    tname = models.CharField(max_length=20, verbose_name=u'姓名')
    tsex = models.CharField(max_length=4, choices=((1, u'男'), (2, u'女'), (3, u'保密')),
                            default=u'保密', verbose_name=u'姓名')
    tbirthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    depart = models.CharField(max_length=20, verbose_name=u'所在系')

    class Meta:
        verbose_name = u'老师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.tname

# 课程
class Course(models.Model):
    cno = models.CharField(primary_key=True, max_length=5,
                           verbose_name=u'编号')
    cname = models.CharField(max_length=20, verbose_name=u'课程名')
    tno = models.ForeignKey(Teacher, verbose_name=u'授课老师')
    sno = models.ManyToManyField(Student, through='OptionalCourse',
                                 verbose_name=u'选修学生')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.cname

# 课程选修
class OptionalCourse(models.Model):
    sno = models.ForeignKey(Student, verbose_name=u'学生')
    cno = models.ForeignKey(Course, verbose_name=u'课程')
    date_pub = models.DateTimeField(auto_now_add=True, verbose_name=u'选修时间')

    class Meta:
        verbose_name = u'课程选修'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

# 成绩
class Score(models.Model):
    sno = models.ForeignKey(Student, verbose_name=u'学生')
    cno = models.ForeignKey(Course, verbose_name=u'课程')
    grade = models.DecimalField(max_digits=3, decimal_places=1,
                                default=60, verbose_name=u'分数')

    class Meta:
        verbose_name = u'成绩'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
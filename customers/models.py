from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create your models here.

class Customer(models.Model):
    custID = models.AutoField(primary_key=True)
    name = models.CharField("Имя", max_length=255)
    birthday = models.DateField("Дата рождения")
    address = models.TextField(blank=True, null=True)
    doctorCert = models.CharField("Врач", max_length=255)  #врач, выдавший справку
    certExpiration = models.DateField("Срок справки")  #срок окончания справки
#    categoryID = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
#    schID = models.ForeignKey('Schedule', on_delete=models.DO_NOTHING)
    categoryChoices = [('H', 'Оздоровительное плавание'), ('D', 'Группы инвалидов'), ('L', 'Обучение плаванию'),
                       ('S', 'Группы спортивного плавания'), ('M', 'Группы от предприятий'),
                       ('G', 'Группы по программам поддержки Правительства')]
    category = models.CharField(
        choices=categoryChoices,
        max_length=1,
        default=None,
        null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Посетители'
        verbose_name_plural = u'Посетители'

#class Category(models.Model):
#    categoryID = models.AutoField(primary_key=True)
#    categoryName = models.CharField("Категория посетителя", max_length=255)
#    price = models.IntegerField("Цена сеанса")

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField("День")
    start = models.TimeField("Время начала")
    end = models.TimeField("Время конца")
    counter = models.IntegerField("Количество")
    duty = models.OneToOneField('Couch', on_delete=models.DO_NOTHING, null=True)
    cust = models.ManyToManyField('Customer', null=True)
    categoryChoices = [('H', 'Оздоровительное плавание'), ('D', 'Группы инвалидов'), ('L', 'Обучение плаванию'),
                       ('S', 'Группы спортивного плавания'), ('M', 'Группы от предприятий'),
                       ('G', 'Группы по программам поддержки Правительства')]
    category = models.CharField(
        choices=categoryChoices,
        max_length=1,
        default=None,
        null=True)

    class Meta:
        verbose_name = u'Расписание'
        verbose_name_plural = u'Расписание'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (
                new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    #def counter(self):
     #   self.counter = self.cust.count()
      #  return self.counter

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start))

    #def get_money

    def clean(self):
        if self.end <= self.start:
            raise ValidationError('Ending times must after starting times')

        events = Schedule.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start, self.end):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))

        if self.cust.count() > 30:
            raise ValidationError("You can't assign more than three regions")
        super(Schedule, self).clean(*args, **kwargs)

class Couch(models.Model):
    couchID = models.AutoField(primary_key=True)
    name = models.CharField("Имя", max_length=255)

    class Meta:
        verbose_name = u'Тренера'
        verbose_name_plural = u'Тренера'

class Cost(models.Model):
    costID = models.AutoField(primary_key=True)
    categoryChoices = [('H', 'Оздоровительное плавание'), ('D', 'Группы инвалидов'), ('L', 'Обучение плаванию'),
                       ('S', 'Группы спортивного плавания'), ('M', 'Группы от предприятий'),
                       ('G', 'Группы по программам поддержки Правительства')]
    category = models.CharField(
        choices=categoryChoices,
        max_length=1,
        default=None,
        null=True)
    money = models.FloatField("Стоимость")

    class Meta:
        verbose_name = u'Стоимость категорий'
        verbose_name_plural = u'Стоимость категорий'

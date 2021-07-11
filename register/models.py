
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_individual = models.BooleanField(default=False)
    is_corporate = models.BooleanField(default=False)



class vote(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey('event_creation',on_delete=models.CASCADE)


class Individual(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=40,unique=True)
    email =models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    state =models.CharField(max_length=100)
    district =models.CharField(max_length=100)
    city_or_town = models.CharField(max_length=100)
    pass_word = models.CharField(max_length=20)

    def __str__(self):
        return self.user_name



class Corporate(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=20,unique=True)
    CIN=models.CharField(max_length=24,unique=True)
    sub_category =models.CharField(max_length=40)
    ROC=models.CharField(max_length=40)
    branch=models.CharField(max_length=40)
    email= models.CharField(max_length=40,unique=True)
    Net_worth = models.CharField(max_length=5)
    pass_word = models.CharField(max_length=20)


    def __str__(self):
        return self.company_name


import datetime
from django.utils.translation import ugettext_lazy as _

class event_creation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    event_name =models.CharField(max_length=100)
    event_location =models.CharField(max_length=40)
    start_date = models.DateField(_("Start_Date"), default=datetime.date.today)
    start_time=models.TimeField()
    end_time= models.TimeField()
    end_date =  models.DateField(_("end_Date"), default=datetime.date.today)
    numv =models.IntegerField(default=0)
    total_budget =models.IntegerField()
    my_budget = models.IntegerField()
    def __str__(self):
        return self.event_name

    def user_can_vote(self, user):
        user_votes=user.vote_set.all()
        qs=user_votes.filter(event=self)
        if qs.exists():
            return False
        return True
    @property
    def num_votes(self):
        return self.vote_set.count()


class event_contrib(models.Model):
    user=models.ForeignKey('User',on_delete='CASCADE')
    event_id=models.ForeignKey('event_creation',on_delete='CASCADE')
    #category is comapny or individual
    category = models.CharField(max_length=30)
    budget = models.IntegerField()
    textfield = models.CharField(max_length=50,default="")
    membercount = models.IntegerField(default=1)
    description = models.CharField(max_length=500,default="")



    def __str__(self):
        return str(self.event_id)

    class Meta:

        unique_together = ("user","event_id")



from chat.models import Room
from django.db.models.signals import post_save

def create_room(sender,**kwargs):
    if(kwargs['created']):
        p=Room.objects.create(title=kwargs['instance'].event_name)


post_save.connect(create_room,sender=event_creation)


def create_contributor(sender,**kwargs):
    print("coooll")
    if(kwargs['created']):
        print(kwargs['instance'],dir(kwargs['instance']))
        p = event_contrib.objects.create(user=kwargs['instance'].user,event_id=kwargs['instance'],category="Individual",
                                         budget=kwargs['instance'].my_budget)


post_save.connect(create_contributor,sender=event_creation)




#--------------------

from django.utils import timezone

class demo(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    message =models.CharField(max_length=20)


''''
>>> a
datetime.datetime(2019, 4, 21, 14, 31, 21, 2049)
>>> o[0].date
datetime.datetime(2019, 4, 21, 14, 29, 27, 885520, tzinfo=<UTC>)
>>> import pytz
>>> b=a.replace(tzinfo=pytz.UTC
... )
>>> b
datetime.datetime(2019, 4, 21, 14, 31, 21, 2049, tzinfo=<UTC>)
>>> a
datetime.datetime(2019, 4, 21, 14, 31, 21, 2049)
>>> o[0].date
datetime.datetime(2019, 4, 21, 14, 29, 27, 885520, tzinfo=<UTC>)
>>> b==o[0].date
False
>>> b<o[0].date
False
>>> b>o[0].date
True
>>>


'''
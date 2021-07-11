
from .models import Individual,User,event_creation
from django.forms import ModelForm

class IndividualForm(ModelForm):
    class Meta:
        model=Individual
        fields =('user_name','email','first_name','last_name','phone_no','state','district','city_or_town','pass_word')


from .models import Corporate

from django.forms import ModelForm

class CorporateForm(ModelForm):
    class Meta:
        model = Corporate
        fields =('company_name','CIN','sub_category','ROC','branch','email',
                 'pass_word')


from django.contrib.auth.forms import UserChangeForm


class editprofileform(UserChangeForm):
    class Meta:
        model = User
        fields =('username',
                  'email',
                 'password',
                 )

class eventform(ModelForm):
    class Meta:
        model = event_creation
        exclude =('user',)



class editform(ModelForm):
    class Meta:
        model =event_creation
        exclude = ('numv',)


from .models import event_contrib


class EventRegister(ModelForm):
    class Meta:
        model = event_contrib
        exclude =('membercount',)



class Eventcool(ModelForm):
    class Meta:
        model = event_contrib
        fields ='__all__'


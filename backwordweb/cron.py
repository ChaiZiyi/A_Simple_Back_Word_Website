from .models import User

def cleardayrecitednum():
    user_obj = User.objects.exclude(dayrecitednum='0')
    for each in user_obj:
        each.dayrecitednum = 0
        each.save()
    return True
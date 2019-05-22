from restapi import models

def check_black_user(user_id):
    count=len(models.UserBlack.objects.filter(user_id=user_id))
    print("count,",count)
    if (count==0):
        return False
    else:
        return True
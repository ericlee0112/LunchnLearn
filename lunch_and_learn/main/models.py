from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key = True, max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # password = models.CharField(max_length=20)

class Skill(models.Model):
    skill_name = models.CharField(max_length = 100, primary_key = True)

# class Food_Options(models.Model):
#     food_name = models.CharField(max_length = 100, primary_key = True)

class Event(models.Model):
    #location = models.CharField(max_length = 100)
    start_date_time = models.DateTimeField(auto_now_add=False)
    end_date_time = models.DateTimeField(auto_now_add=False)
    skill = models.ForeignKey(Skill, on_delete= models.DO_NOTHING)
    organizer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = '%(class)s_orginizer')
    teacher = models.ForeignKey(User, on_delete = models.CASCADE, related_name = '%(class)s_teacher')

class User_Skill(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    skill_name = models.ForeignKey(Skill, on_delete= models.CASCADE)
    skill_level = models.IntegerField()
    wants = models.BooleanField()
    class Meta:
        unique_together = ('username', 'skill_name')

class Event_Attendees(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete = models.CASCADE)
    class Meta:
        unique_together = ('username', 'event_id')

# class Event_Food(models.Model):
#     foodname = models.ForeignKey(Food_Options, on_delete = models.CASCADE)
#     event_id = models.ForeignKey(Event, on_delete = models.CASCADE)
#     class Meta:
#         unique_together = ('foodname', 'event_id')

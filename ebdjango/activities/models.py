from django.db import models

# Create your models here.
class Activity (models.Model):
    strava_id      = models.BigIntegerField()
    user           = models.CharField(max_length=30)
    title           = models.CharField(max_length=30, default=" ")
    activity_type  = models.CharField(max_length=10)
    workout_type   = models.CharField(max_length=30, blank=True)
    date           = models.DateField()
    timestamp      = models.IntegerField()
    heartrate      = models.IntegerField()
    distance       = models.FloatField()
    moving_time    = models.IntegerField()
    elevation      = models.FloatField()
    speed          = models.FloatField()
    suffer         = models.IntegerField()


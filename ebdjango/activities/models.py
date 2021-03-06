from django.db import models

# Create your models here.
class Activity (models.Model):
    strava_id      = models.BigIntegerField()
    user           = models.CharField(max_length=30)
    title          = models.CharField(max_length=50, default=" ")
    activity_type  = models.CharField(max_length=30)
    workout_type   = models.CharField(max_length=30, default=" ")
    date           = models.DateField()
    timestamp      = models.IntegerField()
    heartrate      = models.IntegerField()
    distance       = models.FloatField()
    moving_time    = models.IntegerField()
    elevation      = models.FloatField(default=0)
    speed          = models.FloatField()
    suffer         = models.IntegerField()

    def __str__(self):
        return str(self.title) + ": " + str(self.date) + "\t-\t" + str(self.distance)


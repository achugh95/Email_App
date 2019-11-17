from django.db import models


class EmailStats(models.Model):
    subject = models.CharField(max_length=100000000000000)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.subject + " -- " + str(self.timestamp)

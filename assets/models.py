from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=100)
    service_time = models.DateTimeField()
    expiration_time = models.DateTimeField()
    serviced = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Notification(models.Model):
    NOTIF_TYPE_CHOICES = [
        ('SERVICE', 'Service'),
        ('EXPIRATION', 'Expiration'),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIF_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Violation(models.Model):
    VIOLATION_TYPE_CHOICES = [
        ('SERVICE', 'Service'),
        ('EXPIRATION', 'Expiration'),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    violation_type = models.CharField(max_length=20, choices=VIOLATION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models

# Create your models here.

# Signal Model that stores signal data
class Signal(models.Model):
    signal_id = models.AutoField(primary_key=True)
    signal_name = models.CharField(max_length=50)
    signal_type = models.CharField(max_length=50)
    signal_values = models.ManyToManyField('SignalValue', through='SignalValue')
    signal_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.signal_name


# Signal analysis model that stores analyzed signal information
class SignalAnalysis(models.Model):
    signal = models.ForeignKey('Signal', on_delete=models.CASCADE)
    last_analyzed = models.DateTimeField(auto_now_add=True)
    mean = models.FloatField()
    median = models.FloatField()
    mode = models.FloatField()
    standard_deviation = models.FloatField()
    variance = models.FloatField()
    skewness = models.FloatField()
    kurtosis = models.FloatField()
    min = models.FloatField()
    max = models.FloatField()
    range = models.FloatField()

    def __str__(self):
        return self.signal.signal_name
    
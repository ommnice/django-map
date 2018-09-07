from django.db import models

# Create your models here.
class Cell(models.Model):
    import_csv_name = models.CharField(max_length=256, default='default')
    tech = models.CharField(max_length=256)
    key = models.CharField(max_length=256)
    parent_id = models.CharField(max_length=256)
    sub_parent_id = models.CharField(max_length=256)
    cell_id = models.CharField(max_length=256)
    antenna_id = models.DecimalField(max_digits=2,decimal_places=0)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    azimuth = models.DecimalField(max_digits=3,decimal_places=0)
    beamwidth = models.DecimalField(max_digits=3,decimal_places=0)

    def __str__(self):
        return 'Cell: %s' % (self.key)
from django.db import models

class MTCars(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(db_column='NAME')
    mpg = models.FloatField(db_column='MPG')
    cyl = models.IntegerField(db_column='CYL')
    disp = models.FloatField(db_column='DISP')
    hp = models.IntegerField(db_column='HP')
    drat = models.FloatField(db_column='DRAT')
    wt = models.FloatField(db_column='WT')
    qsec = models.FloatField(db_column='QSEC')
    vs = models.IntegerField(db_column='VS')
    am = models.IntegerField(db_column='AM')
    gear = models.IntegerField(db_column='GEAR') 
    carb = models.IntegerField(db_column='CARB') 
    
    class Meta:
        managed = True
        db_table = 'MTCars'
        ordering = ['id']
    
    def __str__(self):
        return self.name

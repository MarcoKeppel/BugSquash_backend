from django.db import models


class Routine(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=256)
    result = models.CharField(max_length=256)

    def __str__(self):
        return self.name + ' - ' + self.url


class Interaction(models.Model):
    interaction_type = models.CharField(max_length=30)
    element_id = models.CharField(max_length=30)
    content = models.CharField(max_length=100, default=None, null=True)
    fk_routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    pos = models.IntegerField()

    def __str__(self):
        return self.element_id + ' - ' + self.interaction_type + ' - ' + self.fk_routine.name + ' - ' + str(self.pos)
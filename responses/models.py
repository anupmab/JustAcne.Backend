from django.db import models
from django.contrib.postgres.fields import ArrayField

from users.models import AuthUser


class UserResponse(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=254, verbose_name="Question Identifier")
    answers = ArrayField(ArrayField(models.CharField(max_length=1000, blank=True)), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name = 'User Response'
        verbose_name_plural = 'User Responses'

    def __str__(self):
        return f"{self.user.email}-{self.question_id}"

    def __unicode__(self):
        return f"{self.user.email}-{self.question_id}"

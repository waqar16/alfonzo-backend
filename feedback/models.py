from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    stars = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
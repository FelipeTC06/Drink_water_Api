from django.db import models
from django.utils import timezone
from user_auth.models import User_Auth

class WaterIntake(models.Model):
    user = models.ForeignKey(User_Auth, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    intake_ml = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user.fullname} - {self.intake_ml}ml on {self.date}'

    def calculate_daily_goal(self):
        daily_goal = self.user.weight * 35
        return min(daily_goal, 5000)

    def total_intake_today(self):
        total = WaterIntake.objects.filter(user=self.user, date=timezone.now().date()).aggregate(models.Sum('intake_ml'))['intake_ml__sum'] or 0
        return total

    def remaining_intake_today(self):
        return max(0, self.calculate_daily_goal() - self.total_intake_today())

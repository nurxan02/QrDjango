# Django model for Employee and Attendancepython manage.py makemigrations
from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr = qrcode.make(self.user.username)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            self.qr_code.save(f'qr_{self.user.username}.png', ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.user.username} - {self.check_in}"

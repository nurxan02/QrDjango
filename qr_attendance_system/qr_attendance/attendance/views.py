from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['post'])
    def scan_qr(self, request):
        username = request.data.get("username")
        try:
            employee = Employee.objects.get(user__username=username)
            today_records = Attendance.objects.filter(employee=employee, check_in__date=now().date())

            if today_records.exists():
                record = today_records.first()
                if not record.check_out:
                    record.check_out = now()
                    record.save()
                    return Response({"message": "Çıxış qeyd edildi", "check_out": record.check_out})
                else:
                    return Response({"message": "Bu gün artıq giriş-çıxış edilib"})
            else:
                Attendance.objects.create(employee=employee)
                return Response({"message": "Giriş qeyd edildi", "check_in": now()})

        except Employee.DoesNotExist:
            return Response({"error": "İşçi tapılmadı"}, status=400)

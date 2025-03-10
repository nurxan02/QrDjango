import logging
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer

logger = logging.getLogger(__name__)  

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['post'])
    def scan_qr(self, request):


        username = request.data.get("username")
        if not username:
            return Response({"error": "Not logged in Please Log in!"}, status=400)

        try:
            employee = Employee.objects.get(user__username=username)
            today = now().date()
            now_time = now()  
            today_records = Attendance.objects.filter(employee=employee, check_in__date=today)

            if today_records.exists():
                record = today_records.first()
                if not record.check_out:
                    record.check_out = now_time
                    
                    record.save()
                    return Response({"message": "Checked-out", "check_out": record.check_out})
                else:
                    return Response({"message": "Today has already been logged in and out"})
            else:
                Attendance.objects.create(employee=employee, check_in=now_time)
                return Response({"message": "Checked-in", "check_in": now_time})

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found!"}, status=404)
        except Exception as e:
            logger.error(f"Error occured: {str(e)}")
            return Response({"error": "Fatality!"}, status=500)



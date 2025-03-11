from django.contrib import admin
from .models import Employee, Attendance, Report

class AttendanceAdmin(admin.TabularInline):
    model = Attendance
    extra = 0 
    fields = ['check_in', 'check_out'] 

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'qr_code']
    inlines = [AttendanceAdmin]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'message']
    readonly_fields = ['employee']

    def save_model(self, request, obj, form, change):
        if not obj.employee_id:
            try:
                obj.employee = Employee.objects.get(user=request.user)
            except Employee.DoesNotExist:
                obj.employee = None  # Handle the case where the employee does not exist
            
        super().save_model(request, obj, form, change)
    

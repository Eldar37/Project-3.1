from django.contrib import admin

from .models import Employee, Payroll, Position, WorkSchedule


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "base_salary")


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "end_time", "days")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "position", "schedule", "salary", "is_active")
    list_filter = ("position", "schedule", "is_active")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ("employee", "period_end", "gross_pay", "bonus", "paid_on")
    list_filter = ("paid_on",)

from django import forms
from .models import Employee, Payroll, Position, WorkSchedule


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name", "description", "base_salary"]


class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = ["name", "start_time", "end_time", "days"]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "position",
            "schedule",
            "salary",
            "hire_date",
            "is_active",
        ]
        widgets = {
            "hire_date": forms.DateInput(attrs={"type": "date"}),
        }


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ["employee", "period_start", "period_end", "gross_pay", "bonus", "notes"]
        widgets = {
            "period_start": forms.DateInput(attrs={"type": "date"}),
            "period_end": forms.DateInput(attrs={"type": "date"}),
        }

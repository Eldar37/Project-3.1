from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("positions/", views.PositionList.as_view(), name="positions"),
    path("positions/add/", views.PositionCreate.as_view(), name="position_add"),
    path("positions/<int:pk>/edit/", views.PositionUpdate.as_view(), name="position_edit"),
    path("positions/<int:pk>/delete/", views.PositionDelete.as_view(), name="position_delete"),
    path("schedules/", views.ScheduleList.as_view(), name="schedules"),
    path("schedules/add/", views.ScheduleCreate.as_view(), name="schedule_add"),
    path("schedules/<int:pk>/edit/", views.ScheduleUpdate.as_view(), name="schedule_edit"),
    path("schedules/<int:pk>/delete/", views.ScheduleDelete.as_view(), name="schedule_delete"),
    path("employees/", views.EmployeeList.as_view(), name="employees"),
    path("employees/add/", views.EmployeeCreate.as_view(), name="employee_add"),
    path("employees/<int:pk>/edit/", views.EmployeeUpdate.as_view(), name="employee_edit"),
    path("employees/<int:pk>/delete/", views.EmployeeDelete.as_view(), name="employee_delete"),
    path("payrolls/", views.PayrollList.as_view(), name="payrolls"),
    path("payrolls/add/", views.PayrollCreate.as_view(), name="payroll_add"),
    path("payrolls/<int:pk>/delete/", views.PayrollDelete.as_view(), name="payroll_delete"),
    path("payrolls/<int:pk>/pdf/", views.payroll_pdf, name="payroll_pdf"),
]

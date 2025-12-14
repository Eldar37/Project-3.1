from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .forms import EmployeeForm, PayrollForm, PositionForm, WorkScheduleForm
from .models import Employee, Payroll, Position, WorkSchedule


class TitleMixin:
    title: str | None = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title:
            context["title"] = self.title
        elif hasattr(self, "model"):
            context["title"] = str(getattr(self.model._meta, "verbose_name", "запись")).capitalize()
        return context


@login_required
def dashboard(request):
    employees = Employee.objects.count()
    positions = Position.objects.count()
    payrolls = Payroll.objects.count()
    recent_payrolls = Payroll.objects.select_related("employee").order_by("-paid_on")[:5]
    context = {
        "employees": employees,
        "positions": positions,
        "payrolls": payrolls,
        "recent_payrolls": recent_payrolls,
    }
    return render(request, "staff/dashboard.html", context)


@login_required
def logout_view(request):
    """Allow GET logout to avoid 405 when following a link."""
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect("login")


class PositionList(LoginRequiredMixin, ListView):
    model = Position
    template_name = "staff/position_list.html"


class PositionCreate(TitleMixin, LoginRequiredMixin, CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("positions")
    template_name = "staff/form.html"


class PositionUpdate(TitleMixin, LoginRequiredMixin, UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("positions")
    template_name = "staff/form.html"


class PositionDelete(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy("positions")
    template_name = "staff/confirm_delete.html"


class ScheduleList(LoginRequiredMixin, ListView):
    model = WorkSchedule
    template_name = "staff/schedule_list.html"


class ScheduleCreate(TitleMixin, LoginRequiredMixin, CreateView):
    model = WorkSchedule
    form_class = WorkScheduleForm
    success_url = reverse_lazy("schedules")
    template_name = "staff/form.html"


class ScheduleUpdate(TitleMixin, LoginRequiredMixin, UpdateView):
    model = WorkSchedule
    form_class = WorkScheduleForm
    success_url = reverse_lazy("schedules")
    template_name = "staff/form.html"


class ScheduleDelete(LoginRequiredMixin, DeleteView):
    model = WorkSchedule
    success_url = reverse_lazy("schedules")
    template_name = "staff/confirm_delete.html"


class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "staff/employee_list.html"


class EmployeeCreate(TitleMixin, LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("employees")
    template_name = "staff/form.html"


class EmployeeUpdate(TitleMixin, LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("employees")
    template_name = "staff/form.html"


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy("employees")
    template_name = "staff/confirm_delete.html"


class PayrollList(LoginRequiredMixin, ListView):
    model = Payroll
    template_name = "staff/payroll_list.html"
    queryset = Payroll.objects.select_related("employee")


class PayrollCreate(TitleMixin, LoginRequiredMixin, CreateView):
    model = Payroll
    form_class = PayrollForm
    success_url = reverse_lazy("payrolls")
    template_name = "staff/form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Выплата сохранена.")
        return response


class PayrollDelete(LoginRequiredMixin, DeleteView):
    model = Payroll
    success_url = reverse_lazy("payrolls")
    template_name = "staff/confirm_delete.html"


@login_required
def payroll_pdf(request, pk: int):
    payroll = get_object_or_404(Payroll.objects.select_related("employee"), pk=pk)
    response = HttpResponse(content_type="application/pdf")
    filename = f"payslip_{payroll.employee.last_name}_{payroll.period_end}.pdf"
    response["Content-Disposition"] = f'attachment; filename=\"{filename}\"'

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Расчётный лист")
    pdf.setFont("Helvetica", 12)
    y -= 30
    pdf.drawString(50, y, f"Сотрудник: {payroll.employee}")
    y -= 20
    pdf.drawString(50, y, f"Должность: {payroll.employee.position.name}")
    y -= 20
    pdf.drawString(50, y, f"График: {payroll.employee.schedule.name}")
    y -= 20
    pdf.drawString(50, y, f"Период: {payroll.period_start} - {payroll.period_end}")
    y -= 20
    pdf.drawString(50, y, f"Оклад: {payroll.employee.salary}")
    y -= 20
    pdf.drawString(50, y, f"Начисления: {payroll.gross_pay}")
    y -= 20
    pdf.drawString(50, y, f"Бонус: {payroll.bonus}")
    y -= 20
    pdf.drawString(50, y, f"Итого к выплате: {payroll.total_pay}")
    y -= 20
    pdf.drawString(50, y, f"Выплачено: {payroll.paid_on}")
    if payroll.notes:
        y -= 30
        pdf.drawString(50, y, f"Комментарий: {payroll.notes}")
    pdf.showPage()
    pdf.save()
    return response

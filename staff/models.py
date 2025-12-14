from django.db import models


class Position(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)
    base_salary = models.DecimalField("Базовый оклад", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self) -> str:
        return self.name


class WorkSchedule(models.Model):
    name = models.CharField("Название", max_length=100)
    start_time = models.TimeField("Начало смены")
    end_time = models.TimeField("Конец смены")
    days = models.CharField("Дни", max_length=120, help_text="Напр.: Пн-Пт")

    class Meta:
        verbose_name = "График"
        verbose_name_plural = "Графики"

    def __str__(self) -> str:
        return f"{self.name} ({self.days})"


class Employee(models.Model):
    first_name = models.CharField("Имя", max_length=80)
    last_name = models.CharField("Фамилия", max_length=80)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    position = models.ForeignKey(
        Position, verbose_name="Должность", on_delete=models.PROTECT, related_name="employees"
    )
    schedule = models.ForeignKey(
        WorkSchedule, verbose_name="График", on_delete=models.PROTECT, related_name="employees"
    )
    salary = models.DecimalField("Оклад", max_digits=10, decimal_places=2)
    hire_date = models.DateField("Дата приёма")
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class Payroll(models.Model):
    employee = models.ForeignKey(
        Employee, verbose_name="Сотрудник", on_delete=models.CASCADE, related_name="payrolls"
    )
    period_start = models.DateField("Начало периода")
    period_end = models.DateField("Конец периода")
    gross_pay = models.DecimalField("Начисления", max_digits=10, decimal_places=2)
    bonus = models.DecimalField("Бонус", max_digits=10, decimal_places=2, default=0)
    paid_on = models.DateField("Дата выплаты", auto_now_add=True)
    notes = models.CharField("Комментарий", max_length=200, blank=True)

    class Meta:
        verbose_name = "Выплата"
        verbose_name_plural = "Выплаты"
        ordering = ["-paid_on"]

    @property
    def total_pay(self):
        return self.gross_pay + self.bonus

    def __str__(self) -> str:
        return f"Выплата {self.employee} {self.period_end}"

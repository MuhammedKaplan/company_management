from .notification import create_notification


def deduct_leave_for_lateness(employee, late_minutes):
    minutes_per_day = 600  # TODO: Calculate this based on start and end time of the company from settings
    leave_deduction = late_minutes / minutes_per_day

    employee.remaining_leaves = max(0, employee.remaining_leaves - leave_deduction)
    employee.save()

    if employee.remaining_leaves < 3:  # TODO: Move this to settings
        message = f'{employee.user.username} has {employee.remaining_leaves} days of leave remaining.'
        create_notification(message, role='MANAGER')

    return leave_deduction

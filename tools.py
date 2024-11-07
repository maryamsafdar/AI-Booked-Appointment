from langchain_core.tools import tool
import datetime

# List to store appointments
APPOINTMENTS = []

@tool
def get_next_available_appointment():
    """Returns the next available appointment time."""
    current_time = datetime.datetime.now()
    next_slot = current_time + datetime.timedelta(minutes=(30 - current_time.minute % 30))
    return f"Next available appointment is at {next_slot.strftime('%Y-%m-%d %H:%M')}."

@tool
def book_appointment(appointment_year: int, appointment_month: int, appointment_day: int, appointment_hour: int, appointment_minute: int, appointment_name: str):
    """Book an appointment at a specific time."""
    time = datetime.datetime(appointment_year, appointment_month, appointment_day, appointment_hour, appointment_minute)
    for appointment in APPOINTMENTS:
        if appointment["time"] == time:
            return f"Appointment at {time} is already booked."
    APPOINTMENTS.append({"time": time, "name": appointment_name})
    return f"Appointment booked for {time}."

@tool
def cancel_appointment(appointment_year: int, appointment_month: int, appointment_day: int, appointment_hour: int, appointment_minute: int):
    """Cancel an appointment at a specific time."""
    time = datetime.datetime(appointment_year, appointment_month, appointment_day, appointment_hour, appointment_minute)
    for appointment in APPOINTMENTS:
        if appointment["time"] == time:
            APPOINTMENTS.remove(appointment)
            return f"Appointment at {time} cancelled."
    return f"No appointment found at {time}."

# import streamlit as st
# from datetime import datetime
# from tools import book_appointment, get_next_available_appointment, cancel_appointment
# from caller_agent import receive_message, CONVERSATION

# # Initialize appointment data and conversation history
# APPOINTMENTS = []

# # Streamlit App Layout
# st.set_page_config(layout="wide")
# st.title("AI-Powered Appointment Manager")

# # Define columns for layout
# col1, col2 = st.columns([2, 1])

# # Conversation Section
# with col1:
#     st.header("Chat with Assistant")

#     # Display conversation
#     for message in CONVERSATION:
#         if message.type == "human":
#             st.write(f"**User:** {message.content}")
#         else:
#             st.write(f"**Assistant:** {message.content}")

#     # User input for chat
#     user_message = st.text_input("Type your message:")
#     if st.button("Send"):
#         if user_message:
#             receive_message(user_message)
#             st.experimental_rerun()

# # Appointment Section
# with col2:
#     st.header("Appointments")

#     # Show upcoming appointments
#     if APPOINTMENTS:
#         for appointment in APPOINTMENTS:
#             st.write(f"{appointment['time']} - {appointment['name']}")
#     else:
#         st.write("No appointments booked.")

#     # Book an appointment form
#     with st.form(key="appointment_form"):
#         st.subheader("Book Appointment")
#         name = st.text_input("Name")
#         date = st.date_input("Date")
#         time = st.time_input("Time")
        
#         if st.form_submit_button("Book Appointment"):
#             try:
#                 year, month, day = date.year, date.month, date.day
#                 hour, minute = time.hour, time.minute
#                 result = book_appointment(year, month, day, hour, minute, name)
#                 st.success(result)
#                 st.experimental_rerun()
#             except Exception as e:
#                 st.error(f"Error: {e}")

#     # Cancel an appointment form
#     with st.form(key="cancel_form"):
#         st.subheader("Cancel Appointment")
#         cancel_date = st.date_input("Date", key="cancel_date")
#         cancel_time = st.time_input("Time", key="cancel_time")

#         if st.form_submit_button("Cancel Appointment"):
#             try:
#                 year, month, day = cancel_date.year, cancel_date.month, cancel_date.day
#                 hour, minute = cancel_time.hour, cancel_time.minute
#                 result = cancel_appointment(year, month, day, hour, minute)
#                 st.warning(result)
#                 st.experimental_rerun()
#             except Exception as e:
#                 st.error(f"Error: {e}")

import streamlit as st
from langchain_core.messages import HumanMessage
from caller_agent import receive_message, CONVERSATION

# Streamlit Interface
st.title("AI Appointment Assistant")
st.write("This assistant can help you book, check, or cancel appointments. Type your message below.")

# Display conversation history
for message in CONVERSATION:
    if isinstance(message, HumanMessage):
        st.write(f"**User:** {message.content}")
    else:
        st.write(f"**Assistant:** {message.content}")

# User input
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input:
        # Send user input to the assistant and process response
        receive_message(user_input)
        st.experimental_rerun()  # Rerun to refresh the conversation display

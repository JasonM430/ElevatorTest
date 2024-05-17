import streamlit as st
import json
import os

# Define the path to the count file
COUNT_FILE_PATH = "elevator_counts.txt"

# Load counts from file
def load_counts():
    if not os.path.exists(COUNT_FILE_PATH):
        # Initialize the file if it doesn't exist
        with open(COUNT_FILE_PATH, 'w') as file:
            json.dump({"A": 0, "B": 0, "C": 0, "D": 0}, file)

    with open(COUNT_FILE_PATH, 'r') as file:
        return json.load(file)

# Save counts to file
def save_counts(counts):
    with open(COUNT_FILE_PATH, 'w') as file:
        json.dump(counts, file)

# Main function for the Streamlit app
def main():
    st.title("Elevator Status")

    # Load current counts
    counts = load_counts()

    # Initialize session state for counts
    for elevator in counts:
        if f"count_{elevator}" not in st.session_state:
            st.session_state[f"count_{elevator}"] = counts[elevator]

    # Function to update count
    def update_count(elevator):
        counts[elevator] += 1
        save_counts(counts)
        st.session_state[f"count_{elevator}"] = counts[elevator]

    # Display counts and buttons for each elevator
    for elevator in counts:
        st.write(f"Elevator {elevator}: {st.session_state[f'count_{elevator}']} other {('person' if st.session_state[f'count_{elevator}'] == 1 else 'people')} think the elevator is broken.")
        if st.button(f"Elevator {elevator} is broken", key=elevator):
            update_count(elevator)

if __name__ == "__main__":
    main()

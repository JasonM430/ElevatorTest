import streamlit as st
from streamlit_option_menu import option_menu
import json
import os
import random

COUNT_FILE_PATH = "elevator_counts.txt"
LINE_FILE_PATH = "elevator_line_counts.txt"

def load_counts():
    if not os.path.exists(COUNT_FILE_PATH):
        with open(COUNT_FILE_PATH, 'w') as file:
            json.dump({"A": 0, "B": 0, "C": 0, "D": 0}, file)
    with open(COUNT_FILE_PATH, 'r') as file:
        return json.load(file)

def load_line_counts():
    if not os.path.exists(LINE_FILE_PATH):
        with open(LINE_FILE_PATH, 'w') as file:
            json.dump({"A": 0, "B": 0, "C": 0, "D": 0}, file)
    with open(LINE_FILE_PATH, 'r') as file:
        return json.load(file)


def save_counts(counts):
    with open(COUNT_FILE_PATH, 'w') as file:
        json.dump(counts, file)

def save_line_counts(lines):
    with open(LINE_FILE_PATH, 'w') as file:
        json.dump(lines, file)


def main():
    with st.sidebar:
        selected = option_menu("BTHS Elevator Tracker", ["Home", "Elevator Status", "Elevator Line", "Waiting Game"], 
            icons=['house', 'gear', 'person', 'controller'], menu_icon="building", default_index=0)

    # Home Page
    if selected == "Home":
        st.title("Welcome to the BTHS Elevator Tracker")
        st.markdown("![Alt Text](https://i.pinimg.com/originals/06/ee/c5/06eec5cf477e745d92617bf473308323.gif)")

    #Elevator Status Page
    if selected == "Elevator Status":
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

        def decrement_count(elevator):
            if counts[elevator] > 0:
                counts[elevator] -= 1
                save_counts(counts)
                st.session_state[f"count_{elevator}"] = counts[elevator]

        def update_status(elevator):
            if counts[elevator] > 10:
                st.write(f"❌ Elevator **{elevator}** is likely **out of order**")
            else:
                st.write(f"✅ Elevator **{elevator}** is likely **in order**")

        def update_title_status(elevator):
            if counts[elevator] > 10:
                st.title("Elevator: " + elevator + " - Out of Order ❌")
            else:
                st.title("Elevator: " + elevator + " - is Working ✅")

        # Display counts and buttons for each elevator
        for elevator in counts:
            update_title_status(elevator)
            st.write(f"Elevator {elevator}: {st.session_state[f'count_{elevator}']} other {('person' if st.session_state[f'count_{elevator}'] == 1 else 'people')} think the elevator is broken.")
            if st.button(f"Elevator {elevator} is broken", key=f"broken_{elevator}"):
                update_count(elevator)
            if st.button(f"Elevator {elevator} is working", key=f"working_{elevator}"):
                decrement_count(elevator)
            update_status(elevator)

    #Elevator Line Page
    elif selected == "Elevator Line":
        st.title("Elevator Line")
        st.write("These are the approximate line lengths for all the elevators")

        lines = load_line_counts()
        for elevator in lines:
            if f"line_{elevator}" not in st.session_state:
                st.session_state[f"line_{elevator}"] = lines[elevator]

        def update_line(elevator, length):
            lines[elevator] = length
            save_line_counts(lines)
            st.session_state[f"line_{elevator}"] = lines[elevator]

        for elevator in lines:
            st.write(f"Elevator {elevator}: Line length is {st.session_state[f'line_{elevator}']}")

        if st.checkbox("I want to add my approximate amount of people in line for an elevator"):
            elevator = st.selectbox("Please select the elevator you want to add to", ["A", "B", "C", "D"], key="select_elevator")
            line_length = st.selectbox("Please enter the accurate approximation of the elevator line.", ["Short: (~0 - 10)", "Medium: (11-30)", "Long: (31-60)", "Very Long: (60+)"], key="select_line_length")

            length_map = {"Short: (~0 - 10)": 10, "Medium: (11-30)": 30, "Long: (31-60)": 60, "Very Long: (60+)": 100}
            if st.button("Submit", key="submit_line"):
                update_line(elevator, length_map[line_length])
                st.success(f"Line length for Elevator {elevator} updated.")
    
    
    elif selected == "Waiting Game":
        st.title("Waiting Game")
        st.write("Are you bored out of your mind? Here's a little game you can play.")

        # Initialize game state
        if 'floor' not in st.session_state:
          st.session_state.floor = 0
        if 'game_over' not in st.session_state:
          st.session_state.game_over = False
        if 'message' not in st.session_state:
          st.session_state.message = "Welcome to Elevator Adventure! Start your journey by pressing the button below."
        if 'inventory' not in st.session_state:
          st.session_state.inventory = []
        if 'health' not in st.session_state:
          st.session_state.health = 100
        if 'attack' not in st.session_state:
              st.session_state.attack = 0
        if 'defense' not in st.session_state:
              st.session_state.defense = 0
        if 'curse' not in st.session_state:
              st.session_state.curse = 0
        if 'event' not in st.session_state:
          st.session_state.event = None

        def next_floor():
          if st.session_state.game_over:
            return

          st.session_state.floor += 1
          event = random.choice(['nothing', 'item', 'item', "item", 'fight', 'fight', 'fight', 'boss_fight', 'trap', 'trap'])
          st.session_state.event = event

          if event == 'nothing':
            st.session_state.message = f"Floor {st.session_state.floor}: Nothing happens."
          elif event == 'item':
            item = random.choice(['Sword', 'Shield', 'Health Potion', 'Curse Potion'])
            st.session_state.message = f"Floor {st.session_state.floor}: You found a {item}!"
            st.session_state.inventory.append(item)
          elif event == 'fight':
            st.session_state.message = f"Floor {st.session_state.floor}: A wild animal appears! Prepare to fight!"
          elif event == 'boss_fight':
            if st.session_state.floor > 10:
                st.session_state.message = f"Floor {st.session_state.floor}: An unrestrained mythical dragon appears- it doesn't seem to be happy! Prepare to fight!!"
            else:
                st.session_state.message = f"Floor {st.session_state.floor}: A restrained beast attempts to break its chains."
          elif event == 'trap':
            if(st.session_state.defense > 0):
                st.session_state.message = f"Floor {st.session_state.floor}: Your shield protected you from the triggered trap."
                num = random.randint(1, 4)
                if(num == 1):
                    st.session_state.message = "Your shield has broken!"
                    st.session_state.defense -= 1
            else:
                damage = random.randint(5, 10)
                st.session_state.health -= damage
                st.session_state.message = f"Floor {st.session_state.floor}: You triggered a trap and lost {damage} health."

          if st.session_state.health <= 0:
            st.session_state.message = "You have died. Game over."
            st.session_state.game_over = True
          st.session_state.health -= st.session_state.curse
          if st.session_state.curse > 0:
            st.write("You lost " + str(st.session_state.curse) + " health from the curse!")
        

        def fight():
          if st.session_state.attack > 0:
                num = random.randint(st.session_state.attack, 10)
                if num == 1 or num == 2 or num == 3 or num == 4 or num == 5 or num == 6 or num == 7 or num == 8:
                    st.session_state.message = "You were unable to fight off the animal with your sword! You lost " + str(10 - num) + " health!"
                else:
                    st.session_state.message = "You fought off the animal with your sword!"
                    
          else:
            damage = random.randint(10, 30)
            st.session_state.health -= damage
            st.session_state.message = f"You fought the wild animal but lost {damage} health."

          if st.session_state.health <= 0:
            st.session_state.message = "You have died. Game over."
            st.session_state.game_over = True
              
        def d_fight():
              if st.session_state.attack > 0:
                    num = random.randint(st.session_state.attack, 20)
                    if num == 1 or num == 2 or num == 3 or num == 4 or num == 5 or num == 6 or num == 7 or num == 8:
                        st.session_state.message = "You were unable to fight off the dragon with your sword! You lost " + str(20 - num) + " health!"
                    else:
                        st.session_state.message = "You fought off the dragon with your sword!"

              else:
                damage = random.randint(10, 30)
                st.session_state.health -= damage
                st.session_state.message = f"You fought the dragon but lost {damage} health."

              if st.session_state.health <= 0:
                st.session_state.message = "You have died. Game over."
                st.session_state.game_over = True

        def use_item(item):
            if item == 'Health Potion':
                st.session_state.health += 20
                st.session_state.inventory.remove(item)
                st.session_state.message = "You used a Health Potion and gained 20 health."
            if item == 'Sword':
                st.session_state.attack += 1
                st.session_state.inventory.remove(item)
                st.session_state.message = "You have equiped the sword in case of another animal attack"
            if item == 'Shield':
                st.session_state.defense += 1
                st.session_state.inventory.remove(item)
                st.session_state.message = "You have equiped the shield to protect against traps"
            if item == 'Curse Potion':
                if st.session_state.curse >= 2:
                    st.session_state.curse -= 2
                else:
                    st.session_state.curse = 0
                st.session_state.inventory.remove(item)
                st.session_state.message = "You drank the curse potion to remove 2 curses"

          # Additional items can have other effects here
          # Update the message and other game states accordingly

        st.title("Elevator Adventure")
        st.write(st.session_state.message)
        st.write(f"Current Health: {st.session_state.health}")
        st.write(f"Current Floor: {st.session_state.floor}")
        st.write(f"Current Attack: {st.session_state.attack}")
        st.write(f"Current Defense: {st.session_state.defense}")
        st.write(f"Current Curse Level: {st.session_state.curse}")
        st.write(f"Inventory: {', '.join(st.session_state.inventory)}")

        if st.session_state.game_over:
          st.write("Game Over. Restart the game to play again.")
        else:
          if st.button("Go to next floor"):
            if st.session_state.event == 'fight' and "wild animal" in st.session_state.message:
              num = random.randint(1, 10)
              if num == 1:
                  st.write("[Cursed] You attempted to flee, but the wild animal has cast a curse on you.")
                  next_floor()
                  st.session_state.curse += 1
            if st.session_state.message == f"Floor {st.session_state.floor}: An unrestrained mythical dragon appears- it doesn't seem to be happy! Prepare to fight!!":
                  st.write("You tried to flee from a dragon... You got incinerated.")
                  st.session_state.gameover = True
                  st.session_state.message = "gg."
            else:
                next_floor()  

          # Display event message
          st.write(st.session_state.message)

          # Use buttons with unique keys for "Use Item" functionality
          for idx, item in enumerate(st.session_state.inventory):
              if st.button(f"Use {item}", key=f"use_item_{item}_{idx}"):
                  use_item(item)

          # Handle fight event with a separate button with a unique key
          if st.session_state.event == 'fight' and "wild animal" in st.session_state.message:
              st.button("Fight the wild animal", on_click=fight, key="fight_button")
          if st.session_state.event == 'boss_fight' and "mythical dragon" in st.session_state.message:
                st.button("Fight the dragon- or die running", on_click=d_fight, key="d_fight_button")


if __name__ == "__main__":
    main()


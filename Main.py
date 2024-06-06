import streamlit as st
from streamlit.elements.widgets.button import ButtonMixin
from streamlit.runtime.state import session_state_proxy
from streamlit_option_menu import option_menu
import json
import os
import random

COUNT_FILE_PATH = "elevator_counts.txt"
LINE_FILE_PATH = "elevator_line_counts.txt"


def load_counts():
    if not os.path.exists(COUNT_FILE_PATH):
        with open(COUNT_FILE_PATH, 'w') as file:
            json.dump({"A": 0, "B": 0, "C": 0, "D": 0}, file) #AI
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


with st.sidebar:
    selected = option_menu("BTHS Elevator Tracker", ["Home", "Elevator Status", "Elevator Line", "Waiting Game"], 
        icons=['house', 'gear', 'person', 'controller'], menu_icon="building", default_index=0)

if selected == "Home":
    st.title("Welcome to the BTHS Elevator Tracker")
    st.markdown("![Alt Text](https://i.pinimg.com/originals/06/ee/c5/06eec5cf477e745d92617bf473308323.gif)")

if selected == "Elevator Status":
    st.title("Elevator Status")
    counts = load_counts()

    for elevator in counts:
        if f"count_{elevator}" not in st.session_state:
            st.session_state[f"count_{elevator}"] = counts[elevator]
    
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
        if counts[elevator] >= 10:
            st.title("Elevator: " + elevator + " - is Likely Out of Order ❌")
        else:
            st.title("Elevator: " + elevator + " - is Likely Working ✅")

    for elevator in counts:
        update_title_status(elevator)
        st.write(f"Elevator {elevator}: {st.session_state[f'count_{elevator}']} other {('person' if st.session_state[f'count_{elevator}'] == 1 else 'people')} think the elevator is broken.") #AI
        if st.button(f"Elevator {elevator} is broken", key=f"broken_{elevator}"):
            update_count(elevator)
        if st.button(f"Elevator {elevator} is working", key=f"working_{elevator}"):
            decrement_count(elevator)
        # update_status(elevator)

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
            st.write(f"Elevator {elevator}: Line length is around {st.session_state[f'line_{elevator}']}")

        if st.checkbox("I want to add my approximate amount of people in line for an elevator"):
            elevator = st.selectbox("Please select the elevator you want to add to", ["A", "B", "C", "D"], key="select_elevator")
            line_length = st.selectbox("Please enter the accurate approximation of the elevator line.", ["Short: (~0 - 10)", "Medium: (11-30)", "Long: (31-60)", "Very Long: (60+)"], key="select_line_length")

            length_map = {"Short: (~0 - 10)": 5, "Medium: (11-30)": 20, "Long: (31-60)": 45, "Very Long: (60+)": 70}
            if st.button("Submit", key="submit_line"):
                update_line(elevator, length_map[line_length])
                st.success(f"Line length for Elevator {elevator} updated.")
                st.rerun()



elif selected == "Waiting Game":

    st.title("Waiting Game")
    st.write("Are you bored out of your mind waiting for an elevator? Here's a little game you can play.")

    if 'floor' not in st.session_state:
      st.session_state.floor = 1
    if 'game_over' not in st.session_state:
      st.session_state.game_over = False
    if 'message' not in st.session_state:
      st.session_state.message = "Are you ready to begin your elevator adventure?"
    if 'inventory' not in st.session_state:
      st.session_state.inventory = []
    if 'health' not in st.session_state:
      st.session_state.health = 100
    if 'attack' not in st.session_state:
          st.session_state.attack = 1
    if 'defense' not in st.session_state:
          st.session_state.defense = 1
    if 'curse' not in st.session_state:
          st.session_state.curse = 0
    if 'selected_attack' not in st.session_state:
          st.session_state.event = ""
    if 'event' not in st.session_state:
      st.session_state.event = None
    if 'button_clicked' not in st.session_state:
      st.session_state.button_clicked = False
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    if 'selected_answer' not in st.session_state:
        st.session_state.answer = None


    MAX_INVENTORY_SIZE = 5

    def next_floor():
      if st.session_state.game_over:
        return


      events = ['nothing', 'item', 'fight', 'boss_fight', 'boss_fight_v2', 'boss_fight_v3' , 'trap']
      probabilities = [0.1, 0.3, 0.25, 0.05, 0.05, 0.05, 0.2] 

      st.session_state.floor += 1
      event = random.choices(events, probabilities, k=1)[0]
      st.session_state.event = event



      if event == 'nothing':
        st.session_state.message = " Nothing happens."

        if len(st.session_state.inventory) < MAX_INVENTORY_SIZE:
              item_list = (['Sword', 'Katana', 'Golden Sword','Magical Sword', 'Shield', 'Magic Shield', 'Health Potion', 'Curse Potion', 'Gambler\'s Box'])
              probabilities = [0.25, 0.05, 0.03, 0.02, 0.25, 0.01 , 0.29, 0.1, 0.01] 

              item = random.choices(item_list, probabilities, k=1)[0]
              st.session_state.message = " You found a " + str(item) + "!"
              st.session_state.inventory.append(item)
        else:
              st.session_state.message = " You found an item, but your inventory is full!"

      elif event == 'fight':
        st.session_state.message = " A wild animal appears! Prepare to fight!"
      elif event == 'boss_fight':
        if st.session_state.floor > 50:
            st.session_state.message = "An unrestrained mythical dragon appears- it doesn't seem to be happy! Prepare to fight!!"
        else:
            st.session_state.message = " A restrained beast attempts to break its chains from a higher floor."
      elif event == 'boss_fight_v2':
        if st.session_state.floor > 100:
          st.session_state.message = " A mysterious figure has appeared. It seems powerful but you can't quite put your finger on its intentions."
        else:
            st.session_state.message = "A shadowy figure darts in front of you and then backs away."
      elif event == 'boss_fight_v3':
        if st.session_state.floor > 200: 
          st.session_state.message = " A giant stands before you. It seems pretty tanky. You can't kill it head-on. Find the weak spot high up by finding the attack button."
        else:
          st.session_state.message = "You hear a large sound from a higher floor."
      elif event == 'trap':
        if(st.session_state.defense > 0):
          st.session_state.message = " Your shield protected you from the triggered trap."
          num = random.randint(1, 3)
          if(num == 1):
              st.session_state.message = "Your shield has broken!"
              st.session_state.defense -= 1
        else:
            damage = random.randint(5, 10)
            st.session_state.health -= damage
            st.session_state.message = " You triggered a trap and lost " + str(damage) + " health."

      if st.session_state.health <= 0:
        st.session_state.message = "You have died. Game over."
        st.session_state.game_over = True
      st.session_state.health -= st.session_state.curse
      if st.session_state.curse > 0:
        st.write("You lost " + str(st.session_state.curse) + " health from the curse!")


    def fight():
      if st.session_state.attack > 0:
            if st.session_state.attack < 10:
                num = random.randint(1, 10)
                if num > st.session_state.attack:
                    if 10 - num == 0:
                        st.session_state.message = "You were barely able to fight off the animal. Luckily you lost no health."
                    else:
                        st.session_state.health -= (10-num)
                        st.session_state.message = "You were unable to fight off the animal with your sword! You lost " + str(10 - num) + " health!"
                else:
                    st.session_state.message = "You fought off the animal with your sword!"
            else:
                st.session_state.message = "You fought off the animal with your sword!"

      else:
        damage = random.randint(10, 30)
        st.session_state.health -= damage
        st.session_state.message = f"You fought the wild animal but lost " +  str(damage) + " health."

      if st.session_state.health <= 0:
        st.session_state.message = "You have died. Game over."
        st.session_state.game_over = True

    def d_fight():
          if st.session_state.attack > 0:
                if st.session_state.attack < 20:
                    num = random.randint(st.session_state.attack, 20)
                    if num == 1 or num == 2 or num == 3 or num == 4 or num == 5 or num == 6 or num == 7 or num == 8:
                        st.session_state.message = "You were unable to fight off the dragon with your sword! You lost " + str(20 - num) + " health!"
                    else:
                        st.session_state.message = "You fought off the dragon with your sword!"
                        st.session_state.inventory.append("Dragon Scale")
                else:
                    st.session_state.message = "You fought off the dragon with your sword!"

          else:
            damage = random.randint(10, 30)
            st.session_state.health -= damage
            st.session_state.message = f"You fought the dragon but lost " + str(damage) + " health."

          if st.session_state.health <= 0:
            st.session_state.message = "You have died. Game over."
            st.session_state.game_over = True

    def s_fight():
        if st.session_state.attack < 5:
            st.session_state.message = "Your attack is too low. It dodged your attack. You lost 40 health trying to hit it."
            st.session_state.health -= 40
        else:
            if st.session_state.attack < 50:
                num = random.randint(st.session_state.attack, 50)
                if num < 5:
                    st.session_state.message = "A lucky shot. You killed it. It dropped a weird sword."
                    st.session_state.inventory.append("Weird Sword")
                else:
                    st.session_state.message = "You slightly scratched it. It attacks back though. You lost 30 health."
                    st.session_state.health -= 30
            else:
                st.session_state.message = "That's odd. It seems to recognize your strength. It drains 5 of your attack but gives you a mysterious box."
                st.session_state.attack -= 5
                st.session_state.inventory.append("Gambler\'s Box")

    def submit_answer():
        st.session_state.answer_submitted = True
        
    def g_fight():
        st.write("The weak spot is here. Pick a move. Lower risk means lower chance of receiving an item drop.")
        choices = ["Run - Extreme Risk","Stab - Low Risk", "Slash - Medium Risk", "Barrage - High Risk"]
        selected_choice = st.selectbox("Choose one:", choices, key="selected_answer")
        if st.session_state.answer_submitted:
            if st.button("Submit Answer", on_click=submit_answer):
                st.session_state.answer = selected_choice
            if selected_choice == "Run - Extreme Risk":
                num = random.randint(1, 10)
                if num == 1:
                    st.session_state.message = "You lucked out. You successfully ran away from the giant."
                else:
                    st.session_state.health = 1
                    st.session_state.message = "You try to run away from the giant. It catches you and leaves you on the brink of death."
            if selected_choice == "Stab - Low Risk":
                st.session_state.message = "You stab the giant in its weakpoint and kill it."
            if selected_choice == "Slash - Medium Risk":
                st.session_state.message = "You slash the giant."
                num = random.randint(1, 10)
                if num > 5:
                    st.session_state.message = "It worked! You've killed the giant."
                    if num == 6 or num == 8:
                        st.session_state.inventory.append("Giant Armor")
                else:
                    st.session_state.health -= 20
                    st.session_state.message = "Your attack fatally wounds the giant. The giant angrily attacks back though. You lost 20 health."
            if selected_choice == "Barrage - High Risk":
                st.session_state.message = "You sword barrage the giant."
                num = random.randint(1, 10)
                if num == 1:
                    st.session_state.message = "You hit the giant with a barrage of your sword. It's dead."
                    st.session_state.inventory.append("Giant's Armor")
                    item = random.randint(1, 10)
                    if item > 5:
                        st.session_state.inventory.append("Giant's Tooth")
                        st.session_state.message = "You find a giant tooth lying in the remains."
                else:
                    st.session_state.health -= 50
                    st.session_state.message = "Your attack failed. The giant, enraged, attacks back before walking away. You lost 50 health."         
                

    def use_item(item):
        if item == 'Health Potion':
            st.session_state.health += 20
            st.session_state.inventory.remove(item)
            st.session_state.message = "You used a Health Potion and gained 20 health."
        if item == 'Sword':
            st.session_state.attack += 1
            st.session_state.inventory.remove(item)
            st.session_state.message = "You have equipped the sword in case of another animal attack"
        if item == 'Katana':
            st.session_state.attack += 5
            st.session_state.inventory.remove(item)
            st.session_state.message = "You found a Katana! That's pretty rare. You've equiped it."
        if item == 'Golden Sword':
            st.session_state.attack += 10
            st.session_state.inventory.remove(item)
            st.session_state.message = "A nice, shiny Golden Sword. You've equiped it."
        if item == 'Magical Sword':
            st.session_state.attack += 15
            st.session_state.inventory.remove(item)
            st.session_state.message = "Ooo Magical. You've equipped it."
        if item == 'Weird Sword':
            st.session_state.attack += 25
            st.session_state.inventory.remove(item)
            st.session_state.message = "What a weird sword. Pretty powerful though. You've equipped it."
        if item == 'Shield':
            st.session_state.defense += 1
            st.session_state.inventory.remove(item)
            st.session_state.message = "You have equiped the shield to protect against traps"
        if item == 'Magic Shield':
            st.session_state.defense += 5
            st.session_state.health += 50
            st.session_state.inventory.remove(item)
            st.session_state.message = "You've equipped the magical shield. It greatly boosts your health and defense."
        if item == 'Dragon Scale':
            st.session_state.attack += 5
            st.session_state.defense += 5
            st.session_state.inventory.remove(item)
            st.session_state.message = "The dragon scale increased your attack and defense!"
        if item == "Giant's Armor":
            st.session_state.defense += 20
            st.session_state.inventory.remove(item)
            st.session_state.curse += 1
            st.session_state.message = "You've equipped the giant armor. It greatly boosts your defense but its weight makes you lose health over time (curse)!."
        if item == "Giant's Tooth":
            st.session_state.attack += 30
            st.session_state.inventory.remove(item)
            st.session_state.curse += 1
            st.session_state.message = "Wow, what a large and sharp tooth. It seems like it can do some major damage, but the weight makes you lose health over time (curse)!"
        if item == 'Curse Potion':
            if st.session_state.curse >= 2:
                st.session_state.curse -= 2
            else:
                st.session_state.curse = 0
            st.session_state.inventory.remove(item)
            st.session_state.message = "You drank the curse potion to remove 2 curses"
        if item == 'Gambler\'s Box':
            st.session_state.message = "Gambling gambling gambling!!!!"
            st.session_state.inventory.remove(item)
            num = random.randint(1, 6)
            if num == 1:
                st.session_state.defense += 10
                st.session_state.message = "A defense buff. Nice."
            if num == 2:
                st.session_state.attack += 10
                st.session_state.message = "An attack buff. Nice."
            if num == 3:
                st.session_state.curse += 10
                st.session_state.message = "Uh oh. The box cursed you. Better search for some curse potions or use some stored potions!"
            if num == 4:
                st.session_state.health += 100
                st.session_state.message = "Nice health buff."
            if num == 5:
                st.session_state.inventory.append('Gambler\'s Blade')
                st.session_state.message = "You took the gamble and it paid off!"
            if num == 6:
                st.session_state.health = 1
                st.session_state.message = "The box's contents left you on the brink of death."
        if item == 'Gambler\'s Blade':
            st.session_state.attack += 100
            st.session_state.inventory.remove(item)
            st.session_state.message = "You gain 100 attack!"


    st.title("Elevator Adventure")
    st.write(st.session_state.message)
    st.write(f"Current **Health**: {st.session_state.health}")
    st.write(f"Current **Floor**: {st.session_state.floor}")
    st.write(f"Current **Attack**: {st.session_state.attack}")
    st.write(f"Current **Defense**: {st.session_state.defense}")
    st.write(f"Current **Curse Level**: {st.session_state.curse}")
    st.write(f"Inventory: {', '.join(st.session_state.inventory)}") #AI
    if st.session_state.message == " A giant stands before you. It seems pretty tanky. You can't kill it head-on. Find the weak spot high up by finding the attack button.":
        st.write(f"Test: {st.session_state.attack}")
    

    if st.session_state.game_over:
      st.write("Game Over. Restart the game to play again.")
    else:
      if st.button("Go to next floor"):
        if st.session_state.message == " A wild animal appears! Prepare to fight!":
          num = random.randint(1, 2)
          if num == 1:
              st.write("[Cursed] You attempted to flee, but the wild animal has cast a curse on you.")
              next_floor()
              st.session_state.curse += 1
        if st.session_state.message == "An unrestrained mythical dragon appears- it doesn't seem to be happy! Prepare to fight!!":
              st.write("You tried to flee from a dragon... You got incinerated.")
              st.session_state.game_over = True
              st.session_state.message = "gg."
        if st.session_state.message == " A mysterious figure has appeared. It seems powerful but you can't quite put your finger on its intentions.":
            num = random.randint(1, 2)
            if num == 1:   
                st.session_state.message = "The figure seems to appreciate your lack of violence. It gives you a health potion."
                st.session_state.inventory.append("Health Potion")
            else:
                st.session_state.message = "The figure chases you and attacks you. You lost 20 health."
                st.session_state.health -= 20
        else:
            next_floor()  

      st.write(st.session_state.message)

      for idx, item in enumerate(st.session_state.inventory):
          if st.button(f"Use {item}", key=f"use_item_{item}_{idx}"):
              use_item(item)

    
      if st.session_state.event == 'fight' and "wild animal" in st.session_state.message:
          st.button("Fight the wild animal", on_click=fight, key="fight_button")
      if st.session_state.event == 'boss_fight' and "mythical dragon" in st.session_state.message:
            st.button("Fight the dragon- or die running", on_click=d_fight, key="d_fight_button")
      if st.session_state.event == 'boss_fight_v2' and "mysterious figure" in st.session_state.message:
          st.button("Fight?", on_click=s_fight, key="s_fight_button")
      if st.session_state.event == 'boss_fight_v3' and "giant" in st.session_state.message:
        st.button("Fight.", on_click=g_fight, key="g_fight_button")
            

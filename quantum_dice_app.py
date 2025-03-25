import streamlit as st
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
import matplotlib.pyplot as plt
import numpy as np
import time


from Quantum_Dice_With_Luck_Bias.quantum_dice import QuantumDice



# Set page configuration
st.set_page_config(
    page_title="Quantum Dice Simulator",
    page_icon="🎲",
    layout="centered"
)

# Main app
st.title("🎲 Quantum Dice Simulator ⚛️")
st.write("Roll dice using real quantum mechanics with luck modifiers!")

# Initialize the dice simulator
@st.cache_resource
def get_dice():
    return QuantumDice()

dice = get_dice()

# Create two columns for the controls
col1, col2 = st.columns(2)

with col1:
    die_choice = st.selectbox("Choose a die type:", list(dice.dice_types.keys()))

with col2:
    luck = st.slider("Set your luck level (5 is neutral):", 
                     min_value=1, max_value=10, value=5,
                     help="Lower values bias toward lower numbers, higher values bias toward higher numbers")

# Roll button
if st.button("🎲 Roll the Quantum Dice 🎲", use_container_width=True):
    with st.spinner("Quantum circuits are calculating your roll..."):
        result = dice.roll_die(die_choice, luck)
    
    # Display the result with some styling
    st.markdown(f"## ⚛️ You rolled: {result} ⚛️")
    
    # Add some context based on the roll
    max_value = dice.dice_types[die_choice]
    if result == 1:
        st.error("Critical fail! The quantum realm was not kind to you.")
    elif result == max_value:
        st.success("Critical success! The quantum particles aligned perfectly!")
    elif result < max_value / 3:
        st.warning("Not great. Maybe adjust your luck next time?")
    elif result > max_value * 2/3:
        st.info("Nice high roll! The quantum probabilities favored you.")

# Visualization section
st.divider()
st.subheader("Visualize Luck Effects")
st.write("See how different luck values affect the probability distribution")

vis_die = st.selectbox("Die to visualize:", list(dice.dice_types.keys()), key="vis_die")
num_rolls = st.slider("Number of simulated rolls:", 100, 2000, 1000, 100)

if st.button("Generate Visualization", use_container_width=True):
    with st.spinner("Running quantum simulations..."):
        die_size = dice.dice_types[vis_die]
        luck_values = [1, 3, 5, 7, 10]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for luck in luck_values:
            results = []
            for _ in range(num_rolls):
                results.append(dice.roll_die(vis_die, luck))
            
            # Create histogram
            ax.hist(results, bins=range(1, die_size + 2), alpha=0.6, 
                   label=f"Luck = {luck}", density=True)
        
        ax.set_title(f"Effect of Luck on {vis_die} Rolls ({num_rolls} rolls per luck value)")
        ax.set_xlabel("Roll Result")
        ax.set_ylabel("Probability")
        ax.set_xticks(range(1, die_size + 1))
        ax.legend()
        ax.grid(alpha=0.3)
        
        st.pyplot(fig)
        
        st.info("Notice how higher luck values shift the probability toward higher numbers!")

# Add some information
st.divider()
st.write("### How it works")
st.write("""
This simulator uses quantum computing principles to generate truly random dice rolls. 
When luck is set to 5, it uses pure quantum randomness through superposition.
Other luck values introduce a controlled bias while still using quantum randomness as the base.
""")

st.write("Made with ❤️ and ⚛️ (quantum physics)")
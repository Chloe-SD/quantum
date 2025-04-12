#to run: streamlit run quantum_dice_app.py

import streamlit as st
import matplotlib.pyplot as plt



from Quantum_Dice_With_Luck_Bias.quantum_dice import QuantumDice



# Set page configuration
st.set_page_config(
    page_title="Quantum Dice Simulator",
    page_icon="🎲",
    layout="centered"
)

dice_images = {
    "d4": "images/d4.png",
    "d6": "images/d6.png",
    "d8": "images/d8.png",
    "d10": "images/d10.png",
    "d12": "images/d12.png",
    "d20": "images/d20.png",
    "d100": "images/d100.png"
}

# Main app
st.title("🎲 Quantum Dice Simulator ⚛️")
st.write("Roll dice using real quantum mechanics with luck modifiers!")
st.divider()

#=================================================================================================
# ================================ROLL SECTION====================================================
#=================================================================================================
st.subheader("🤞 Try your luck! 🎲")
# Initialize the dice simulator
@st.cache_resource
def get_dice():
    return QuantumDice()

dice = get_dice()

# Create two columns for the controls
col1, col2 = st.columns(2)
with col2:
    die_choice = st.selectbox("Choose a die:", list(dice.dice_types.keys()), index=5)

    luck = st.slider("Set your luck level (5 is neutral):", 
        min_value=1, max_value=10, value=5,
        help="Lower values bias toward lower numbers, higher values bias toward higher numbers")
    
with col1:
    st.image(dice_images[die_choice], width=150)

# Roll button
if st.button("🎲 Roll the Quantum Dice 🎲", use_container_width=True):
    with st.spinner("rolling..."):
        result = dice.roll_die(die_choice, luck)
    
    # Display the result with some styling
    st.markdown(f"## ⚛️ You rolled: {result} ⚛️")
    
    # Add some context based on the roll
    max_value = dice.dice_types[die_choice]
    if result == 1:
        st.error("Critical fail! The quantum realm was not kind to you.")
    elif result == max_value:
        st.success("Critical success! The quantum particles aligned perfectly!")


#=================================================================================================
# ==========================Visualization Section=================================================
#=================================================================================================

st.divider()
st.subheader("📉 Visualize Luck Effects 📈")
st.write("See how different luck values affect the probability distribution")

visCol1, visCol2 = st.columns(2)
with visCol2:
    vis_die = st.selectbox("Die to visualize:", list(dice.dice_types.keys()), key="vis_die", index=3)
    c3 = st.container(border=True)
    c3.write("This simulation takes some time, please be patient!")
    c3.write("More rolls == better visualization!")
    
with visCol1:
    st.image(dice_images[vis_die], width=150, caption=f"{vis_die}")
    

num_rolls = st.slider("Number of simulated rolls:", 100, 1000, 700, 100)

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
                   label=f"Luck = {luck}")
        
        ax.set_title(f"Effect of Luck on {vis_die} Rolls ({num_rolls} rolls per luck value)")
        ax.set_xlabel("Roll Result")
        ax.set_ylabel("NUmber of hits")
        ax.set_xticks(range(1, die_size + 1))
        ax.legend()
        ax.grid(alpha=0.3)
        
        st.pyplot(fig)
        
        st.info("Notice how higher luck values shift the probability toward higher numbers!")

#=================================================================================================
# ==============================ABOUT SECTION=====================================================
#=================================================================================================
st.divider()
st.subheader("⚛️ About the Simulator ⚛️")
t1, t2, t3 = st.tabs(["How it works", "Emerging Trends", "Impact & Ethics"])

with t1:
    st.write("### How it works")
    st.write("""
    This simulator uses quantum computing principles to generate truly random dice rolls. 
            
    When luck is set to 5, it uses pure quantum randomness through superposition.
    """)
    c = st.container(border=True)
    c.write("A Hadamard gate is applied to a qubit to turn a state of 0 or 1 into an equal superposition of both.")    
    c.image("images/hgateMatrix.png", width=500)
    c.markdown("[Source: IBM Quantum Documentation](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.HGate)")

    c.write("The qubit is then measured to collapse the superposition into a single classical bit (0 or 1).")


    st.write("""    
    Other luck values introduce a controlled bias while still using quantum randomness as the base.
            
    The bias (the luck slider) is applied via weights to the quantum probability distribution, Whereas each
    face of the die would have an equal probability of being rolled (a weight of 1), the bias shifts the weights
    to favor certain faces.
            
            unbiased d6 wights=[1,1,1,1,1,1]
            with luck 8=[0.7, 0.82, 0.94, 1.06, 1.18, 1.3]
    """)

    st.write("In a quantum environment, we would normally use a rotation gate to apply this bias, allowing us to adjust the superposition of states.")

    c2 = st.container(border=True)
    c2.write("A visual representation of a rotation gate applied to a qubit. We can see that applying a rotation to any axis of the qubit will influence the outcome in a biased direction.")
    c2.image("images/rotationExample.png", width=500)   
    c2.markdown("[Source: Rainer Kaltenbaek - ResearchGate](https://www.researchgate.net/figure/shows-measurement-results-for-single-qubit-rotations-of-the-logical-input-state-H-ie_fig4_45913144")

    st.write("For simplicity, we use a classical method to apply the bias in this simulator. with adjusted weights applied to the probability distribution.")

    st.write("### How is this different from classical random number generators?")
    st.write(" - Classical RNGs (Random Number Generators) are actually 'pseudo-random' in that they:")
    st.markdown(" - Use mathematical algorithms to generate numbers that appear random")
    st.markdown(" - Are determined by a 'seed' value, meaning the same input will always produce the same output")
    st.markdown(" - Can be predicted by skilled attackers who could guess future seed values")

    st.write("Quantum RNGs, on the other hand, use the inherent randomness of quantum mechanics to produce truly random and unpredictable numbers.")

    st.write("### How are you running quantum circuits on a normal computer?")
    st.write("The short answer is: I'm not!")
    st.write("The hardware of a quantum computer is very different from a classical computer, and would play a large role in the randomness of the circuit.")
    st.write("This app uses a quantum simulator, which is a classical computer that mimics the behavior of a quantum computer, using mathematical models to simulate quantum circuits.")
    st.write("This allows us to run quantum algorithms and circuits on a classical computer, but with some limitations.")
    st.write("""
             The results are not truly random, as its very difficult to get randomness from a classical computer, but they are still more random than a classical RNG. However this comes 
             at the cost of speed and complexity, as simulating quantum circuits on a classical computer is computationally expensive.
             """)

#=================================================================================================
# ==============================EMERGING TRENDS=====================================================
# =================================================================================================         

with t2:
    st.write("### Technical Emerging Trends")
    st.markdown("- Quantum Computing Simulations")
    st.write("""
    Quantum computing is an emerging field with the potential to revolutionize many industries, including gaming.     
    Projects like this allow developers to experiment with quantum concepts and algorithms in a more accessible way. This serves as a stepping stone for 
    future education and development in quantum computing.
    """)
    st.markdown("- AI-Assisted Development")
    st.write("""
    The development process for this project incorporated the assistance of AI, for help with ideas, code snippets, debugging, and optimization! Using AI as a collaborative
    tool can help developers to be more efficient and creative. Though it is important to note that developers should be able to read and understand any code or content 
    that ends up in their projects, as AI can produce incorrect or misleading information.
    """)

    st.write("### Non-Technical Emerging Trends")

#=================================================================================================
# ==============================IMPACT & ETHICS=====================================================
# =================================================================================================

with t3:
    st.write("### Impact & Ethics")
    st.write("""
    By introducing quantum concepts through familiar actions that we can all tangibly understand, like rolling dice,
    we can demystify the science in a fun a relatable way. 
             
    Tis simulation demonstrates how quantum phenomena can be harnessed for practical everyday applications, and understanding 
    these concepts will become necessary for future workforce preperation in many fields 
    """)

st.divider()
st.write("Made with ❤️ and ⚛️ (quantum physics)")

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


app_style = """
<style>
    /* Make buttons more attractive */
    .stButton button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    
    /* Tab styling - enhanced */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1c9404;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #007fff;
        color: white;
        box-shadow: 0 4px 12px rgba(0,123,255,0.2);
    }
    
    /* Divider styling - enhanced */
    hr {
        height: 3px !important;  /* Make the divider bolder */
        background: #1c9404 !important;  /* Neon green color */
        border: none !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 0 8px #39FF14 !important;  /* Add a neon glow effect */
    }
    
</style>
"""
st.markdown(app_style, unsafe_allow_html=True)

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
col1, col2 = st.columns([1, 2])
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

visCol1, visCol2 = st.columns([1, 2])
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
st.markdown("## ⚛️ About the Simulator ⚛️")
st.markdown("**Explore these tabs to learn more:**")

# Add custom CSS to make tabs more prominent
# tab_style = """
# <style>
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 10px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         background-color: #1c9404;
#         border-radius: 5px;
#         padding: 10px 20px;
#         font-weight: bold;
#     }
#     .stTabs [aria-selected="true"] {
#         background-color: #007fff;
#         color: white;
#     }
# </style>
#"""
st.markdown(app_style, unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🔍 How it works", "🚀 Emerging Trends", "💡 Impact & Ethics"])

with t1:
    st.write("### 🎲 How it works")
    
    # Introduction
    st.write("""
    This simulator uses quantum computing principles to generate truly random dice rolls. The randomness comes
    from quantum superposition, with luck modifiers introducing controlled bias.
    """)
    
    # Quantum Randomness Section
    st.subheader("⚛️ Quantum Randomness")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        When luck is set to 5 (neutral), the simulator uses pure quantum randomness:
        - A Hadamard gate creates an equal superposition of 0 and 1 states
        - Measuring the qubit collapses this superposition into a classical bit
        - This process creates true randomness unlike classical random generators
        """)
    
    with col2:
        st.image("images/hgateMatrix.png", width=200, caption="Hadamard Gate Matrix")
        st.caption("[Source: IBM Quantum Documentation](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.HGate)")
    
    # Add a fun fact
    st.success("""
    **Fun Fact:** The measurement problem in quantum mechanics suggests that particles exist in multiple states 
    simultaneously (superposition) until they're observed. This is both the source of quantum randomness and 
    the inspiration for Schrödinger's famous cat thought experiment! 🐱
    """)

    # Luck Bias Section
    st.subheader("🍀 Luck Bias Mechanism")
    
    st.write("""
    Other luck values introduce a controlled bias while preserving quantum randomness:
    - The luck slider adjusts weights in the probability distribution
    - Higher luck values shift probability toward higher numbers
    - Example for d6:
    - Neutral luck (5): [1, 1, 1, 1, 1, 1]
    - High luck (8): [0.7, 0.82, 0.94, 1.06, 1.18, 1.3]
    """)
        
    st.image("images/rotationExample.png", width=350, caption="Qubit Rotation")
    st.caption("[Source: Rainer Kaltenbaek - ResearchGate](https://www.researchgate.net/figure/)")
    st.write("In a true quantum computer, rotation gates would apply this bias by adjusting the superposition states.")

    # Comparison Section
    st.subheader("🎯 Quantum vs Classical Randomness")
    
    col5, col6 = st.columns([1, 1])
    
    with col5:
        st.markdown("#### 💻 Classical RNGs")
        st.markdown("""
        - Use mathematical algorithms
        - Deterministic (same seed = same output)
        - Predictable patterns
        - Vulnerable to skilled attackers
        """)
    
    with col6:
        st.markdown("#### ⚛️ Quantum RNGs")
        st.markdown("""
        - Use inherent quantum uncertainty
        - Truly random outcomes
        - No predictable patterns
        - Statistically superior randomness
        """)
    
    # Implementation Note
    st.info("""
    **Note:** This app uses a quantum simulator (not actual quantum hardware) to mimic quantum behavior. 
    While more random than classical methods, it still runs on classical hardware with some limitations in 
    true randomness and performance.
    """)
    
    

#=================================================================================================
# ==============================EMERGING TRENDS=====================================================
# =================================================================================================         

with t2:
    st.subheader("🤖 Technical Emerging Trends")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **Quantum Computing Simulations**")
    with col2:
        st.write("""
        Quantum computing is an emerging field with the potential to revolutionize many industries, including gaming.     
        Projects like this allow developers to experiment with quantum concepts and algorithms in a more accessible way. This serves as a stepping stone for 
        future education and development in quantum computing.
        """)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **AI-Assisted Development**")
    with col2:
        st.write("""
        The development process for this project incorporated the assistance of AI, for help with ideas, code snippets, debugging, and optimization! Using AI as a collaborative
        tool can help developers to be more efficient and creative. Though it is important to note that developers should be able to read and understand any code or content 
        that ends up in their projects, as AI can produce incorrect or misleading information.
        """)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **Interactive Data Visualization**")
    with col2:
        st.write("""
        The project employs dynamic visualization techniques to make quantum concepts accessible and intuitive. Real-time visualization of probability distributions 
        helps bridge the gap between complex quantum theory and practical understanding.
        """)
    
    st.subheader("🧮 Non-Technical Emerging Trends")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **Gamification of Scientific Concepts**")
    with col2:
        st.write("""
        By transforming abstract quantum principles into an interactive dice-rolling application with luck modifiers, this project exemplifies the trend of using 
        game mechanics to increase engagement with complex scientific ideas.
        """)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **Open Source Scientific Tools**")
    with col2:
        st.write("""
        The project builds upon open-source quantum computing frameworks like Qiskit, reflecting the broader trend toward collaborative, 
        community-driven development of scientific tools and resources.
        """)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **Experiential Learning & Interactive Education**")
    with col2:
        st.write("""
        With a growing shift from passive to active learning experiences, especially for complex scientific concepts. 
        Interactive tools like this quantum dice simulator exemplify how abstract scientific principles can be experienced firsthand 
        rather than just read about. This learning trend makes advanced concepts more accessible and understandable to broader audiences.
        """)

#=================================================================================================
# ==============================IMPACT & ETHICS=====================================================
# =================================================================================================

with t3:
    # Societal Impact Section
    st.subheader("🌍 Societal Impact")
    st.write("""
    This quantum dice simulator contributes to scientific literacy by making quantum concepts tangible and interactive. 
    By demystifying quantum mechanics through a familiar context like dice rolling, it helps bridge the considerable gap 
    between quantum science and public understanding.
    """)
    
    st.write("""
    The project demonstrates how quantum phenomena can be harnessed for practical applications like random number 
    generation, potentially inspiring users to explore further applications of quantum computing. As quantum 
    technologies continue to develop, tools that build fundamental understanding will be crucial for workforce 
    preparation and public engagement with these emerging technologies.
    """)

    # Ethical Considerations Section
    st.subheader("⚖️ Ethical Considerations")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **Randomness in Sensitive Applications**")
    with col2:
        st.write("""
        True quantum random number generators are increasingly used in applications like cryptography, 
        gambling, and security systems. When developing tools that simulate quantum randomness, it's important 
        to be transparent about their limitations compared to hardware-based quantum RNGs.
        """)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **Computational Resource Usage**")
    with col2:
        st.write("""
        Quantum simulations can be computationally intensive. As these tools become more widespread, 
        developers should consider the energy and resource implications of running complex simulations at scale.
        """)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("- **Accessibility**")
    with col2:
        st.write("""
        Interactive educational tools should strive to be accessible to users with different abilities and 
        technical backgrounds. Ensuring that visualizations and interfaces accommodate diverse users helps 
        prevent creating new barriers to scientific understanding.
        """)

st.divider()
st.write("Made with ❤️ and ⚛️ (quantum physics)")

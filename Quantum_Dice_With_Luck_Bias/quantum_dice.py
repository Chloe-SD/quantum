from qiskit import QuantumCircuit
from qiskit.primitives import StateVectorSampler
import matplotlib.pyplot as plt
import numpy as np
import time

class QuantumDice:
    def __init__(self):
        """Initialize the quantum dice simulator"""
        # These will be the types of dice we can roll
        # Standard tabletop dice, with a d100 added in for fun
        self.sampler = StateVectorSampler()
        self.dice_types = {
            "d4": 4,
            "d6": 6,
            "d8": 8,
            "d10": 10,
            "d12": 12,
            "d20": 20,
            "d100": 100
        }
    
    def _calculate_bias(self, luck, die_size):
        """
        Calculate bias parameters based on luck (1-10)
        luck = 5 means no bias (50/50)
        luck < 5 biases toward lower numbers
        luck > 5 biases toward higher numbers
        """
        # Convert luck to a scale from -0.4 to 0.4 (0 is neutral)
        # This gives us a moderate range of bias without being too extreme
        # any higher of a bias gives us very skewed distributions, setting
        # probability of some faces almost to 0 if were not careful
        bias = (luck - 5) / 10
        
        # Create weights for each face value
        weights = np.ones(die_size)
        # ever face of the die starts with a probability of 1
        # Apply bias: positive bias increases probability of higher numbers
        for i in range(die_size):
            # Normalized position in the range (0 to 1)
            position = i / (die_size - 1)
            # Apply a bias that increases or decreases based on position of the face and luck modifier
            weights[i] += bias * (2 * position - 1)
            """
            Much needed example for this calculation:
            die_size = 6 / luck modifier = 8
            this gives a bias of 0.3
            initial face weights = [1, 1, 1, 1, 1, 1]
            weights[i] += bias * (2 * position - 1) = 0.3 * (2 * i/5 - 1)
            weights AFTER bias calculation = [0.7, 0.82, 0.94, 1.06, 1.18, 1.3]
            """
        
        # Ensure all weights are positive
        weights = np.maximum(weights, 0.1)
        
        # Normalize weights to sum to 1
        return weights / np.sum(weights)
    
    def roll_die(self, die_type="d20", luck=5):
        """
        Roll a quantum die with optional luck modifier
        
        Parameters:
        die_type (str): Type of die to roll (d4, d6, d8, d10, d12, d20, d100)
        luck (int): Luck modifier from 1-10, with 5 being neutral
            - Lower values bias toward lower numbers
            - Higher values bias toward higher numbers
        
        Returns:
        int: The result of the die roll
        """
        # Validate inputs
        if die_type not in self.dice_types:
            raise ValueError(f"Invalid die type. Choose from: {', '.join(self.dice_types.keys())}")
        
        if not 1 <= luck <= 10:
            raise ValueError("Luck must be between 1 and 10")
        
        die_size = self.dice_types[die_type]
        
        # For perfectly neutral luck (5), use the unbiased quantum RNG
        if luck == 5:
            return self._roll_unbiased(die_size)
        else:
            # Otherwise use the biased version
            return self._roll_biased(die_size, luck)
    
    def _roll_unbiased(self, die_size):
        """Roll an unbiased quantum die"""
        # Calculate bits needed
        num_bits = max(1, (die_size - 1).bit_length())
        
        while True:
            # Create circuit with required qubits
            qc = QuantumCircuit(num_bits, num_bits)
            
            # Apply Hadamard gates for pure 50/50 randomness
            for i in range(num_bits):
                qc.h(i)
                
            # Measure all qubits
            qc.measure(range(num_bits), range(num_bits))
            
            # Run the circuit
            job = self.sampler.run(qc, shots=1)
            result = job.result()
            
            # Get the result
            value = list(result.quasi_dists[0].keys())[0]
            
            # Ensure the value is in range for our die
            if 0 <= value < die_size:
                return value + 1  # +1 because dice start at 1, not 0
    
    def _roll_biased(self, die_size, luck):
        """Roll a quantum die with luck-based bias"""
        # Get probability weights based on luck
        weights = self._calculate_bias(luck, die_size)
        
        # We'll use the quantum RNG to generate a random number
        # and then use that to select from our weighted distribution
        random_value = self._roll_unbiased(1000) / 1000.0  # Random value between 0 and 1
        
        # Calculate cumulative probabilities
        cumulative = np.cumsum(weights)
        
        # Find where our random value falls in the cumulative distribution
        for i in range(die_size):
            if random_value <= cumulative[i]:
                return i + 1  # +1 because dice start at 1
        
        # Fallback (should never reach here)
        return die_size
    
    def visualize_bias(self, die_type="d20", num_rolls=1000):
        """
        Visualize how different luck values affect die rolls
        
        Parameters:
        die_type (str): Type of die to simulate
        num_rolls (int): Number of rolls to simulate for each luck value
        """
        if die_type not in self.dice_types:
            raise ValueError(f"Invalid die type. Choose from: {', '.join(self.dice_types.keys())}")
        
        die_size = self.dice_types[die_type]
        luck_values = [1, 3, 5, 7, 10]  # Selected luck values to display
        
        plt.figure(figsize=(12, 8))
        
        for luck in luck_values:
            results = []
            for _ in range(num_rolls):
                results.append(self.roll_die(die_type, luck))
            
            # Create histogram
            plt.hist(results, bins=range(1, die_size + 2), alpha=0.6, 
                     label=f"Luck = {luck}", density=True)
        
        plt.title(f"Effect of Luck on {die_type} Rolls ({num_rolls} rolls per luck value)")
        plt.xlabel("Roll Result")
        plt.ylabel("Probability")
        plt.xticks(range(1, die_size + 1))
        plt.legend()
        plt.grid(alpha=0.3)
        plt.show()

# Interactive test
if __name__ == "__main__":
    dice = QuantumDice()
    
    print("🎲 QUANTUM DICE SIMULATOR 🎲")
    print("Using real quantum mechanics to roll dice with luck modifiers!")
    print("\nAvailable dice:", ", ".join(dice.dice_types.keys()))
    
    while True:
        try:
            die_choice = input("\nChoose a die type (or 'q' to quit, 'v' to visualize): ").lower()
            
            if die_choice == 'q':
                print("Thanks for playing with quantum dice!")
                break
                
            elif die_choice == 'v':
                vis_die = input("Which die to visualize? ").lower()
                dice.visualize_bias(vis_die)
                continue
                
            luck = int(input("Enter your luck (1-10, 5 is neutral): "))
            
            print("\nRolling the quantum", die_choice, "...")
            # Add a slight delay for dramatic effect
            time.sleep(0.5)
            
            result = dice.roll_die(die_choice, luck)
            
            print(f"⚛️ You rolled: {result} ⚛️")
            
            # Offer to roll again
            again = input("\nRoll again? (y/n): ").lower()
            if again != 'y':
                print("Thanks for playing with quantum dice!")
                break
                
        except ValueError as e:
            print("Error:", e)
        except KeyboardInterrupt:
            print("\nThanks for playing with quantum dice!")
            break
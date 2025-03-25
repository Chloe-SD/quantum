from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
import matplotlib.pyplot as plt
import numpy as np

def generate_random_bits(num_bits): 
# pass in minimum number of bits needed to represent the range of numbers we want to generate (in binary)
# for example, if we want to generate numbers between 0 and 15, we need 4 bits to represent 16 numbers
# if we want to generate numbers between 0 and 100, we need 7 bits to represent 128 numbers
    """Generate random bits using quantum superposition and measurement"""
    # Create a quantum circuit with num_bits qubits
    qc = QuantumCircuit(num_bits, num_bits)
    
    # Place all qubits in superposition
    for i in range(num_bits):
        qc.h(i)  # Apply Hadamard gate - placing bits is superposition state between 0 and 1 equally.
    
    # At this point, all bit have equal probability of being measured as 0 or 1.
    # Measure all qubits
    qc.measure(range(num_bits), range(num_bits))
    
    # Execute the circuit using Sampler (This runs the created circuit on a quantum simulator)
    # This step forces the bit to collapse and "choose" a value (0 or 1) when measured.
    sampler = Sampler()
    job = sampler.run(qc, shots=1)
    result = job.result()
    
    # Get the binary outcome from quasi-distribution (format returned by the Sampler)
    # The quasi-distribution is a dictionary where the keys are the binary outcomes and the values are the probabilities.
    # basically this 'extracts' the binary outcome into a readable format for us
    binary_outcome = list(result.quasi_dists[0].keys())[0]
    return binary_outcome


def generate_random_number(min_val, max_val):
    """Generate a random number between min_val and max_val (inclusive)"""
    # Calculate how many bits we need (based on the range of numbers we want to generate)
    range_size = max_val - min_val + 1
    num_bits = max(4, range_size.bit_length())
    
    while True:
        # Generate random bits
        random_value = generate_random_bits(num_bits)
        
        # Check if it's in our desired range
        if min_val <= random_value <= max_val:
            return random_value

def visualize_distribution(min_val, max_val, samples):
    """Generate multiple random numbers and visualize their distribution"""
    results = []
    for _ in range(samples):
        results.append(generate_random_number(min_val, max_val))
    
    # Plot the distribution
    plt.figure(figsize=(10, 6))
    plt.hist(results, bins=max_val-min_val+1, range=(min_val-0.5, max_val+0.5), 
             alpha=0.7, color='blue', edgecolor='black')
    plt.title(f'Distribution of {samples} Quantum Random Numbers')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(range(min_val, max_val+1))
    plt.show()
    
    # Print some statistics
    print(f"Mean: {np.mean(results):.2f}")
    print(f"Standard Deviation: {np.std(results):.2f}")
    print(f"Min: {min(results)}")
    print(f"Max: {max(results)}")


# Demo: Generate a single random number
print("Generating a single quantum random number between 1 and 100...")
random_num = generate_random_number(1, 100)
print(f"Your quantum random number is: {random_num}")

# Demo: Visualize the distribution (optional)
print("\nGenerating 1000 random numbers between 1 and 6 (like rolling a quantum die)...")
visualize_distribution(1, 20, 1000)

# to run - python rng.py
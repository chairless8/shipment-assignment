import numpy as np
from scipy.optimize import linear_sum_assignment

# Function to calculate the suitability score (SS) between a driver and a destination.
def suitability_score(driver_name, address):
    vowels = "AEIOUaeiou"
    consonants = "BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz"
    
    # Count the vowels and consonants in the driver's name.
    num_vowels = sum(1 for char in driver_name if char in vowels)
    num_consonants = sum(1 for char in driver_name if char in consonants)
    
    # Calculate the base score depending on the length of the shipment's street name.
    street_name = address.split(',')[0]  # Extract the street name.
    if len(street_name) % 2 == 0:
        base_ss = num_vowels * 1.5
    else:
        base_ss = num_consonants
        
    # Increase the base score by 50% if the street name and driver's name share common factors.
    common_factors = [i for i in range(2, min(len(street_name), len(driver_name)) + 1) if len(street_name) % i == 0 and len(driver_name) % i == 0]
    if common_factors:
        base_ss *= 1.5
        
    return base_ss

# Read the list of drivers and addresses from the files.
with open("10-list-drivers (3).txt", "r") as f:
    drivers = f.read().splitlines()

with open("10-list-addresses (3).txt", "r") as f:
    addresses = f.read().splitlines()

# Create a cost matrix (negative since we want to maximize the SS).
cost_matrix = np.array([[-suitability_score(driver, address) for address in addresses] for driver in drivers])

# Use the Hungarian algorithm to find the optimal assignment.
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Display the optimal assignments and the total SS.
print("Optimal Assignments:")
total_ss = 0
for r, c in zip(row_ind, col_ind):
    ss = -cost_matrix[r][c]
    total_ss += ss
    print(f"{addresses[c]} : {drivers[r]} : {ss}")

print(f"Total SS: {total_ss}")

import numpy as np
from scipy.optimize import linear_sum_assignment

def calculate_suitability_score(address, driver):
    vowels = "aeiouAEIOU"
    consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    
    address_length = len(address)
    driver_length = len(driver)
    
    num_vowels = sum(1 for char in driver if char in vowels)
    num_consonants = sum(1 for char in driver if char in consonants)
    
    if address_length % 2 == 0:
        base_ss = num_vowels * 1.5
    else:
        base_ss = num_consonants
    
    for i in range(2, min(address_length, driver_length) + 1):
        if address_length % i == 0 and driver_length % i == 0:
            base_ss *= 1.5
            break
    
    return base_ss

def optimal_shipment_assignment(addresses, drivers):
    ss_matrix = [[calculate_suitability_score(address, driver) for driver in drivers] for address in addresses]
    
    max_ss = np.max(ss_matrix)
    cost_matrix = max_ss - np.array(ss_matrix)

    row_indices, col_indices = linear_sum_assignment(cost_matrix)
    
    optimal_assignments = [(addresses[i], drivers[j], ss_matrix[i][j]) for i, j in zip(row_indices, col_indices)]
    total_ss = sum(ss_matrix[i][j] for i, j in zip(row_indices, col_indices))
    
    return optimal_assignments, total_ss

if __name__ == "__main__":
    with open("10-list-drivers (3).txt", "r") as f:
        drivers = f.read().splitlines()

    with open("10-list-addresses (3).txt", "r") as f:
        addresses = f.read().splitlines()

    assignments, total_ss = optimal_shipment_assignment(addresses, drivers)
    
    print("Optimal Assignments:")
    for address, driver, ss in assignments:
        print(f"{address} : {driver} : {ss}")
    print(f"Total SS: {total_ss}")

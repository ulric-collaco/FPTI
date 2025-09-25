import matplotlib.pyplot as plt

def compound_interest_simulator(principal, annual_rate, monthly_contribution, years):
    monthly_rate = annual_rate / 12 / 100  # convert percentage to decimal monthly rate
    months = years * 12
    balances = []
    balance = principal

    for month in range(1, months + 1):
        # Apply monthly interest
        balance = balance * (1 + monthly_rate)
        # Add monthly contribution
        balance += monthly_contribution

        # Store balance at the end of each year
        if month % 12 == 0:
            balances.append(balance)

    # Print year-wise table
    print("Year\tBalance")
    for year, bal in enumerate(balances, start=1):
        print(f"{year}\t{bal:,.2f}")

    # Plot growth curve
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, years + 1), balances, marker='o')
    plt.title('Compound Interest Simulator: Investment Growth Over Time')
    plt.xlabel('Year')
    plt.ylabel('Balance')
    plt.grid(True)
    plt.show()

# Example usage:
principal = 10000      # Initial investment
annual_rate = 6        # Annual interest rate in %
monthly_contribution = 200  # Monthly contribution amount
years = 20             # Investment duration in years

compound_interest_simulator(principal, annual_rate, monthly_contribution, years)
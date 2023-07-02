
annual_salary = float(input("Enter the starting salary: "))
total_cost = 1000000
semi_annual_raise = 0.07
portion_down_payment = 0.25
r = 0.04
number_of_months = 36

steps_in_bisection_search = 0
current_savings = 0
high = 10000
low = 0
possible = True

while(abs(current_savings - total_cost * portion_down_payment) > 100):

    portion_saved = (high + low) // 2
    current_savings = 0
    monthly_salary = annual_salary / 12
    steps_in_bisection_search += 1 
    for i in range(0, number_of_months):
        current_savings += current_savings * r / 12 + (portion_saved / 10000) * monthly_salary
        if((i) % 6 == 0):
            monthly_salary += monthly_salary * semi_annual_raise

    if (current_savings < total_cost * portion_down_payment):
        low = portion_saved
    else:
        high = portion_saved 

    if(high - low <= 1):
        possible = False
        break

if(possible):    
    print("Best savings rate: ", portion_saved / 10000)
    print("Steps in bisection search: ", steps_in_bisection_search)
else:
    print("It is not possible to pay the down payment in three years.")
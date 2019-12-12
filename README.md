### IS 590 Porgramming Analytics and Data Preprocessing - Final Project

## Project Title:
Profit/Loss Analysis of Surplus Hotel Room Reservations using Monte-Carlo Simulation

## Team Members:
Yasaswi Boyapati (Yasaswi08)
Zainab Aziz Zaveri (Zainabzav)

## Project Outline: 
- It is a very common trend in the hospitality industry to accept more bookings than available vacant rooms for a particular day of the year. 
- According to previous research and real-life examples, many hotels either make extra money off- no shows or account for the risk of loss experienced when guests cancel their reservations a few days ahead of arrival using surplus room booking. 
- Hotels also tend to make money due to cancellations as in many cases they do not refund the entire amount back to the customer.

Taking into account the type of booking, class of room booked, size of booking, date of booking, gap between booking date and date of stay, hotel compensation and other variables, we try to randomly simulate a hotel reservation system.

## Hypothesis to test:
- The higher the nummber of overbooked rooms, the higher the revenue generated by the hotel
- The higher the number of rooms cancelled, the higher the revenue generated by the hotel 

## Approach:
We used a monte-carlo simulation to find the optimal number of overbookings for a particular day which would give the hotel maximum revenue on that day. You can refer to the program flowchart [here](https://github.com/Zainabzav/final_projects/blob/master/project_workflow.png) to get a rough idea about the workflow of our project.

1. We first take in the follwing inputs from the user(modelled for hotel staff/managers):
![Alt text](https://github.com/Zainabzav/final_projects/blob/master/images/Screen%20Shot%202019-12-12%20at%2011.05.34%20AM.png?raw=true "Optional Title")

2. Based on the inputs we run our monte-carlo simulation which includes the following random distributions and probabilities:
   - Show-up probability: the probability of a guest who has made a reservation, to show up on the day on reservation.
   - Demand probability: the probability of demand of a hotel room on a particular date
   - Demand Hype: A poisson distribution which randomnly generates the number of rooms in demand 
     - For a special day/holiday: `demand_hyp = np.random.poisson(room_capacity * 1.5)` 
     - For a weekday when its a business hotel or a weekend when its a resort : `demand_hyp = np.random.poisson(room_capacity * 1.2)`
   - Number of rooms actually in demand : Based on the hype of rooms and their demand probability, we use a binomial distribution to generate the actual number of rooms that the guests reserve `numofrooms_demand = np.random.binomial(demand_hyp, probability_of_demand)`
   - Number of guests who make reservation and show-up : To calculate the number of guests who show up we use a binomial distribution where n = number of reservations made based on numofrooms_demand and p = probability of showing up `number_of_guests_showup = np.random.binomial(number_of_rooms_reserved, showup_prob)`
   - Number of guests who dont show-up: `number_of_guests_dont_showup = number_of_rooms_reserved - number_of_guests_showup`
   - Number of guests who cancel their reservations: Considering the range as 80% of the number of guests who don't show up, we use a random integer function to generate the cancelllation number `range_x = math.floor(number_of_guests_dont_showup*0.8), number_of_guests_cancel = np.random.randint(0,range_x)`
   
3. Next, we calculate the revenue keeping into consideration the number of people who we need to give a compensation to in-case the number of people who show-up is greater than the total capacity of the hotel

4. We generate mean profits earned by the hotel, associate it with the corresponding overbooking number and then take the optimum overbooking number when the mean profit is the highest throughout the simulation

5. Finally, we create three distinct plots to display our results

## Outputs

### Case 1: 
rooms = 100, date = 01-17-2019, Type= business
#### Input:
![Alt text](https://github.com/Zainabzav/final_projects/blob/master/images/Screen%20Shot%202019-12-12%20at%2011.05.34%20AM.png?raw=true "Optional Title")
#### Output:
##### Plot 1: 
Displays the plot of the revenues generated for each category of rooms vs the number of overbookings
![Alt text](https://github.com/Zainabzav/final_projects/blob/master/images/Screen%20Shot%202019-12-12%20at%2012.23.34%20PM.png?raw=true "Optional Title")
##### Plot 2:
Displays the plot of the total revenues vs the number of overbookings
![Alt text](https://github.com/Zainabzav/final_projects/blob/master/images/Screen%20Shot%202019-12-12%20at%2012.27.10%20PM.png?raw=true "Optional Title")
##### Plot 3:
Plot all the cancellation numbers and their corresponding total revenues
![Alt text](https://github.com/Zainabzav/final_projects/blob/master/images/Screen%20Shot%202019-12-12%20at%2012.29.29%20PM.png?raw=true "Optional Title")
##### Optimal overbooking number and maximum cancellations for this case:
![Alt text](https://github.com/Zainabzav/final_projects/blob/master/images/Screen%20Shot%202019-12-12%20at%2012.29.46%20PM.png?raw=true "Optional Title")



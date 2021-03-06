#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import math 
import statistics as st

# code used from https://www.geeksforgeeks.org/find-day-of-the-week-for-a-given-date/
def dayofweek(d, m, y):
    """
    The function tells us weather the given day of the year is a weekday or weekend.
    :param d: date of the day, str data type
    :param m: the month of the day given, str data type
    :param y: the year of the day, str data type
    :return the number from 0 to 7 for day of week

    >>> dayofweek(2, 1, 2019)
    3
    >>> dayofweek(13, 3, 2020)
    5
    """
    t = [0, 3, 2, 5, 0, 3,
         5, 1, 4, 6, 2, 4]
    y -= m < 3
    return ((y + int(y / 4) - int(y / 100)
             + int(y / 400) + t[m - 1] + d) % 7)

def datesplitfunction(holiday_boolean, date_of_booking_temp):
    """
    The functions does the action of removig the leading and trailing 0s in the date of booking from the month and the day portion of the date to calculate the day of booking
    
    :param holiday_boolean: has the boolean value of the booking day being holiday, boolean data type
    :param date_of_booking_temp: the date of the booking, str data type
    :return date_list: the list containing the day of booking and date of booking

    >>> datesplitfunction(True, '01-01-2019')
    You're booking on a public holiday! Since the hotel runs in high demand during this time, your customer will not get the full amount in refund_per_cancellation if they wish to cancel at anytime.
    ['1-1-2019', 2]
    >>> datesplitfunction(False, '01-17-2019')
    ['1-17-2019', 4]
    >>> datesplitfunction(False, '12-15-2019')
    ['12-15-2019', 0]
    """

    date_list = []
    if holiday_boolean:
        print(
            "You're booking on a public holiday! Since the hotel runs in high demand during this time, your customer "
            "will not get the full amount in refund_per_cancellation if they wish to cancel at anytime.")
    if date_of_booking_temp[3:4] == '0' and date_of_booking_temp[0:1] == '0':
        month_of_booking = date_of_booking_temp[1:2]
        day_of_booking = date_of_booking_temp[4:5]
        year_of_booking = date_of_booking_temp[-4:]
    elif date_of_booking_temp[3:4] == '0' and date_of_booking_temp[0:1] != '0':
        month_of_booking = date_of_booking_temp[0:2]
        day_of_booking = date_of_booking_temp[4:5]
        year_of_booking = date_of_booking_temp[-4:]
    elif date_of_booking_temp[3:4] != '0' and date_of_booking_temp[0:1] == '0':
        month_of_booking = date_of_booking_temp[1:2]
        day_of_booking = date_of_booking_temp[3:5]
        year_of_booking = date_of_booking_temp[-4:]
    else:
        month_of_booking = date_of_booking_temp[0:2]
        day_of_booking = date_of_booking_temp[3:5]
        year_of_booking = date_of_booking_temp[-4:]
    date_of_booking = month_of_booking + "-" + day_of_booking + "-" + year_of_booking
    list_date = date_of_booking.split("-")
    day_of_booking = dayofweek(int(list_date[1]), int(list_date[0]), int(list_date[2]))
    date_list = [date_of_booking, day_of_booking]
    return date_list

# code design inspired from https://github.com/Lavinialau/Airline-Overbooking and https://github.com/Xuefeng4/Monte-Carlo-Simulation-of-Airplane-Ticket-Overbooking/blob/master/simulation.ipynb. Basic code design is inspired from these links, but we have made substantial changes to the program logic to apply to the hotel scenario and consider more complex scenarios to account for more uncertanity in our project. 
class HotelRoom:
    """
    This is a object-oriented class. It stores the necessary information of hotel capacity, holiday boolean, capacities
    of each kind of room, cost of each kind of room, split by kind of room, date and day of booking and finally
    category of hotel.
    """
    holiday_list = ['01-01', '01-21', '02-18', '05-27', '07-04', '09-02', '10-14', '10-11', '11-28', '12-25', '12-31']

    def __init__(self, hotel_capacity_x, holiday_boolean, standard_capacity, deluxe_capacity, superior_capacity,
                 standard_cost, deluxe_cost, superior_cost, superior_split_percentage, deluxe_split_percentage,
                 standard_split_percentage, date_of_booking, day_of_booking, hotel_category):
        """
        Constructor method in our class. It assigns the attribute to an object everytime a new object is created. The attributes are mentioned below in parameters
        
        :param hotel_capacity_x: total capacity of the hotel, int
        :param holiday_boolean: true if the date of booking is a holiday, else false, boolean
        :param standard_capacity: number of standard rooms in the hotel, int
        :param deluxe_capacity: number of deluxe rooms in the hotel, int
        :param superior_capacity: number of deluxe rooms in the hotel, int
        :param standard_cost: cost of superior room, int
        :param deluxe_cost: cost of deluxe room, int
        :param superior_cost: cost of superior room, int
        :param superior_split_percentage: Percentage of standard rooms in total rooms, int
        :param deluxe_split_percentage: Percentage of deluxe rooms in total rooms, int
        :param standard_split_percentage:Percentage of superior rooms in total rooms, int
        :param date_of_booking: The date for which the booking is to be made, string
        :param day_of_booking: The day between 0-7 of the weekday corresponding to the date of booking, string
        :param hotel_category: if the hotel is a business or a vacation hotel type, string
        :returns None

        """
        self.hotel_capacity = hotel_capacity_x
        self.holiday_boolean = holiday_boolean
        self.standard_capacity = standard_capacity
        self.deluxe_capacity = deluxe_capacity
        self.superior_capacity = superior_capacity
        self.standard_cost = standard_cost
        self.deluxe_cost = deluxe_cost
        self.superior_cost = superior_cost
        self.superior_split_percentage = superior_split_percentage
        self.deluxe_split_percentage = deluxe_split_percentage
        self.standard_split_percentage = standard_split_percentage
        self.date_of_booking = date_of_booking
        self.day_of_booking = day_of_booking
        self.hotel_category = hotel_category

    @classmethod
    def attribute_collector(cls):
        """
        This class method passes the actual class object within the function call
        :return: class object, object
        
        """
        # present_date = time.strftime('%m-%d', time.localtime(time.time()))
        date_of_booking_temp = input("Enter the date you want to book (MM-DD-YYYY):")
        holiday_boolean = date_of_booking_temp[0:5] in HotelRoom.holiday_list
        date_list = datesplitfunction(holiday_boolean, date_of_booking_temp)
        date_of_booking = date_list[0]
        day_of_booking = date_list[1]
        satisfy = True
        while satisfy:
            print(
                'You will now be required to create your own hotel, please give required input as per the prompt. '
                'According to this program, you can create a hotel with 3 types of rooms (Standard|Deluxe|Superior). '
                'The system will ask you for the split of each category and room and their corresponding costs.')
            hotel_capacity_x = int(input('Enter the total number of rooms:'))
            superior_capacity = int(input("Enter the superior room split:"))
            superior_split_percentage = superior_capacity / hotel_capacity_x
            deluxe_capacity = int(input("Enter the deluxe room split:"))
            deluxe_split_percentage = deluxe_capacity / hotel_capacity_x
            standard_capacity = int(input("Enter the standard room split:"))
            standard_split_percentage = standard_capacity / hotel_capacity_x
            if hotel_capacity_x == (superior_capacity + deluxe_capacity + standard_capacity):
                satisfy = False
            else:
                print("The split isn't right. Please try again:")

        superior_cost = int(input("Enter the price of Superior room:"))
        deluxe_cost = int(input("Enter the price of deluxe room:"))
        standard_cost = int(input("Enter the standard room price:"))

        hotel_category = input("What is your hotel's type? Business/Vacation")

        return cls(hotel_capacity_x, holiday_boolean, standard_capacity, deluxe_capacity, superior_capacity,
                   standard_cost, deluxe_cost, superior_cost, superior_split_percentage,
                   deluxe_split_percentage, standard_split_percentage, date_of_booking, day_of_booking,
                   hotel_category)
    
def parameter_generator(demand_hyp, probability_of_demand, showup_prob, number_of_rooms_overbooked, capacity):
    """
    This function does the job of creating random variables like num of rooms_demand, number of guests showup and number
    of guests cancel. By using these we will calculate the number of rooms reserved on particular day.

    :param demand_hyp: the maximum overbooking percentage possible, int data type
    :param probability_of_demand: the probability of each person's ticket reservation, float data type
    :param showup_prob: the probability that persons shows-up on given day,float data type
    :param number_of_rooms_overbooked: the number of rooms that are overbooked,int data type
    :param capacity: the total rooms available in a hotel, int data type
    :return: number of rooms reserved, number of guests showup and number of guests cancel.

    >>> parameter_generator(83, 0.9, 0.85, 7, 200)[0] > 70
    True
    >>> parameter_generator(95, 0.8, 0.8, 10, 90)[1] < 60
    False
    """

    numofrooms_demand = np.random.binomial(demand_hyp, probability_of_demand)

    if numofrooms_demand >= capacity:
        number_of_rooms_reserved = capacity + number_of_rooms_overbooked
    else:
        number_of_rooms_reserved = numofrooms_demand

    number_of_guests_showup = np.random.binomial(number_of_rooms_reserved, showup_prob)
    number_of_guests_dont_showup = number_of_rooms_reserved - number_of_guests_showup

    if number_of_guests_dont_showup != 0:
        range_x = math.floor(number_of_guests_dont_showup*0.8)
        if range_x == 0:
            number_of_guests_cancel = np.random.randint(0,range_x+1)
        else:
            number_of_guests_cancel = np.random.randint(0,range_x)
    else:
        number_of_guests_cancel = number_of_guests_dont_showup

    return number_of_rooms_reserved, number_of_guests_showup, number_of_guests_cancel

def revenue_generator(number_of_rooms_reserved, hotel_capacity, number_of_guests_showup, profit,
                      number_of_guests_cancel, refund_per_cancellation, holiday_boolean, standard_cost, deluxe_cost,
                      superior_cost, room_category):
    """
    This function assists in calculating the total profits of the hotel.

    :param number_of_rooms_reserved : the count of final reservation done, int data type
    :param hotel_capacity: the number of rooms in hotel, int data type
    :param number_of_guests_showup: the number of customers that actually show up, int data type
    :param profit: the profit made on particular room, float data type
    :param number_of_guests_cancel: the count of customers that cancel the reservation, int data type
    :param refund_per_cancellation: the money hotel administration pays to those who cancel the reservation, int data type
    :param holiday_boolean: has boolean value of being a special day or not, boolean data type
    :param standard_cost: the cost of the standard kind of room, int data type
    :param deluxe_cost: the price of the deluxe type of room, int data type
    :param superior_cost: the amount paid for the superior variation of room, int data type
    :param room_category: the kind of room that is reserved, str data type
    :return: the profit that hotel makes, float data type

    >>> revenue_generator(105, 100, 103, 30, 1, 120, True, 100, 200, 300,'Standard')
    2640.0
    """

    loss_list = []

    if number_of_guests_showup <= hotel_capacity:
        revenue = profit * number_of_rooms_reserved - refund_per_cancellation * number_of_guests_cancel
    else:
        for i in range(number_of_guests_showup - hotel_capacity):
            if holiday_boolean:
                if room_category == 'Standard':
                    compensation_per_roomtype = standard_cost*1.3
                elif room_category == 'Deluxe':
                    compensation_per_roomtype = deluxe_cost*1.3
                else:
                    compensation_per_roomtype = superior_cost*1.3
            else:
                if room_category == 'Standard':
                    compensation_per_roomtype = standard_cost
                elif room_category == 'Deluxe':
                    compensation_per_roomtype = deluxe_cost 
                else:
                    compensation_per_roomtype = superior_cost 

            single_loss_list = compensation_per_roomtype
            loss_list.append(single_loss_list)
        revenue = profit * number_of_rooms_reserved - sum(loss_list) - refund_per_cancellation * number_of_guests_cancel
    return revenue

def Monte_Carlo(capacity, holiday_boolean, standard_cost, deluxe_cost, superior_cost, standard_capacity,
                deluxe_capacity, superior_capacity, superior_split_percentage, deluxe_split_percentage,
                standard_split_percentage):
    """
    Here we simulate the situation when overbook number is from 0 to 20% of capacity, and for each scenario,
    we simulate for 5000 times.

    :param capacity: the count of hotel capacity, int data type
    :param holiday_boolean: has boolean value of being a special day or not, boolean data type
    :param standard_cost: the cost of the standard kind of room, int data type
    :param deluxe_cost: the price of the deluxe type of room, int data type
    :param superior_cost: the amount paid for the superior variation of room, int data type
    :param standard_capacity: the number of standard rooms, int data type
    :param deluxe_capacity: the count id deluxe kind of rooms, int data type
    :param superior_capacity: the count for number of superior rooms, int data type
    :param superior_split_percentage: the percentage of superior rooms in hotel, float data type
    :param deluxe_split_percentage: the percentage of deluxe rooms in hotel, float data type
    :param standard_split_percentage: the percentage of standard rooms in hotel, float data type
    :return: the dictionary data type with the information of overbooked rooms count, standard overbooked count,
    deluxe overbooked count, superior overbooked count, standard rooms mean revenue, deluxe rooms mean revenue,
    superior rooms mean revenue, total mean revenue, max number of guests cancel, standard cancels, deluxe cancels,
    superior cancels, total refund for cancellations

    >>> len(Monte_Carlo(500, True, 100, 300, 500, 75, 150, 275, 0.15, 0.3, 0.55)['mean_revenues'])
    done
    100
    >>> len(Monte_Carlo(100, False, 90, 120, 150, 20, 30, 50, 0.2, 0.3, 0.5)['mean_revenues'])
    done
    20
    >>> len(Monte_Carlo(1000, False, 80, 110, 140, 250, 350, 400, 0.25, 0.35, 0.4)['cancel'])
    done
    200
    >>> len(Monte_Carlo(100, True, 90, 120, 150, 20, 30, 50, 0.2, 0.3, 0.5)['dict'])
    done
    20
    """
    result_of_montecarlo = {'mean_revenues': [], 'cancel': [], 'dict':[]}
    roomcategories = ["Standard", 'Deluxe', 'Superior']

    showup_prob = 0.9
    probability_of_demand = 0.95

    for i in range(0, int(capacity * 0.20)):
        list_of_totalrevenues = []
        
        can_sub_list = []
        
        standard_revenue, deluxe_revenue, superior_revenue = [], [], []
        list_of_cancellationnumbers = []
        for n in range(5000):
            
            list_of_cancellationnumbers_1 = []

            standard_overbooking = math.ceil(i * standard_split_percentage)
            deluxe_overbooking = math.floor(i * deluxe_split_percentage)
            superior_overbooking = i - standard_overbooking - deluxe_overbooking
            list_of_revenue = []
            for room_category in roomcategories:
                if room_category == "Standard":
                    profit = standard_cost * 0.30
                    capacity = standard_capacity
                    number_of_rooms_overbooked = standard_overbooking
                    if holiday_boolean:
                        demand_hyp = np.random.poisson(standard_capacity * 1.5)
                        refund_per_cancellation = standard_cost * 0.4
                    else:
                        demand_hyp = np.random.poisson(standard_capacity * 1.2)
                        refund_per_cancellation = standard_cost * 0.7
                elif room_category == 'Deluxe':
                    profit = deluxe_cost * 0.4
                    capacity = deluxe_capacity
                    number_of_rooms_overbooked = deluxe_overbooking
                    if holiday_boolean:
                        demand_hyp = np.random.poisson(deluxe_capacity * 1.5)
                        refund_per_cancellation = deluxe_cost * 0.4
                    else:
                        demand_hyp = np.random.poisson(deluxe_capacity * 1.2)
                        refund_per_cancellation = deluxe_cost * 0.7
                else:
                    profit = superior_cost * 0.5
                    capacity = superior_capacity
                    number_of_rooms_overbooked = superior_overbooking
                    if holiday_boolean:
                        demand_hyp = np.random.poisson(superior_capacity * 1.5)
                        refund_per_cancellation = superior_cost * 0.4
                    else:
                        demand_hyp = np.random.poisson(superior_capacity * 1.2)
                        refund_per_cancellation = superior_cost * 0.7

                parameters = parameter_generator(demand_hyp, probability_of_demand, showup_prob,
                                                 number_of_rooms_overbooked,
                                                 capacity)
                number_of_rooms_reserved = parameters[0]
                number_of_guests_showup = parameters[1]
                number_of_guests_cancel = parameters[2]

                list_of_cancellationnumbers.append(number_of_guests_cancel)
                list_of_cancellationnumbers_1.append(number_of_guests_cancel)
                revenue = revenue_generator(number_of_rooms_reserved, capacity, number_of_guests_showup, profit,
                                            number_of_guests_cancel, refund_per_cancellation, holiday_boolean,
                                            standard_cost, deluxe_cost, superior_cost, room_category)
                list_of_revenue.append(revenue)
            standard_revenue.append(list_of_revenue[0])
            deluxe_revenue.append(list_of_revenue[1])
            superior_revenue.append(list_of_revenue[2])
            total_revenue = sum(list_of_revenue)
            list_of_totalrevenues.append(total_revenue)
            
            can_sub_list.append(sum(list_of_cancellationnumbers_1))

        max_number_of_guests_cancel = max(list_of_cancellationnumbers)
        st_number_of_guests_cancel = int(max_number_of_guests_cancel * standard_split_percentage)
        del_number_of_guests_cancel = int(max_number_of_guests_cancel * deluxe_split_percentage)
        sup_number_of_guests_cancel = int(max_number_of_guests_cancel - st_number_of_guests_cancel - del_number_of_guests_cancel)
        standard_cancellation_refund = standard_cost * st_number_of_guests_cancel * 0.8
        deluxe_cancellation_refund = deluxe_cost * del_number_of_guests_cancel * 0.8
        superior_cancellation_refund = superior_cost * sup_number_of_guests_cancel * 0.8
        total_refund = standard_cancellation_refund + deluxe_cancellation_refund + superior_cancellation_refund

        mean_revenue = st.mean(list_of_totalrevenues)
        standard_mean_revenue = st.mean(standard_revenue)
        mean_revenue_del = st.mean(deluxe_revenue)
        superior_mean_revenue = st.mean(superior_revenue)
        percentage_change = mean_revenue - total_refund

        result_of_montecarlo['dict'].append((i, can_sub_list, list_of_totalrevenues))
        
        result_of_montecarlo['mean_revenues'].append((i, standard_overbooking, deluxe_overbooking, superior_overbooking,
                                                      standard_mean_revenue, mean_revenue_del, superior_mean_revenue,
                                                      mean_revenue))
        result_of_montecarlo['cancel'].append((max_number_of_guests_cancel, st_number_of_guests_cancel,
                                               del_number_of_guests_cancel, sup_number_of_guests_cancel, total_refund,
                                               percentage_change))

    print('done')
    return result_of_montecarlo


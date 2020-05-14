import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

monthDict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',6: 'Jun',
             7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

weekDayDict = {'1': 'Monday', '2': 'Tuesday', '3': 'Wednesday', '4': 'Thursday',
               '5': 'Friday', '6': 'Saturday', '7': 'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Please, enter a city to explore: (Chicago, New York City or Washington)').lower()
    while city not in CITY_DATA.keys():
        city = input('Please, enter a valid city to explore: (Chicago, New York City or Washington)').lower()
        if city in CITY_DATA.keys():
            break
    
    # Get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = eval(input('Please, enter a valid month to explore: "1 for January, 2 for February, ... ,12 for December"'))
            if month not in range(1,13):
                raise ValueError
            break
        except (ValueError, NameError):
            print("Oops! That was not a valid month. Read carefully! Try again...")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = eval(input('Please, enter a valid day to explore: "1 for Monday, 2 for Tuesday, ... , 7 for Sunday"'))
            if day not in range(1,8):
                raise ValueError
            break
        except (ValueError, NameError):
            print("Oops! That was not a valid day. Read carefully! Try again...")

    print('-'*40)
    
    # Detect if the city is Washington because this dataset is slightly different
    isWashington = True if city == 'washington' else False
    
    return city.replace(' ', '_'), month, day, isWashington


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read the city filtered
    city = city.replace(' ', '_')
    df = pd.read_csv('data/' + city + '.csv')
    
    # Convert dates to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y/%m/%d')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y/%m/%d')

    # Apply date filter
    df = df[(df['Start Time'].dt.month == month) & ((df['Start Time'].dt.dayofweek + 1) == day)]
    
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Start Time'].dt.month.mode()[0]
    print('The most common month of the year is {}.'.format(monthDict.get(most_common_month)))


    # Display the most common day of week
    most_common_day = str(df['Start Time'].dt.dayofweek.mode()[0])
    print('The most common day of the week is {}.'.format(weekDayDict.get(most_common_day)))

    # Display the most common start hour
    most_common_start_hour = str(df['Start Time'].dt.hour.mode()[0])
    print('The most common start hour is at {}.'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print('The most common start Station is "{}".'.format(most_common_start_station))

    # Display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print('The most common end Station is "{}".'.format(most_common_end_station))


    # Display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' - ' + df['End Station']
    most_common_station_combination = str(df['Station Combination'].mode()[0])
    print('The most common Station Combination is "{}".'.format(most_common_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('The total travel time has been: {}'.format(total_trip_duration))

    # Display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print('The mean travel time has been: {}'.format(round(mean_trip_duration,2)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df,isWashington):
    """
    Displays statistics on bikeshare users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df.groupby('User Type')['User Type'].count()
    print('The count of user types is: ')
    print(count_user_types)
    print('-'*40)

    if isWashington != True:
        # Display counts of gender
        count_gender = df.groupby('Gender')['Gender'].count()
        print('The count of gender is: ')
        print(count_gender)
        print('-'*40)

        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('The most earliest year is {}'.format(int(earliest_year)))

        recent_year = df['Birth Year'].max()
        print('The most recent year is {}'.format(int(recent_year)))

        common_year = df['Birth Year'].mode()[0]
        print('The most common year is {}'.format(int(common_year)))

        print('-'*40)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

        
def display_data(df):
    """
    Asks the user if wants to display raw data.
    """
    # Get user input for displaying raw data
    is_first_time = True
    count_plus_5 = 5
    message = 'Do you want to see{}raw data? (Enter 1 for "Yes" and 0 for "No")'
    while True:
        try:
            show_data = eval(input(message.format(' '))) if is_first_time else eval(input(message.format(' 5 more lines of ')))
            print(show_data)
            if show_data == 1:
                print(df.head(count_plus_5))
                count_plus_5 += 5
            elif show_data == 0:
                break
            else:
                raise ValueError
            print("-"*40,show_data)
        except (ValueError, NameError):
            print("Oops! That was not a 1 (yes) or a 0 (no). Read carefully, WTH? Try again...")
        finally:
            is_first_time = False if count_plus_5 > 5 else True
            
    print('-'*40)
    
    

def main():
    '''
    Main code snippet that call all the functionalities
    '''
    while True:
        city, month, day, isWashington = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,isWashington)
        
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes (y) or no(n).\n')
        if restart.lower() not in ['yes', 'y']:
            break


if __name__ == "__main__":
	main()
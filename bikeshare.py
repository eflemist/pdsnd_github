import time
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

FILTER = { 'filtertype': 'none' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
        
    If user specifies "Both" then a Month and Day of week must be supplied.
    If user specifies "None" then the value of "None" is returned for both month and day
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        
        city = input("Which City would you like to analyze (Chicago, New York City, Washington): ").lower()

        try:
            #print(city)
            if city not in ['chicago', 'new york city', 'washington']:
                raise ValueError('Please enter a valid city!!!')
        except ValueError as error:
            print(error)
            continue
        break
    
    while True:
        filter_type = input("Which would you like to filter on [Month, Day, Both, or None]: ").lower()
        
        try:
            if filter_type not in ['month', 'day', 'both', 'none']:
                raise ValueError('Please enter a valid filter type from list above!')
        except ValueError as error:
            print(error)
            continue
        break
    
    if filter_type == 'month':
        # get user input for month (all, january, february, ... , june)
        FILTER['filtertype'] = 'Month'
        while True:
            month = input("Which month? (Type out full month name: [January, February, March, April, May or June]) ").lower()
            day = 'All'
 
            try:
                if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                    raise ValueError('Please enter a valid month (and without abbreviations) !!!')
            except ValueError as error:
                print(error)
                continue
            break
    
    elif filter_type == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        FILTER['filtertype'] = 'Day'
        while True:
            day = input("Which day of week? (Type out full weekday name: [Monday, Tuesday, Wednesday, etc]) ").lower()
            month = 'None'
            
            try:
                if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    raise ValueError('Please enter a valid weekday (and without abbreviations) !!!')
            except ValueError as error:
                print(error)
                continue
            break
            
    elif filter_type == 'both':
        FILTER['filtertype'] = 'Both'
        while True:
            month = input("Which month? (Type out full month name: [January, February, March, April, May or June]) ").lower()
 
            try:
                if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                    raise ValueError('Please enter a valid month (and without abbreviations) !!!')
            except ValueError as error:
                print(error)
                continue
            break

        while True:
            day = input("Which day of week? (Type out full weekday name: [Monday, Tuesday, Wednesday, etc]) ").lower()

            try:
                if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    raise ValueError('Please enter a valid weekday (and without abbreviations) !!!')
            except ValueError as error:
                print(error)
                continue
            break
        
    else:
        FILTER['filtertype'] = 'None'
        month = 'None'
        day = 'None'

    print('-'*40)
    return city, month, day


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
    
    df = pd.read_csv(CITY_DATA[city])
    
    #convert start time to datetime datatype
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #create additional fields needed for calculating stats
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day Name'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    df['StatCombined'] = df['Start Station'] + '--' + df['End Station']
    
    #filter the data based on user selection criteria
    if FILTER['filtertype'] == 'Month':
        if month not in ['All','None']:
            df = df[df['Month']==month.title()]
            
    if FILTER['filtertype'] == 'Day':
        if day not in ['All','None']:
            df = df[df['Day Name']==day.title()]

    if FILTER['filtertype'] == 'Both':
        df = df[df['Month']==month.title()]
        df = df[df['Day Name']==day.title()]
         
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if FILTER['filtertype'] ==  'None':  # only show this stat if filter is None
        popular_month = df['Month'].mode()[0]
        print('Most common month is: ', popular_month)
    
    # display the most common day of week
    if FILTER['filtertype'] in  ['None', 'Month']: # only show this stat if filter is None of Month
        popular_day = df['Day Name'].mode()[0]
        print('Most common day is: ', popular_day)     


    # display the most common start hour

    popular_hour = df['Hour'].mode()[0]
    print('Most common hour is: ', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    popular_start_sta = df['Start Station'].mode()[0]
    print('Most common start station is: ', popular_start_sta)

    # display most commonly used end station

    popular_end_sta = df['End Station'].mode()[0]
    print('Most common end station is: ', popular_end_sta)

    # display most frequent combination of start station and end station trip

    df2 = df.groupby('StatCombined')['StatCombined'].count()
    trip_count = df2.max()
    mf_trip = df2.idxmax().split("--")
    mf_trip_start = mf_trip[0]
    mf_trip_end = mf_trip[1]

    print('Most common trip is {} to {}; it has been taking {} times' .format(mf_trip_start,mf_trip_end,trip_count)) 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Stats for Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration_sum = df['Trip Duration'].sum()
    print('Total Trip Duration is: ', trip_duration_sum)

    # display mean travel time
    trip_duration_mean = df['Trip Duration'].mean()
    print('Mean Trip Duration is: ', trip_duration_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users.
       Note the data for Washington does not contain any Gender or Birth Year data
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    df3 = df.groupby('User Type')['User Type'].count()
    print('User Counts are: ')
    for ind, val in df3.items():
        print(ind, ' - ',  val) 

    for key, value in CITY_DATA.items():
        #print(key, value)
        if key == 'washington' and city == 'washington':
           print('\nNo Gender and Birth Yr stats for Washington') 
        elif (key == 'chicago' and city == 'chicago') or (key == 'new york city' and city == 'new york city'):
    # Display counts of gender          
            df4 = df.groupby('Gender')['Gender'].count()
            print('\nGender Counts are: ')
            print(df4.index[0], ' - ', df4[0])
            print(df4.index[1], ' - ', df4[1])

    # Display earliest, most recent, and most common year of birth
            early_byear = popular_end_sta = df['Birth Year'].min()
            recent_byear = popular_end_sta = df['Birth Year'].max()
            most_byear = popular_end_sta = df['Birth Year'].mode()[0]    

            print('\nEarliest Birth Yr: ', str(int(early_byear)))
            print('Most Recent Birth Yr: ', str(int(recent_byear)))
            print('Most Common Birth Yr: ', str(int(most_byear)))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        
        view_data = input("Do you wish to continue? (yes or no): ").lower()

        if view_data != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        
        print('City is: ' + city + ' Month is: '+ month + ' Day is: ' + day + '\n')
        
        city = city.lower()
        df = load_data(city, month, day)
        #print(df.head())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june','all']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday','all' ]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        if city in CITY_DATA :
            break

    print('Looks like you want to hear about {}! If it is not true ,restart the programe now! \n'.format(city))


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month - January, February, March, April, May, June or by all ?\n').lower()
        if month in MONTHS:
            print('We will make sure to filter data by {}!\n '.format(month))
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or by all ?\n')
        if day in DAYS:
            print('We will make sure to filter data by {}!\n '.format(day))
            break

    print('Just one moment ... to loading the  data \n')
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

    # convert the Start Time column to datetime
    
    Time = pd.to_datetime(df['Start Time'])


    # extract month and day of week from Start Time to create new columns
    
    df['month'] =Time.dt.month
    
    df['day_of_week'] = Time.dt.day_name()
    
    df['hour'] = Time.dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month :', popular_month)

    # display the most common day of week
    popular_week = df['day_of_week'].mode()[0]
    print('Most Popular Start Week :', popular_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour :', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station :', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost Popular End Station :', popular_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df.groupby(['Start Station'])['End Station'].value_counts().idxmax()
    print("\nThe most commonly used start station and end station :\n",most_common_start_end_station)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_traval_time = df['Trip Duration'].sum()
    print("\nTotal travel time :",total_traval_time)

    # display mean travel time
    Average_traval_time = df['Trip Duration'].mean()
    print("\nAverage travel time :",Average_traval_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('\nThe count of User type is :\n',user_type)

   
    try:
        # Display counts of gender
        # Display earliest, most recent, and most common year of birth
        user_gander = df['Gender'].value_counts()
        popular_year = df['Birth Year'].value_counts().idxmax()
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()

        print('\nThe count of User Gander is :\n',user_gander)
        print('\nThe popular_year of birth is : ',popular_year)
        print('\nThe oldest is : ',earliest_year)
        print('\nThe youngest is : ',recent_year)

    except KeyError:
        print('The washington not have Gander and birthday data  ')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):

        yes = input('\nWould you like to examine the particular user trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break

        # retrieve and convert data to json format
        # split each json row data
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

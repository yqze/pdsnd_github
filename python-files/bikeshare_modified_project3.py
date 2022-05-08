import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_option = ['all','january', 'february','march','april','may','june' ]
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Choose a city from Chicago, New York City and Washington :')
    city = str(input ().lower())
    city_option = list(CITY_DATA.keys())
    city_option.append('all')
    while city not in city_option:
        print('Oops, it seems like that was not an option, let\'s try again')
        city = str(input().lower())
    else :
        if city != 'all':
            print('OK! Let\'s take a look at the data from ' + city + '!')
        else:
            print('OK! Let\'s take a look at the data from all three cities!')

    # get user input for month (all, january, february, ... , june)
    print('From the months January to June, please choose the month you would like to take a look at, or simply reply "all" to apply no month filter :')
    month = str(input ().lower())
    while month not in month_option:
        print('Oops, it seems like that was not an option, let\'s try again')
        month = str(input ().lower())
    else:
        if month != 'all':
            print ('OK! Let\'s take a look at the data from the month of ' + month +"!")
        else:
            print('OK! Let\'s take a look at the data from all available months!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Now please choose the day of week you would like to take a look at, or simply reply "all" to apply no filter :')
    day = str(input().lower())
    weekday_option = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    while day not in weekday_option:
        print ('Oops, it seems like that was not an option, let\'s try again')
        day = str(input().lower())
    else:
        if day !='all':
            print('OK! Let\'s take a look at the data from ' + day +'!')
        else:
            print ('OK! Let\'s take a look at the data from all available weekdays!')

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        month = month_option.index(month) + 2
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = month_option[(df['month'].mode()[0]) - 2].title()
    print('The Most Popular Month of Travel : ' + popular_month)
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The Most Popular day of Travel : ' + popular_day)
    # display the most common start hour
    popular_starthour = str(df['Start Time'].dt.hour.mode()[0])
    print('The Most Popular Start Hour of Travel :' + popular_starthour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The Most Popular Start Station: ' + popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The Most Popular End Station: ' + popular_end_station)

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] +' to ' + df['End Station']
    popular_combination = df['combination'].mode()[0]
    print('The Most Popular Combination of Start Station and End Station: ' + popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] =  (df['Trip Duration'].div(3600))
    trip_duration_total = str(round((df['Trip Duration'].sum(axis = 0)),2))
    print('The total travel time is ' + trip_duration_total + "hours.")

    # display mean travel time
    trip_duration_mean = str(round(df['Trip Duration'].mean(),2))
    print('The average travel time is ' + trip_duration_mean + 'hours.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('Below are the user types and associated counts: ')
    print(user_type_count)
    # Display counts of gender
    if 'Gender' in df:

        gender_count = df['Gender'].value_counts()
        print('\nBelow are the gender information and associated counts: \n')
        print(gender_count)
    else:
        print('\nThe gender information is not available for the selected city.\n')

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        earliest_year = str(int(df['Birth Year'].min()))
        most_recent = str(int(df['Birth Year'].max()))
        most_common = str(int(df['Birth Year'].mode()[0]))
        print('\nThe earliest year of birth from this user group is: ' + earliest_year)
        print('The most recent year of birth from this user group is: ' + most_recent)
        print('The most common year of birth from this user group is: ' + most_common)

    else:
        print('\nThe birth year information is not available for the selected city.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data_input(df):
    print('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n')
    view_data_input = input().lower()
    start_loc = 0
    while view_data_input == 'yes':
        print(df.iloc[start_loc: (start_loc + 5)])
        start_loc +=5
        print('\nWould you like to view more rows of individual trip data? Enter yes or no.\n')
        view_data_input = input().lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        view_data_input(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    while True:
        try:
            city = input('\nPlease type the desired city, \'Washington\', \'Chicago\' or \'New York City\' for relevant bikeshare information: ').lower()
            city_list = ['washington', 'chicago', 'new york city']
            if city in city_list:
                break
            else:
                print("*** Invalid input! Please choose from the provided options.  ***")
        except (ValueError):
            print('\nThat\'s not a valid city! Please input one of the indicated cities!')

    while True:
        try:
            option_filter = input('\nWoud you like to filter data by \'day\', \'month\' or \'all\': ').lower()
            option_list = ['day', 'month', 'all']
            if option_filter in option_list:
                break
            else:
                print("*** Invalid input! Please choose from the provided options.  ***")
        except ValueError:
            print('\nThat\'s not a valid filter type! Please input either \'day\', \'month\', \'none\'')

    # TO DO: get user input for month (all, january, february, ... , june)
    if option_filter == 'month':
         while True:
            try:
                month = input('\nPlease type the desired month, Jan, Feb, Mar, Apr, May or Jun: ').lower()
                month_list = ['jan', 'feb', 'mar', 'apr', 'may','jun']
                if month in month_list:
                    day = 'all'
                    break
                else:
                    print("*** Invalid input! Please choose from the provided options.  ***")
            except ValueError:
                print('\nThat\'s not a valid month! Please input either of the months indicated.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    elif option_filter == 'day':
        while True:
            try:
                day = input('\nPlease enter day of the week, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday: ').lower()
                day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday']
                if day in day_list:
                    month = 'all'
                    break
                else:
                    print("*** Invalid input! Please choose from the provided options.  ***")
            except ValueError:
                print('\nThat\'s not a valid day of the week! Please input either of the days indicated.')
    else:
        month = 'all'
        day = 'all'

    print('-'*60)
    return city, month, day, option_filter


def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns called month and day_of_week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
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

    # TO DO: display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most popular start month:', popular_month)

    # TO DO: display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('Most popular start day:', popular_day)

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_count = df['Start Station'].value_counts().idxmax()
    print('Most popular start station:',start_station_count)

    # TO DO: display most commonly used end station
    end_station_count = df['End Station'].value_counts().idxmax()
    print('Most popular end station:',end_station_count)

    # TO DO: display most frequent combination of start station and end station trip
    df["start_end_combo"] = df["Start Station"] + " || " + df["End Station"]
    start_end_combo_count = df['start_end_combo'].value_counts().idxmax()
    print('Most frequent combination of start station and end station trip:',start_end_combo_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:',total_travel_time)

    # TO DO: display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average travel time:',avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCounts of user types:\n',user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        count_gender = df['Gender'].value_counts()
        print('\nCounts of gender:\n',count_gender)
    else:
        print('\n*** Your selection of, \'' + city.upper() + '\' city, does not contain gender information! ***\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year:\n',earliest_birth_year)

        recent_birth_year = df['Birth Year'].max()
        print('\nMost recent birth year:\n',recent_birth_year)

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nMost common birth year:\n',most_common_birth_year)
    else:
        print('*** Your selection of, \'' + city.upper() + '\' city, does not contain birth year information! ***\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def df_stats(df, city, option_filter):
    df_index = 0
    df_index_column = 0
    while True:
        try:
            stats_option = input('\nWould you like to view sample data for your selection of, \'' + city.upper() + '\' city, and option of, \'' + option_filter.upper() + '\' filter? \nType \'Yes\' or \'No\': ').lower()
            stats_option_list = ['yes', 'no']
            if stats_option in stats_option_list:
                if stats_option == 'yes':
                   df_num_of_columns = len(df.columns)
                   df_num_of_rows = len(df.index)
                   while df_index_column < df_num_of_columns:
                        print(str(df.columns[df_index_column]) + ': \t' + str(df.iloc[df_index,df_index_column]))
                        df_index_column += 1
                   df_index += 1
                   df_index_column=0
                else:
                    break
            else:
                print("*** Invalid input! Please choose from the provided options. ***")
        except (ValueError):
            print('\nThat\'s not a valid option!')


def main():
    while True:
        city, month, day, option_filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        df_stats(df, city, option_filter)

        restart = input('\nWould you like to restart? \nType \'Yes\' or \'No\': ')
        if restart.lower() != 'yes':
            print('\n*** Good-bye! Thank\'s for exploring US bikeshare data! :) ***\n')
            break


if __name__ == "__main__":
	main()

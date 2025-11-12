"""
Bikeshare Data Exploration Script

This script provides an interactive command-line experience for exploring
US bikeshare data. It is designed to satisfy the rubric requirements for:
- Code quality (functions, loops, conditionals, packages, docstrings)
- Handling raw user input safely and interactively
- Computing descriptive statistics
- Displaying raw data in 5-row chunks on demand
"""

import time
import pandas as pd
import numpy as np

# Mapping between city names and their CSV files.
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Ask the user to specify a city, month, and day to analyze.

    Returns:
        (str, str, str): city, month, day
            city: one of "chicago", "new york city", "washington"
            month: one of "january", "february", ..., "june" or "all"
            day: one of "monday", "tuesday", ..., "sunday" or "all"
    """
    print("Hello! Let\'s explore some US bikeshare data!")

    # Get user input for city (with validation and case-insensitive handling)
    allowed_cities = list(CITY_DATA.keys())
    city = ""
    while True:
        city = input("\nPlease enter a city (Chicago, New York City, Washington): ").strip().lower()
        if city in allowed_cities:
            break
        else:
            print("Invalid city. Please choose from: Chicago, New York City, Washington.")

    # Get user input for month
    allowed_months = ["january", "february", "march", "april", "may", "june", "all"]
    month = ""
    while True:
        month = input("\nEnter month (January–June) or 'all' to apply no month filter: ").strip().lower()
        if month in allowed_months:
            break
        else:
            print("Invalid month. Please choose January–June or 'all'.")

    # Get user input for day of week
    allowed_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
    day = ""
    while True:
        day = input("\nEnter day of week (e.g., Monday) or 'all' to apply no day filter: ").strip().lower()
        if day in allowed_days:
            break
        else:
            print("Invalid day. Please enter a valid weekday name or 'all'.")

    print("\nYou chose:")
    print(f"  City : {city.title()}")
    print(f"  Month: {month.title()}")
    print(f"  Day  : {day.title()}")

    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified city and filter by month and day if applicable.

    Args:
        city (str): city name in lowercase matching CITY_DATA keys
        month (str): month name in lowercase or 'all'
        day (str): day name in lowercase or 'all'

    Returns:
        pd.DataFrame: filtered bikeshare data
    """
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # Convert Start Time to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month and day of week and hour
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["hour"] = df["Start Time"].dt.hour

    # Filter by month if applicable
    if month != "all":
        month_names = ["january", "february", "march", "april", "may", "june"]
        month_index = month_names.index(month) + 1  # months are 1–6
        df = df[df["month"] == month_index]

    # Filter by day of week if applicable
    if day != "all":
        df = df[df["day_of_week"].str.lower() == day.lower()]

    return df


def time_stats(df):
    """
    Display statistics on the most frequent times of travel.

    Args:
        df (pd.DataFrame): bikeshare data
    """
    print("\nCalculating The Most Frequent Times of Travel...")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    # Most common month
    popular_month = df["month"].mode()[0]
    # Most common day of week
    popular_day = df["day_of_week"].mode()[0]
    # Most common start hour
    popular_hour = df["hour"].mode()[0]

    print(f"Most common month (1=January): {popular_month}")
    print(f"Most common day of week      : {popular_day}")
    print(f"Most common start hour       : {popular_hour}:00")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")


def station_stats(df):
    """
    Display statistics on the most popular stations and trip.

    Args:
        df (pd.DataFrame): bikeshare data
    """
    print("\nCalculating The Most Popular Stations and Trip...")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    # Most commonly used start station
    start_station = df["Start Station"].mode()[0]
    # Most commonly used end station
    end_station = df["End Station"].mode()[0]
    # Most frequent combination of start and end station
    df["trip"] = df["Start Station"] + " -> " + df["End Station"]
    common_trip = df["trip"].mode()[0]

    print(f"Most common start station: {start_station}")
    print(f"Most common end station  : {end_station}")
    print(f"Most common trip         : {common_trip}")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")


def trip_duration_stats(df):
    """
    Display statistics on the total and average trip duration.

    Args:
        df (pd.DataFrame): bikeshare data
    """
    print("\nCalculating Trip Duration...")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    # Total travel time
    total_travel_time = df["Trip Duration"].sum()
    # Mean travel time
    mean_travel_time = df["Trip Duration"].mean()

    print(f"Total travel time (seconds): {total_travel_time:.2f}")
    print(f"Mean travel time (seconds) : {mean_travel_time:.2f}")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")


def user_stats(df):
    """
    Display statistics on bikeshare users.

    Args:
        df (pd.DataFrame): bikeshare data
    """
    print("\nCalculating User Stats...")
    start_time = time.time()

    if df.empty:
        print("No data available for the selected filters.")
        return

    # Counts of user types
    if "User Type" in df.columns:
        print("\nCounts of user types:")
        print(df["User Type"].value_counts())
    else:
        print("\nUser Type data is not available.")

    # Counts of gender
    if "Gender" in df.columns:
        print("\nCounts of gender:")
        print(df["Gender"].value_counts())
    else:
        print("\nGender data is not available for this city.")

    # Earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = int(df["Birth Year"].min())
        most_recent = int(df["Birth Year"].max())
        most_common = int(df["Birth Year"].mode()[0])
        print("\nBirth year statistics:")
        print(f"  Earliest year: {earliest}")
        print(f"  Most recent  : {most_recent}")
        print(f"  Most common  : {most_common}")
    else:
        print("\nBirth year data is not available for this city.")

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")


def display_raw_data(df):
    """
    Ask the user if they want to see raw data, 5 rows at a time.

    Displays 5 lines of raw data each time the user types 'yes'.

    Args:
        df (pd.DataFrame): bikeshare data
    """
    show_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no: ").strip().lower()
    start_loc = 0
    rows_per_page = 5

    # Only proceed if the dataframe is not empty
    if df.empty:
        print("No data available to display.")
        return

    while show_data in ["yes", "y"]:
        end_loc = start_loc + rows_per_page
        print("\nShowing rows", start_loc, "to", end_loc - 1, ":")
        print(df.iloc[start_loc:end_loc])

        start_loc += rows_per_page
        if start_loc >= len(df):
            print("\nNo more data to display.")
            break

        show_data = input("\nWould you like to see the next 5 lines of raw data? Enter yes or no: ").strip().lower()

    # If user says 'no' or input is not 'yes'/'y', we stop without error.


def main():
    """
    Main program loop for running the bikeshare analysis.

    It repeatedly:
    - Asks the user for filters (city, month, day)
    - Loads and filters the data accordingly
    - Computes and prints descriptive statistics
    - Optionally displays raw data in chunks of 5 rows
    - Asks the user if they want to restart
    """
    while True:
        city, month, day = get_filters()

        try:
            df = load_data(city, month, day)
        except FileNotFoundError:
            print(f"\nError: Data file for {city.title()} not found. Please ensure the CSV files are in the same folder as this script.")
            # Safely continue to next loop iteration
            restart = input("\nWould you like to try again with another city? Enter yes or no: ").strip().lower()
            if restart not in ["yes", "y"]:
                print("Goodbye!")
                break
            else:
                continue

        # Compute and display statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask if the user wants to see raw data
        display_raw_data(df)

        # Ask if the user wants to restart the analysis
        restart = input("\nWould you like to restart? Enter yes or no: ").strip().lower()
        if restart not in ["yes", "y"]:
            print("\nThank you for exploring US bikeshare data! Goodbye.")
            break


if __name__ == "__main__":
    main()

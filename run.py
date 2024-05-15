import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime  # To get the current month

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('oxford_weather_data')

# List of month names for conversion
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


def display_menu():
    """Display the menu options for the user to choose."""
    print("\nWelcome to the Oxford Weather comparison tool. Select an option:")
    options = ["1. Compare sun hours",
               "2. Compare rainfall",
               "3. Compare maximum temperature",
               "4. Compare minimum temperature",
               "5. Input or delete weather data for 2024"]
    for option in options:
        print(option)
    return input("Enter your choice (1-5):\n ")


def get_month_input():
    """Get and validate month input from the user."""
    try:
        month = int(input("Please input a month number (1-12):\n "))
        current_month = datetime.now().month  # Get the current month
        if 1 <= month <= current_month:
            return month
        else:
            print("That month is in the future!")
            print(f"Please enter a number between 1 and {current_month}.")
            return None
    except ValueError:
        print("Please enter a valid number for month.")
        return None


def fetch_data(month, column):
    """Fetch the data from the spreadsheet for a given month and column."""
    try:
        sheet_1950 = SHEET.worksheet("1950")
        sheet_2022 = SHEET.worksheet("2022")
        row_index = month + 1  # Adjusted for header row
        value_1950 = sheet_1950.cell(row_index, column).value
        value_2022 = sheet_2022.cell(row_index, column).value
        data_1950 = int(value_1950) if value_1950.isdigit() else None
        data_2022 = int(value_2022) if value_2022.isdigit() else None
        return data_1950, data_2022
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None, None


def compare_data(data_type, column):
    """General function comparing weather data."""
    month = get_month_input()
    if month is None:
        return
    month_name = MONTH_NAMES[month - 1]

    data_1950, data_2022 = fetch_data(month, column)
    if data_1950 is None and data_2022 is None:
        print(f"No data available for {data_type} in {month_name}.")
        return
    elif data_1950 is None:
        print(f"No data for {data_type} in {month_name} 1950.")
    elif data_2022 is None:
        print(f"No data for {data_type} in {month_name} 2022.")

    if data_1950 is not None:
        print(f"\n{data_type.capitalize()} in {month_name} 1950: {data_1950}")
    if data_2022 is not None:
        print(f"{data_type.capitalize()} in {month_name} 2022: {data_2022}")

    if data_1950 and data_2022:
        if data_1950 < data_2022:
            print(f"More {data_type} in 2022.")
        elif data_1950 > data_2022:
            print(f"More {data_type} in 1950.")
        else:
            print(f"The {data_type} is the same in both years.")


def input_or_delete_data():
    """Choose whether to input or delete data for a month."""
    print("\n1. Input new data\n2. Delete existing data")
    choice = input("Choose an option (1-2):\n ")
    month = get_month_input()
    if month is None:
        return
    if choice == '1':
        input_weather_data(month)
    elif choice == '2':
        delete_weather_data(month)
    else:
        print("Invalid choice. Please enter 1 or 2.")


def input_weather_data(month):
    """Function to input new weather data for 2024, for a specified month."""
    try:
        sun_hours = round(float(input("Enter sun hours: ")))
        min_temp = round(float(input("Enter minimum temperature: ")))
        max_temp = round(float(input("Enter maximum temperature: ")))
        rain_mm = round(float(input("Enter rainfall in mm: ")))

        sheet_2024 = SHEET.worksheet("2024")
        row_index = month + 1

        sheet_2024.update_cell(row_index, 2, max_temp)
        sheet_2024.update_cell(row_index, 3, min_temp)
        sheet_2024.update_cell(row_index, 4, rain_mm)
        sheet_2024.update_cell(row_index, 5, sun_hours)

        memo = format(MONTH_NAMES[month-1])
        print(f"Data successfully added for {memo} 2024.")
    except ValueError:
        print("Please enter valid numerical values.")
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_weather_data(month):
    """Function to delete data for 2024, for a specified month."""
    sheet_2024 = SHEET.worksheet("2024")
    row_index = month + 1

    attempts = 0
    while attempts < 2:
        confirm = input(f"delete {MONTH_NAMES[month-1]}2024?(y/n):\n").lower()
                        
        if confirm == 'y':
            try:
                # Clearing data from the row
                sheet_2024.update_cell(row_index, 2, "")
                sheet_2024.update_cell(row_index, 3, "")
                sheet_2024.update_cell(row_index, 4, "")
                sheet_2024.update_cell(row_index, 5, "")
                month_deleted = format(MONTH_NAMES[month-1])
                print(f"Data successfully deleted for {month_deleted} 2024.")
                return
            except Exception as e:
                print(f"An error occurred: {e}")
                return
        elif confirm == 'n':
            print("Data deletion cancelled.")
            return
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            attempts += 1
            if attempts == 2:
                print("Returning to the main menu after 2 failed attempts.")
            return


def main():
    """We need some docstring here!!!"""
    while True:
        choice = display_menu()
        if choice == '1':
            compare_data("sun hours", 5)
        elif choice == '2':
            compare_data("rainfall", 4)
        elif choice == '3':
            compare_data("maximum temperature", 2)
        elif choice == '4':
            compare_data("minimum temperature", 3)
        elif choice == '5':
            input_or_delete_data()
        else:
            print("Invalid choice. Please choose between 1 and 5.")


if __name__ == "__main__":
    main()
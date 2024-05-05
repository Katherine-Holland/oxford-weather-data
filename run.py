import gspread
from google.oauth2.service_account import Credentials

# Google Sheets API setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('oxford_weather_data')

#Function for 'user menu' to select criteria to compare
def display_menu():
    print("Please select an option:")
    print("1. Compare sun hours for a specific month")
    print("2. Compare rainfall for a specific month")
    print("3. Compare maximum temperature for a specific month")
    print("4. Compare minimum temperature for a specific month")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")
    return choice

# Function to compare sun hours for 1950 and 2022
def compare_sun_hours():
    """
    Asks the user to input a month number and compares sun hours for that month for the years 1950 and 2022.
    """
    print("Please input a month number to compare sun hours for 1950 and 2022.")
    print("Example: January would be entered as 1, February as 2, etc.")
    try:
        month = int(input("Enter the month number (1-12): "))
        if not 1 <= month <= 12:
            print("Invalid month. Please enter a number between 1 and 12.")
            return

        # Access worksheets for both years
        sheet_1950 = SHEET.worksheet("1950")
        sheet_2022 = SHEET.worksheet("2022")

        # Fetch sun hours for the given month from each sheet
        # Google Sheets header text is on line 1 so add 1 to row index because of header row.
        # Sun hours are in column E (column 5).
        row_index = month + 1
        sun_hours_1950 = int(sheet_1950.cell(row_index, 5).value) 
        sun_hours_2022 = int(sheet_2022.cell(row_index, 5).value)  

        # Print comparison
        print(f"Sun hours in {month} 1950: {sun_hours_1950} hours")
        print(f"Sun hours in {month} 2022: {sun_hours_2022} hours")
        if sun_hours_1950 < sun_hours_2022:
            print(f"More sun hours in 2022 ({sun_hours_2022} hours) than in 1950 ({sun_hours_1950} hours).")
        elif sun_hours_1950 > sun_hours_2022:
            print(f"More sun hours in 1950 ({sun_hours_1950} hours) than in 2022 ({sun_hours_2022} hours).")
        else:
            print("Sun hours are the same in both years.")
    except ValueError:
        print("Please enter a valid integer.")
        #If there is an error with the execution (eg. Retrieving the Google spreadsheet)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to compare rainfall for the years 1950 and 2022
def compare_rain_mm():
    """
    Asks the user to input a month number and compares rainfall for that month for the years 1950 and 2022.
    """
    print("Please input a month number to compare rainfall for 1950 and 2022.")
    print("Example: January would be entered as 1, February as 2, etc.")
    try:
        month = int(input("Enter the month number (1-12): "))
        if not 1 <= month <= 12:
            print("Invalid month. Please enter a number between 1 and 12.")
            return

        # Access worksheets for both years
        sheet_1950 = SHEET.worksheet("1950")
        sheet_2022 = SHEET.worksheet("2022")

        # Fetch rainfall for the given month from each sheet
        # Google Sheets header text is on line 1 so add 1 to row index because of header row.
        # Rainfall is in column D (column 4).
        row_index = month + 1
        rain_mm_1950 = int(sheet_1950.cell(row_index, 4).value) 
        rain_mm_2022 = int(sheet_2022.cell(row_index, 4).value)  

        # Print comparison
        print(f"Rainfall in mm in {month} 1950: {rain_mm_1950}")
        print(f"Rainfall in mm in {month} 2022: {rain_mm_2022}")
        if rain_mm_1950 < rain_mm_2022:
            print(f"More rainfall in 2022 ({rain_mm_2022}) than in 1950 ({rain_mm_1950}).")
        elif rain_mm_1950 > rain_mm_2022:
            print(f"More rainfall in 1950 ({rain_mm_1950}) than in 2022 ({rain_mm_2022}).")
        else:
            print("Rainfall was the same in both years.")
    except ValueError:
        print("Please enter a valid integer.")
        #If there is an error with the execution (eg. Retrieving the Google spreadsheet)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to compare maximum temperature for the years 1950 and 2022
def compare_max_temp():
    """
    Asks the user to input a month number and compares the maximum temperature for that month for the years 1950 and 2022.
    """
    print("Please input a month number to compare the maximum temperature for 1950 and 2022.")
    print("Example: January would be entered as 1, February as 2, etc.")
    try:
        month = int(input("Enter the month number (1-12): "))
        if not 1 <= month <= 12:
            print("Invalid month. Please enter a number between 1 and 12.")
            return

        # Access worksheets for both years
        sheet_1950 = SHEET.worksheet("1950")
        sheet_2022 = SHEET.worksheet("2022")

        # Fetch maximum temperature for the given month from each sheet
        # Google Sheets header text is on line 1 so add 1 to row index because of header row.
        # Maximum temperature is in column B (column 2).
        row_index = month + 1
        max_temp_1950 = int(sheet_1950.cell(row_index, 2).value) 
        max_temp_2022 = int(sheet_2022.cell(row_index, 2).value)  

        # Print comparison
        print(f"Maximum temperature in {month} 1950: {max_temp_1950}")
        print(f"Maximum temperature in {month} 2022: {max_temp_2022}")
        if max_temp_1950 < max_temp_2022:
            print(f"Hotter in 2022 ({max_temp_2022}) than in 1950 ({max_temp_1950}).")
        elif max_temp_1950 > max_temp_2022:
            print(f"Hotter in 1950 ({max_temp_1950}) than in 2022 ({max_temp_2022}).")
        else:
            print("The temperature was the same in both years.")
    except ValueError:
        print("Please enter a valid integer.")
        #If there is an error with the execution (eg. Retrieving the Google spreadsheet)
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to compare minimum temperature for the years 1950 and 2022
def compare_min_temp():
    """
    Asks the user to input a month number and compares the minimum temperature for that month for the years 1950 and 2022.
    """
    print("Please input a month number to compare the minimum temperature for 1950 and 2022.")
    print("Example: January would be entered as 1, February as 2, etc.")
    try:
        month = int(input("Enter the month number (1-12): "))
        if not 1 <= month <= 12:
            print("Invalid month. Please enter a number between 1 and 12.")
            return

        # Access worksheets for both years
        sheet_1950 = SHEET.worksheet("1950")
        sheet_2022 = SHEET.worksheet("2022")

        # Fetch minimum temperature for the given month from each sheet
        # Google Sheets header text is on line 1 so add 1 to row index because of header row.
        # Minimum temperature is in column C (column 3).
        row_index = month + 1
        min_temp_1950 = int(sheet_1950.cell(row_index, 3).value) 
        min_temp_2022 = int(sheet_2022.cell(row_index, 3).value)  

        # Print comparison
        print(f"Minimum temperature in {month} 1950: {min_temp_1950}")
        print(f"Minimum temperature in {month} 2022: {min_temp_2022}")
        if min_temp_1950 < min_temp_2022:
            print(f"Cooler in 1950 ({min_temp_1950}) than in 2022 ({min_temp_2022}).")
        elif min_temp_1950 > min_temp_2022:
            print(f"Hotter in 1950 ({min_temp_1950}) than in 2022 ({min_temp_2022}).")
        else:
            print("The temperature was the same in both years.")
    except ValueError:
        print("Please enter a valid integer.")
        #If there is an error with the execution (eg. Retrieving the Google spreadsheet)
    except Exception as e:
        print(f"An error occurred: {e}")

# Main script to run the programme
if __name__ == "__main__":
    while True:
        choice = display_menu()
        if choice == '1':
            compare_sun_hours()
        elif choice == '2':
            compare_rain_mm()
        elif choice == '3':
            compare_max_temp()
        elif choice == '4':
            compare_min_temp()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

#Part 2: Scrape and Analyze Mars Weather Data

from splinter import Browser
from bs4 import BeautifulSoup as soup
import matplotlib.pyplot as plt
import pandas as pd

browser = Browser('chrome')

# Visit the website
url = "https://static.bc-edx.com/data/web/mars_facts/temperature.html"
browser.visit(url)

# Delay to allow the page to fully load
browser.is_element_present_by_css("table", wait_time=1)

# Get the HTML content of the website
html = browser.html

# Create a BeautifulSoup object
mars_weather_soup = soup(html, "html.parser")

# Find the HTML table containing the data
table = mars_weather_soup.find("table")

# Extract the table headers
headers = [header.text.strip() for header in table.find_all("th")]

# Extract the table rows
rows = table.find_all("tr")

# Initialize an empty list to store the scraped data
weather_data = []

# Iterate over the rows, skipping the header row
for row in rows[1:]:
    # Extract the data from each cell in the row
    cells = row.find_all("td")
    data_row = [cell.text.strip() for cell in cells]
    
    # Store the data in a dictionary with column names as keys
    row_data = dict(zip(headers, data_row))
    
    # Append the dictionary to the list of weather data
    weather_data.append(row_data)

# Convert the list of dictionaries to a Pandas DataFrame
weather_df = pd.DataFrame(weather_data)

# Display the DataFrame
print(weather_df)

# Display the data types of each column
print(weather_df.dtypes)

# Convert 'terrestrial_date' column to datetime type
weather_df['terrestrial_date'] = pd.to_datetime(weather_df['terrestrial_date'])

# Convert 'sol', 'ls', and 'month' columns to int64
weather_df['sol'] = weather_df['sol'].astype('int64')
weather_df['ls'] = weather_df['ls'].astype('int64')
weather_df['month'] = weather_df['month'].astype('int64')

# Display the updated data types
print(weather_df.dtypes)


# Convert 'min_temp' and 'pressure' columns to appropriate numeric types
weather_df['min_temp'] = pd.to_numeric(weather_df['min_temp'], errors='coerce')
weather_df['pressure'] = pd.to_numeric(weather_df['pressure'], errors='coerce')

# Display the updated data types
print(weather_df.dtypes)

# 1. How many months exist on Mars?
num_months = weather_df['terrestrial_date'].dt.month.nunique()
print("Number of months on Mars:", num_months)

# 2. How many Martian (and not Earth) days worth of data exist in the scraped dataset?
num_martian_days = weather_df['sol'].nunique()
print("Number of Martian days worth of data:", num_martian_days)

# 3. What is the average low temperature by month?
# Calculate the average low temperature by month
avg_low_temp_by_month = weather_df.groupby('month')['min_temp'].mean()

print("Average low temperature by month:\n", avg_low_temp_by_month)

# What are the coldest and warmest months on Mars (at the location of Curiosity)?

# Find the coldest month
coldest_month = avg_low_temp_by_month.idxmin()

# Find the warmest month
warmest_month = avg_low_temp_by_month.idxmax()

print("Coldest month:", coldest_month)
print("Warmest month:", warmest_month)

# Calculate the average minimum daily temperature for each month
monthly_avg_min_temp = weather_df.groupby('month')['min_temp'].mean()

# Plot the results as a bar chart
plt.figure(figsize=(10, 6))
monthly_avg_min_temp.plot(kind='bar', color='coral')
plt.title('Average Minimum Daily Temperature for Each Month on Mars')
plt.xlabel('Month')
plt.ylabel('Average Minimum Daily Temperature (°C)')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()

plt.savefig('resources/monthly_avg_min_temp_plot.png')

plt.show()

# Calculate the average pressure by Martian month
average_pressure_by_month = weather_df.groupby('month')['pressure'].mean()

# Convert to DataFrame and reset index
average_pressure_by_month = average_pressure_by_month.to_frame().reset_index()

# Print the result
print(average_pressure_by_month)


# Which months have hte lowest and highest atmospheric pressure on Mars?

# Find the month with the lowest atmospheric pressure
lowest_pressure_month = average_pressure_by_month.loc[average_pressure_by_month['pressure'].idxmin()]

# Find the month with the highest atmospheric pressure
highest_pressure_month = average_pressure_by_month.loc[average_pressure_by_month['pressure'].idxmax()]

print("Month with the lowest atmospheric pressure:", lowest_pressure_month['month'])
print("Month with the highest atmospheric pressure:", highest_pressure_month['month'])


# Calculate the average daily atmospheric pressure for each month
monthly_avg_pressure = weather_df.groupby('month')['pressure'].mean()

# Plot the results as a bar chart
plt.figure(figsize=(10, 6))
monthly_avg_pressure.plot(kind='bar', color='lightgreen')
plt.title('Average Daily Atmospheric Pressure for Each Month on Mars')
plt.xlabel('Month')
plt.ylabel('Average Daily Atmospheric Pressure (Pa)')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()

plt.savefig('resources/monthly_avg_pressure_plot.png')

plt.show()


# Convert the date column to datetime format
weather_df['terrestrial_date'] = pd.to_datetime(weather_df['terrestrial_date'])

# Calculate the number of terrestrial days
weather_df['num_terrestrial_days'] = (weather_df['terrestrial_date'] - weather_df['terrestrial_date'].min()).dt.days

# Plot the daily minimum temperature
plt.figure(figsize=(10, 6))
plt.plot(weather_df['num_terrestrial_days'], weather_df['min_temp'], color='orange')
plt.title('Daily Minimum Temperature on Mars')
plt.xlabel('Number of Terrestrial Days')
plt.ylabel('Minimum Temperature (°C)')
plt.grid(True)
plt.tight_layout()
plt.xlim(left=0)

plt.savefig('resources/mars_min_temp_plot.png')

plt.show()

# About how many terrestrial (Earth) days exist in a martian year?

# Calculate the number of terrestrial days in a Martian year
num_terrestrial_days_in_martian_year = (weather_df['terrestrial_date'].max() - weather_df['terrestrial_date'].min()).days

print("Number of terrestrial (Earth) days in a Martian year:", num_terrestrial_days_in_martian_year)

# Define the file path for saving the CSV file
csv_file_path = "resources/mars_weather_data.csv"

# Save the DataFrame to a CSV file
weather_df.to_csv(csv_file_path, index=False)

print("Data has been saved to mars_weather_data.csv")

browser.quit()

















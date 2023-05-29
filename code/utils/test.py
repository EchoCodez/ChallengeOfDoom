import schedule
import time

def my_function():
    # Replace this with your desired function code
    print("Executing my function at 5:30 PM!")

# Schedule the function to run daily at 5:30 PM
schedule.every().day.at("17:28").do(my_function)

while True:
    schedule.run_pending()
    time.sleep(1)

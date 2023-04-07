#########################################################
### An alternative form to clear() in cmd python code ###
#########################################################
def clear():
    import os
    return os.system('cls' if os.name == 'nt' else 'clear')

#########################
### Percentage_change ###
#########################
def pct_change(inicial, final):
    """
    Output: percentage change.
    interpretation: If positive, it's represent an increase. Otherwise it's represent a decrease
    """
    return (final/inicial)-1

###################
### Next n Days ###
###################
def is_leap(year):
    if year%400 == 0:
        return True
    elif year%100 ==0:
        return False
    elif year%4 == 0:
        return True
    else:
        return False
def next_day(inicial_date):
    year = int(inicial_date[0:4])
    month = int(inicial_date[5:7])
    day = int(inicial_date[8:10])

    if month in [1, 3, 5, 7, 8, 10, 12]:
        MAX_DAY = 31
    elif month == 2:
        if is_leap(year):
            MAX_DAY = 29
        else:
            MAX_DAY = 28
    else:
        MAX_DAY = 30

    MAX_MONTH = 12
    if month > MAX_MONTH:
        return "You should inform a correct date."
    elif day < MAX_DAY:
        return "%d-%02d-%02d" % (year,month, day + 1)
    elif day == MAX_DAY:
        if month == MAX_MONTH:
            return "%d-%02d-%02d" % (year + 1, 1, 1)
        else:
            return "%d-%02d-%02d" % (year, month + 1, 1)
    else:
        return "You should inform a correct date."
def next_n_days(inicial_date, n):
    c = 1
    while c <= n: 
        inicial_date = next_day(inicial_date)
        c = c + 1

    return inicial_date

def main():
    import time
    time.sleep(3)
    print("This was not meant to be called directly!")

#############################################################################
### Transform an amount of seconds to amount of time in D:HH:MM:SS format ###
#############################################################################
def amount_time(seconds):
    SECONDS_PER_DAY = (60*60*24)
    SECONDS_PER_HOUR = (60*60)
    SECONDS_PER_MINUTE = (60)

    days = seconds//SECONDS_PER_DAY
    seconds = seconds%SECONDS_PER_DAY

    hours = seconds//SECONDS_PER_HOUR
    seconds = seconds%SECONDS_PER_HOUR

    minutes = seconds//SECONDS_PER_MINUTE
    seconds = seconds%SECONDS_PER_MINUTE

    return "The equivalent duration is", \
        "%d:%02d:%02d:%02d" % (days, hours, minutes, seconds), \
            "in D:HH:MM:SS format."
    
if __name__ == "__main__":
    print(amount_time(432000)) # 5! hours is 5 days
    
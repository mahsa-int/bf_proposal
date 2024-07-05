
def hour_bins(hour):
    hour = int(hour)
    if 0 <= hour < 3:
        return '00:00-02:59'
    elif 3 <= hour < 6:
        return '03:00-05:59'
    elif 6 <= hour < 9:
        return '06:00-08:59'
    elif 9 <= hour < 12:
        return '09:00-11:59'
    elif 12 <= hour < 15:
        return '12:00-14:59'
    elif 15 <= hour < 18:
        return '15:00-17:59'
    elif 18 <= hour < 21:
        return '18:00-20:59'
    else:
        return '21:00-23:59'
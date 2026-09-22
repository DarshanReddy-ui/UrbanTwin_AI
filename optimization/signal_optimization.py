def optimize_signal(congestion, vehicle_count):
    if congestion == "Low":
        green_time = 30
        red_time = 30

    elif congestion == "Medium":
        green_time = 45
        red_time = 30

    else:
        green_time = 60
        red_time = 20

    return green_time, red_time


# Current traffic information
vehicle_count = 4
congestion = "Medium"

green_time, red_time = optimize_signal(
    congestion,
    vehicle_count
)

print("\n===== UrbanTwin AI Signal Optimization =====")
print("Vehicle Count:", vehicle_count)
print("Congestion:", congestion)
print("Recommended Green Time:", green_time, "seconds")
print("Recommended Red Time:", red_time, "seconds")
print("=============================================")
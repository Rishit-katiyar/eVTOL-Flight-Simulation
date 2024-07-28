import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
g = 9.81  # Gravity (m/s^2)
mass = 1500  # eVTOL mass (kg)
max_thrust = 20000  # Maximum thrust (N)
cruise_altitude = 1000  # Cruise altitude (m)
cruise_velocity = 50  # Cruise horizontal velocity (m/s)
time_step = 0.1  # Time step for simulation (s)
total_time = 300  # Total simulation time (s)

# Flight phases
take_off_time = 30  # Time to reach cruise altitude (s)
cruise_time = 200  # Time to cruise (s)
landing_time = 30  # Time to land (s)

# Time arrays
time = np.arange(0, total_time, time_step)

# Initialize arrays for altitude and vertical velocity
altitude = np.zeros_like(time)
vertical_velocity = np.zeros_like(time)
horizontal_velocity = np.zeros_like(time)

# Take-off phase
for i in range(1, int(take_off_time / time_step)):
    thrust = max_thrust
    vertical_acceleration = (thrust - mass * g) / mass
    vertical_velocity[i] = vertical_velocity[i - 1] + vertical_acceleration * time_step
    altitude[i] = altitude[i - 1] + vertical_velocity[i - 1] * time_step + 0.5 * vertical_acceleration * time_step ** 2

# Cruise phase
for i in range(int(take_off_time / time_step), int((take_off_time + cruise_time) / time_step)):
    vertical_velocity[i] = 0
    altitude[i] = cruise_altitude
    horizontal_velocity[i] = cruise_velocity

# Landing phase
for i in range(int((take_off_time + cruise_time) / time_step), len(time)):
    thrust = max_thrust * (1 - (i - int((take_off_time + cruise_time) / time_step)) * time_step / landing_time)
    vertical_acceleration = (thrust - mass * g) / mass
    vertical_velocity[i] = vertical_velocity[i - 1] + vertical_acceleration * time_step
    altitude[i] = altitude[i - 1] + vertical_velocity[i - 1] * time_step + 0.5 * vertical_acceleration * time_step ** 2
    if altitude[i] <= 0:
        altitude[i] = 0
        vertical_velocity[i] = 0
        break

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(time, altitude, label='Altitude (m)')
plt.plot(time, vertical_velocity, label='Vertical Velocity (m/s)')
plt.plot(time, horizontal_velocity, label='Horizontal Velocity (m/s)')
plt.axvline(take_off_time, color='gray', linestyle='--', label='Take-off End')
plt.axvline(take_off_time + cruise_time, color='gray', linestyle='--', label='Cruise End')
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m) / Velocity (m/s)')
plt.title('eVTOL Flight Simulation')
plt.legend()
plt.grid(True)
plt.show()

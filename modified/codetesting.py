

import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
g = 9.81  # Gravity (m/s^2)
mass = 1500  # eVTOL mass (kg)
max_thrust = 20000  # Maximum thrust (N)
drag_coefficient = 0.5  # Drag coefficient (dimensionless)
air_density = 1.225  # Air density at sea level (kg/m^3)
frontal_area = 1.5  # Frontal area (m^2)
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

# Initialize arrays for altitude, vertical velocity, horizontal velocity, thrust, and drag
altitude = np.zeros_like(time)
vertical_velocity = np.zeros_like(time)
horizontal_velocity = np.zeros_like(time)
thrust = np.zeros_like(time)
drag = np.zeros_like(time)

# Take-off phase
for i in range(1, int(take_off_time / time_step)):
    thrust[i] = max_thrust
    vertical_acceleration = (thrust[i] - mass * g) / mass
    vertical_velocity[i] = vertical_velocity[i - 1] + vertical_acceleration * time_step
    altitude[i] = altitude[i - 1] + vertical_velocity[i - 1] * time_step + 0.5 * vertical_acceleration * time_step ** 2
    drag[i] = 0.5 * air_density * (vertical_velocity[i] ** 2) * drag_coefficient * frontal_area

# Cruise phase
for i in range(int(take_off_time / time_step), int((take_off_time + cruise_time) / time_step)):
    vertical_velocity[i] = 0
    altitude[i] = cruise_altitude
    horizontal_velocity[i] = cruise_velocity
    thrust[i] = 0.5 * air_density * (horizontal_velocity[i] ** 2) * drag_coefficient * frontal_area

# Landing phase
for i in range(int((take_off_time + cruise_time) / time_step), len(time)):
    thrust[i] = max_thrust * (1 - (i - int((take_off_time + cruise_time) / time_step)) * time_step / landing_time)
    vertical_acceleration = (thrust[i] - mass * g) / mass
    vertical_velocity[i] = vertical_velocity[i - 1] + vertical_acceleration * time_step
    altitude[i] = altitude[i - 1] + vertical_velocity[i - 1] * time_step + 0.5 * vertical_acceleration * time_step ** 2
    drag[i] = 0.5 * air_density * (vertical_velocity[i] ** 2) * drag_coefficient * frontal_area
    if altitude[i] <= 0:
        altitude[i] = 0
        vertical_velocity[i] = 0
        break

# Plotting the results
fig, ax = plt.subplots(2, 1, figsize=(12, 10))

# Altitude plot
ax[0].plot(time, altitude, label='Altitude (m)', color='b')
ax[0].axvline(take_off_time, color='gray', linestyle='--', label='Take-off End')
ax[0].axvline(take_off_time + cruise_time, color='gray', linestyle='--', label='Cruise End')
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Altitude (m)')
ax[0].set_title('Altitude Profile')
ax[0].legend()
ax[0].grid(True)

# Velocity plot
ax[1].plot(time, vertical_velocity, label='Vertical Velocity (m/s)', color='g')
ax[1].plot(time, horizontal_velocity, label='Horizontal Velocity (m/s)', color='r')
ax[1].axvline(take_off_time, color='gray', linestyle='--', label='Take-off End')
ax[1].axvline(take_off_time + cruise_time, color='gray', linestyle='--', label='Cruise End')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Velocity (m/s)')
ax[1].set_title('Velocity Profile')
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

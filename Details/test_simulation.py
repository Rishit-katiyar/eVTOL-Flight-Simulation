





import numpy as np
import matplotlib.pyplot as plt

# Function to simulate eVTOL flight
def simulate_eVTOL(mass, max_thrust, drag_coefficient, air_density, frontal_area, cruise_altitude, cruise_velocity, time_step, total_time):
    g = 9.81  # Gravity (m/s^2)

    # Time arrays
    time = np.arange(0, total_time, time_step)

    # Initialize arrays for altitude, vertical velocity, horizontal velocity, thrust, and drag
    altitude = np.zeros_like(time)
    vertical_velocity = np.zeros_like(time)
    horizontal_velocity = np.zeros_like(time)
    thrust = np.zeros_like(time)
    drag = np.zeros_like(time)

    # Take-off phase
    for i in range(1, int(total_time / 3 / time_step)):
        thrust[i] = max_thrust
        vertical_acceleration = (thrust[i] - mass * g) / mass
        vertical_velocity[i] = vertical_velocity[i - 1] + vertical_acceleration * time_step
        altitude[i] = altitude[i - 1] + vertical_velocity[i - 1] * time_step + 0.5 * vertical_acceleration * time_step ** 2
        drag[i] = 0.5 * air_density * (vertical_velocity[i] ** 2) * drag_coefficient * frontal_area

    # Cruise phase
    for i in range(int(total_time / 3 / time_step), int((2 * total_time / 3) / time_step)):
        vertical_velocity[i] = 0
        altitude[i] = cruise_altitude
        horizontal_velocity[i] = cruise_velocity
        thrust[i] = 0.5 * air_density * (horizontal_velocity[i] ** 2) * drag_coefficient * frontal_area

    # Landing phase
    for i in range(int((2 * total_time / 3) / time_step), len(time)):
        thrust[i] = max_thrust * (1 - (i - int((2 * total_time / 3) / time_step)) * time_step / (total_time / 3))
        vertical_acceleration = (thrust[i] - mass * g) / mass
        vertical_velocity[i] = vertical_velocity[i - 1] + vertical_acceleration * time_step
        altitude[i] = altitude[i - 1] + vertical_velocity[i - 1] * time_step + 0.5 * vertical_acceleration * time_step ** 2
        drag[i] = 0.5 * air_density * (vertical_velocity[i] ** 2) * drag_coefficient * frontal_area
        if altitude[i] <= 0:
            altitude[i] = 0
            vertical_velocity[i] = 0
            break

    return time, altitude, vertical_velocity, horizontal_velocity

# Test parameters
mass = 1500  # eVTOL mass (kg)
max_thrust = 20000  # Maximum thrust (N)
drag_coefficient = 0.5  # Drag coefficient (dimensionless)
air_density = 1.225  # Air density at sea level (kg/m^3)
frontal_area = 1.5  # Frontal area (m^2)
cruise_altitude = 1000  # Cruise altitude (m)
cruise_velocity = 50  # Cruise horizontal velocity (m/s)
time_step = 0.1  # Time step for simulation (s)
total_time = 300  # Total simulation time (s)

# Run simulation
time, altitude, vertical_velocity, horizontal_velocity = simulate_eVTOL(mass, max_thrust, drag_coefficient, air_density, frontal_area, cruise_altitude, cruise_velocity, time_step, total_time)

# Plot results (optional for visual verification)
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(time, altitude, label='Altitude (m)')
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')
plt.title('Altitude Profile')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time, vertical_velocity, label='Vertical Velocity (m/s)')
plt.plot(time, horizontal_velocity, label='Horizontal Velocity (m/s)')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity Profile')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Assertions (basic checks)
assert altitude[-1] == 0, "The simulation did not land properly"
assert np.max(vertical_velocity) <= max_thrust / mass + g, "Vertical velocity exceeded thrust capabilities"
assert np.max(horizontal_velocity) <= cruise_velocity, "Horizontal velocity exceeded cruise speed"

print("Simulation test passed successfully!")

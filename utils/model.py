
def get_individual_proportions(vel, a_vel, wheel_radius, wheel_base_length):
    l_vel, r_vel = unicycle_to_differential_drive(vel, a_vel, wheel_radius, wheel_base_length)
    m = max(abs(l_vel), abs(r_vel))
    if m == 0:
        m = 1
    return l_vel / m, r_vel / m

"""
velocity -> forward velocity, m/s
angular_velocity > angular velocity, radians/s

@returns left and right wheel velocities (in m/s?)
see http://faculty.salina.k-state.edu/tim/robotics_sg/Control/kinematics/unicycle.html
"""
def unicycle_to_differential_drive(velocity, angular_velocity, radius, length):
    left_vel = (2 * velocity - angular_velocity * length) / (2 * radius)
    right_vel = (2 * velocity + angular_velocity * length) / (2 * radius)
    return left_vel, right_vel
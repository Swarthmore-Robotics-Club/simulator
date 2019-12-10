
def get_individual_proportions(self, vel, a_vel):
    l_vel, r_vel = self.unicycle_to_differential_drive(vel, a_vel)
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
def unicycle_to_differential_drive(self, velocity, angular_velocity):
    radius = self.wheel_radius
    length = self.wheel_base_length
    left_vel = (2 * velocity - angular_velocity * length) / (2 * radius)
    right_vel = (2 * velocity + angular_velocity * length) / (2 * radius)
    return left_vel, right_vel
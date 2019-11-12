class PIDLoop():
    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.p_error = 0
        self.i_error = 0
        self.d_error = 0
        return


    def updateError(self, error, dt):
        old_error = self.p_error
        self.p_error = error
        self.i_error = (self.i_error + error * dt) if error != 0 else 0
        self.d_error = (error - old_error) / dt
        return -self.kP * self.p_error - self.kI * self.i_error - self.kD * self.d_error


    def updateErrorPlus(self, error, dt):
        old_error = self.p_error
        self.p_error = error
        self.i_error = (self.i_error + error * dt) if error != 0 else 0
        self.d_error = (error - old_error) / dt
        return self.kP * self.p_error + self.kI * self.i_error + self.kD * self.d_error


    def reset(self):
        self.p_error, self.i_error, self.d_error = (0, 0, 0)
        return
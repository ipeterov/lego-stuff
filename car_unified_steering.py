from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Port, Stop, Direction


class Car:
    TOLERANCE = 3

    GEAR_1 = {
        "speed": 50,
        "color": Color.GREEN,
        "max_angle": 30,
        "sensitivity": 0.05,
    }
    GEAR_2 = {
        "speed": 100,
        "color": Color.ORANGE,
        "max_angle": 30,
        "sensitivity": 0.05,
    }

    def __init__(self):
        self.steering = Motor(
            Port.A,
            gears=[[12, 20], [12, 20]],
        )
        self.drive = Motor(Port.D)
        self.remote = Remote()

        self.gear = self.GEAR_1
        self.remote.light.on(self.gear["color"])

        self.desired_speed = 0
        self.desired_angle = 0

    def switch_gear(self):
        if self.gear == self.GEAR_1:
            self.gear = self.GEAR_2
        else:
            self.gear = self.GEAR_1
        self.remote.light.on(self.gear["color"])

    def control_cycle(self):
        self.steering.track_target(self.desired_angle)

        if self.desired_speed == 0:
            self.drive.stop()
        else:
            self.drive.dc(self.desired_speed)

    def control_loop(self):
        center_was_pressed = False
        while True:
            pressed = self.remote.buttons.pressed()

            if Button.LEFT_PLUS in pressed:
                self.desired_speed = -1 * self.gear["speed"]
            elif Button.LEFT_MINUS in pressed:
                self.desired_speed = self.gear["speed"]
            else:
                self.desired_speed = 0

            if Button.RIGHT_MINUS in pressed:
                new_angle = self.desired_angle + self.gear["sensitivity"]
                self.desired_angle = min(new_angle, self.gear["max_angle"])
            elif Button.RIGHT_PLUS in pressed:
                new_angle = self.desired_angle - self.gear["sensitivity"]
                self.desired_angle = max(new_angle, self.gear["max_angle"] * -1)
            elif Button.RIGHT in pressed:
                self.desired_angle = 0

            if Button.CENTER not in pressed and center_was_pressed:
                self.switch_gear()
            center_was_pressed = Button.CENTER in pressed

            self.control_cycle()


car = Car()
car.control_loop()

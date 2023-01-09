import umath

from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Port, Stop, Direction


class Car:
    TOLERANCE = 3

    WHEELBASE_LENGTH = 25
    WHEELBASE_WIDTH = 9

    GEAR_1 = {
        "speed": 50,
        "color": Color.GREEN,
        "max_angle": 35,
        "sensitivity": 0.1,
    }
    GEAR_2 = {
        "speed": 100,
        "color": Color.ORANGE,
        "max_angle": 30,
        "sensitivity": 0.05,
    }

    def __init__(self):
        self.steering_left = Motor(
            Port.A, 
            positive_direction=Direction.COUNTERCLOCKWISE,
            gears=[[12, 20]],
        )
        self.steering_right = Motor(
            Port.B, 
            positive_direction=Direction.COUNTERCLOCKWISE,
            gears=[12, 20],
        )
        self.drive = Motor(Port.D)
        self.remote = Remote()

        self.gear = self.GEAR_1
        self.remote.light.on(self.gear["color"])

        self.desired_speed = 0
        self.desired_angle = 0

    def calculate_steering_angles(self, center_degrees) -> [int, int]:
        if center_degrees == 0:
            return 0, 0

        angle = umath.radians(umath.fabs(center_degrees))

        rotation_distance = self.WHEELBASE_LENGTH / umath.tan(angle)
        inner_distance = rotation_distance - self.WHEELBASE_WIDTH / 2
        outer_distance = rotation_distance + self.WHEELBASE_WIDTH / 2

        inner_degrees = umath.degrees(
            umath.atan2(self.WHEELBASE_LENGTH, inner_distance)
        )
        outer_degrees = umath.degrees(
            umath.atan2(self.WHEELBASE_LENGTH, outer_distance)
        )

        if center_degrees > 0:
            return inner_degrees, outer_degrees
        elif center_degrees < 0:
            return -1 * outer_degrees, -1 * inner_degrees

    def switch_gear(self):
        if self.gear == self.GEAR_1:
            self.gear = self.GEAR_2
        else:
            self.gear = self.GEAR_1
        self.remote.light.on(self.gear["color"])

    def control_cycle(self):
        left, right = self.calculate_steering_angles(self.desired_angle)

        current_left = self.steering_left.angle()
        current_right = self.steering_right.angle()

        if umath.fabs(left - current_left) > self.TOLERANCE:
            self.steering_left.track_target(left)

        if umath.fabs(right - current_right) > self.TOLERANCE:
            self.steering_right.track_target(right)

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

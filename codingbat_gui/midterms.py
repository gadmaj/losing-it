"""Practice tasks transcribed from the two local midterms; answers stay on the server."""
import math


def problem(number, title, method, original, task, inputs, reference, diagram=None):
    cases = []
    for i, values in enumerate(inputs):
        cases.append({"label": "Original exam values" if i == 0 else f"Practice variant {i}",
                      "input": values, "expected": reference(**values)})
    result = {"number": number, "title": title, "method": method,
              "description": original + "\n\nCoding task: " + task
              + "\nUse degrees for angle inputs and return an unrounded number. Use the supplied g where present.",
              "arguments": list(inputs[0]), "cases": cases, "cppReturnType": "double"}
    if diagram:
        result["diagram"] = {"src": "/diagrams/" + diagram[0] + ".png", "alt": diagram[1]}
    return result


def resultant(displacements):
    x = sum(magnitude * math.cos(math.radians(angle)) for magnitude, angle in displacements)
    y = sum(magnitude * math.sin(math.radians(angle)) for magnitude, angle in displacements)
    return math.hypot(x, y)


def speed_at_x(initialSpeed, ax, ay, targetX):
    time = (math.sqrt(initialSpeed**2 + 2 * ax * targetX) - initialSpeed) / ax
    return math.hypot(initialSpeed + ax * time, ay * time)


def wall_distance(speed, angleDegrees, height, g):
    vx = speed * math.cos(math.radians(angleDegrees))
    vy = speed * math.sin(math.radians(angleDegrees))
    return vx * (vy + math.sqrt(vy**2 - 2 * g * height)) / g


def static_friction(hangingMassRatio, angleDegrees, muStatic):
    required = abs(hangingMassRatio - math.sin(math.radians(angleDegrees)))
    maximum = muStatic * math.cos(math.radians(angleDegrees))
    return required if required <= maximum + 1e-12 else -1.0


SPRING = [
    problem(1, "Add Three Displacements", "resultantDisplacement",
        "Three displacements are A = 100 m due south, B = 100 m due west, and C = 150 m at 30° east of north. Find the magnitude of R = A + B + C.\nChoices: a) 154 m; b) 178 m; c) 129 m; d) 90.1 m; e) 39.0 m.",
        "displacements contains [magnitude in meters, angle in degrees counterclockwise from east] pairs. Return the magnitude of their sum in meters. East is 0°, north 90°, west 180°, south 270°; 30° east of north is 60°.",
        [{"displacements": [[100, 270], [100, 180], [150, 60]]},
         {"displacements": [[3, 0], [4, 90]]},
         {"displacements": [[5, 45], [5, 225]]}], resultant),
    problem(2, "When Does Velocity Become Zero?", "zeroVelocityTime",
        "A particle moves along the x axis. Its position is x = −4.2t + 2t², with x in meters and t in seconds. Find the time when its instantaneous velocity is zero.\nChoices: a) 2.40 s; b) 2.10 s; c) 1.05 s; d) 1.58 s; e) 2.80 s.",
        "For x(t) = linear * t + quadratic * t², return the time in seconds when velocity is zero. quadratic is nonzero, and inputs give a nonnegative answer.",
        [{"linear": -4.2, "quadratic": 2}, {"linear": -12, "quadratic": 3},
         {"linear": 6, "quadratic": -1.5}], lambda linear, quadratic: -linear / (2 * quadratic)),
    problem(3, "A Ball Returns to Its Launch Height", "returnTime",
        "A ball is thrown directly upwards, reaching a height of 2.5 m above its initial position before descending. How long does it take to return to its initial position?\nChoices: a) 1.43 s; b) 2.85 s; c) 1.71 s; d) 2.06 s; e) 1.87 s.",
        "Given maximum rise maxHeight in meters and gravitational acceleration g, return the total flight time in seconds. Ignore air resistance.",
        [{"maxHeight": 2.5, "g": 9.8}, {"maxHeight": 4.9, "g": 9.8},
         {"maxHeight": 8, "g": 10}], lambda maxHeight, g: 2 * math.sqrt(2 * maxHeight / g)),
    problem(4, "Speed at a Given x Coordinate", "speedAtX",
        "A particle moves with constant acceleration ax = 4.0 m/s² and ay = 3.0 m/s². At t = 0 it is at the origin, moving at 8.0 m/s in the +x direction. What is its speed when x = 24.0 m?\nChoices: a) 17.1 m/s; b) 17.9 m/s; c) 18.9 m/s; d) 20.0 m/s; e) 22.0 m/s.",
        "Return the speed in m/s at targetX. The initial velocity is [initialSpeed, 0] and the initial position is [0, 0]. ax > 0, initialSpeed ≥ 0, and targetX ≥ 0.",
        [{"initialSpeed": 8, "ax": 4, "ay": 3, "targetX": 24},
         {"initialSpeed": 0, "ax": 2, "ay": 0, "targetX": 9},
         {"initialSpeed": 3, "ax": 2, "ay": -4, "targetX": 4}], speed_at_x),
    problem(5, "Projectile Hits a Wall on the Way Down", "wallDistance",
        "A ball is kicked from ground level at 25.0 m/s and 53.1° above horizontal. It hits a vertical wall 5 m above the ground while descending. What is the horizontal distance to the wall?\nChoices: a) 41 m; b) 35 m; c) 46 m; d) 52 m; e) 57 m.",
        "Return the horizontal distance in meters when the projectile reaches height on its descending path. Use the later of the two possible times. Ignore air resistance; every height is reachable.",
        [{"speed": 25, "angleDegrees": 53.1, "height": 5, "g": 9.8},
         {"speed": 20, "angleDegrees": 45, "height": 0, "g": 10},
         {"speed": 15, "angleDegrees": 60, "height": 5, "g": 9.8}], wall_distance,
        ("spring-projectile", "A ball follows an arc to a wall, hitting at height h while descending.")),
    problem(6, "Contact Force Between Two Blocks", "contactForceRatio",
        "A force F = 2Mg pushes block A of mass M at 30° from the vertical. A pushes block B of mass 3M on a frictionless horizontal surface. What is the magnitude of the contact force?\nChoices: a) (1/2)Mg; b) (5/6)Mg; c) (7/8)Mg; d) (9/10)Mg; e) (3/4)Mg.",
        "Block A has mass M, block B has mass massRatioB * M, and the applied force is forceWeightMultiple * Mg, directed downwards and to the right. Return contact force divided by Mg, a dimensionless number. The angle is measured FROM VERTICAL.",
        [{"forceWeightMultiple": 2, "massRatioB": 3, "angleFromVerticalDegrees": 30},
         {"forceWeightMultiple": 4, "massRatioB": 1, "angleFromVerticalDegrees": 90},
         {"forceWeightMultiple": 3, "massRatioB": 2, "angleFromVerticalDegrees": 0}],
        lambda forceWeightMultiple, massRatioB, angleFromVerticalDegrees:
            forceWeightMultiple * math.sin(math.radians(angleFromVerticalDegrees)) * massRatioB / (1 + massRatioB),
        ("spring-blocks", "Force F pushes block A downwards and right, 30 degrees from vertical; A pushes B along a frictionless floor.")),
    problem(7, "Static Friction on a Wedge", "staticFrictionRatio",
        "A block m2 = M sits on a wedge inclined 30° above horizontal. A massless rope over a frictionless peg connects it to a hanging block m1 = 0.7M. The coefficient of static friction is 0.577, and the system is in equilibrium. What is the magnitude of friction on m2?\nChoices: a) 0.100Mg; b) 0.200Mg; c) 0.300Mg; d) 0.400Mg; e) 0.500Mg.",
        "The inclined block has mass M and the hanging block has mass hangingMassRatio * M. Return the required friction magnitude divided by Mg. Return −1 if the required force exceeds the maximum available static friction. Account for friction acting in either direction.",
        [{"hangingMassRatio": 0.7, "angleDegrees": 30, "muStatic": 0.577},
         {"hangingMassRatio": 0.3, "angleDegrees": 30, "muStatic": 0.6},
         {"hangingMassRatio": 2, "angleDegrees": 30, "muStatic": 0.1}], static_friction,
        ("spring-wedge", "Block m2 on an incline is connected over a pulley to the hanging block m1.")),
    problem(8, "Radius from String Tension", "radiusCoefficient",
        "An object of mass m attached to a string moves at constant speed v in a circle on a horizontal frictionless table. String tension is 49 times its weight. What is the radius?\nChoices: a) v²/(81g); b) v²/(64g); c) v²/(49g); d) v²/(36g); e) v²/(25g).",
        "For tension = tensionWeightRatio * mg, return the dimensionless coefficient C in r = C * v²/g. Return a number, rather than a formula string.",
        [{"tensionWeightRatio": 49}, {"tensionWeightRatio": 4}, {"tensionWeightRatio": 1}],
        lambda tensionWeightRatio: 1 / tensionWeightRatio,
        ("spring-circle", "An object is attached to a string and moves in a horizontal circle on a table.")),
    problem(9, "Work by the String in Circular Motion", "ropeWork",
        "In the same setup as question 8, an object moves in a circle at constant speed on a frictionless horizontal table. String tension is 49 times its weight. What work does the rope do during one complete revolution?\nChoices: a) 0; b) 50πmgr; c) 72πmgr; d) 98πmgr; e) 128πmgr.",
        "Return the work in joules done by a purely radial string tension over revolutions complete turns at fixed radius and speed. Inputs mass, speed, and radius are in SI units.",
        [{"mass": 1, "speed": 7, "radius": 1 / 9.8, "revolutions": 1},
         {"mass": 2, "speed": 4, "radius": 3, "revolutions": 2},
         {"mass": 0.2, "speed": 10, "radius": 0.5, "revolutions": 3}],
        lambda mass, speed, radius, revolutions: 0.0,
        ("spring-circle", "Tension points towards the center while the object's motion is tangential.")),
    problem(10, "Work Done by an Opposing Wind", "windWorkRatio",
        "A block starts from rest on a frictionless horizontal surface. A constant force F acts through distance d, giving final speed v. With the same force and distance but an opposing wind, the final speed is (7/29)v. What work did the wind do?\nChoices: a) −672Fd/841; b) −720Fd/841; c) −760Fd/841; d) −792Fd/841; e) −816Fd/841.",
        "speedRatio is final speed with wind divided by final speed without wind. Return wind work divided by Fd, including its sign. Both trials start from rest.",
        [{"speedRatio": 7 / 29}, {"speedRatio": 0.5}, {"speedRatio": 1}],
        lambda speedRatio: speedRatio**2 - 1),
]
SPRING[8]["cases"][0]["label"] = "Exam setup (m = 1 kg, v = 7 m/s)"


FALL = [
    problem(1, "A Boat's Total Displacement", "resultantDisplacement",
        "On a large lake, a motor boat travels 500 m east, then 400 m at 30° north of east, then 100 m west. What is the magnitude of its total displacement?\nChoices: a) 584 m; b) 629 m; c) 677 m; d) 725 m; e) 773 m.",
        "displacements contains [magnitude in meters, angle in degrees counterclockwise from east] pairs. Return the magnitude of their sum in meters. East is 0°, north 90°, west 180°, south 270°.",
        [{"displacements": [[500, 0], [400, 30], [100, 180]]},
         {"displacements": [[6, 0], [8, 90]]},
         {"displacements": [[10, 180], [4, 0]]}], resultant),
    problem(2, "Two Stones Dropped at Different Times", "stoneSeparation",
        "A stone is dropped from a high building. A second stone is dropped 1.5 s later. How far apart are they when the first stone reaches 30 m/s?\nChoices: a) 43.0 m; b) 37.0 m; c) 40.0 m; d) 34.0 m; e) 31.0 m.",
        "Both stones start from rest at the same height. Return their vertical separation in meters when the first reaches firstSpeed. The second is released delay seconds later; inputs guarantee both are falling and neither has hit the ground.",
        [{"firstSpeed": 30, "delay": 1.5, "g": 9.8},
         {"firstSpeed": 20, "delay": 1, "g": 10},
         {"firstSpeed": 9.8, "delay": 0, "g": 9.8}],
        lambda firstSpeed, delay, g: 0.5 * g * ((firstSpeed / g)**2 - (firstSpeed / g - delay)**2)),
    problem(3, "Distance During Uniform Acceleration", "acceleratingDistance",
        "A bicycle travels at 3 m/s, then accelerates uniformly for 10 s until its speed is 9 m/s. How far does it travel in those 10 s?\nChoices: a) 70.0 m; b) 60.0 m; c) 40.0 m; d) 80.0 m; e) 50.0 m.",
        "Return distance in meters for uniform acceleration from initialSpeed to finalSpeed over time seconds. Motion stays in the same direction; all speeds and time are nonnegative.",
        [{"initialSpeed": 3, "finalSpeed": 9, "time": 10},
         {"initialSpeed": 10, "finalSpeed": 2, "time": 4},
         {"initialSpeed": 5, "finalSpeed": 5, "time": 3}],
        lambda initialSpeed, finalSpeed, time: (initialSpeed + finalSpeed) * time / 2),
    problem(4, "Tension in an Accelerating Elevator", "upperCordTension",
        "A 5 kg pail hangs by a massless cord from a 3 kg pail, itself suspended from the ceiling of an elevator. What is the upper-cord tension when the elevator accelerates downwards at 1.2 m/s²?\nChoices: a) 64.0 N; b) 61.5 N; c) 68.8 N; d) 71.2 N; e) 66.4 N.",
        "Return upper-cord tension in newtons. upperMass and lowerMass are kilograms. accelerationDown is signed: positive means downwards, negative means upwards. The cord remains taut or reaches zero tension.",
        [{"upperMass": 3, "lowerMass": 5, "accelerationDown": 1.2, "g": 9.8},
         {"upperMass": 2, "lowerMass": 3, "accelerationDown": -2, "g": 10},
         {"upperMass": 1, "lowerMass": 4, "accelerationDown": 9.8, "g": 9.8}],
        lambda upperMass, lowerMass, accelerationDown, g: (upperMass + lowerMass) * (g - accelerationDown),
        ("fall-elevator", "Two pails hang one below the other from cords attached to the elevator ceiling.")),
    problem(5, "Range of a Jump", "jumpRange",
        "A jumper leaves the ground at 12° above horizontal at 6.3 m/s. Find the horizontal distance traveled while in the air.\nChoices: a) 1.65 m; b) 2.21 m; c) 2.86 m; d) 3.02 m; e) 3.59 m.",
        "Return the range in meters for launch speed speed and angleDegrees. Landing is at launch height. Ignore air resistance.",
        [{"speed": 6.3, "angleDegrees": 12, "g": 9.8},
         {"speed": 10, "angleDegrees": 45, "g": 10},
         {"speed": 20, "angleDegrees": 30, "g": 9.8}],
        lambda speed, angleDegrees, g: speed**2 * math.sin(2 * math.radians(angleDegrees)) / g),
    problem(6, "Tangential and Radial Acceleration", "circularAcceleration",
        "A car starts from rest on a circular path of radius 6.5 m, with tangential acceleration 2 m/s². Find the magnitude of its acceleration after 2.3 s. Consider both tangential and radial acceleration.\nChoices: a) 2.84 m/s²; b) 3.19 m/s²; c) 3.46 m/s²; d) 3.82 m/s²; e) 2.56 m/s².",
        "Return total acceleration magnitude in m/s² after time seconds. The car starts from rest and tangentialAcceleration remains constant and nonnegative; radius > 0.",
        [{"radius": 6.5, "tangentialAcceleration": 2, "time": 2.3},
         {"radius": 4, "tangentialAcceleration": 1, "time": 2},
         {"radius": 10, "tangentialAcceleration": 3, "time": 0}],
        lambda radius, tangentialAcceleration, time:
            math.hypot(tangentialAcceleration, (tangentialAcceleration * time)**2 / radius)),
    problem(7, "Friction on an Incline at Constant Speed", "kineticFrictionCoefficient",
        "A hockey puck slides down a 33° incline at constant velocity. Find the coefficient of kinetic friction.\nChoices: a) 0.231; b) 0.424; c) 0.649; d) 0.756; e) 0.933.",
        "Return the dimensionless coefficient of kinetic friction for an object sliding down an incline at constant velocity. Only gravity, the normal force, and kinetic friction act; 0° ≤ angleDegrees < 90°.",
        [{"angleDegrees": 33}, {"angleDegrees": 45}, {"angleDegrees": 0}],
        lambda angleDegrees: math.tan(math.radians(angleDegrees))),
    problem(8, "Apparent Weight at the Top of a Hill", "hillNormalForce",
        "You travel in a car at constant speed 10 m/s. On a horizontal road, the seat's normal force on you is 500 N. The road goes over a circular hill of radius 100 m. What is the normal force at its top?\nChoices: a) 385 N; b) 449 N; c) 181 N; d) 296 N; e) 526 N.",
        "levelNormal is your normal force on a level road in newtons. Return the seat's normal force at the top of a convex circular hill, in newtons. Return zero if maintaining contact would require a negative normal force.",
        [{"levelNormal": 500, "speed": 10, "radius": 100, "g": 9.8},
         {"levelNormal": 600, "speed": 0, "radius": 20, "g": 10},
         {"levelNormal": 500, "speed": 20, "radius": 10, "g": 9.8}],
        lambda levelNormal, speed, radius, g: max(0.0, levelNormal * (1 - speed**2 / (g * radius)))),
    problem(9, "Ice in a Bowl on a Scale", "bowlScaleReading",
        "A bowl sits on a scale tared to zero with the bowl empty. Its inner surface is hemispherical with radius 0.2 m. A frictionless 0.1 kg ice cube falls from rest 0.1 m above the rim and continues smoothly down the inner wall. What does the scale read when the ice reaches the bottom? The scale reads a normal force.\nChoices: a) 2.92 N; b) 4.90 N; c) 3.92 N; d) 6.86 N; e) 5.88 N.",
        "Return the instantaneous scale reading in newtons at the bottom. mass is the ice mass in kilograms, radius the bowl radius in meters, and heightAboveRim the initial drop height above the rim. The bowl is fixed, and all motion is frictionless.",
        [{"mass": 0.1, "radius": 0.2, "heightAboveRim": 0.1, "g": 9.8},
         {"mass": 1, "radius": 0.5, "heightAboveRim": 0, "g": 10},
         {"mass": 0.2, "radius": 0.4, "heightAboveRim": 0.4, "g": 9.8}],
        lambda mass, radius, heightAboveRim, g: mass * g * (1 + 2 * (heightAboveRim + radius) / radius),
        ("fall-bowl", "Ice falls from height Y above the rim into a hemispherical bowl of radius R on a tared scale.")),
    problem(10, "Friction from an Energy Change", "slopeFriction",
        "A 1 kg mass slides from rest down a uniform slope, traveling 40 m along the slope and dropping 10 m vertically. Its speed at the bottom is 7 m/s. What is the frictional force? Gravity does positive work and friction negative work.\nChoices: a) 1.23 N; b) 1.05 N; c) 1.56 N; d) 1.47 N; e) 1.84 N.",
        "Return the magnitude of constant friction in newtons. slopeDistance is distance along the slope, heightDrop is vertical loss, and finalSpeed is the bottom speed. The mass starts from rest, and gravity and friction are the only forces doing work. Inputs give nonnegative friction.",
        [{"mass": 1, "slopeDistance": 40, "heightDrop": 10, "finalSpeed": 7, "g": 9.8},
         {"mass": 2, "slopeDistance": 10, "heightDrop": 5, "finalSpeed": 0, "g": 10},
         {"mass": 1, "slopeDistance": 8, "heightDrop": 5, "finalSpeed": 10, "g": 10}],
        lambda mass, slopeDistance, heightDrop, finalSpeed, g:
            (mass * g * heightDrop - 0.5 * mass * finalSpeed**2) / slopeDistance),
]

"""Additional papers, curriculum metadata, and general numerical cases."""
from copy import deepcopy
import math

from midterms import FALL, SPRING, problem

G = 6.67e-11
UNITS = {
    "vectors": "Vectors & relative motion", "kinematics": "Kinematics & projectiles",
    "forces": "Newton's laws & friction", "circular": "Circular motion",
    "energy": "Work & energy", "momentum": "Momentum & collisions",
    "rotation": "Rotation & angular momentum", "equilibrium": "Static equilibrium",
    "gravity": "Gravitation & orbits", "oscillations": "Oscillations",
}


def p(n, title, method, unit, story, task, inputs, reference):
    value = problem(n, title, method, story, task, inputs, reference)
    value["unit"] = unit
    return value


def balloon(ledgeHeight, timeAfterLedge, g):
    speed = (ledgeHeight - .5 * g * timeAfterLedge**2) / timeAfterLedge
    if speed < 0:
        raise ValueError("The balloon must already be moving down at the ledge.")
    return speed**2 / (2 * g)


MIDTERM_S25 = [
    p(1, "The Bowling Ball and the Returning Sound", "bowlingSpeed", "kinematics",
      "A bowling ball rolls at constant speed down a 16.5 m lane. The bowler hears it strike the pins 2.75 s after release. Sound travels back at 340 m/s. Find the ball's speed.",
      "Return the ball speed in m/s. totalTime includes the ball's outward trip and the sound's return trip; totalTime > laneLength / soundSpeed.",
      [dict(laneLength=16.5,totalTime=2.75,soundSpeed=340),dict(laneLength=20,totalTime=4.1,soundSpeed=200),dict(laneLength=10,totalTime=2.5,soundSpeed=20)],
      lambda laneLength,totalTime,soundSpeed: laneLength/(totalTime-laneLength/soundSpeed)),
    p(2, "A Balloon Passes a Ledge", "balloonReleaseHeight", "kinematics",
      "A pigeon sits on a ledge 20 m above a sidewalk. A balloon, dropped from rest, passes the ledge and hits the sidewalk 0.92 s later. How far above the ledge was it released?",
      "Return the release height ABOVE the ledge in meters, given ledgeHeight, timeAfterLedge, and g. Ignore air resistance.",
      [dict(ledgeHeight=20,timeAfterLedge=.92,g=9.8),dict(ledgeHeight=15,timeAfterLedge=1,g=10),dict(ledgeHeight=5,timeAfterLedge=1,g=10)],balloon),
    p(3, "Drifting Across a River", "riverDrift", "vectors",
      "A boat heads directly north across a 725 m wide river at 5 m/s relative to the water. A current flows east at 3 m/s. How far east of the opposite point does the boat arrive?",
      "Return downstream drift in meters. The boat points perpendicular to the banks. boatSpeed is relative to the water, and currentSpeed is parallel to the banks.",
      [dict(width=725,boatSpeed=5,currentSpeed=3),dict(width=100,boatSpeed=2,currentSpeed=1),dict(width=40,boatSpeed=4,currentSpeed=0)],
      lambda width,boatSpeed,currentSpeed: width*currentSpeed/boatSpeed),
    p(4, "An Arrow on Another Planet", "arrowDistanceRatio", "kinematics",
      "An arrow launched horizontally travels distance L before hitting below the bullseye on Earth. On a planet with 35% of Earth's gravity, the same arrow speed must give the same vertical drop. How far away should the astronaut stand?",
      "Return the new horizontal distance divided by L. gravityRatio is planet gravity / Earth gravity; the launch speed and vertical drop stay fixed.",
      [dict(gravityRatio=.35),dict(gravityRatio=.25),dict(gravityRatio=1)],lambda gravityRatio:1/math.sqrt(gravityRatio)),
    p(5, "Pulling a Crate Up an Incline", "inclineAcceleration", "forces",
      "A 12 N force pulls a 2.1 kg crate UP a frictionless incline tilted 30° above horizontal. Find its acceleration along the incline.",
      "Return signed acceleration in m/s², positive UP the incline. pullForce acts parallel to the surface.",
      [dict(mass=2.1,pullForce=12,angleDegrees=30,g=9.8),dict(mass=2,pullForce=20,angleDegrees=30,g=10),dict(mass=1,pullForce=0,angleDegrees=30,g=10)],
      lambda mass,pullForce,angleDegrees,g:pullForce/mass-g*math.sin(math.radians(angleDegrees))),
    p(6, "Two Hanging Masses", "atwoodAcceleration", "forces",
      "Two blocks of masses 25 kg and 30 kg hang from opposite sides of a massless string over a massless, frictionless pulley. Find the acceleration magnitude.",
      "Return the magnitude in m/s²; either mass may be the heavier one. Ignore the mass of the rope and pulley.",
      [dict(mass1=25,mass2=30,g=9.8),dict(mass1=1,mass2=3,g=10),dict(mass1=4,mass2=4,g=9.8)],
      lambda mass1,mass2,g:abs(mass2-mass1)*g/(mass1+mass2)),
    p(7, "Revolutions per Minute from Tension", "stringRPM", "circular",
      "A 0.2 kg stone moves in a circle of radius 0.6 m on a frictionless horizontal surface. String tension is 30 N. How many revolutions per minute does it make?",
      "Return revolutions per minute, given mass in kg, radius in meters, and tension in newtons.",
      [dict(mass=.2,radius=.6,tension=30),dict(mass=1,radius=1,tension=4),dict(mass=2,radius=.5,tension=0)],
      lambda mass,radius,tension:60/(2*math.pi)*math.sqrt(tension/(mass*radius))),
    p(8, "An Inclined Block Moves at Constant Speed", "inclinePulleyFriction", "forces",
      "Equal masses are connected over a massless, frictionless pulley. One hangs vertically; the other slides UP a 27° incline at constant speed. Find the kinetic-friction coefficient.",
      "Return the coefficient of kinetic friction for equal masses, with the inclined block moving UP at constant speed. The incline angle is above horizontal.",
      [dict(angleDegrees=27),dict(angleDegrees=30),dict(angleDegrees=0)],
      lambda angleDegrees:(1-math.sin(math.radians(angleDegrees)))/math.cos(math.radians(angleDegrees))),
    p(9, "Sliding to a Stop", "stoppingDistance", "energy",
      "A 10 kg box slides along horizontal ground at 3.1 m/s. The coefficient of kinetic friction is 0.30. How far does it slide before stopping?",
      "Return stopping distance in meters. mass is included to let you check whether it affects your result. muK > 0; the only horizontal force is kinetic friction.",
      [dict(mass=10,initialSpeed=3.1,muK=.3,g=9.8),dict(mass=1,initialSpeed=10,muK=.5,g=10),dict(mass=20,initialSpeed=0,muK=.2,g=9.8)],
      lambda mass,initialSpeed,muK,g:initialSpeed**2/(2*muK*g)),
    p(10, "Speed After More Work", "distanceSpeedRatio", "energy",
      "A constant horizontal force accelerates a block from rest on a frictionless surface. After distance d its speed is v. It then travels an ADDITIONAL 8d. What is its new speed in units of v?",
      "Return final speed / v. extraDistanceRatio is the ADDITIONAL distance divided by d, not total distance divided by d.",
      [dict(extraDistanceRatio=8),dict(extraDistanceRatio=3),dict(extraDistanceRatio=0)],lambda extraDistanceRatio:math.sqrt(1+extraDistanceRatio)),
]


def gravity(planetMass,planetRadiusKm,altitudeKm,G):
    return G*planetMass/((planetRadiusKm+altitudeKm)*1000)**2


FINAL_F25 = [
    p(1,"A Rocket Fragment Launched Horizontally","horizontalRange","kinematics",
      "A fireworks rocket explodes 32 m above the ground. A fragment is thrown horizontally at 67 m/s. How far horizontally does it travel before hitting the ground?",
      "Return range in meters for a horizontal launch from height, with horizontalSpeed and zero initial vertical speed. Ignore air resistance.",
      [dict(height=32,horizontalSpeed=67,g=9.8),dict(height=5,horizontalSpeed=10,g=10),dict(height=20,horizontalSpeed=0,g=10)],lambda height,horizontalSpeed,g:horizontalSpeed*math.sqrt(2*height/g)),
    p(2,"The Speed Limit on a Flat Curve","flatCurveSpeed","circular",
      "A car travels around a flat circular road of radius 63 m. The coefficient of static friction is 0.6. Find the maximum speed without skidding.",
      "Return maximum speed in m/s. The road is unbanked; static friction supplies the horizontal centripetal force.",
      [dict(radius=63,muStatic=.6,g=9.8),dict(radius=50,muStatic=.5,g=10),dict(radius=20,muStatic=0,g=9.8)],lambda radius,muStatic,g:math.sqrt(muStatic*g*radius)),
    p(3,"Speed from Net Work","speedFromWork","energy",
      "Net work of 24.4 J is done on a 0.42 kg object initially at rest. What is its final speed?",
      "Return final speed in m/s for netWork joules, mass kg, and initialSpeed m/s. Inputs have nonnegative final kinetic energy.",
      [dict(netWork=24.4,mass=.42,initialSpeed=0),dict(netWork=-6,mass=2,initialSpeed=3),dict(netWork=0,mass=4,initialSpeed=5)],lambda netWork,mass,initialSpeed:math.sqrt(initialSpeed**2+2*netWork/mass)),
    p(4,"A Block Released from a Spring","springSpeed","energy",
      "A 2.3 kg block on a horizontal frictionless surface is attached to a 120 N/m spring, compressed 0.3 m and released from rest. What is its speed 0.1 m from equilibrium?",
      "Return speed in m/s. initialCompression is the amplitude in meters; displacement can be on either side of equilibrium and its magnitude does not exceed the amplitude.",
      [dict(mass=2.3,springConstant=120,initialCompression=.3,displacement=.1),dict(mass=1,springConstant=100,initialCompression=.2,displacement=0),dict(mass=2,springConstant=20,initialCompression=.3,displacement=-.3)],lambda mass,springConstant,initialCompression,displacement:math.sqrt(max(0,springConstant/mass*(initialCompression**2-displacement**2)))),
    p(5,"Work Done by Kinetic Friction","frictionWork","energy",
      "A 3.4 kg block travels 7 m along a rough horizontal surface with kinetic-friction coefficient 0.73. Find the work done by kinetic friction.",
      "Return SIGNED work in joules. distance is nonnegative, and friction opposes the displacement.",
      [dict(mass=3.4,distance=7,muK=.73,g=9.8),dict(mass=2,distance=4,muK=.5,g=10),dict(mass=1,distance=0,muK=.2,g=9.8)],lambda mass,distance,muK,g:-muK*mass*g*distance),
    p(6,"An Explosion into Three Fragments","thirdFragmentSpeed","momentum",
      "A 5 kg mass at rest explodes into three fragments. A 1 kg fragment moves at [10, 0] m/s and another 1 kg fragment at [0, 10] m/s. Find the third fragment's speed.",
      "Return the third fragment's speed in m/s. velocity1 and velocity2 are [vx, vy]. The original object is at rest and totalMass > mass1 + mass2.",
      [dict(totalMass=5,mass1=1,velocity1=[10,0],mass2=1,velocity2=[0,10]),dict(totalMass=6,mass1=2,velocity1=[3,0],mass2=1,velocity2=[-6,0]),dict(totalMass=4,mass1=1,velocity1=[2,3],mass2=1,velocity2=[2,3])],lambda totalMass,mass1,velocity1,mass2,velocity2:math.hypot(*(mass1*a+mass2*b for a,b in zip(velocity1,velocity2)))/(totalMass-mass1-mass2)),
    p(7,"A Golf Ball Hits an Oncoming Bus","elasticBallSpeed","momentum",
      "A 0.050 kg golf ball moving at −10 m/s collides elastically with a 10,000 kg bus moving at +10 m/s. Find the ball's speed after the collision. The bus is so massive that 30 m/s is an excellent approximation.",
      "Return the ball's speed magnitude using the EXACT one-dimensional elastic-collision equations for the two finite masses. velocityBall and velocityBus are signed along the same axis.",
      [dict(massBall=.05,velocityBall=-10,massBus=10000,velocityBus=10),dict(massBall=1,velocityBall=4,massBus=1,velocityBus=0),dict(massBall=2,velocityBall=-3,massBus=6,velocityBus=2)],lambda massBall,velocityBall,massBus,velocityBus:abs(((massBall-massBus)*velocityBall+2*massBus*velocityBus)/(massBall+massBus))),
    p(8,"An Atwood Machine with a Massive Pulley","massivePulleySpeed","rotation",
      "Masses of 10 kg and 17 kg hang from a rope over a solid-disk pulley of mass 10 kg and moment of inertia 1.25 kg·m². Released from rest, the heavier mass falls 1 m. Find its speed. The rope does not slip.",
      "Return speed in m/s after dropHeight. Infer pulley radius from its SOLID-DISK inertia and mass; include translational and rotational kinetic energy. heavierMass ≥ lighterMass.",
      [dict(lighterMass=10,heavierMass=17,pulleyMass=10,pulleyInertia=1.25,dropHeight=1,g=9.8),dict(lighterMass=1,heavierMass=3,pulleyMass=4,pulleyInertia=.5,dropHeight=2,g=10),dict(lighterMass=2,heavierMass=2,pulleyMass=3,pulleyInertia=.2,dropHeight=1,g=9.8)],lambda lighterMass,heavierMass,pulleyMass,pulleyInertia,dropHeight,g:math.sqrt(2*(heavierMass-lighterMass)*g*dropHeight/(lighterMass+heavierMass+pulleyMass/2))),
    p(9,"Pulling a Lawnmower Starter Cord","torqueTime","rotation",
      "A flywheel starts from rest with moment of inertia 1 kg·m². A constant 15 N·m torque gives it 100 J of rotational kinetic energy. How long was the cord pulled?",
      "Return elapsed time in seconds for a constant positive torque, given inertia and final rotational energy. The wheel starts at rest.",
      [dict(inertia=1,torque=15,energy=100),dict(inertia=2,torque=4,energy=16),dict(inertia=3,torque=10,energy=0)],lambda inertia,torque,energy:math.sqrt(2*inertia*energy)/torque),
    p(10,"Reversing a Space Station's Axis","reorientationTorque","rotation",
      "A space station is a thin hoop of mass 10⁵ kg and radius 1 km, spinning once every 150 s. Steering rockets reverse its axis from +k to −k over 1 hour without changing its spin rate. Find the magnitude of the average torque.",
      "Return average torque magnitude in N·m for a hoop. axisAngleDegrees is the angle BETWEEN initial and final angular-momentum vectors. radius is in meters, period and duration in seconds.",
      [dict(mass=1e5,radius=1000,period=150,duration=3600,axisAngleDegrees=180),dict(mass=10,radius=2,period=4,duration=2,axisAngleDegrees=90),dict(mass=5,radius=1,period=2,duration=3,axisAngleDegrees=0)],lambda mass,radius,period,duration,axisAngleDegrees:2*mass*radius**2*(2*math.pi/period)*math.sin(math.radians(axisAngleDegrees)/2)/duration),
    p(11,"A Painter on a Suspended Board","rightRopeTension","equilibrium",
      "A uniform 3 m board of mass 12 kg hangs from vertical ropes at its ends. An 85 kg painter stands 1 m from the left end. Find the tension in the RIGHT rope.",
      "Return right-rope tension in newtons. painterPosition is measured from the left end; the uniform board's center of mass is at its midpoint. The system is stationary.",
      [dict(length=3,boardMass=12,painterMass=85,painterPosition=1,g=9.8),dict(length=4,boardMass=10,painterMass=20,painterPosition=2,g=10),dict(length=2,boardMass=8,painterMass=30,painterPosition=0,g=9.8)],lambda length,boardMass,painterMass,painterPosition,g:(boardMass*g*length/2+painterMass*g*painterPosition)/length),
    p(12,"Gravity Above Earth's Surface","gravityAtAltitude","gravity",
      "Find gravitational acceleration at an altitude of 5500 km above Earth. Use Earth mass 5.97 × 10²⁴ kg, radius 6370 km, and G = 6.67 × 10⁻¹¹ N·m²/kg².",
      "Return gravitational acceleration in m/s². planetRadiusKm and altitudeKm are kilometers; use the distance from the planet's CENTER.",
      [dict(planetMass=5.97e24,planetRadiusKm=6370,altitudeKm=5500,G=G),dict(planetMass=5.97e24,planetRadiusKm=6370,altitudeKm=0,G=G),dict(planetMass=6e24,planetRadiusKm=6000,altitudeKm=6000,G=G)],gravity),
    p(13,"The Orbital Period of Io","orbitalPeriodDays","gravity",
      "Io orbits Jupiter at center-to-center distance 422 × 10⁶ m. Jupiter's mass is 1.90 × 10²⁷ kg. Assuming a circular orbit, find the period in Earth days.",
      "Return the circular-orbit period in Earth days (86,400 seconds per day). orbitalRadius is measured from the planet's center in meters.",
      [dict(orbitalRadius=422e6,planetMass=1.9e27,G=G),dict(orbitalRadius=7e6,planetMass=5.97e24,G=G),dict(orbitalRadius=1e8,planetMass=1e25,G=G)],lambda orbitalRadius,planetMass,G:2*math.pi*math.sqrt(orbitalRadius**3/(G*planetMass))/86400),
    p(14,"A Spring's Period from Its Stretch","springPeriodFromStretch","oscillations",
      "A 2.5 kg block hangs at rest from a vertical spring, stretching it 15 cm. After a small push it oscillates. Find its period.",
      "Return period in seconds. stretchCm is the STATIC equilibrium stretch in centimeters. mass is in kg; neglect damping.",
      [dict(mass=2.5,stretchCm=15,g=9.8),dict(mass=1,stretchCm=25,g=10),dict(mass=10,stretchCm=100,g=9.8)],lambda mass,stretchCm,g:2*math.pi*math.sqrt(stretchCm/100/g)),
    p(15,"A Pendulum on Another Planet","pendulumPeriod","oscillations",
      "A simple pendulum has period 3.5 s on Earth. What is its period on a planet where gravitational acceleration is 7 m/s²?",
      "Return the new small-angle period in seconds. Pendulum length stays fixed; gravityEarth and gravityPlanet are in m/s².",
      [dict(periodEarth=3.5,gravityEarth=9.8,gravityPlanet=7),dict(periodEarth=2,gravityEarth=10,gravityPlanet=2.5),dict(periodEarth=5,gravityEarth=9.8,gravityPlanet=9.8)],lambda periodEarth,gravityEarth,gravityPlanet:periodEarth*math.sqrt(gravityEarth/gravityPlanet)),
]

FINAL_S25 = [
    p(1,"Two Balls Meet in Midair","collisionHeight","kinematics",
      "One ball is dropped from a 30 m roof. Simultaneously, another is thrown vertically upward from the ground at 20 m/s, aimed at the falling ball. At what height do they collide?",
      "Return collision height above ground in meters. Both balls share the same g; inputs guarantee a collision before either hits the ground.",
      [dict(buildingHeight=30,launchSpeed=20,g=9.8),dict(buildingHeight=20,launchSpeed=20,g=10),dict(buildingHeight=10,launchSpeed=10,g=10)],lambda buildingHeight,launchSpeed,g:buildingHeight-.5*g*(buildingHeight/launchSpeed)**2),
    p(2,"A Rough Table and a Hanging Block","tablePulleyAcceleration","forces",
      "A 7 kg block on a horizontal surface is connected over a massless pulley to a hanging 4 kg block. The kinetic-friction coefficient on the table is 0.25. Find the acceleration magnitude as the hanging block moves down.",
      "Return acceleration magnitude in m/s² while the hanging block moves down. Inputs have hangingMass ≥ muK * tableMass.",
      [dict(tableMass=7,hangingMass=4,muK=.25,g=9.8),dict(tableMass=2,hangingMass=3,muK=.5,g=10),dict(tableMass=4,hangingMass=2,muK=.5,g=9.8)],lambda tableMass,hangingMass,muK,g:(hangingMass-muK*tableMass)*g/(tableMass+hangingMass)),
    p(3,"Net Work Down a Rough Ramp","roughRampWork","energy",
      "A 2 kg block slides from rest down a 25° ramp with kinetic-friction coefficient 0.20. What is the TOTAL work done as its vertical height decreases by 1 m?",
      "Return net work in joules. heightDrop is the VERTICAL drop, not distance along the ramp. angleDegrees is above horizontal.",
      [dict(mass=2,angleDegrees=25,muK=.2,heightDrop=1,g=9.8),dict(mass=1,angleDegrees=45,muK=.5,heightDrop=2,g=10),dict(mass=2,angleDegrees=30,muK=0,heightDrop=1,g=10)],lambda mass,angleDegrees,muK,heightDrop,g:mass*g*heightDrop*(1-muK/math.tan(math.radians(angleDegrees)))),
    p(4,"Speed at a Fraction of Maximum Height","projectileFractionSpeed","energy",
      "A projectile launches at 30 m/s and 30° above horizontal. What is its speed when its height is 0.2 of its maximum height? Ignore air resistance.",
      "Return speed in m/s for heightFraction of maximum height, on either ascent or descent. 0 ≤ heightFraction ≤ 1.",
      [dict(launchSpeed=30,angleDegrees=30,heightFraction=.2),dict(launchSpeed=10,angleDegrees=60,heightFraction=1),dict(launchSpeed=20,angleDegrees=45,heightFraction=0)],lambda launchSpeed,angleDegrees,heightFraction:launchSpeed*math.sqrt(1-heightFraction*math.sin(math.radians(angleDegrees))**2)),
    p(5,"A Roller Coaster Loses Energy","coasterSpeed","energy",
      "A 450 kg roller coaster starts at 6.5 m/s and travels to a point 15 m lower. Friction and air resistance do −6.50 kJ of work. Find the speed at the lower point.",
      "Return final speed in m/s. nonconservativeWork is SIGNED work in JOULES; heightDrop is positive for a descent. Final kinetic energy is nonnegative.",
      [dict(mass=450,initialSpeed=6.5,heightDrop=15,nonconservativeWork=-6500,g=9.8),dict(mass=2,initialSpeed=0,heightDrop=5,nonconservativeWork=0,g=10),dict(mass=1,initialSpeed=4,heightDrop=0,nonconservativeWork=-8,g=10)],lambda mass,initialSpeed,heightDrop,nonconservativeWork,g:math.sqrt(initialSpeed**2+2*g*heightDrop+2*nonconservativeWork/mass)),
    p(6,"A Collision Followed by a Spring Compression","collisionSpringCompression","momentum",
      "A mass 2m moving at speed v₁ collides with a stationary mass 3m on a frictionless surface. They stick together and then compress an ideal spring of stiffness k. Find maximum compression.",
      "Return compression in meters for movingMass and stationaryMass in kg, initialSpeed in m/s, and springConstant in N/m. Treat the sticking collision and the later spring compression as separate stages.",
      [dict(movingMass=2,stationaryMass=3,initialSpeed=10,springConstant=100),dict(movingMass=1,stationaryMass=1,initialSpeed=4,springConstant=8),dict(movingMass=2,stationaryMass=1,initialSpeed=0,springConstant=20)],lambda movingMass,stationaryMass,initialSpeed,springConstant:movingMass*initialSpeed/math.sqrt((movingMass+stationaryMass)*springConstant)),
    p(7,"Two Vehicles Lock Together","carInitialSpeed","momentum",
      "A northbound car collides with an eastbound pickup of equal mass. They stick together and move at 25 m/s, 46° north of east. Find the car's INITIAL speed.",
      "Return the northbound car's initial speed in m/s. northAngleDegrees is the FINAL direction measured north of east; the two vehicles have equal mass.",
      [dict(finalSpeed=25,northAngleDegrees=46),dict(finalSpeed=10,northAngleDegrees=30),dict(finalSpeed=20,northAngleDegrees=90)],lambda finalSpeed,northAngleDegrees:2*finalSpeed*math.sin(math.radians(northAngleDegrees))),
    p(8,"Work to Raise a Circular Orbit","orbitWorkCoefficient","gravity",
      "A satellite moves from a circular orbit of radius 3D to another circular orbit of radius 11D. Find the ratio of required work W to G Mₑ m, expressed as a coefficient of 1/D.",
      "For radii initialRadiusMultiple * D and finalRadiusMultiple * D, return C in W / (G M m) = C / D. Include the change in BOTH kinetic and gravitational potential energy.",
      [dict(initialRadiusMultiple=3,finalRadiusMultiple=11),dict(initialRadiusMultiple=1,finalRadiusMultiple=2),dict(initialRadiusMultiple=4,finalRadiusMultiple=4)],lambda initialRadiusMultiple,finalRadiusMultiple:.5*(1/initialRadiusMultiple-1/finalRadiusMultiple)),
    p(9,"Gravity at 6000 km Altitude","gravityAtAltitude","gravity",
      "Find gravitational acceleration 6000 km above Earth's surface. Use Earth mass 5.97 × 10²⁴ kg, radius 6370 km, and G = 6.67 × 10⁻¹¹ N·m²/kg².",
      "Return gravitational acceleration in m/s². Radius and altitude inputs are kilometers; gravity depends on distance from the planet's CENTER.",
      [dict(planetMass=5.97e24,planetRadiusKm=6370,altitudeKm=6000,G=G),dict(planetMass=5.97e24,planetRadiusKm=6370,altitudeKm=0,G=G),dict(planetMass=6e24,planetRadiusKm=6000,altitudeKm=12000,G=G)],gravity),
    p(10,"Radial Acceleration on a Spinning Disk","diskRadialAcceleration","rotation",
      "A uniform disk of radius 5 cm and mass 7 kg starts at rest with constant angular acceleration 0.1 rad/s². After 80 s, what is the centripetal acceleration of a point on the rim?",
      "Return centripetal acceleration in cm/s². radiusCm is centimeters. mass is supplied to let you consider whether it affects this kinematics calculation.",
      [dict(radiusCm=5,mass=7,angularAcceleration=.1,time=80),dict(radiusCm=10,mass=1,angularAcceleration=2,time=3),dict(radiusCm=4,mass=10,angularAcceleration=1,time=0)],lambda radiusCm,mass,angularAcceleration,time:radiusCm*(angularAcceleration*time)**2),
    p(11,"Finding a Rolling Object's Inertia","rollingInertiaFraction","rotation",
      "An object with rotational inertia I = fMR² rolls down a ramp without slipping, starting at rest. After dropping height H, its speed satisfies v² = (5/3)gH. Find f.",
      "Return inertia fraction f for speedSquaredCoefficient C defined by v² = C * gH. Rolling is without slipping, and 0 < C ≤ 2.",
      [dict(speedSquaredCoefficient=5/3),dict(speedSquaredCoefficient=1),dict(speedSquaredCoefficient=10/7)],lambda speedSquaredCoefficient:2/speedSquaredCoefficient-1),
    p(12,"Children Walk Inward on a Merry-Go-Round","merryGoRoundEnergyRatio","rotation",
      "Two children of mass m each stand at opposite points on the rim of a uniform disk of mass 7m. With no external torque, they walk slowly to the center. Find final total kinetic energy / initial total kinetic energy.",
      "diskMassRatio is disk mass / each child's mass. children start as point masses at the rim and finish at the center. Return Kfinal / Kinitial. The axle is frictionless.",
      [dict(diskMassRatio=7,children=2),dict(diskMassRatio=4,children=2),dict(diskMassRatio=10,children=0)],lambda diskMassRatio,children:1+2*children/diskMassRatio),
    p(13,"How Close to the Edge Before Tipping?","tableEdgeDistance","equilibrium",
      "A symmetric uniform table has mass 27 kg, top length 2.20 m, and legs 1.20 m apart (0.50 m overhang at each end). How close can a 45 kg person sit to an edge without tipping it?",
      "Return the MINIMUM distance from the nearest edge to the person's center of mass in meters. The supports are symmetric about the table center; tableLength ≥ supportSeparation. A zero answer means the edge is safe.",
      [dict(tableMass=27,personMass=45,tableLength=2.2,supportSeparation=1.2),dict(tableMass=10,personMass=10,tableLength=4,supportSeparation=2),dict(tableMass=5,personMass=20,tableLength=4,supportSeparation=2)],lambda tableMass,personMass,tableLength,supportSeparation:max(0,(tableLength-supportSeparation)/2-tableMass*supportSeparation/(2*personMass))),
    p(14,"Position from Speed in Simple Harmonic Motion","shmDisplacementRatio","oscillations",
      "A spring-block oscillator has amplitude A and maximum speed vₘₐₓ. When its speed is (9/41)vₘₐₓ, how far is it from equilibrium in units of A?",
      "Return |x| / A for speedRatio = speed / maximum speed. 0 ≤ speedRatio ≤ 1.",
      [dict(speedRatio=9/41),dict(speedRatio=.6),dict(speedRatio=1)],lambda speedRatio:math.sqrt(1-speedRatio**2)),
    p(15,"A Pendulum in Weaker Gravity","pendulumGravityRatio","oscillations",
      "A simple pendulum has a small-angle period of 10.0 s on Earth. What is its period on a planet with gravity (4/9) of Earth's?",
      "Return period in seconds; gravityRatio is new gravity / old gravity. The pendulum length stays fixed.",
      [dict(initialPeriod=10,gravityRatio=4/9),dict(initialPeriod=2,gravityRatio=.25),dict(initialPeriod=3,gravityRatio=1)],lambda initialPeriod,gravityRatio:initialPeriod/math.sqrt(gravityRatio)),
]


BASE_UNITS = {
    "midterm-s26": ["vectors","kinematics","kinematics","kinematics","kinematics","forces","forces","circular","energy","energy"],
    "midterm-f25": ["vectors","kinematics","kinematics","forces","kinematics","circular","forces","circular","energy","energy"],
    "hw8": ["energy","energy","energy","energy","energy","energy","energy","energy","energy","energy"],
}


def spring_version(letter):
    values={"b":(200,-8.4,4.3,5,15,7,.9,64,13),
            "c":(250,-9.6,5.2,6,20,9,.6,36,5),
            "d":(160,-6.3,3.6,4,10,5,.8,25,11)}[letter]
    west,linear,height,ay,wall,mass,hang,tension,wind=values
    replacements=[("100 m due west",f"{west} m due west"),
                  ("−4.2t",f"{linear:g}t"),("2.5 m",f"{height:g} m"),
                  ("ay = 3.0",f"ay = {ay:.1f}"),("wall 5 m",f"wall {wall} m"),
                  ("mass 3M",f"mass {mass}M"),("0.7M",f"{hang:g}M"),
                  ("49 times",f"{tension} times"),("49 times",f"{tension} times"),
                  ("(7/29)v",f"({wind}/29)v")]
    tasks=deepcopy(SPRING)
    changes=[dict(displacements=[[100,270],[west,180],[150,60]]),dict(linear=linear),dict(maxHeight=height),dict(ay=ay),dict(height=wall),dict(massRatioB=mass),dict(hangingMassRatio=hang),dict(tensionWeightRatio=tension),{},dict(speedRatio=wind/29)]
    for index,(task,change,(old,new)) in enumerate(zip(tasks,changes,replacements)):
        task["unit"]=BASE_UNITS["midterm-s26"][index]
        task["description"]=task["description"].replace(old,new)
        case=task["cases"][0]
        case["input"].update(change)
        case["expected"]=task["_reference"](**case["input"])
    return tasks


def expand_cases(task):
    reference=task.get("_reference")
    if not reference:return
    original=task["cases"][0]["input"]
    seen={str(case["input"]) for case in task["cases"]}
    for factor in (.8,1.1,1.25):
        def scale(value,name):
            if isinstance(value,list): return [scale(x,name) for x in value]
            if name in ("G","children","revolutions"):return value
            return value*factor
        values={k:scale(v,k) for k,v in original.items()}
        # Preserve the documented domains for proportions and angles.
        for name,value in list(values.items()):
            if name in ("speedRatio","heightFraction"):values[name]=min(1,value)
            if "angle" in name.lower():values[name]=min(value,85) if name!="axisAngleDegrees" else min(value,180)
            if name=="displacement" and "initialCompression" in values:
                values[name]=math.copysign(min(abs(value),values["initialCompression"]),value)
        if task["method"]=="collisionHeight" and values["buildingHeight"]-.5*values["g"]*(values["buildingHeight"]/values["launchSpeed"])**2<0:continue
        if task["method"]=="tablePulleyAcceleration" and values["hangingMass"]<values["muK"]*values["tableMass"]:continue
        if task["method"]=="roughRampWork" and values["muK"]>math.tan(math.radians(values["angleDegrees"])):continue
        try:
            result=reference(**values)
            def finite(value):
                if isinstance(value,(list,tuple)):return all(finite(x) for x in value)
                return isinstance(value,str) or isinstance(value,(int,float)) and math.isfinite(value)
            if not finite(result):continue
        except (ValueError,ZeroDivisionError):continue
        if str(values) not in seen:
            task["cases"].append({"label":f"General case {len(task['cases'])}","input":values,"expected":result})
            seen.add(str(values))


def graph_work(points,intervals):
    answer=[]
    for start,end in intervals:
        work=0
        for (x0,y0),(x1,y1) in zip(points,points[1:]):
            a,b=max(start,x0),min(end,x1)
            if b>a:
                fa=y0+(y1-y0)*(a-x0)/(x1-x0)
                fb=y0+(y1-y0)*(b-x0)/(x1-x0)
                work+=(fa+fb)*(b-a)/2
        answer.append(work)
    return answer


def vector_work(force,displacement):
    dot=sum(a*b for a,b in zip(force,displacement))
    cosine=dot/(math.hypot(*force)*math.hypot(*displacement))
    return [dot,math.degrees(math.acos(max(-1,min(1,cosine))))]


def constant_force(mass,initialVelocity,finalPosition,time):
    acceleration=[2*(x-v*time)/time**2 for x,v in zip(finalPosition,initialVelocity)]
    return [.5*mass*sum(v*v for v in initialVelocity),mass*math.hypot(*acceleration),
            math.degrees(math.atan2(acceleration[1],acceleration[0]))%360,
            math.hypot(*(v+a*time for v,a in zip(initialVelocity,acceleration)))]


HOMEWORK_REFERENCES={
 "workByForces":lambda mass,distance,force,angleDegrees:[force*distance*math.cos(math.radians(angleDegrees)),0,0,force*distance*math.cos(math.radians(angleDegrees))],
 "workAndAngle":vector_work,
 "compareCartPush":lambda force,angleDegrees,distance:[force*distance*math.cos(math.radians(angleDegrees)),"same" if angleDegrees==0 else "smaller","same"],
 "workFromGraph":graph_work,
 "drawBow":lambda drawDistance,finalForce:[finalForce/drawDistance,finalForce*drawDistance/2],
 "calibrateSpring":lambda knownMass,knownStretchCm,newMass,targetStretchCm:[newMass/knownMass*knownStretchCm,.5*(knownMass*9.8/(knownStretchCm/100))*(targetStretchCm/100)**2],
 "rockEnergy":lambda mass,initialVelocity,finalVelocity:[.5*mass*sum(v*v for v in initialVelocity),.5*mass*(sum(v*v for v in finalVelocity)-sum(v*v for v in initialVelocity))],
 "energyBetweenPoints":lambda mass,initialSpeed,finalKineticEnergy:[.5*mass*initialSpeed**2,math.sqrt(2*finalKineticEnergy/mass),finalKineticEnergy-.5*mass*initialSpeed**2],
 "constantForceMotion":constant_force,
 "wellPotential":lambda mass,heightAboveRim,wellDepth:[mass*9.8*heightAboveRim,-mass*9.8*wellDepth,-mass*9.8*(heightAboveRim+wellDepth)],
}


def add_papers(sets):
    for key,title,file,tasks,kind,semester,year,version in [
        ("midterm-s25","Midterm · Spring 2025","1013X1aS25.pdf",MIDTERM_S25,"midterm","Spring",2025,"A"),
        *[(f"midterm-s26-{letter}",f"Midterm · Spring 2026 · {letter.upper()}",f"1013X1{letter}S26.pdf",spring_version(letter),"midterm","Spring",2026,letter.upper()) for letter in "bcd"],
        ("final-f25","Final · Fall 2025","1013X2aF25.pdf",FINAL_F25,"exam","Fall",2025,"A"),
        ("final-s25","Final · Spring 2025","1013X2aS25.pdf",FINAL_S25,"exam","Spring",2025,"A"),
    ]:
        sets[key]=dict(title=title,file=file,problems=tasks,kind=kind,semester=semester,year=year,version=version)
    for key,meta in sets.items():
        meta.setdefault("kind","homework" if key=="hw8" else "midterm")
        meta.setdefault("semester","Fall" if key in ("hw8","midterm-f25") else "Spring")
        meta.setdefault("year",2025 if key=="midterm-f25" else 2026)
        meta.setdefault("version","A")
        if key=="midterm-s26":meta["title"]="Midterm · Spring 2026 · A"
        for i,task in enumerate(meta["problems"]):
            task.setdefault("unit",BASE_UNITS.get(key,[])[i] if key in BASE_UNITS else "energy")
            task["uid"]=key+":"+str(task["number"])
            task["set"]=key
            task["family"]=task["method"]
            task["paperTitle"]=meta["title"]
            if key=="hw8":
                task["originalCase"]=1
                task["_reference"]=HOMEWORK_REFERENCES[task["method"]]
            task["scenario"],_,task["task"]=task["description"].partition("\n\nCoding task: ")
            if not task["task"]:
                task["scenario"],separator,rest=task["description"].partition("Return ")
                task["task"]="Return "+rest if separator else task["description"]
                task["task"]=task["task"].split("Original HW8:")[0].strip()
            expand_cases(task)
    return sets

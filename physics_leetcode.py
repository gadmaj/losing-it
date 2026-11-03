#!/usr/bin/env python3
"""HW8 as ten LeetCode-style Python challenges (Python 3.10+).

List problems:       python physics_leetcode.py
Read a problem:      python physics_leetcode.py --show 1
Test your solution:  python physics_leetcode.py 1
Test everything:     python physics_leetcode.py all

Implement the methods in Solution. Each has a demonstration test, your original
homework data, and a further test. Reference answers live in the adjacent JSON
file; the methods below contain no solutions. These are local exercises, not
problems published on leetcode.com. No packages or internet access are needed.

Use g = 9.8 m/s^2. Angles are in degrees. Do not round intermediate results.
The checker accepts numeric answers within absolute or relative error 1e-6.
"""

from __future__ import annotations

import argparse
import inspect
import json
import math
from pathlib import Path


class Solution:
    def workByForces(
        self, mass: float, distance: float, force: float, angleDegrees: float
    ) -> list[float]:
        """1. Push a Box [Easy]

        A worker pushes a box along a horizontal, frictionless floor. A constant
        force points angleDegrees BELOW the horizontal, toward the direction
        of travel. The box remains in contact with the floor.

        Return [workApplied, workNormal, workGravity, workNet], in joules.
        Inputs: mass in kg, distance in m, force in N; mass > 0,
        distance >= 0, force >= 0, 0 <= angleDegrees < 90.

        Original HW8: mass=4.00, distance=6.80, force=16.0, angleDegrees=30.0.
        """
        raise NotImplementedError("Implement problem 1")

    def workAndAngle(
        self, force: list[float], displacement: list[float]
    ) -> list[float]:
        """2. Vector Work and the Included Angle [Easy]

        A constant force [Fx, Fy], in newtons, acts while a particle undergoes
        displacement [dx, dy], in meters. Both vectors are nonzero.

        Return [workJoules, angleDegrees]. The angle is the smaller included
        angle between the vectors, from 0 through 180 degrees.

        Original HW8: force=[8, -5], displacement=[2, 1].
        """
        raise NotImplementedError("Implement problem 2")

    def compareCartPush(
        self, force: float, angleDegrees: float, distance: float
    ) -> list[float | str]:
        """3. Push the Shopping Cart [Easy]

        A shopper pushes with constant force at angleDegrees BELOW horizontal.
        Friction balances the horizontal force, so the cart has constant speed.
        It travels distance meters down the first aisle.

        On a second aisle of the same length, the shopper pushes horizontally
        at the same constant speed. Friction does the same work on both aisles.

        Return [workFirstAisle, forceComparison, workComparison].
        workFirstAisle is the shopper's work in joules. Each comparison is
        "larger", "smaller", or "same", comparing SECOND aisle with FIRST.
        Compare the magnitude of the applied force, then its work.
        force > 0, distance > 0, 0 <= angleDegrees < 90.

        Original HW8: force=26.0, angleDegrees=25.0, distance=46.1.
        """
        raise NotImplementedError("Implement problem 3")

    def workFromGraph(
        self, points: list[list[float]], intervals: list[list[float]]
    ) -> list[float]:
        """4. Work from a Force Graph [Medium]

        points contains [positionMeters, forceNewtons] pairs, ordered by
        strictly increasing position. Straight lines connect neighboring
        points. Forces may be negative.

        For each interval [start, end], return the work in joules as the
        particle moves toward increasing x from start to end. Return answers
        in the same order as intervals. Boundaries may lie between vertices.
        Every interval satisfies points[0][0] <= start <= end <= points[-1][0].
        There are 2 to 1000 points and 1 to 1000 intervals.

        Original HW8 graph:
          A=(0,0), B=(10,6), C=(20,0), D=(25,-3), E=(30,0).
        Original intervals: [[0,20], [20,30], [0,30]].
        """
        raise NotImplementedError("Implement problem 4")

    def drawBow(self, drawDistance: float, finalForce: float) -> list[float]:
        """5. Draw the Bow [Easy]

        An archer draws a bowstring drawDistance meters from its relaxed
        position. The required force increases LINEARLY from zero to
        finalForce newtons. Model the bow as an ideal spring.

        Return [equivalentSpringConstant, workByArcher], in N/m and joules.
        drawDistance > 0 and finalForce > 0.

        Original HW8: drawDistance=0.370, finalForce=253.
        """
        raise NotImplementedError("Implement problem 5")

    def calibrateSpring(
        self,
        knownMass: float,
        knownStretchCm: float,
        newMass: float,
        targetStretchCm: float,
    ) -> list[float]:
        """6. Calibrate a Hanging Spring [Easy]

        An ideal, light spring stretches knownStretchCm CENTIMETERS when
        knownMass kg hangs from it at rest. Replace that mass with newMass kg.

        Return [newEquilibriumStretchCm, workToStretchJoules]. The second value
        is the external work needed to stretch this spring from its relaxed
        length to targetStretchCm, neglecting changes in gravitational energy
        during this separate stretching operation. All extensions are measured
        from the unstretched length.

        knownMass > 0, knownStretchCm > 0; newMass, targetStretchCm >= 0.
        Original HW8: knownMass=3.30, knownStretchCm=2.20, newMass=1.50,
        targetStretchCm=4.00. Return the first answer in cm, NOT meters.
        """
        raise NotImplementedError("Implement problem 6")

    def rockEnergy(
        self,
        mass: float,
        initialVelocity: list[float],
        finalVelocity: list[float],
    ) -> list[float]:
        """7. A Rock Changes Velocity [Easy]

        A rock of mass kg changes from initialVelocity=[vx,vy] to
        finalVelocity=[vx,vy]. Components are in m/s and may be negative.

        Return [initialKineticEnergy, netWork], both in joules. Net work is
        the total work done on the rock during the velocity change.
        mass > 0. Each velocity has exactly two components.

        Original HW8: mass=2.20, initialVelocity=[5.60,-1.40],
        finalVelocity=[8.00,4.00].
        """
        raise NotImplementedError("Implement problem 7")

    def energyBetweenPoints(
        self, mass: float, initialSpeed: float, finalKineticEnergy: float
    ) -> list[float]:
        """8. From Point A to Point B [Easy]

        A particle of mass kg has speed initialSpeed m/s at A and kinetic
        energy finalKineticEnergy joules at B.

        Return [kineticEnergyAtA, speedAtB, netWorkFromAToB], in J, m/s, J.
        mass > 0, initialSpeed >= 0, finalKineticEnergy >= 0.

        Original HW8: mass=0.500, initialSpeed=1.50, finalKineticEnergy=7.90.
        """
        raise NotImplementedError("Implement problem 8")

    def constantForceMotion(
        self,
        mass: float,
        initialVelocity: list[float],
        finalPosition: list[float],
        time: float,
    ) -> list[float]:
        """9. Recover the Constant Force [Medium]

        At t=0, an object of mass kg passes through the ORIGIN with velocity
        initialVelocity=[vx,vy] m/s. A constant net force acts. At time seconds,
        it is at finalPosition=[x,y] meters.

        Return [initialKineticEnergy, forceMagnitude, forceAngleDegrees,
        finalSpeed], in J, N, degrees, m/s. Measure force direction
        counterclockwise from +x and normalize it to [0,360).
        mass > 0, time > 0; both vectors have exactly two components.
        Test inputs guarantee a nonzero net force so its angle is defined.

        Original HW8: mass=5.42, initialVelocity=[5.50,-2.85],
        finalPosition=[8.50,5.00], time=2.00.
        """
        raise NotImplementedError("Implement problem 9")

    def wellPotential(
        self, mass: float, heightAboveRim: float, wellDepth: float
    ) -> list[float]:
        """10. Drop a Stone into a Well [Easy]

        A stone of mass kg is held heightAboveRim meters above a well's rim,
        then dropped. The bottom is wellDepth meters BELOW the rim. Set
        gravitational potential energy to zero AT THE RIM.

        Return [initialPotentialEnergy, finalPotentialEnergy, changeInEnergy],
        all in joules. The last value is FINAL minus INITIAL potential energy,
        not the change in total mechanical energy.
        mass > 0; heightAboveRim >= 0 and wellDepth >= 0.

        Original HW8: mass=0.30, heightAboveRim=1.5, wellDepth=4.8.
        """
        raise NotImplementedError("Implement problem 10")


def _matches(actual: object, expected: object) -> bool:
    if isinstance(expected, str):
        return actual == expected
    if isinstance(expected, (list, tuple)):
        return (
            isinstance(actual, (list, tuple))
            and len(actual) == len(expected)
            and all(_matches(a, e) for a, e in zip(actual, expected))
        )
    if isinstance(expected, (int, float)):
        return (
            isinstance(actual, (int, float))
            and not isinstance(actual, bool)
            and math.isclose(actual, expected, rel_tol=1e-6, abs_tol=1e-6)
        )
    return actual == expected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", nargs="?", help="1 through 10, or 'all'")
    parser.add_argument("--show", type=int, metavar="N", help="read problem N")
    args = parser.parse_args()
    case_path = Path(__file__).with_name("physics_leetcode_cases.json")
    try:
        problems = json.loads(case_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot read {case_path.name}: {error}\n")
    by_number = {p["number"]: p for p in problems}

    if args.show is not None:
        if args.show not in by_number:
            parser.error("--show must be between 1 and 10")
        problem = by_number[args.show]
        method = getattr(Solution, problem["method"])
        print(inspect.getdoc(method))
        example = problem["cases"][0]
        print("\nExample input:")
        print(json.dumps(example["input"], indent=2))
        print("\nExpected output:")
        print(json.dumps(example["expected"]))
        print(f"\nImplement Solution.{problem['method']}{inspect.signature(method)}")
        print(f"Run: python {Path(__file__).name} {args.show}")
        return 0

    if args.problem is None:
        print("HW8 — LeetCode-style Python practice\n")
        for p in problems:
            print(f"{p['number']:2}. {p['title']} — {p['method']}")
        print(f"\nRead: python {Path(__file__).name} --show 1")
        print(f"Test: python {Path(__file__).name} 1")
        return 0

    if args.problem == "all":
        selected = problems
    else:
        try:
            number = int(args.problem)
        except ValueError:
            parser.error("problem must be 1 through 10, or 'all'")
        if number not in by_number:
            parser.error("problem must be 1 through 10, or 'all'")
        selected = [by_number[number]]

    total = passed = 0
    for p in selected:
        print(f"\n{p['number']}. {p['title']}")
        for case in p["cases"]:
            total += 1
            try:
                # Give each case a fresh solution and fresh input containers.
                result = getattr(Solution(), p["method"])(**case["input"])
                if _matches(result, case["expected"]):
                    passed += 1
                    print(f"  PASS — {case['label']}")
                else:
                    print(f"  FAIL — {case['label']}")
                    print(f"    Input:    {case['input']}")
                    print(f"    Expected: {case['expected']}")
                    print(f"    Received: {result!r}")
            except NotImplementedError:
                print(f"  TODO — {case['label']}")
            except Exception as error:
                print(f"  ERROR — {case['label']}: {type(error).__name__}: {error}")
    print(f"\n{passed}/{total} tests passed.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())

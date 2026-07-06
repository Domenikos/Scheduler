"""
Python Dependency & Scheduling Engine
Electrical, Computer, and Biomedical Option Engineering Graduation Pathway Optimizer
This script generates a valid graduation schedule for an Engineering student at ATU,
taking into account completed coursework, prerequisites, co-requisites, and semester restrictions.

Features:
* Select from Electrical Engineering, Computer Engineering, or Biomedical Option course databases
* Seasonal Filtering: Evaluates term restrictions ('Fall' vs 'Spring') before scheduling
* Credit Constrained (Greedy Evaluation): Keeps coursework under 16 hours per term
* Unless otherwise specified, the default maximum hours per semester is 16
* Simultaneous Co-requisite Aggregation: Ensures co-reqs are scheduled in the same term
* Deadlock Detection: Identifies unschedulable course chains with detailed diagnostics
"""

# from collections import defaultdict

class Scheduler:  # Class Scheduler
    """Class-based planner for graduation pathways."""

    def __init__(self, course_db=None, max_hours=16, max_iterations=20):
        self.course_db = course_db if course_db is not None else EE_COURSE_DB
        self.max_hours = max_hours
        self.max_iterations = max_iterations
        self.validate_course_db_references()

    def validate_course_db_references(self):
        """Ensure every prereq/coreq in course_db points to a valid course key."""
        invalid_refs = []
        valid_courses = set(self.course_db.keys())

        for course, (_, _, prereqs, coreqs) in self.course_db.items():
            for prereq in prereqs:
                if prereq not in valid_courses:
                    invalid_refs.append((course, "prereq", prereq))

            for coreq in coreqs:
                if coreq not in valid_courses:
                    invalid_refs.append((course, "coreq", coreq))

        if invalid_refs:
            print("\nInvalid prerequisites/corequisites found in course_db:")
            for course, ref_type, invalid_course in invalid_refs:
                print(
                    f"  ❌ Course '{course}' has invalid {ref_type}: '{invalid_course}'"
                )
            raise SystemExit(1)

    def validate_constraints(self, completed_courses, remaining_courses):
        """
        Validate that all remaining courses can eventually be scheduled.
        Returns (is_valid, issues) where issues is a list of problematic courses.
        """
        issues = []

        for course, (_, restriction, prereqs, coreqs) in remaining_courses.items():
            unmet_prereqs = [
                p for p in prereqs if p not in completed_courses and p in self.course_db
            ]

            # Check if prereqs can be satisfied from remaining courses
            for prereq in unmet_prereqs:
                if prereq not in remaining_courses:
                    issues.append(
                        f"  ❌ {course}: Prerequisite '{prereq}' cannot be satisfied (not in remaining courses)"
                    )

            # Check for circular co-req dependencies
            for coreq in coreqs:
                if coreq in remaining_courses:
                    coreq_info = remaining_courses[coreq]
                    if course in coreq_info[3]:  # Check if coreq lists course back
                        pass  # Circular co-reqs are OK if both are remaining

        return len(issues) == 0, issues

    def generate_schedule(self, completed_courses, start_semester_is_fall=True):
        """
        Generates a valid path to graduation given completed coursework.
        Handles semester pacing, seasonal constraints, and corequisites.
        Includes detailed deadlock diagnostics.
        """
        completed_courses = set(completed_courses)
        remaining_courses = {
            c: info for c, info in self.course_db.items() if c not in completed_courses
        }

        current_fall = start_semester_is_fall
        semester_num = 1
        plan = {}

        while remaining_courses and semester_num <= self.max_iterations:
            current_season = "Fall" if current_fall else "Spring"
            semester_label = f"Semester {semester_num} ({current_season})"

            eligible_this_semester = []

            for course, (
                credits,
                restriction,
                prereqs,
                coreqs,
            ) in remaining_courses.items():
                if restriction != "Any" and restriction != current_season:
                    continue

                prereqs_met = all(p in completed_courses for p in prereqs)
                if prereqs_met:
                    eligible_this_semester.append((course, credits, coreqs))

            semester_backlog = []
            current_hours = 0

            for course, credits, coreqs in sorted(
                eligible_this_semester, key=lambda x: -len(x[2])
            ):
                if current_hours + credits > self.max_hours:
                    continue

                # Check if all co-requisites can be met
                coreqs_met = all(
                    (req in completed_courses)
                    or (req in semester_backlog)
                    or (req in [c[0] for c in eligible_this_semester])
                    for req in coreqs
                )

                if coreqs_met:
                    semester_backlog.append(course)
                    current_hours += credits

            if not semester_backlog:
                print(f"\n⚠️  Scheduling Deadlock at {semester_label}!")
                print(f"Remaining courses: {len(remaining_courses)}")

                is_valid, issues = self.validate_constraints(
                    completed_courses, remaining_courses
                )
                if not is_valid:
                    print("\n📋 Unschedulable Course Issues:")
                    for issue in issues[:5]:
                        print(issue)
                    if len(issues) > 5:
                        print(f"  ... and {len(issues) - 5} more issues")
                else:
                    print("\n📋 Stuck courses (may need alternative sequencing):")
                    for course in list(remaining_courses.keys())[:5]:
                        credits, restriction, prereqs, coreqs = remaining_courses[
                            course
                        ]
                        print(
                            f"  • {course}: Season={restriction}, Prereqs={prereqs}, Coreqs={coreqs}"
                        )

                break

            plan[semester_label] = (semester_backlog, current_hours)

            for course in semester_backlog:
                completed_courses.add(course)
                del remaining_courses[course]

            current_fall = not current_fall
            semester_num += 1

        if remaining_courses:
            print(
                f"\n⚠️  Warning: {len(remaining_courses)} courses remain after {semester_num - 1} semesters"
            )

        return plan


# --------------------------------------------------------------------------
# 2. RUNTIME SIMULATION
# --------------------------------------------------------------------------

if __name__ == "__main__":
    from EE_COURSE_DB import EE_COURSE_DB
    student_history = {
        "ENGL 1013",
        "MATH 2914",
        "CHEM 2124",
        "STEM/TECH 1001",
        "ELEG 1011",
        "Fine Arts I",
        "ENGL 1023",
        "MATH 2924",
        "COMS 1013",
        "COMS 1011",
    }

    COURSE_DB = EE_COURSE_DB  # Use the Electrical Engineering course database for this simulation
    print("\n" + "=" * 60)
    print("ATU Electrical Engineering - Graduation Pathway Optimizer")
    print("=" * 60)
    print(f"\n📚 Student Status: {len(student_history)} courses completed")
    print(f"   Total Courses in Degree: {len(COURSE_DB)}")
    print(f"   Remaining: {len(COURSE_DB) - len(student_history)} courses\n")

    scheduler = Scheduler(course_db=COURSE_DB, max_hours=16, max_iterations=20)
    optimized_plan = scheduler.generate_schedule(
        student_history, start_semester_is_fall=True
    )

    print("=" * 60)
    print("GENERATED SCHEDULE")
    print("=" * 60)

    total_hours = 0
    for semester, (courses, hours) in optimized_plan.items():
        print(f"\n{semester:.<45} {hours:>3} hrs")
        for course in sorted(courses):
            credits = COURSE_DB[course][0]
            print(f"   • {course:<30} {credits:>2} hrs")
        total_hours += hours

    print("\n" + "=" * 60)
    print(f"Total Planned Credits: {total_hours} hours")
    print("=" * 60)

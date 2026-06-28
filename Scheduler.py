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

# Electrical Engineering Course Database
# Course Database Format: 'COURSE_CODE': (Credit_Hours, Term_Restriction, [Prereqs], [Co-reqs])
# Term Restrictions: 'Any', 'Fall', 'Spring'
EE_COURSE_DB = {
    # Semester 1
    "ENGL 1013": (3, "Any", [], []),
    "MATH 2914": (4, "Any", [], []),
    "CHEM 2124": (4, "Any", [], ["CHEM 2120"]),  # Lecture
    "CHEM 2120": (0, "Any", [], ["CHEM 2124"]),  # Lab
    "TECH 1001": (1, "Any", [], []),
    "ELEG 1011": (1, "Any", [], []),
    "Fine Arts I": (3, "Any", [], []),
    # Semester 2
    "ENGL 1023": (3, "Any", ["ENGL 1013"], []),
    "MATH 2924": (4, "Any", ["MATH 2914"], []),
    "COMS 1011": (1, "Any", [], ["COMS 1013"]),  # Lab (no prereq, just co-req)
    "COMS 1013": (3, "Any", [], ["COMS 1011"]),  # Lecture (no prereq, just co-req)
    "ELEG 2134": (4, "Any", ["ELEG 1011"], ["ELEG 2130"]),
    "ELEG 2130": (0, "Any", ["ELEG 1011"], ["ELEG 2134"]),  # Lab
    # Semester 3
    "PHYS 2114": (4, "Any", ["MATH 2924"], ["PHYS 2000"]),  # Lecture
    "PHYS 2000": (0, "Any", ["MATH 2924"], ["PHYS 2114"]),  # Lab
    "MATH 3243": (3, "Any", ["MATH 2924"], []),
    "ELEG 2103": (3, "Any", ["MATH 2924"], []),
    "COMS 2203": (3, "Any", ["COMS 1013"], []),
    "ELEG 3133": (3, "Any", ["ELEG 2134", "COMS 1013"], []),
    # Semester 4
    "PHYS 2124": (4, "Any", ["PHYS 2114"], []),
    "PHYS 2010": (0, "Any", ["PHYS 2114"], ["PHYS 2124"]),  # Lab
    "MATH 2934": (4, "Any", ["MATH 2924"], []),
    "ELEG 2111": (1, "Any", ["ELEG 2103"], ["ELEG 2113"]),  # Lab
    "ELEG 2113": (3, "Any", ["ELEG 2103", "MATH 3243"], ["ELEG 2111"]),
    "STAT 3153": (3, "Any", ["MATH 2924"], []),
    # Semester 5
    "Tech Elective 1": (3, "Any", [], []),
    "ELEG Elective 1": (3, "Any", [], []),
    "ELEG/MCEG 3003": (3, "Any", ["MATH 3243", "ELEG 2113"], []),
    "ELEG 3103": (3, "Fall", ["ELEG 2113"], []),
    "ELEG 3153": (3, "Fall", ["ELEG 2113"], []),
    # Semester 6
    "MATH 2703": (3, "Any", ["MATH 2914"], []),
    "ELEG 3143": (3, "Spring", ["MATH 2934", "PHYS 2124"], []),
    "ELEG 3123": (3, "Spring", ["ELEG 2113", "MATH 3243"], []),
    "ELEG 4103": (3, "Spring", ["ELEG 3103"], []),
    "ELEG/MCEG 4202": (2, "Any", ["ELEG/MCEG 3003"], []),
    # Semester 7
    "Social Science": (3, "Any", [], []),
    "ELEG 4143": (3, "Fall", ["ELEG 3123"], []),
    "ELEG 4113": (3, "Fall", ["ELEG 3123"], []),
    "ELEG 4303": (3, "Any", ["ELEG/MCEG 3003", "ELEG 3123"], []),
    "ELEG 4191": (1, "Any", ["ELEG/MCEG 4202"], []),
    "US History/Gov": (3, "Any", [], []),
    # Semester 8
    "ELEG Elective 2": (3, "Any", [], []),
    "Tech Elective 2": (3, "Any", [], []),
    "Fine Arts II": (3, "Any", [], []),
    "ELEG 4122": (2, "Spring", ["ELEG 4103", "ELEG 4113"], []),
    "ELEG 4192": (2, "Any", ["ELEG 4191"], []),
}

# Computer Engineering Course Database
CMPE_COURSE_DB = {
    # Semester 1
    "ENGL 1013": (3, "Any", [], []),
    "MATH 2914": (4, "Any", [], []),
    "CHEM 2124": (4, "Any", [], ["CHEM 2120"]),  # Lecture
    "CHEM 2120": (0, "Any", [], ["CHEM 2124"]),  # Lab
    "TECH 1001": (1, "Any", [], []),
    "ELEG 1011": (1, "Any", [], []),
    "Fine Arts I": (3, "Any", [], []),
    # Semester 2
    "ENGL 1023": (3, "Any", ["ENGL 1013"], []),
    "MATH 2924": (4, "Any", ["MATH 2914"], []),
    "COMS 1011": (1, "Any", [], ["COMS 1013"]),  # Lab (no prereq, just co-req)
    "COMS 1013": (3, "Any", [], ["COMS 1011"]),  # Lecture (no prereq, just co-req)
    "ELEG 2134": (4, "Any", ["ELEG 1011"], ["ELEG 2130"]),
    "ELEG 2130": (0, "Any", ["ELEG 1011"], ["ELEG 2134"]),  # Lab
    # Semester 3
    "PHYS 2114": (4, "Any", ["MATH 2924"], ["PHYS 2000"]),  # Lecture
    "PHYS 2000": (0, "Any", ["MATH 2924"], ["PHYS 2114"]),  # Lab
    "MATH 3243": (3, "Any", ["MATH 2924"], []),
    "ELEG 2103": (3, "Any", ["MATH 2924"], []),
    "COMS 2203": (3, "Any", ["COMS 1013"], []),
    "ELEG 3133": (3, "Any", ["ELEG 2134", "COMS 1013"], []),
    # Semester 4
    "PHYS 2124": (4, "Any", ["PHYS 2114"], []),
    "PHYS 2010": (0, "Any", ["PHYS 2114"], ["PHYS 2124"]),  # Lab
    "MATH 2934": (4, "Any", ["MATH 2924"], []),
    "ELEG 2111": (1, "Any", ["ELEG 2103"], ["ELEG 2113"]),  # Lab
    "ELEG 2113": (3, "Any", ["ELEG 2103", "MATH 3243"], ["ELEG 2111"]),
    "STAT 3153": (3, "Any", ["MATH 2924"], []),
    # Semester 5
    "ELEG/MCEG 3003": (3, "Any", ["MATH 3243", "ELEG 2113"], []),
    "ELEG 3103": (3, "Fall", ["ELEG 2113"], []),
    "Fine Arts II": (3, "Any", [], []),
    "MATH 2703": (3, "Any", ["MATH 2914"], []),
    "Social Science": (3, "Any", [], []),
    # Semester 6
    "ELEG 3143": (3, "Spring", ["MATH 2934", "PHYS 2124"], []),
    "ELEG 3123": (3, "Spring", ["ELEG 2113", "MATH 3243"], []),
    "ELEG 4103": (3, "Spring", ["ELEG 3103"], []),
    "ELEG/MCEG 4202": (2, "Any", ["ELEG/MCEG 3003"], []),
    "COMS 2213": (3, "Any", ["COMS 2203", "MATH 2703"], []),  # Data Structures
    "COMS 2223": (3, "Any", ["COMS 2203", "MATH 2703"], []),  # Computer Organization
    # Semester 7
    "CMPE 4191": (1, "Any", ["ELEG/MCEG 4202"], []),
    "ELEG 4303": (3, "Any", ["ELEG/MCEG 3003", "ELEG 3123"], []),
    "ELEG 4113": (3, "Fall", ["ELEG 3123"], []),
    "ELEG 4143": (3, "Fall", ["ELEG 3123"], []),
    "ELEG 4133": (3, "Fall", ["ELEG 2134"], []),
    # Semester 8
    "CMPE 4192": (2, "Any", ["CMPE 4191"], []),
    "COMS 3703": (3, "Any", ["COMS 2213"], []),  # Operating Systems
    "ELEG 4122": (2, "Spring", ["ELEG 4103", "ELEG 4113"], []),
    "ELEG Elective 1": (3, "Any", [], []),
    "US History/Gov": (3, "Any", [], []),
}

# Electrical Engineering with Biomedical Option Course Database
# Optional Biomedical Engineering courses beyond those required for the BS degree
# are not included in this version of the scheduler.
BME_COURSE_DB = {
    # Semester 1
    "BIOL 1114": (4, "Any", [], []),
    "ENGL 1013": (3, "Any", [], []),
    "MATH 2914": (4, "Any", [], []),
    "CHEM 2124": (4, "Any", [], ["CHEM 2120"]),  # Lecture
    "CHEM 2120": (0, "Any", [], ["CHEM 2124"]),  # Lab
    "TECH 1001": (1, "Any", [], []),
    "ELEG 1011": (1, "Any", [], []),
    # Semester 2
    "BIOL 2014": (4, "Any", [], []),
    "CHEM 2134": (4, "Any", ["CHEM 2124"], ["CHEM 2130"]),  # Lecture
    "CHEM 2130": (0, "Any", ["CHEM 2124"], ["CHEM 2134"]),  # Lab
    "ENGL 1023": (3, "Any", ["ENGL 1013"], []),
    "MATH 2924": (4, "Any", ["MATH 2914"], []),
    # Semester 3
    "PHYS 2114": (4, "Any", ["MATH 2924"], ["PHYS 2000"]),  # Lecture
    "PHYS 2000": (0, "Any", ["MATH 2924"], ["PHYS 2114"]),  # Lab
    "MATH 3243": (3, "Any", ["MATH 2924"], []),
    "ELEG 2103": (3, "Any", ["MATH 2924"], []),
    "CHEM 3254": (4, "Any", ["CHEM 2134"], ["CHEM 3250"]),  # Lecture
    "CHEM 3250": (0, "Any", ["CHEM 2134"], ["CHEM 3254"]),  # Lab
    # Semester 4
    "ELEG 2111": (1, "Any", ["ELEG 2103"], ["ELEG 2113"]),  # Lab
    "ELEG 2113": (3, "Any", ["ELEG 2103", "MATH 3243"], ["ELEG 2111"]),
    "COMS 1011": (1, "Any", [], ["COMS 1013"]),  # Lab (no prereq, just co-req)
    "COMS 1013": (3, "Any", [], ["COMS 1011"]),  # Lecture (no prereq, just co-req
    "SOC 1003": (3, "Any", [], []),
    "US History/Gov": (3, "Any", [], []),
    # Semester 5
    "ELEG 3103": (3, "Fall", ["ELEG 2113"], []),
    "MATH 2703": (3, "Any", ["MATH 2914"], []),
    "MATH 2934": (4, "Any", ["MATH 2924"], []),
    "PHYS 2124": (4, "Any", ["PHYS 2114"], []),
    "PHYS 2010": (0, "Any", ["PHYS 2114"], ["PHYS 2124"]),  # Lab
    # Semester 6
    "ELEG 3143": (3, "Spring", ["MATH 2934", "PHYS 2124"], []),
    "ELEG 3123": (3, "Spring", ["ELEG 2113", "MATH 3243"], []),
    "ELEG 4103": (3, "Spring", ["ELEG 3103"], []),
    "ELEG 4122": (2, "Spring", ["ELEG 4103", "ELEG 4113"], []),
    "ELEG/MCEG 4202": (2, "Any", ["ELEG/MCEG 3003"], []),
    "STAT 3153": (3, "Any", ["MATH 2924"], []),
    # Semester 7
    "ELEG 2134": (4, "Any", ["ELEG 1011"], ["ELEG 2130"]),
    "ELEG 2130": (0, "Any", ["ELEG 1011"], ["ELEG 2134"]),  # Lab
    "ELEG/MCEG 3003": (3, "Any", ["MATH 3243", "ELEG 2113"], []),
    "ELEG 4113": (3, "Fall", ["ELEG 3123"], []),
    "ELEG 4143": (3, "Fall", ["ELEG 3123"], []),
    "ELEG 4191": (1, "Any", ["ELEG/MCEG 4202"], []),
    "PSY 2003": (3, "Any", [], []),
    # Semester 8
    "BIOL 3074": (4, "Any", ["BIOL 1114", "BIOL 2014"], []),
    "ELEG 3133": (3, "Any", ["ELEG 2134", "COMS 1013"], []),
    "ELEG 4303": (3, "Any", ["ELEG/MCEG 3003", "ELEG 3123"], []),
    "ELEG 4192": (2, "Any", ["ELEG 4191"], []),
    "Fine Arts II": (3, "Any", [], []),
}


class Scheduler:  # Class Scheduler
    """Class-based planner for graduation pathways."""

    def __init__(self, course_db=None, max_hours=16, max_iterations=20):
        self.course_db = course_db if course_db is not None else EE_COURSE_DB
        self.max_hours = max_hours
        self.max_iterations = max_iterations

    def validate_constraints(self, completed_courses, remaining_courses):
        """
        Validate that all remaining courses can eventually be scheduled.
        Returns (is_valid, issues) where issues is a list of problematic courses.
        """
        issues = []

        for course, (restriction, prereqs, coreqs) in remaining_courses.items():
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
    student_history = {
        "ENGL 1013",
        "MATH 2914",
        "CHEM 2124",
        "TECH 1001",
        "ELEG 1011",
        "Fine Arts I",
        "ENGL 1023",
        "MATH 2924",
        "COMS 1011",
        "COMS 1013",
    }

    COURSE_DB = EE_COURSE_DB  # Use the Electrical Engineering course database for this simulation
    print("\n" + "=" * 60)
    if COURSE_DB == EE_COURSE_DB:
        print("ATU Electrical Engineering - Graduation Pathway Optimizer")
    elif COURSE_DB == CMPE_COURSE_DB:
        print("ATU Computer Engineering - Graduation Pathway Optimizer")
    elif COURSE_DB == BME_COURSE_DB:
        print("ATU Biomedical Engineering Option - Graduation Pathway Optimizer")
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

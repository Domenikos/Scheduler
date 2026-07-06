"""Generate an optimized graduation schedule for a Mechanical Engineering student."""

from Scheduler import Scheduler
from MCEG_COURSE_DB import MCEG_COURSE_DB

# Use the Mechanical Engineering course database for this simulation

student_history = {
    "ENGL 1013",
    "MATH 2914",
    "CHEM 2124",
    "CHEM 2120",
    "STEM/TECH 1001",
    "Fine Arts I",
    "ENGL 1023",
    "MATH 2924",
    "COMS 1011",
    "COMS 1013",
}

# Use either the Mechanical Engineering courses with Chemistry option or Physics option
CHEM_II_OPTION = True  # Set to True to use CHEM II option, False to use PHYS II option
MAX_HOURS = 18  # Maximum credit hours per semester
FALL_START = True  # Start scheduling from Fall semester; if False, start from Spring semester

# ========== Should not be necessary to make changes below this line ======================
COURSE_DB = MCEG_COURSE_DB  # Use the Mechanical Engineering courses without Chemistry or Physics option
# Remove courses in student_history that are not in the course database like MATH 1113
student_history = {course for course in student_history if course in COURSE_DB}
# print("remaining courses after filtering student history:", student_history)
# Add the CHEM II or PHYS II course to the course database based on the option selected
# Additional courses for Mechanical Engineering with Physics option
MCEG_PHYS_COURSE_DB = {
    # Semester 3
    "PHYS 2124": (4, "Any", ["PHYS 2114"], ["PHYS 2010"]),  # Lecture
    "PHYS 2010": (0, "Any", ["PHYS 2114"], ["PHYS 2124"]),  # Lab
}
# Additional courses for Mechanical Engineering with Chemistry option
MCEG_CHEM_COURSE_DB = {
    # Semester 3
    "CHEM 2134": (4, "Any", ["CHEM 2124"], ["CHEM 2130"]),  # Lecture
    "CHEM 2130": (0, "Any", ["CHEM 2124"], ["CHEM 2134"]),  # Lab
}
if CHEM_II_OPTION:
    COURSE_DB.update(MCEG_CHEM_COURSE_DB)
else:
    COURSE_DB.update(MCEG_PHYS_COURSE_DB)

print("\n" + "=" * 60)
print("ATU Mechanical Engineering - Graduation Pathway Optimizer")
print("=" * 60)
print(f"\n📚 Student Status: {len(student_history)} courses completed")
print(f"   Total Courses in Degree: {len(COURSE_DB)}")
print(f"   Remaining: {len(COURSE_DB) - len(student_history)} courses\n")

# print(f"Course Database: {COURSE_DB} courses")
scheduler = Scheduler(course_db=COURSE_DB, max_hours=MAX_HOURS, max_iterations=20)
optimized_plan = scheduler.generate_schedule(
    student_history, start_semester_is_fall=FALL_START
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

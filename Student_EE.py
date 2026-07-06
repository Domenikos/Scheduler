"""Generate an optimized graduation schedule for an Electrical Engineering student."""

from Scheduler import Scheduler
from EE_COURSE_DB import EE_COURSE_DB

# Use the Electrical Engineering course database for this simulation

student_history = {
    "ENGL 1013",
    "MATH 2914",
    "CHEM 2124",
    "CHEM 2120",
    "STEM/TECH 1001",
    "ELEG 1011",
    "Fine Arts I",
    "ENGL 1023",
    "MATH 2924",
    "COMS 1011",
    "COMS 1013",
    "MATH 1113",
}

# COURSE_DB = EE_COURSE_DB  # Use the Electrical Engineering
MAX_HOURS = 18  # Maximum credit hours per semester
FALL_START = True  # Start scheduling from Fall semester; if False, start from Spring semester

# ========== Should not be necessary to make changes below this line ======================
COURSE_DB = EE_COURSE_DB  # Use the Electrical Engineering course database
# Remove courses in student_history that are not in the course database like MATH 1113
student_history = {course for course in student_history if course in COURSE_DB}
# print("remaining courses after filtering student history:", student_history)   # Debugging

print("\n" + "=" * 60)
print("ATU Electrical Engineering - Graduation Pathway Optimizer")
print("=" * 60)
print(f"\n📚 Student Status: {len(student_history)} courses completed")
print(f"   Total Courses in Degree: {len(COURSE_DB)}")
print(f"   Remaining: {len(COURSE_DB) - len(student_history)} courses\n")

scheduler = Scheduler(course_db=COURSE_DB, max_hours=MAX_HOURS, max_iterations=20)
optimized_plan = scheduler.generate_schedule(student_history, start_semester_is_fall=FALL_START)
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

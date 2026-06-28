"""Generate an optimized graduation schedule for a BME Option student."""

from Scheduler import BME_COURSE_DB, Scheduler

# Use the Biological Engineering course database for this simulation

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

COURSE_DB = BME_COURSE_DB  # Use the Biological Engineering Option

print("\n" + "=" * 60)
print("ATU Biological Engineering Option - Graduation Pathway Optimizer")
print("=" * 60)
print(f"\n📚 Student Status: {len(student_history)} courses completed")
print(f"   Total Courses in Degree: {len(COURSE_DB)}")
print(f"   Remaining: {len(COURSE_DB) - len(student_history)} courses\n")

scheduler = Scheduler(course_db=COURSE_DB, max_hours=18, max_iterations=20)
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

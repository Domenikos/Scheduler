# ATU Engineering Scheduler

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A Python-based graduation pathway optimizer for Arkansas Tech University engineering programs.

The project generates semester-by-semester schedules based on completed coursework, prerequisites, co-requisites, term availability (Fall/Spring), and a configurable credit-hour cap.  A course degree flowchart can be created with the create_course_flowchart function in the Degree_Flowchart.py file.

## Why this project is useful

- Supports multiple program tracks from one engine:
  - Electrical Engineering
  - Computer Engineering
  - Electrical Engineering with Biomedical Option
  - Mechanical Engineering with Chemistry II or Physics II
  - Additional majors may be added
- Enforces prerequisite and co-requisite rules automatically.
- Accounts for course seasonality (`Any`, `Fall`, `Spring`).
- Applies per-semester hour limits to keep plans realistic.
- Detects and reports scheduling deadlocks with diagnostics.

## Project structure

- `Scheduler.py`: Core scheduler engine and course databases (`EE_COURSE_DB`, `CMPE_COURSE_DB`, `BME_COURSE_DB`).
- `Student_EE.py`: Example run for Electrical Engineering.
- `Student_CMPE.py`: Example run for Computer Engineering.
- `Student_BME.py`: Example run for Biomedical Option.
- `Student_EE_Nuc.py`: Example run for Electrical Engineering with Nuclear Technology option.

Can be modified for any major by adding its curriculum database.  See EE_COURSE_DB.py file for an example.

## Getting started

- Create a file for the student using one of the example files, for example Student_EE.py
- Modify the student_history set in the example file
- Change the max_hours in the call to Scheduler for the maximum number of hours per semester.
- Set FALL_START to True to begin in the Fall or False for a Spring start.
- Add a new course database for an additional major.  Use one of the exiting databases (EE_COURSE_DB.py) as a template.


### Prerequisites

- Python 3.10 or newer
- graphviz for degree flowcharts

### Installation

Clone the repository and move into it:

```bash
git clone <your-repository-url>
cd Scheduler
```

No third-party packages are required for the Scheduler.

### Quick start

Run one of the provided student scenarios:

```bash
python3 Student_EE.py
python3 Student_CMPE.py
python3 Student_BME.py
python3 Student_EE_Nuc.py
```

Each script prints:

- Number of completed courses
- Remaining courses
- Generated term-by-term schedule
- Planned credit totals

### Usage example (custom script)

Use the scheduler directly in your own script:

```python
from Scheduler import Scheduler, EE_COURSE_DB

student_history = {
    "ENGL 1013",
    "MATH 2914",
    "CHEM 2124",
    "TECH 1001",
    "ELEG 1011",
}

planner = Scheduler(course_db=EE_COURSE_DB, max_hours=16, max_iterations=20)
plan = planner.generate_schedule(completed, start_semester_is_fall=True)

for semester, (courses, hours) in plan.items():
    print(semester, hours, courses)
```

## Help and support

- Review implementation details in `Scheduler.py`.
- Open an issue in this repository for bugs or feature requests.
- Share the exact `student_history`, chosen course database, and `max_hours` value when reporting scheduling problems.
- Include the COURSE_DB file for issues with the Degree_Flowchart

## Maintainer and contributing

Maintainer: Carl Greco

Contributions are welcome through pull requests. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

## License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt).

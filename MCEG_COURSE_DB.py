# Mechanical Engineering Course Database
# These courses are required for the BS degree in Mechanical Engineering.
# Need to select either the Physics or Chemistry option for the degree.
# Course Database Format: 'COURSE_CODE': (Credit_Hours, Term_Restriction, [Prereqs], [Co-reqs])
# Term Restrictions: 'Any', 'Fall', 'Spring'
# Note: Co-requisites are not strictly enforced in this version of the scheduler, but are used to prioritize scheduling.
# Add prerequisites to ELEG & Technical Elective courses as needed for more accurate scheduling.
MCEG_COURSE_DB = {
    # Semester 1
    "ENGL 1013": (3, "Any", [], []),
    "MATH 2914": (4, "Any", [], []),
    "CHEM 2124": (4, "Any", [], ["CHEM 2120"]),  # Lecture
    "CHEM 2120": (0, "Any", [], ["CHEM 2124"]),  # Lab
    "STEM/TECH 1001": (1, "Any", [], []),
    "MCEG 1011": (1, "Any", [], []),
    "Fine Arts I": (3, "Any", [], []),
    # Semester 2
    "ENGL 1023": (3, "Any", ["ENGL 1013"], []),
    "MATH 2924": (4, "Any", ["MATH 2914"], []),
    "MCEG 1002": (1, "Any", [], []),
    "MCEG 2203": (
        3,
        "Any",
        ["MCEG 1011", "MATH 2914"],
        [],
    ),  # Computational Methods in Engineering
    "PHYS 2114": (4, "Any", ["MATH 2924"], ["PHYS 2000"]),  # Lecture
    "PHYS 2000": (0, "Any", ["MATH 2924"], ["PHYS 2114"]),  # Lab
    # Semester 3
    "MATH 2934": (4, "Any", ["MATH 2924"], []),
    "MCEG 2013": (3, "Any", ["MATH 2924", "PHYS 2114"], []),
    "MCEG 2023": (3, "Any", ["CHEM 2124"], []),
    # Semester 4
    "ELEG 2103": (3, "Any", ["MATH 2924"], []),
    "MATH 3243": (3, "Any", ["MATH 2924"], []),
    "MCEG 2033": (1, "Any", ["MCEG 2013"], []),
    "MCEG 3013": (3, "Any", ["MCEG 2013"], []),
    "Social Science": (3, "Any", [], []),
    # Semester 5
    "ELEG 2113": (3, "Any", ["ELEG 2103", "MATH 3243"], []),
    "MCEG 3313": (3, "Any", ["MATH 2924", "PHYS 2114"], []),
    "MCEG 3413": (3, "Any", ["MCEG 2033", "MCEG 3013", "MATH 3243"], []),
    "MCEG 3442": (2, "Any", ["MCEG 2023", "MCEG 3013"], []),
    "ENGR Elective 1": (3, "Any", ["MATH 3243"], []),
    # Semester 6
    "ENGR Elective 2": (3, "Any", ["MATH 3243"], []),
    "MATH Elective": (3, "Any", ["MATH 2924"], []),
    "ELEG/MCEG 4202": (2, "Any", ["ELEG/MCEG 3003"], []),
    "MCEG 4403": (3, "Any", ["MCEG 2033", "MCEG 3313", "MATH 3243"], []),
    "MCEG 4423": (3, "Any", ["MCEG 3413"], []),
    # Semester 7
    "ELEG/MCEG 3003": (3, "Any", ["MATH 3243", "ELEG 2113"], []),
    "MCEG 4433": (3, "Any", ["MATH 2934", "MCEG 3313"], []),
    "MCEG 4442": (3, "Any", ["MCEG 4403"], []),
    "MCEG 4491": (1, "Any", ["MCEG 3413", "ELEG/MCEG 4202"], []),
    "Tech Elective 1": (3, "Any", ["MATH 2924"], []),
    "US History/Gov": (3, "Any", [], []),
    # Semester 8
    "ELEG 4303": (3, "Any", ["ELEG/MCEG 3003", "ELEG 2113"], []),
    "ENGR Elective 3": (3, "Any", ["ENGR Elective 2"], []),
    "ENGR Lab Elective 1": (3, "Any", ["MCEG 3442"], []),
    "Fine Arts II": (3, "Any", [], []),
    "MCEG 4443": (2, "Any", ["MCEG 4403"], []),
    "MCEG 4492": (2, "Any", ["MCEG 4491"], []),
}

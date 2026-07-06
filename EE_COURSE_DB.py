# Electrical Engineering Course Database
# Course Database Format: 'COURSE_CODE': (Credit_Hours, Term_Restriction, [Prereqs], [Co-reqs])
# Term Restrictions: 'Any', 'Fall', 'Spring'
# Note: Co-requisites are not strictly enforced in this version of the scheduler, but are used to prioritize scheduling.
# Add prerequisites to ELEG & Technical Elective courses as needed for more accurate scheduling.
EE_COURSE_DB = {
    # Semester 1
    "ENGL 1013": (3, "Any", [], []),
    "MATH 2914": (4, "Any", [], []),
    "CHEM 2124": (4, "Any", [], ["CHEM 2120"]),  # Lecture
    "CHEM 2120": (0, "Any", [], ["CHEM 2124"]),  # Lab
    "STEM/TECH 1001": (1, "Any", [], []),
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
    "PHYS 2124": (4, "Any", ["PHYS 2114"], ["PHYS 2010"]),  # Lecture
    "PHYS 2010": (0, "Any", ["PHYS 2114"], ["PHYS 2124"]),  # Lab
    "MATH 2934": (4, "Any", ["MATH 2924"], []),
    "ELEG 2111": (1, "Any", ["ELEG 2103"], ["ELEG 2113"]),  # Lab
    "ELEG 2113": (3, "Any", ["ELEG 2103", "MATH 3243"], ["ELEG 2111"]),
    "STAT 3153": (3, "Any", ["MATH 2924"], []),
    # Semester 5
    "Tech Elective 1": (3, "Any", ["MATH 2924"], []),
    "ELEG Elective 1": (3, "Any", ["MATH 3243"], []),
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
    "ELEG 4113": (3, "Fall", ["ELEG/MCEG 3003", "ELEG 3123"], []),
    "ELEG 4303": (3, "Any", ["ELEG/MCEG 3003", "ELEG 2113"], []),
    "ELEG 4191": (1, "Any", ["ELEG/MCEG 4202"], []),
    "US History/Gov": (3, "Any", [], []),
    # Semester 8
    "ELEG Elective 2": (3, "Any", ["ELEG Elective 1"], []),
    "Tech Elective 2": (3, "Any", ["MATH 2924"], []),
    "Fine Arts II": (3, "Any", [], []),
    "ELEG 4122": (2, "Spring", ["ELEG 4103", "ELEG 4113"], []),
    "ELEG 4192": (2, "Any", ["ELEG 4191"], []),
}

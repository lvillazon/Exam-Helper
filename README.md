# Exam-Helper

GCSE Paper 2 Exam Helper
The Exam Helper Utility.py script is designed to reset and populate the candidate folders with the correct files for each GCSE coding exam. This must be run for each new exam

Y10 practice in June/July
Y11 Mock in March
Y11 practice in April/May
Y11 actual exam in May/June

The program presents the following menu:

+============================================================+
| BEXLEY GRAMMAR SCHOOL Edexcel Computer Science Exam Helper |
| ---------------------------------------------------------- |
|                                                            |
| Center Number    : 14105                                   |
| Root folder      : //bex-file-03/csexam$/                  |
| Students imported: 52                                      |
|                                                            |
| Menu                                                       |
| 1. Import student names                                    |
| 2. List student names                                      |
| 3. Set root folder for exam files                          |
| 4. Wipe all student folders                                |
| 5. Fill student folders from master folder                 |
| 6. Create new (empty) folders for each student             |
| 7. Delete all candidate folders                            |
| 8. Print all candidate solutions                           |
| 9. Quit                                                    |
|                                                            |
+============================================================+

Import student names
This reads in student names and candidate numbers from a text file which should be in this format:
CENTRE NUMBER: 14105,
,
Full Name,Exam Number
"Ahmad, Ayid",8001
"Arkwright, Jack",8005
"Atigogo, Joseph",8007
"Austin, Daniel",8008

The header doesn't matter, as long as it does not contain any double-quotes as the first character. This is used to detect the first actual candidate row.

The list of students begins empty and so you must use Option 1 to read in student names before doing anything else. The program will prompt for the name of the CSV file, but it always expects this file to be found in the Root folder. If the file cannot be found you will be prompted to try again.

The program checks that the following minimum requirements are met:
The list contains pairs of NAME, NUMBER
 Each name contains no numbers
 Each number is a 4-digit number with no other characters
List student names
This displays the records for each student, giving candidate number, name and user account on the school network.
Set root folder for exam files
Allows a new root folder to be specified. This is not saved and will revert to the default option each time the program is run. The root folder is where the student CSV file should be and also should be where each of the user account folders are.

Wipe all student folders
This will delete the STUDENT_CODING and COMPLETED_CODING folders from each user account, but will keep the (now empty) folder with the student's name in the Desktop folder of their user account.
Fill student folders from master folder
Copies the STUDENT_CODING and the (empty) COMPLETED_CODING folders from MASTER in the root folder to each of the student name folders.
Create new (empty) folders for each student
Creates a folder in the Desktop of each user account with a name assembled from the centre number, candidate number, and candidate name. This associates the specific user with that user account and it is important that each candidate only uses their corresponding account.
Delete all candidate folders
This deletes the named student folder from the desktop of each user account. This will also delete both the coding folders inside it as well. This should be used when preparing the accounts for a new cohort of students.

There are hard-coded default file names and paths, but these can so these may need to be tweaked each time. Two functions are called that perform the same actions for each candidate on the list:
Print all candidate solutions
This attempts to print all the answers for each student. The answers must be in the COMPLETED_CODING folder and it will only print files with the .py extension. All the files in a given student's folder are concatenated together with a header at the top of each question identifying the student and the filename. The concatenated output is saved as toprint.txt in the student's COMPLETED_CODING folder and printed by spawning a new process with the default print action for a text file in Windows. This means that the students cannot be guaranteed to be sent to the printer in list order - shorter files may finish spooling sooner and hit the print queue first. But all the answers for each student should be collated together.

If you don't want to print every student's answers, you can specify a numeric range of login numbers. For example, selecting a lower bound of 52 and an upper bound of 75 would print the solutions for every account from CSEXAM-52 to CSEXAM-75 inclusive. If both bounds are the same, it will print just a single candidate's answers.
Quit
Exits the program.

Confirmation
Menu options that make changes to files or folders require a separate confirmation step. If you type "actual" when prompted, the changes are made immediately. If you hit Enter (or type anything other than "actual") the program will display output messages indicating what would have happened, but will not make any changes to the filing system.


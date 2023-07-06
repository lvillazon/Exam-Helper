# Create candidate folders for Y10 mock exams
# These should have the following format:
#   CENTRE NUMBER_CANDIDATE NUMBER_SURNAME_FORENAME. 
#   For example: 12345_0123_SMITH_ADAM

# TODO
# Print only answers for a given numeric range of candidate numbers

# TEST LOGIN
# CSEXAM-01
# 2Bgsexam01

import os, shutil, unicodedata, time

# GLOBAL VARIABLES
SLASH = os.sep
master_folder_name = "MASTER"

raw_list = []

def valid_names(names):
    # checks the raw name list meets minimum validation criteria:
    # The list should contains pairs of NAME, NUMBER
    # Each name should contain no numbers
    # Each number should be a 4-digit number with no other characters
    if len(names) % 2 !=0:
        return False, "different number of names and candidate numbers"  # must be an even number of records, since 1 name + 1 number for each candidate

    for i in range(0, len(names)-1, 2):
        if isinstance(names[i], str):
            for char in names[i]:
                if char in '012345679':
                    return False, names[i] + " - invalid candidate name"  # cannot contain a digit"
        else:
            return False, str(names[i]) +  " - invalid candidate name"  # must be a string"
        if isinstance(names[i+1], int):
            if names[i+1] <1000 or names[i+1] > 9999:
                return False, str(names[i+1]) + " - invalid candidate number (must be 4 digits)"  # candidate number must be 4 digits
        elif isinstance(names[i+1], str):
            if len(names[i+1]) != 4:
                return False, str(names[i+1]) + " - invalid candidate number (must be 4 digits)"  # candidate number must be 4 digits
        else:
            return False, str(names[i+1]) + " - invalid candidate number"  # candidate number must be a number
    return True, ""  # assume correct otherwise

def create_folder(pathname):
    # Create the directory 
    try: 
        os.mkdir(pathname) 
    except OSError as error: 
        print(error)  
  

# read names & exam numbers of all candidates from a file
def get_raw_names(filename):
    # the expected file format is
    # "surname, firstname", 0001
    # names must always be enclosed in quotes
    # any header rows before the first name will be ignored
    # provided they do not begin with a double-quote "
    raw_data = []
    with open(filename, 'r') as f:
        for record in f:
            if record[0] == '"':  # ignore everything up to the first student record, which begins with "
                fields = record.strip().split('",')  # can't just split on , because the names contain commas within the quotes
                raw_data.append(eval(fields[0]+'"'))  # restore the trailing " that was removed by split
                raw_data.append(str(fields[1]))
    return raw_data
        

# contruct properly formatted candidate folder names
def build_candidate_folder_name(full_name, candidate_number):
    names = full_name.split(',')
    first_name = names[1].strip()
    surname = names[0].strip()

    candidate_folder = (
        centre + '_' +
        str(candidate_number) + '_' +
        surname.upper() + '_' +
        first_name.upper()
        )
    return candidate_folder

# concatenate filepaths, using valid slash characters
def join_path(*paths):
    return os.path.normpath(os.path.join(*paths))

def get_desktop_path(folder_number):
    return join_path(root, "CSEXAM-" + f'{folder_number:02}', 'Desktop')


def wipe_student_folders(for_real = False):
    # remove everything from STUDENT_CODING and COMPLETED_CODING for each student
    # ready for the next exam

    folder_number = 1
    for i in range(0, len(raw_list), 2):
        
        desktop_path = get_desktop_path(folder_number)
        candidate_folder = build_candidate_folder_name(raw_list[i], raw_list[i+1])

        # wipe all folders in this list
        for folder_name in ['STUDENT CODING', 'COMPLETED CODING']:    
            # assemble the filepath for the folder
            target_folder_path = join_path(desktop_path, candidate_folder, folder_name)
            print("removing", target_folder_path, end='')
            if for_real:
                try:
                    shutil.rmtree(target_folder_path)
                except OSError:
                    print("...FAILED")
                else:
                    print("...SUCCESS")
            else:
                print("...SUCCESS")     
        folder_number += 1

def list_master_folder():
    # displays all files in the master folder
    # this is the folder that is used to distribute the exam Qs
    master_folder = join_path(root, master_folder_name)
    print("\nThe MASTER folder is", master_folder)
    print("it contains:\n")
    top_level_folders = os.listdir(master_folder)
    for folder_name in top_level_folders:
        print(' '*3, folder_name + ':')
        folder_contents = os.listdir(join_path(root, master_folder_name, folder_name))
        if folder_contents:
            for file in folder_contents:
                print(' '*7, file)
        else:
            print('    <EMPTY>')
        print()

def fill_student_coding_folders(for_real = False):
    # copy the MASTER\STUDENT_CODING folder to each student

    folder_number = 1
    for i in range(0, len(raw_list), 2):
        
        desktop_path = get_desktop_path(folder_number)
        candidate_folder = build_candidate_folder_name(raw_list[i], raw_list[i+1])
             
        # copy the STUDENT CODING folder in MASTER to the candidate folder (this moves the actual exam Qs)
        copy_from = join_path(root, master_folder_name, 'STUDENT CODING')
        copy_to = join_path(desktop_path, candidate_folder, 'STUDENT CODING')
        print('copying:', copy_from, "to:", copy_to)
        if for_real:
            shutil.copytree(copy_from, copy_to)

            # create empty COMPLETED CODING folder in the candidate folder
            completed_folder = join_path(desktop_path, candidate_folder, 'COMPLETED CODING')
            try:
                os.mkdir(completed_folder)
            except OSError:
                print ("FAILED TO CREATE", completed_folder)
            else:
                print ("Created:", completed_folder)
            
        folder_number += 1

# WIP - this is not accessible from the menu and has not been tested properly yet
# I'm not even convinced it is useful
def copy_single_file(filename, for_real = False):
    # copy filename to the STUDENT_CODING folder of each student

    folder_number = 1
    for i in range(0, len(raw_list), 2):
        
        desktop_path = get_desktop_path(folder_number)
        candidate_folder = build_candidate_folder_name(raw_list[i], raw_list[i+1])

        # copy the specified filename to the candidate folder
        copy_from = join_path(root, filename)
        copy_to = join_path(desktop_path, candidate_folder, 'STUDENT CODING')
        print('copying:', copy_from, "to:", copy_to)
        if for_real:
            shutil.copytree(copy_from, copy_to)
            
        folder_number += 1

def create_candidate_folders(for_real = False):
    # creates the folder on the account desktop, for each specific student
    folder_number = 1
    for i in range(0, len(raw_list), 2):
        # build the numbered CSEXAM-xx folder
        user_folder_path = os.path.join(root, "CSEXAM-" + f'{folder_number:02}')
        desktop_path = os.path.join(root, "CSEXAM-" + f'{folder_number:02}', 'Desktop')
        if for_real:
            create_folder(user_folder_path)
            create_folder(desktop_path)
                
        candidate_folder = build_candidate_folder_name(raw_list[i], raw_list[i+1])
            
        # create the candidate folder on the desktop
        folder_pathname = os.path.normpath(os.path.join(desktop_path, candidate_folder))
        print("Creating", folder_pathname)
        if for_real:
            create_folder(folder_pathname)
        folder_number += 1

def empty_folder(folder_name, exceptions, for_real = False):
    # deletes everything in the folder, but not the folder itself
    # folder_name is assumed to be a fully qualified path
    # exceptions is a list of folders of files that should not be removed

    if not os.path.exists(folder_name):
        print("WARNING! PATH NOT FOUND:", folder_name)
        return
    
    contents = os.listdir(folder_name)
    for c in contents:
        if c.lower() not in exceptions:
            to_delete = join_path(root, folder_name, c)
            print('Deleting', to_delete, end='')
            if for_real:
                try:
                    # delete process depends on whether the target is a file or folder
                    if os.path.isdir(to_delete):
                        shutil.rmtree(to_delete)
                    else:
                        os.remove(to_delete)
                except OSError:
                    print("...FAILED")
                else:
                    print("...SUCCESS")
            else:
                print("...SUCCESS")


def delete_candidate_folders(for_real = False):
    # deletes the all folders except the Recycle bin on each account desktop
    # deleting all files in them as well

    # get list of all candidate folders (beginning with CSEXAM)
    top_level_folders = [t for t in os.listdir(root) if 'CSEXAM' in t]
    for folder in top_level_folders:
        # first delete everything apart from 'desktop' and 'documents'
        empty_folder(join_path(root, folder), ['desktop', 'documents'], for_real)
        # next, delete everything in 'documents' (but not the folder itself)
        empty_folder(join_path(root, folder, 'documents'), ['$recycle.bin'], for_real)
        # now empty the recycle bin
        empty_folder(join_path(root, folder, 'documents', '$recycle.bin'), [], for_real)
        # finally, empty the desktop folder
        empty_folder(join_path(root, folder, 'desktop'), [], for_real)

    
def old_delete_candidate_folders(for_real = False):
    # deletes the candidate folders on each account desktop
    # deleting all files in them as well
    # THIS VERSION IS DEPRECATED, SINCE IT USES THE LIST OF STUDENTS TO DECIDE WHICH
    # FOLDER TO DELETE. THIS IS INCONVENIENT WHEN PREPARING FOR THE NEXT COHORT
    # BECAUSE THE STUDENT LIST MAY HAVE ALREADY BEEN REPLACED WITH THE NEW NAMES
    folder_number = 1
    for i in range(0, len(raw_list), 2):
        
        desktop_path = os.path.join(root, "CSEXAM-" + f'{folder_number:02}', 'Desktop')
        candidate_folder = build_candidate_folder_name(raw_list[i], raw_list[i+1])
            
        # delete the candidate folder on the desktop
        folder_pathname = os.path.normpath(os.path.join(desktop_path, candidate_folder))
        print("Deleting", folder_pathname)
        if for_real:
            shutil.rmtree(folder_pathname)
        
        folder_number += 1


def print_solutions(for_real = False, lower=0, upper=9999):
    # create a single text file containing the collated answers for each student
    # padded to 54 lines so that each Q starts on a new page.
    # Then send each one to print. Because each print job spawns a new thread, they will not
    # necessarily reach the printer in the order that they were sent, so collating at least
    # means that student answers will not get jumbled together.
    # lower and upper are the min/max candidate numbers to be printed
    LINES_PER_PAGE = 54
    folder_number = 1
    print("Printing candidates from", lower, "to", upper)
    for i in range(0, len(raw_list), 2):
        if folder_number < lower or folder_number > upper:  # skip folders outside of the print range
            print("Skipping folder CSEXAM-"+f'{folder_number:02}')
            folder_number += 1
            continue

        desktop_path = get_desktop_path(folder_number)
        candidate_folder = build_candidate_folder_name(raw_list[i], raw_list[i+1])
        completed_folder = join_path(desktop_path, candidate_folder, "COMPLETED CODING")

        if os.path.exists(completed_folder):

            # get a list of all .py files in COMPLETED CODING
            completed_files = [f for f in os.listdir(completed_folder) if '.py' in f]  # TODO should this look for all files?

            # process all the files for a single student into one file
#            combined_filename = join_path(completed_folder, candidate_folder, ".txt")
            combined_filename = join_path(completed_folder, "toprint.txt")
            print("combining", completed_files, "into", candidate_folder+".txt")
            if for_real:
                with open(combined_filename, 'w') as output_file:
                    for f in completed_files:
                        if f == "toprint.txt":  # skip over the file that we are concatenating to
                            continue
                        with open(join_path(completed_folder, f)) as input_file:
                            # write a header line with the candidate name and file name at the top of each new file
                            output_file.write(candidate_folder+"   "+f+"\n\n")
                            line_count = 2
                            for line in input_file:
                                output_file.write(line)
                                line_count = (line_count + 1)% LINES_PER_PAGE
                        # pad with enough blank lines to take us up to a new page for the next file
                        # TODO there is a subtle bug where this does not pad correctly for multi-page files
                        # EDIT 3/7/23 This seems to have been fixed
                        for i in range(line_count, LINES_PER_PAGE):
                            output_file.write("\n")
                        line_count = 0
                
                print("printing...", end='')
                if for_real:
                    os.startfile(join_path(completed_folder,"toprint.txt"), "print")
                print("done.")
                
        folder_number += 1

def confirm_master_folder():
    print("The current master folder is set to:" + master_folder_name)
    name = input("Hit <ENTER> to confirm, or enter a different folder name:")
    if name == "":
        return master_folder_name  # return original unchanged name
    else:
        return name  # return new name

def menu_border(w):
    print("+", "=" * (w+2), "+", sep='')

def menu_line(text, w):
    print('| {a:<{b}} |'.format(a=text, b=w))

def menu(center_number, root):
    choice = "0"
    while choice not in "123456789":
        title = "BEXLEY GRAMMAR SCHOOL Edexcel Computer Science Exam Helper"
        width = len(title)
        print()
        menu_border(width)
        menu_line("BEXLEY GRAMMAR SCHOOL Edexcel Computer Science Exam Helper", width)
        menu_line("-" * len(title), width)
        menu_line("", width)
        menu_line("Center Number    : " + str(center_number), width)
        menu_line("Root folder      : " + root, width)

        valid, error = valid_names(raw_list)
        if valid:
            menu_line("Students imported: " + str(len(raw_list)//2), width)
        else:
            menu_line("STUDENT DATA INVALID - CHECK FILE AND RE-IMPORT!", width)
            menu_line(error, width)

        menu_line("", width)
        menu_line("Menu", width)
        menu_line("1. Import student names", width)
        menu_line("2. List student names", width)
        menu_line("3. Set root folder for exam files", width)
        menu_line("4. Wipe all student folders", width)
        menu_line("5. Fill student folders from master folder", width)
        menu_line("6. Create new (empty) folders for each student", width)
        menu_line("7. Delete all candidate folders", width)       
        menu_line("8. Print all candidate solutions", width) # WIP - test only
        menu_line("9. Quit", width)
        menu_line("", width)
        menu_border(width)
        choice = input("Enter selection:")
    return choice

def confirm_action():
    check = "invalid"
    while check != "" and check != "actual":
        print("\nEnter 'actual' to perform this action for real")
        print("or hit ENTER to just preview without making changes.")
        check = input(">")
    if check == "actual":
        return True
    else:
        return False

# input an int with default value and validation
def get_number(prompt, default):
    answer = "dummy"
    while not answer.isnumeric():
        answer = input(prompt)
        if answer == '':
            return default
    return int(answer)

# MAIN PROGRAM
root = "//bex-file-03/csexam$/"
centre = "14105"

finished = False
while not finished:
    action = menu(centre, root)
    if action == "1":  # Import
        print("Student names should be in a CSV file.")
        print("The expected file format is")
        print('"surname, firstname", 0001')
        print("Names must always be enclosed in quotes.")
        print("Any header rows before the first name will be ignored")
        print("provided they do not begin with a double-quote.")
        valid_file = False
        while not valid_file:
            list_file = input("Enter CSV file for student names:")
            if os.path.exists(list_file):
                valid_file = True
            else:
                print("File not found:", list_file)
        raw_list = get_raw_names(list_file)

    elif action == "2":  # List
        folder = 1
        print('{0:<6}{1:<30}{2}'.format('CAND#', 'NAME', 'USER NAME'))
        print('-'*50)
        # output CSV list (so it can be copy-pasted to a spreadsheet
        for i in range(0, len(raw_list)-1, 2):
            print('{0:<6}{1:<30}CSEXAM-{2:02}'.format(str(raw_list[i+1])+',', raw_list[i]+',', folder))
            folder += 1

    elif action == "3":  # Set root
        print("Enter a new root folder (or hit return to keep the existing one)")
        new_folder = input(">")
        if new_folder != "":
            root = new_folder

    elif action == "4":  # Wipe folders
        print("This will delete the STUDENT_CODING and COMPLETED_CODING folders")
        print("from each candidate's folder on the Desktop, but leave the")
        print("candidate folder itself.")
        print("Use this to reset the folders for a given set of students")
        print("eg between mocks and the final exams.")
        wipe_student_folders(confirm_action())

    elif action == "5":  # Fill folders from master
        print("This will copy the STUDENT_CODING folder and an empty COMPLETED_CODING folder")
        print("from the master folder, to each candidate in the list.")
        print("Use this to copy the exam questions across on the day of the exam.")
        # give the option to change the master folder and list the contents each time until confirmed
        confirmed_name = ''
        while master_folder_name != confirmed_name:
            list_master_folder()
            confirmed_name = master_folder_name
            master_folder_name = confirm_master_folder()
        fill_student_coding_folders(confirm_action())

    elif action == "6":  # Create new top-level candidate folders
        print("This will create empty folders for each candidate, 1 per account")
        print("The names use the required convention, with center number, candidate number and name.")
        create_candidate_folders(confirm_action())

    elif action == "7":  # Delete top-level candidate folders
        print("This will remove the top-level folders for each candidate and delete all files in them.")
        print("Use this when preparing the user accounts for a new year group.")
        delete_candidate_folders(confirm_action())

    elif action == "8":  # Print all 6 solutions from all candidates
        print("This will print all the files in every candidate's COMPLETED_CODING folder.")
        print("This should NOT be done for actual exams, but may be useful for mocks.")
        lower = get_number("Enter lower bound for candidate folder, or [Enter] for all:", default=0) 
        upper = get_number("Enter upper bound, or [Enter] for all:", default=9999) 
        print_solutions(confirm_action(), lower, upper)

    elif action == "9":
        finished = True

print("Thank you for using Exam Helper.")
print("Remember to double-check folder contents")

# TODO add menu options to create and remove the student folders
''' OLD CODE TO SET UP THE FOLDER INITIALLY
# process all the candidates in the list
folder_number = 1
for i in range(0, len(raw_list), 2):
    
    desktop_path = os.path.join(root, "CSEXAM-" + f'{folder_number:02}', 'Desktop')
    candidate_folder = build_candidate_folder_name(raw_list[i], raw_list[i+1])
        
    # create the candidate folder on the desktop
    print(os.path.normpath(os.path.join(desktop_path, candidate_folder)))
    create_folder(os.path.normpath(os.path.join(desktop_path, candidate_folder)))

    # move the COMPLETED CODING folder into the candidate folder
    print('moving to ', candidate_folder)
    move_from = join_path(desktop_path, 'COMPLETED CODING')
    move_to = join_path(desktop_path, candidate_folder, 'COMPLETED CODING')
    print('moving:', move_from, "to:", move_to)
    shutil.copytree(move_from, move_to)
    shutil.rmtree(move_from)
 
    # copy the STUDENT CODING folder in MASTER to the candidate folder (this moves the actual exam Qs)
    move_from = join_path(root, 'MASTER', 'STUDENT CODING')
    move_to = join_path(desktop_path, candidate_folder, 'STUDENT CODING')
    print('moving:', move_from, "to:", move_to)
    shutil.copytree(move_from, move_to)
    # remove the empty STUDENT CODING folder in the CSEXAM-xx folder
    shutil.rmtree(join_path(desktop_path, 'STUDENT CODING'))
    
    folder_number += 1

'''

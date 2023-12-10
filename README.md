

### This repository contains a recruitment task.
The candidates were asked to do the following:

- Merge and clean data from multiple files (from the 'data' directory).
- Develop a Command-Line Interface (CLI) application with specified commands.
- Create a user manual in Markdown (MD) format.

----------------------------------------------------------------------------------------------------------------
## USER MANUAL

### Welcome! This file contains useful information for executing script.py



  - To display the help message in the terminal, please run:
  
         >python script.py --help
  
  - If you launch this program for the first time, please run:
  
         >python script.py create-database

  - To execute a command, please provide your login and password. Please mind that the password should be put within **single quotes**, f.e.:
  
         >python script.py <name of the command> --login 123456789 --password 'mypassword'

### For the users without admin privileges, the following commands are available:
  - Command: `python script.py print-children`
  - Displays information about your children.

         >python script.py print-children --login 123456789 --password 'mypassword'
         Adam, 4
         Nicole, 10

  - Command: `python script.py find-similar-children-by-age`
  - Displays users with children of the same age as at least one of your children.

         >python script.py find-similar-children-by-age --login 123456789 --password 'mypassword'
         Michael, 345678123: Sarah, 4
         Roger, 987654321: Manuel, 4; Sol, 2

### In addition to the commands listed above, the users with admin privileges can execute the following commands:
  - Command: `python script.py print-all-accounts`
    - Prints the total number of valid accounts.
  
           >python script.py print-all-accounts --login 234567891 --password 'clandestina'
           12345

  - Command: `python script.py print-oldest-account`
    - Prints information about the account with the longest existence.

          >python script.py print-oldest-account --login 234567891 --password 'clandestina'
          name: Roger
          email_address: roger88@gmail.com
          created_at: 1999-12-31 23:59:99

  - Command: `python script.py group-by-age`
    - Groups children by age and displays relevant information.
  
           >python script.py group-by-age --login 234567891 --password 'clandestina'
           age: 1, count: 12
           age: 3, count: 5
           age: 5, count: 7
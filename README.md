# Bike-Share-System

![banner.png](./bss/ui/img/banner.png)

The bike-sharing system named **BikeSims** is built by the members of the group **Lab 1_2d** as an outcome of the team project. It provides several graphical user interfaces (GUI) and demonstrates a general bike rental process. For more info regarding the description of building the project, please refer to our report.

## System Requirements

- Windows 7 or above.
- Python 3 (version 3.7 or above recommended) with required packages installed.

We have tested that BikeSims can be error-free if the above requirements are satisfied.

## How to Run BikeSims

The system is not packaged as an executable file, and the command prompt is needed to run it. The steps to run BikeSims on Windows are listed as follows.

1. In the command prompt, navigate to the project directory whose name should contain `Bike-Share-System` (e.g., `C:\Bike-Share-System-main`).
2. Run the command `python setup.py` in the command prompt. The script file will check and install any missing third-party package. If everything is fine, it will import the entry to the system and execute it. You may refer to the text file [`requirements.txt`](./requirements.txt) for the list of the required packages.
3. It should be good to go if you see a login view. The existing account details are listed in the following table. Please remember to **select a correct role** when you log in. You can also sign up a new account as a **customer**. Any newly registered customer account's username and password must satisfy the specified rules. Please refer to the user manual for further guides on how to use BikeSims.

    | Role | Username | Password |
    | :--: | :--: | :--: |
    | Customer | tony | 1234 |
    | Customer | jichen | 12345 |
    | Customer | shihao | 123456 |
    | Customer | yuan | 1234567 |
    | Operator | jiamin | 1234 |
    | Operator | nan | 12345 |
    | Manager | xiaoran | 1234 |

## ATTENTION

1. The third-party packages can also be installed by running the command `pip3 install -r requirements.txt`. You may need to do this if the script file "setup.py" says that you need to install the packages manually. Typically, according to our tests, this would not happen if the environment is Windows 10 + Python 3.
2. Most functionality can work properly on MacOS, since we mainly use [`ttk`](https://docs.python.org/3/library/tkinter.ttk.html) of Python. However, we have **NOT** specially optimised the performance on MacOS because it is not our top priority.

## Lab 1_2d's Group Members

- Antonios Evmorfopoulos
- Jiamin Ji
- Jichen Zhao
- Nan Chen
- Shihao Chen
- Xiaoran Kang
- Yuan Gao

Time is limited, and we have attempted to achieve as much as possible. Hope you feel satisfied with BikeSims!

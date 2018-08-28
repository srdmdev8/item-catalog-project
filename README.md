# FSWD Item Catalog Project


## App Overview
This project utilizes the Flask microframework to run my console and game catalog
and the SQLAlchemy toolkit to connect to my database. The initial database
was created from scratch. This catalog displays all the available consoles and
provides options to view games from each console, add a new console, and
edit/delete consoles. If you select to view the games of a specific console, you
will see a list of all applicable games for that console. You will also have
options to add a new game and edit/delete games.  

A login/logout authentication process has also been implemented using Google's
OAuth 2.0 API. There will be two ways to login: Facebook and Google. The provided
Python script has logic to prevent access to certain features if you are not
logged in. For example, the modification options mentioned above will be
unavailable until you have been successfully logged in, providing more of a
"read-only" type view.

## Installation and Setup
First, you will need to install Python on your computer:
- Go to [Python.org](https://www.python.org/downloads/) and install Python (we
  are running version 2.7.14)

Then, you will need to install Git in order to run this program on your local
host.
- Go to [Git's website](https://git-scm.com/downloads) and install Git (we are
  running version 2.18.0)

Next, you will need to install Vagrant and VirtualBox.
- For Vagrant, go to [Vagrantup.com](https://www.vagrantup.com/downloads.html)
(we are running version 2.1.2)
- For the VirtualBox, go to [Virtualbox.org](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) (we
  are running version 5.1.38)

Now, you need to configure the VirtualMachine (VM):
- Download the ZIP file
[here](https://github.com/udacity/fullstack-nanodegree-vm)
  - Select **Clone or download**
  - Then select **Download ZIP**
- Save the ZIP file in desired location on your computer
- Unzip/extract all files
- Open the command prompt using Git or Git Bash
- Navigate to the **vagrant** subdirectory within the *fullstack-nanodegree-vm*
folder
- Run the command `vagrant up`
- Once the vagrant up process completes, run `vagrant ssh`

If you get a shell prompt that starts with the word **vagrant**, you have
successfully logged into your VM! *Keep your command prompt open as we will be
coming back to it later.*

Next, you need to download the items catalog program:
- Download the program's ZIP file
[here](https://github.com/srdmdev8/item-catalog-project)
  - Select **Clone or download**
  - Then select **Download ZIP**
- Save the ZIP file in the **vagrant** subdirectory within the
*fullstack-nanodegree-vm* folder
- Unzip/extract all files

Lastly, we need to set up and load the database the program will be analyzing:
- Go back to your command prompt and `cd` into your **/vagrant** directory
- Then `cd` into the **item-catalog** folder
- Now run the command `python database_setup.py`
  - This will create a blank database
- Then run the command `python lotsofgames.py`
  - This will load the initial database items

## Running the Program
Ensure that you are still logged into your VM and are in the **/vagrant**
directory in the Git or Git Bash command prompt, then:
- `cd` into the **item-catalog** directory (if you are not already)
- Run the command `python gameCatalog.py`
- Once your local host is running successfully:
  - Open a web browser and enter **localhost:8000** in the URL field and press
  enter

Now you are ready to navigate through my console and game catalog. Thank you for
checking out my Item Catalog Project!

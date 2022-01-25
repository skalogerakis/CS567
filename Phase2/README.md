# General Setup Instructions

Go to the project directory, open a terminal and run the following commands

- Create a virtual environment

    
        python3 -m venv env


- Activate it using the command

    
        source env/bin/activate

- Run the following command to fetch the dependancies

    
        python3 -m pip install -r requirements.txt

# Bonus Setup Instructions

## Setup Steps
The Bonus Question(2.6) was executed using the ROBOT external tool. There are the different ways to execute the library the
most simple of which was to download the jar file containing the tool and execute it using the 
**java -jar** command. The jar file was too large to include in the final deliverable and below there are the steps 
in order to download it.

- Step 1) Go the website of ROBOT and download the latest version
    
      
    http://robot.obolibrary.org/

- Step 2) Go the section **getting started** -> **1. Getting Started** -> **Mac & Linux** -> **Step 1.**. These steps should lead to this link

     
    https://github.com/ontodev/robot/releases/tag/v1.8.3



A possible way to execute the jar file now, is using the go the directory where the .jar file resides on and execute **java -jar robot.jar (parameters)**. An execution example is

    java -jar robot.jar extract --method BOT --input /home/skalogerakis/Documents/Workspace/CS567/main_final_onto.owl --term-file /home/skalogerakis/Documents/Workspace/CS567/Robot/term_sample.txt --output /home/skalogerakis/Documents/Workspace/CS567/Robot/bonus_final_onto.owl


The above process is automated as requested in the python script **main.py** containing the function **get_Smodule()** which is
responsible to execute the robot .jar library with the required parameters. In order to execute that function successfully, 
the parameters of the functions must change in order to match the full paths of the corresponding system that is executed. 
    
All the required parameters are analysed in the code, but are also showcased below:

- **jar_location:** full path that robor.jar file exists
- **method:** method used from robot API, Options: BOT, TOP, STAR
- **input_location:** full path that the initial .owl file exists
- **term_location:** full path that the term file exists
- **output location:** full path and new file name that the produced .owl file will be placed

    
**NOTE: It is important to note that everything was tested in Linux environments, and changes may be required to execute in Windows**
## Version Information

All the setup steps where executed using the following versions tools:

- ROBOT version,  **v1.8.3(current latest)**
- Java version,  **openjdk version "1.8.0_312"**
- Operating System, **Ubuntu 20.04.3 LTS**

# Remarks on the deliverable

The central directory contains all the required files for the phase two. More specifically, **main.py** file contains the 
main implementation in python, **main_file_onto.owl** contains the required .owl file after changes are applied from phase 1(more on that later), 
the **requirements.txt** is required when building a virtual environment to fetch the required dependencies and lastly the **termfile.txt** is 
a signature file required for the bonus part of the assignment. 

An additional directory **/Phase2Owl** contains a different .owl file after applying the reasoner. In some cases, a reasoner
may alter the ontology and re-parent some of its instances if deemed necessary. While this file is not required from the assignment
it is also delivered for completeness. This different .owl file is generated in the last line of the python code(Currently commented out)

Finally, the directory **/BonusOwl** contains the output .owl file after executing the bonus question.


In comparison with phase 1, the changes are highlighted in the code with the comment **UPDATED**. After following 
all the suggestions from the instructor the following changes transpired

- rules 5) and 19) are commented out since they were deemed unnecessary
- rule 3) changed by removing the notion of Dwarf Planet as it was redundant. The new rule is 

        
        PlanetarySystemBody is_a CeletialBody & Not(Planet) & Not(NaturalSatellite)

- A few of the Abox rules in the CelestialBody where redudant so they where commented 


After examining the implementation of phase the below change was necessary. The Abox Instances of Ceres

    Ceres = PlanetarySystemBody("Ceres")

proved to be the instance that made our ontology inconsistent after examining the code and so it is commented out.
If commented back in, that will change the result of question 2.1, as the consistent will be inconsistent and the result 
value will be "Yes" (now the answer is "No")

Regarding the bonus and the term file provided many different scenarios were attempted however, the output .owl file
was more or less the same. Also the STAR method that was chosen was advised from the instructor as the most suitable to experiment on.
Since the different scenarios did not produce different results in .owl files a simple case is showcased as a term file.
Despite that after, comparing the .owl of the phase 1 and the output file of the tool we notice that the new ontology is slighlty more compact and minimal which was the final goal

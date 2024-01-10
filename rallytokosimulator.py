import pandas as pd
import random

START = "LÄHTÖ"
END = "MAALI"

speedchange_allowed = False
object_allowed = False
level_selection = "ALO"

if level_selection == "ALO":
    src = rf"C:\Users\taruh\rallytoko\{level_selection}.json"
    df = pd.read_json(src)
    MAX_STOP = 6

    tracklength = random.randint(10, 15)
elif level_selection == "AVO":
    src = rf"C:\Users\taruh\rallytoko\{level_selection}.json"
    tracklength = random.randint(12, 17)
    MAX_STOP = 7

elif level_selection == "VOI":
    src = rf"C:\Users\taruh\rallytoko\{level_selection}.json"
    tracklength = random.randint(15, 20)
    MAX_STOP = 8

else:
    src = rf"C:\Users\taruh\rallytoko\{level_selection}.json"
    tracklength = random.randint(18, 20) 
    MAX_STOP = 9


# Modify the pool of tasks based on preferences
# src = rf"C:\Users\taruh\rallytoko\{level_selection}.json"
df = pd.read_json(src)
if object_allowed == False:
    df = df[df.columns[df.loc["esine"] == 0]]
if speedchange_allowed == False:
    df = df[df.columns[df.loc["vauhti"] == 0]]
# Length of upcoming track
# tracklength = random.randint(10, 15)

# ALO:
# tehtävät 1-34
# lähtö+maali+10-15 tehtävää
# max 6 pysäytystä

task, prev_task = START, START
print(task)

stopcounter, i = 0, 0
while i < tracklength:
    # Select task
    task = df.iloc[:, random.randint(0, len(df))]

    # Prevent: two same tasks in a row, too many stopping tasks, and check if objects are allowed in tasks
    stopcounter += task.pysäytys
    if task.name == prev_task or stopcounter > MAX_STOP or (task.esine == 1 and object_allowed == False):
        continue
    else:
        if i+2 > tracklength: # if maximum length is reached, select task without turning
            task = df[random.choice(df.columns[df.loc["käännös"].isin([0, 360])])]
            print(str(i+1), task.name)
            break

        if task.käännös != 0 and task.käännös != 360:
            print(str(i+1), task.name) # 1. turning
            prev_task = task
            i += 1

            # selecting new suitable task
            task = random.choice(df.columns[df.loc["käännös"] == 180])
            print(str(i+1), task) # 2. turning
            prev_task = task
            i += 1
        else:
            print(str(i+1), task.name)
            prev_task = task.name
            i += 1

task = END
print(task)
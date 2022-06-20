"""
Group Information:
    Member 1: 620127969 
    Member 2: N/A
"""

#!/bin/python3

import math
import os
import random
import re
import sys


# global variable used to compute next unique number.

__nextUniqueNumber__ = 0


# This function computes next unique number by incrementing the current
# value of the global variable __nextUniqueNumber__ by one.

def __getUniqueNumber__():
    global __nextUniqueNumber__
    __nextUniqueNumber__= __nextUniqueNumber__ + 1
    return __nextUniqueNumber__



# This function expects a name as a parameter, and returns a
# PatientRecord object - tuple with a tag and a dictionary
 
def makePatientRecord(patient):    
    return ( "patient_record", { 'name': patient,
                                 'medical_record': __getUniqueNumber__(),
                                 'currentEncounter': None,
                                 'previousEncounters': [] } )


# accepts a value and returns a boolean based on whether the value
# conforms to the structure of a patient record
 
def isPatientRecord(obj):
    if type(obj) == type(()):
        if (obj[0]) == "patient_record":
            if len(obj) == 2:
                if type(obj[1]) == dict:
                    if len(obj[1]) == 4:
                        if ('name' in obj[1]) + ('medical_record'in obj[1]) + ('currentEncounter' in obj[1]) + ('previousEncounters' in obj[1])  == 4:
                            return True
    return False



# This function accepts a record and returns the dictionary section at index 1.

def getContents(record):
    return record[1] 
    
    
    
# This function accepts a value and dtermines whether or not it is an encounter

def isEncounter(obj):
    if type(obj) == dict:
        return ("department" in obj) + ("hpc" in obj) + ("plan" in obj) + ("progressUpdates" in obj) + ("dischargeSummary" in obj) +  (len(obj) == 5) == 6
    else:
        return False

    
    
#  This function accepts as its parameters a department in the form of a string
# and returns a new encounter object - a dictionary.
 
def createEncounter(department):
    return { "department": department,
             "hpc": "",
             "plan": "",
             "progressUpdates": [],
             "dischargeSummary": "" }


    
# This function accepts, as a parameter, a patient record and an encounter and stores
# the encounter as a current encounter in the patient record.
 
def setCurrentEncounter(record, encounter):
    if isPatientRecord(record):
        if isEncounter(encounter):
            if getContents(record)['currentEncounter'] != None: # prevent adding None to previous encounters
                getContents(record)['previousEncounters'].append(getContents(record)['currentEncounter']) 
            getContents(record).update({"currentEncounter": encounter})
        else:
            print("Error: invalid type of argument2")
    else:
        print("Error: invalid type of argument1")

    
# This function accepts a patient record as a parameter.
# It closes the current encounter of a patient by adding it to the previous
# encounters and then updates the current encounter to None.
  
def closeEncounter(record):
    if isPatientRecord(record):
        if getContents(record)['currentEncounter'] != None:    # if crrent e is None, do not add to pr
            getContents(record)['previousEncounters'].append(getContents(record)['currentEncounter'])  
        getContents(record).update({"currentEncounter": None})
    else:
        print("Error: Invalid argument type")
        

# This function accepts two parameters - a patient's encounter,
# and a chief symptom as a string.
# it adds the symptom to the encounter.
  
def addHPC(encounter, symptom):
    if isEncounter(encounter): 
        encounter.update({"hpc": symptom})
    else:
        print("Error: argument1 is not an encounter")

        
        
# This function accepts a patient's encounter as a parameter,
# and returns a string, the hpc, - the chief complaint or presenting
# symptom of the patient.
  
def getHPC(encounter):
    if isEncounter(encounter):
        return encounter['hpc']
    else:
        return 'Error: argument1 is not an encounter'


    
# This function accepts an encounter, and a care plan as a string then
# adds it to the patient's encounter.
 
def addPlan(encounter, care_plan):
    if isEncounter(encounter): 
        encounter.update({"plan": care_plan})
    else:

        print("Error: argument1 is not an encounter")


# This function accepts a patient's encounter and returns the care plan
# from the the encounter.
 
def getPlan(encounter):
    if isEncounter(encounter):
        return encounter['plan']
    else:
        return 'Error: argument1 is not an encounter'


# This function accepts a patient's encounter and a progress update 
# as a string. It then adds the the progress update to the encounter
# by updating the encounter with the list of all previous updates
# added with the new update.
   
def addProgressUpdate(encounter, prog_update):
    if isEncounter(encounter):
        temp = getProgressUpdates(encounter)[:]
        temp = temp + [prog_update]
        encounter.update({"progressUpdates": temp})
    else:
        print("Error: argument1 is not an encounter")    


# This function accepts a patient's encounter and returns a list of
# the patient's progress updates.
 
def getProgressUpdates(encounter):
    if isEncounter(encounter):
        return encounter['progressUpdates']
    else:
        return None
    

# This functions accepts two parameters: a patient's encounter
# and summary of the discharge. The summary is added to the patient's encounter.

def addDischargeSummary(encounter,summary):
    if isEncounter(encounter):
        encounter.update({"dischargeSummary": summary})
    else:
        print("Error: argument1 is not an encounter")        

        
# This function accepts a patient's encounter and returns the
# discharge summary.
 
def getDischargeSummary(encounter):
    if isEncounter(encounter):
        return encounter['dischargeSummary']
    else:
        return 'Error: argument1 is not an encounter'    
    



# This function accepts a patient's record and returns True if the
# patient is currently admitted, and false otherwise.
 
def isCurrentlyAdmitted(p_record):
    if isPatientRecord(p_record):      # is it a valid UWIH record.       
        if getContents(p_record)['currentEncounter'] != None:  # tests whether the patient has a current encounter.
            return True
    return False   

    

# This function accepts a patient record then determines whether the person is
# currently admitted at the facility. If yes, the Department from the current
# encounter on record is returned.

def locatePatient(record):
    if isCurrentlyAdmitted(record):
        return getContents(record)['currentEncounter']['department'] # returns the department of the patient's current encounter.
    return 'Discharged'    
    


# This function accepts a list of patient records, and a name as string.
# It searches the library using the given name. If found the electronic
# file from the library is returned.
      
    
def getPatientRecord(library, name):
    if library != []:
        for p in library:            # traverses the records library.
            if getContents(p)['name'] == name: # campares the name on each record to the given name,
                return p                 # return the record from the library.
    return None
    

    
# This function presents the user with a list of menu options and prompts
# for a valid input, which is then returned to the calling function.
  
def menu():
    print('UHWI - Electronic Health Record System - Main Menu\n')
    print('1) New Registration')
    print('2) Search for patient')
    print('3) Admit Patient')
    print('4) Discharge Patient')
    print('5) Locate Patient')
    print('6) Add Clinical Notes')
    print('7) View Progress Updates')
    print('X) Exit Application')

    response = input('')    
    while not response in ['1','2','3','4','5','6','7','X','x']:
        response = input('')         
    return response
 
    
    
# This function prompts the user for a name, then creates and returns a new record.

def registration():
    print('UHWI - Electronic Health Record System - Register new patient\n')
    name = input('What is the full name of the patient? ')
    return makePatientRecord(name)



# This function accepts a list of patient records.
# It prompts the user for the full name of an individual, then searches the library
# for a record containing that name. If the record is found it is returned.
# If the name is not found the user is prompted to
# enter 'Y' or 'N' for whether further searches should be done.

def searchRecords(library):
    print('UHWI - Electronic Health Record System - Search for patient\n')

    name = input('What is the full name of the patient? ')
    record = getPatientRecord(library, name)

    if record != None:
        print('Patient Found. Retrieving Patient.') 
        return record
    else:        
        continue_ = 'Y'
        while continue_.upper() == 'Y':
            continue_ = input('Record with '+name+' Not Found.  Do you want to keep searching (Y/N)? ')
            
            if continue_.upper() == 'Y':
                name = input('What is the full name of the patient? ')
                record = getPatientRecord(library, name)
                if record != None:
                    print('Patient Found. Retrieving Patient.')
                    return record
                    continue_ = 'N'
 


# This function accepts a patient record and prompts the user to enter the name of
# the department where the patient should be admitted. If the user does not cancel,
# the department name is used to create an encounter which is then added to the
# patient's record. 

def admitPatient(record):
    print('UHWI - Electronic Health Record System - Admit Patient\n')
    dept = input("Where do you want to admit the patient? Type 'X' to cancel: ")
    
    if dept.upper() == 'X':
        print('Cancelling Admission')
    else:
        encounter = createEncounter(dept)
        setCurrentEncounter(record, encounter)
        print('Admitted to',dept)


    
# This function accepts a patient record and prompts the user to enter Y or N
# to determine whether or not the patient gets discharged.

def dischargePatient(record):
    print('UHWI - Electronic Health Record System - Discharge Patient\n')

    response = input('Are you sure you want to discharge the patient Y/N? ')
    while response not in ['Y','N','y','n']:
        response = input('')
        
    if response.upper() == 'Y':
        closeEncounter(record)
        print('Patient Discharged!')
    else:
        print('Discharge Cancelled!')


        
# This function accepts a list of records and prompts the user for the name of
# the person to be located. Appropriate messages are printed for whether the
# person is currently admitted in a department, has been discharged, or cannot
# be found.
   
def locatePatientUI(library):
    print('UHWI - Electronic Health Record System - Patient Location\n')    
    name = input('Please enter the name of the patient you are trying to locate: ')

    if library == []:
        print('Unable to find patient')
    else:
        record = getPatientRecord(library, name)

        if record == None:
            print('Unable to find patient')
        else:
            location = locatePatient(record)
            print('Patient Location:',location)

    

# This function accepts a patient record.
# It calls the submenu function which returns a value.
# Based on the value, prompts are made to the user for various information
# then function calls are made to produce the desired results.

def addDocumentation(record):
    print('UHWI - Electronic Health Record System - Patient Documentation\n')
    value = submenu()
    encounter = getContents(record)['currentEncounter']
    
    while value.upper() != 'X':
        if value == '1':
            symptom = input('Please enter the HPC: ')
            addHPC(encounter, symptom)

        elif value == '2':
            care_plan = input('Please enter the Plan: ')
            addPlan(encounter, care_plan)

        elif value == '3':
            prog_update = input('Please enter the Progress Notes: ')
            addProgressUpdate(encounter, prog_update)

        elif value == '4':
            summary = input('Please enter the Discharge Summary: ')
            addDischargeSummary(encounter,summary)
            
        value = submenu()
   

# This function accepts no prameters.
# It prints a menu and returns a valid input.

def submenu():
    print('Please select an option below: (X) to exit\n')
    print('1) Add HPC')
    print('2) Add Plan')
    print('3) Add Progress Notes')
    print('4) Add Discharge Summary')

    response = input('')
    while response not in ['1','2','3','4','X','x']:
        response = input('')
    return response

            
#    
# This function prompts the user to enter the name of the patient to be located.
# If found the progress updates for that patient are printed.
#

def viewProgressUpdates(library):
    print('UHWI - Electronic Health Record System - View Progress Updates\n')
    name = input('Please enter the name of the patient you are trying to view: ')
    record = getPatientRecord(library, name)
    if record == None:
        print('Unable to find patient')
    else:
        encounter = getContents(record)['currentEncounter']
        p_updates = getProgressUpdates(encounter) 
        for n in p_updates:
            print(n)
                             


#
# This is the main function  that automatically launches the 
# interface menu that gives the users various abilities.
#

def patient_rec():
    def checkRecordSelected(record):
        if record == None:
            print("Please register or search for a patient ")
            return False
        else:
            return True

    library = []
    record = None
    exitWindow = False

    while not exitWindow:
        value = menu()
        if value == "1":
            record = registration()
            library.append(record)   # adds the new record to the library.
            
        elif value == "2":
            record = searchRecords(library)
            
        elif value == "3":
            if checkRecordSelected(record):
                admitPatient(record)
                
        elif value == "4":
            if checkRecordSelected(record):
                dischargePatient(record)
                
        elif value == "5":                        
            locatePatientUI(library)
               
        elif value == "6":
            if checkRecordSelected(record):
                addDocumentation(record)
            
        elif value == "7":
            viewProgressUpdates(library)            

        else:
            exitWindow = True

            
patient_rec()


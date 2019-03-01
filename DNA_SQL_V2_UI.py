# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 18:21:43 2019

@author: karapet
"""
import os
import sys
import sqlite3

import matplotlib.pyplot as plt

from pandas.plotting import scatter_matrix

import DNA_OBJECT_CLASS as DNA_OBJ

import pandas as pd

import string

import re


def main():
    
# Code for having user input database information before starting/ommitted as database is same in folder       
#    database_name = input('Enter the SQLITE database name: ').lower()
#    con=sqlite3.connect(database_name)
#    cur = con.cursor() 
    
    database_name="dna_sequencer_database.sqlite"
    
    con=sqlite3.connect(database_name)
    cur = con.cursor()
      
    user_choice=None
    while(user_choice != -1 ):
        user_choice=first_dash_select_processing_options(con,cur,database_name)
        if user_choice==1:
            SQL_CREATE_TABLE_amino_acids(con,cur)
        elif user_choice==2:
            DNA_Processing(con,cur,database_name)
        elif user_choice==3:
            PROTEIN_proccesing(con,cur,database_name)
        elif user_choice==4:
            SQL_main(con,cur,database_name)
        elif user_choice==5:
            print("Database {} has the following Information:".format(database_name))
            current_table_names(con,cur)
        elif user_choice==6:
            database_name = input('Enter the SQLITE database name: ').lower()
            con=sqlite3.connect(database_name)
            cur = con.cursor()
            
    cur.close()
    con.close()
    
#ORGINAL CODE OF CREATING EACH INDIVDUAL LAYER BEFORE UI WAS ESTABLISHED
#    user_choice=input("Would you like to create a new amino acid database in dna_sequencer_database? -'y' or 'n': ").lower()
#    while(user_choice!='y'and user_choice!='n'):
#        user_choice=input("Would you like to create a new amino acid database in dna_sequencer_database? -'y' or 'n': ").lower()
#        
#    if (user_choice=='y'):
#        SQL_CREATE_TABLE_amino_acids(con,cur)
#        
#    user_choice=input("Would you like to create process a New DNA Sequence? -'y' or 'n': ").lower()
#    while(user_choice!='y'and user_choice!='n'):
#        user_choice=input("Would you like to create a new amino acid database in dna_sequencer_database? -'y' or 'n': ").lower()
#
#    if (user_choice=='y'):
#        DNA_Processing(con,cur,database_name)
#
#    user_choice=input("Would you like to process a DNA Sequence's Protein Sequence? -'y' or 'n': ").lower()
#    while(user_choice!='y'and user_choice!='n'):
#        user_choice=input("Would you like to process a DNA Sequence's Protein Sequence? -'y' or 'n': ").lower()
#    
#    if user_choice=='y':
#        PROTEIN_proccesing(con,cur,database_name)


#--------------------------------------

#START OF FUNCTIONS

#--------------------------------------
    
    
#--------------------------------------
    #UI PROCESSING

#--------------------------------------

#USER INTERFACE ON START GIVES OPTIONS OF HOW TO PROCCESS FILES
def first_dash_select_processing_options(con,cur,database_name):
    
    while True:
        print("===============================================================================")
        print("HERE IS A LIST OF OPTIONS YOU MAY TAKE IN PROCESSING DNA INFORMATION: ")
        print("1. AMINO ACIDS - CREATE TWO TABLES (AMINO ACIDS & AMINO ACIDS DETAILED)")
        print("2. DNA - PROCESS DNA FILE INPUT INO DATABASE (SEQUNCES AND READING FRAMES TABLES)")
        print("3. PROTEIN - PROCESS ANY DNA FILE FOUND IN SEQUENCES TABLE FOR PROTIEN CONFIGURAITON")
        print("4. SQL - Statements for Accessing DNA/PROTEIN INFORMATION")
        print("5. TABLES- LIST OF ALL THE TABLES IN CURRENT DATABASE {}".format(database_name))
        print("6. DATABASE - CHANGE DATABASE FROM CURRENT {} TO NEW DATABASE".format(database_name))
        print("===============================================================================")
        try:
            user_choice=int(input("Please select an OPTION above (-1 to exit program): "))
            if((user_choice>0 and user_choice<7) or user_choice==-1):
                return user_choice
            else:
                print("INVALID OPTION PLEASE TYPE A CHOICE OF '1' THRU '6' OR -1 TO EXIT PROGRAM!")
        except:
            print("ONLY NUMBERS # ARE VALID OPTIONS; PLEASE TYPE A CHOICE OF '1' THRU '6' OR -1 TO EXIT PROGRAM!")

    
#LIST OF ACTIONS FOR SELECTION BY USER IN PROTEIN SEQUENCE; FOR SQL SELECT STATEMENT  
def protein_ui_choice_screen(database_name):
    print("/n")
    print("=======================================================")
    print("Below are the options for protein sequencing of DNA stored in {}".format(database_name))
    print("1. Select Protein segement from a table in {} Database".format(database_name))
    print("2. Sequence with Amino Acid Name")
    print("3. Sequence with 3-Letter-Symbol")
    print("4. Sequence with 1-Letter-Symbol")
    print("5. Moleculuar weight of segement")
    print("Please select a number as choice or 'n' to exit")
    choice=input()
    print("/n")
    print("=======================================================") 
    return choice
    
    
#PRINTS AND RETURNS A LIST OF TABLES CURRENTLY IN DATABASE PYTHON IS ACTIVE ON
def current_file_names_in_table(con,cur,table_name):
     file_names=SQL_file_names_in_table(con,cur,table_name)
     ui_number=0
     for name in file_names:
        print("{}. {}".format(ui_number+1,name))
        ui_number+=1
     return file_names
    
#EXITS PROGRAM OR RETURNS THE SELECTED FILE NAME WANTED FOR PROTEIN SEQUENCES. USES A TABLE SELECTED BY USER PRIOR; GIVES OPTION TO CHANGE IN FUCNTION IF NEEDED
def DNA_file_name_selection_from_table(con,cur):
        print("===============================================================================")
        print("TABLE SELECTION FOR DNA FILE NAME")
        table_name=table_name_selection(con,cur,'y')

        
        print("===============================================================================")
        print("DNA FILE NAME SELECTION")
        print("Please select the file_name in current table {} to proccess for a protein sequence. ".format(table_name))
        print("SEE OPTIONS BELOW:")
        print("===============================================================================")
        file_names=current_file_names_in_table(con,cur,table_name) 
        
        user_input=int(input("Please select number of table you want to access: '{}' to '{}' or '-1' FOR ANOTHER TABLE: ".format(1,len(file_names))))

        while(user_input<=0 or user_input>len(file_names)):
            
            print("INVLAID CHOICE PLEASE TYPE A NUMBER LISTED")
            user_input=input("Do you still want a file to proccess from table {} - 'y' or 'n':".format(table_name)).lower()
            while(user_input!='y'and user_input!='n'):
                user_input=input("Do you still want a file to proccess from table {} - 'y' or 'n':".format(table_name)).lower()
            if user_input=='y':
                current_file_names_in_table(con,cur,table_name)
                user_input=int(input("Please select number of table you want to access: '{}' to '{}' or '-1' FOR ANOTHER TABLE: ".format(1,len(file_names))))        
            else:
                user_input=input("Would you like to process ANOTHER table in current DATABASE? - 'y' or 'n':" ).lower()
                while(user_input!='y'and user_input!='n'):
                    user_input=input("Would you like to process ANOTHER table in current DATABASE? - 'y' or 'n':" ).lower()
                if user_input=='y':
                    table_name=table_name_selection(con,cur,user_input)
                    file_names=current_file_names_in_table(con,cur,table_name)
                    user_input=int(input("Please select number of table you want to access: '{}' to '{}' or '-1' FOR ANOTHER TABLE: ".format(1,len(file_names))))
                else: 
                    sys.exit("Can't proccess for Protein for SQL without file_name for DNA" )
                    return None
            
        return((table_name,file_names[user_input-1]))


    
#retrives all tables names from active database in python
#and prints them out in a UI for selection in two other functions table_name_selection  and DNA_filE_name_selection_from_table
def current_table_names(con,cur):
    print("===============================================================================")
    print("HERE IS A LIST OF ALL TABLE NAMES IN CURRENT DATABASE:")
    table_names=SQL_database_all_table_names(con,cur)
    ui_number=0
    for name in table_names:
        print("{}. {}".format(ui_number+1,name))
        ui_number+=1
    print("===============================================================================")
    return table_names

#returns table name selected or None if none selected
def table_name_selection(con,cur,user_input):

        
        while(user_input!='y'and user_input!='n'):
            user_input=input("Select a Table found in Current Database? - 'y' or 'n': ").lower()
            
        if user_input=='y':
    
            
            table_names=current_table_names(con,cur) 
            
            user_input=int(input("Please select number of table you want to access: '{}' to '{}' or '-1' to exit: ".format(1,len(table_names))))
    
            while(user_input<=0 or user_input>len(table_names)):
                
                print("INVLAID CHOICE PLEASE TYPE A NUMBER LISTED")
                user_input=input("Select a Table found in Current Database? - 'y' or 'n': ").lower()
                while(user_input!='y'and user_input!='n'):
                    user_input=input("Select a Table found in Current Database? - 'y' or 'n': ").lower()
                if user_input=='n':
                    return None
                
                current_table_names(con,cur)   
                user_input=int(input("Please select number of table you want to access '{}' to '{}' or '-1' to exit: ".format(1,len(table_names))))
                if(user_input==-1):
                    return None
    
            return(table_names[user_input-1])
        else:
            return None

#--------------------------------------
    #AMINO ACIDS PROCESSING

#--------------------------------------

#builds amino acid chart in both a list and dataFrame
#Sends data off to a sql table as well, named amino_acid_chart
#makes also amino_acid_chart_detailed with more infromation, 
#CREATES TABLE FOR AMINO ACIDS AND AMINO ACIDS DETAILED. USES TWO FILES aminochart.txt and aminochartdetailed.csv
#USES A DATAFRAME FOR BOTH AND SENDS TO FUNCTION SQL_build_amino_table_by_df
#WILL ALWAYS DELETE AND CREATE A NEW TABLE; 
#UPDATE TOOK AWAY USER OPTION OF NAME, NOW HARD CODED AS amino_acids and amino_acids_detailed
def SQL_CREATE_TABLE_amino_acids(con,cur):
   
    fname = input('Enter the file name WITH AMINO CHART: ')
    
    file_object=open_file(fname)
    
#    count=0
    AMINO_CHART_RAW=list()
 ## makes a list that can be used to build dictionary; opted to use data frame kept to show details      
    for line in file_object:
#        print(count," ",line)
#        count+=1
        line_parsed=line.split()
#        print(line_parsed)
        AMINO_CHART_RAW.append(line_parsed)
    
    df=pd.read_csv(fname,header=None)

   
    df=pd.DataFrame(AMINO_CHART_RAW)
    df.columns=["amino_sequence","name","three_letter_symbol","one_letter_symbol"]

    SQL_build_amino_table_by_df(df,con,cur,"amino_acids")
    
    fname = input('Enter the file name WITH AMINO CHART Detailed: ')
    
    file_object=open_file(fname)
    
    df=pd.read_csv(fname,header=0)

    SQL_build_amino_table_by_df(df,con,cur,"amino_acids_detailed")    
        
#--------------------------------------
    #DNA MAIN PROCESSING

#--------------------------------------

#Process a DNA SEQUENCE by creating all 6 open reading frames to find all start and stop sequences and indicates which start and stop combination
#codes for the proetin found in the sequence
def DNA_Processing(con,cur,database_name):
    
    #   FILE OPENING VARIABLES, FOR DNA RAW
    DNA_FILE_NAME = input('Enter the file name WITH DNA SEQUENCE: ').lower()  
    fhand=open_file(DNA_FILE_NAME)
    DNA_temp=fhand.read().replace('\n','')
    DNA_RAW = re.sub("[^a-zA-Z]","", DNA_temp).lower()
    
#   DNA HANDLING CONDITIONS; SEES HOW TO INITIALIZE VARIABLES
    dna_ends=input("Is the DNA SEQUENCE in 5' to 3' End - 'y' or 'n': ").lower()
    while(dna_ends!='y'and dna_ends!='n'):
        dna_ends=input("Is the DNA SEQUENCE in 5' to 3' End - 'y' or 'n': ").lower()   
    dna_strand_type_user_choice=input("What Type of Strand are you importing Template 't' or Coding 'c', or DON'T KNOW 'n': ").lower()
    while (dna_strand_type_user_choice !='t'and dna_strand_type_user_choice !='c' and dna_strand_type_user_choice !='n'):
        dna_strand_type_user_choice=input("What Type of Strand are you importing Temlate 't', Coding 'c', or DON'T KNOW 'n': ").lower()

#creates DNA OBJECT CALLED DNA_R
    if dna_ends=='y':
        DNA_R=DNA_OBJ.DNA_STRAND(DNA_RAW,dna_strand_type_user_choice)
    else:
        DNA_R=DNA_OBJ.DNA_STRAND(DNA_RAW[::-1],dna_strand_type_user_choice)
      

#CREATES sequence TABLE; Holds all start codons and related sequence found in DNA OBJECT and ALL 6 READING FRAMES
    sequence_table_name=SQL_CREATE_TABLE_sequenes(DNA_R,con,cur,DNA_FILE_NAME,database_name)
#CREATES readingFrames TABLE; Holds all 6 Reading Frames and there sequences as a legend
    readingFrames_table_name=SQL_CREATE_TABLE_reading_rames(DNA_R,con,cur,DNA_FILE_NAME,database_name)


#finds all and Stores ALL START SEQUENCES in sequence table; WILL STORE EVEN WITHOUT A STOP CODON input NULL IN END INDEX if so
    dna_rna_choice=input("Would you like to Process DNA strand or RNA: 'DNA' or 'RNA' or 'BOTH': ").upper()
    while(dna_rna_choice!='DNA'and dna_rna_choice!='RNA' and dna_rna_choice!='BOTH'):
        dna_rna_choice=input("Would you like to Process DNA strand or RNA: 'DNA' or 'RNA' or 'BOTH':").upper() 

    if dna_rna_choice=='BOTH':
        sequence_finder(DNA_R.READING_FRAMES,DNA_R.codons['DNA']['STOP'],DNA_R.codons['DNA']['START'],con,cur,sequence_table_name,readingFrames_table_name,DNA_FILE_NAME,'DNA')
        sequence_finder(DNA_R.READING_FRAMES,DNA_R.codons['RNA']['STOP'],DNA_R.codons['RNA']['START'],con,cur,sequence_table_name,readingFrames_table_name,DNA_FILE_NAME,'RNA')
    else:
        sequence_finder(DNA_R.READING_FRAMES,DNA_R.codons[dna_rna_choice]['STOP'],DNA_R.codons[dna_rna_choice]['START'],con,cur,sequence_table_name,readingFrames_table_name,DNA_FILE_NAME,dna_rna_choice)
#--------------------------------------
    #PROTEIN MAIN PROCESSING

#--------------------------------------
    
#OBTAINS TABLE AND DNA FILE THAT NEEDS TO BE PROCESSED FOR PROTEIN INPUT IN PROTEIN TABLE
def PROTEIN_proccesing(con,cur,database_name):
        
#       GET TABLE NAME AND FILE NAME OF DNA SEQUENCE THAT WILL BE PROCESSED
        table_name,file_name=DNA_file_name_selection_from_table(con,cur)
#       CREATES OR RETRIEVES PROTEIN TABLE NAME TO INPUT NEW PROTEIN 
        protein_table_name=SQL_CREATE_TABLE_proteins(con,cur,file_name,database_name)
#       RETRIVES ALL ROWS IN TABLE SELECTED THAT HAVE A PROTEIN SIGNALED 
        rows_of_protein_indicators=SQL_rows_identified_with_protein_sequence_from_specific_table_and_file_name(con,cur,table_name,file_name)
#       RETRIEVES  LIST AND RNA SEQUENCE TO PROCESS 
        found,table_list,rna_sequence=get_RNA_sequence(rows_of_protein_indicators)
        if found:
#           CREATES A LIST THAT HOLDS ALL AMINO ACIDS 
            amino_acids=SQL_JOIN_amino_acids(con,cur)
#           CREATES AND INSERTS PROETIN INTO PROTEIN TABLE IN DATABASE 
            protein=SQL_INSERT_protein(cur,con,table_list,rna_sequence,amino_acids,protein_table_name)
            print("INSERT FOLLOWING PROTEIN SEQUENCE INTO {} TABLE".format(protein_table_name))
            print(protein)
          
#--------------------------------------

#FILE PROCESSING

#--------------------------------------

#Opens file and returns file object
def open_file(fname):
    try:
        fhand = open(fname)
    except:
        print('File cannot be opened:', fname)
        exit()
    return(fhand)

#CREATES OR SELECTS TABLE FOR USER IN READING FRAMES, SEQUENCES TABLES NEEDED FOR DATABASE AND PROCCESSING OF FILES IN DNA PROCESSING AND PROTEIN PROCESSING
def user_table_input_loop(con,cur,table_name,dna_name,database_name):
    print("===============================================================================")
    print("{} TABLE CREATION OR SELECTION".format(table_name))
    print("===============================================================================")
    end_loop=False
    user_input=input("CREATE A NEW TABLE that contains all {} of {} DNA Sequence?: 'y' or 'n' or '-1' TO EXIT PROGRAM: ".format(table_name,dna_name)).lower()
    while(not(end_loop)):
        
        while(user_input!='y'and user_input!='n' and user_input!='-1'):
            user_input=input("CREATE A NEW TABLE that contains all {} of {} DNA Sequence?: 'y' or 'n' or '-1' TO EXIT PROGRAM: ".format(table_name,dna_name)).lower()
            
        if user_input=='y':
            return user_input
        elif user_input=='-1':
            sys.exit("PROGRAM EXIT COULD NOT SELECT OR CREATE VIABLE TABLE IN DATABASE")
        else:
            
            tableSelect_user_input=input("SELECT A TABLE in Current Database {}? - 'y' or 'n': ".format(database_name)).lower()
            while(tableSelect_user_input!='y'and tableSelect_user_input!='n'):
                tableSelect_user_input=input("SELECT A TABLE in Current Database {}? - 'y' or 'n': ".format(database_name)).lower()
                
            if tableSelect_user_input=='y':
                user_table_name=table_name_selection(con,cur,tableSelect_user_input)
                print("===============================================================================")
                print("TABLE SELECTED {}".format(user_table_name))
                print("===============================================================================")
                if user_table_name !=None:
                        print("\n"+ user_table_name+" WILL BE USED")
                        return user_table_name
            else:
                user_input=input("CREATE A NEW TABLE that contains all {} of {} DNA Sequence?: 'y' or 'n' or '-1' TO EXIT PROGRAM: ".format(table_name,dna_name)).lower()
                while(user_input!='y'and user_input!='n' and user_input!='-1'):
                    user_input=input("CREATE A NEW TABLE that contains all {} of {} DNA Sequence?: 'y' or 'n' or '-1' TO EXIT PROGRAM: ".format(table_name,dna_name)).lower()
                
               
#--------------------------------------

#SQL PROCESSING
    
#--------------------------------------
#RETRIEVES ALL THE INSTANCES A PROTEIN SEQUENCE WAS FOUND FROM THE SEQUENCES TABLE FOR A SPECIFIC FILE NAME
def SQL_rows_identified_with_protein_sequence_from_specific_table_and_file_name(con,cur,table_name,file_name):
    
    select_statement=("SELECT *FROM {} WHERE file_name=? AND file_protein_sequence_indicator=? ;".format(table_name))
    cur.execute(select_statement,(file_name,1))
    sequences_with_protein=cur.fetchall()
    con.commit()
  
    return sequences_with_protein

#RETRIEVES ALL THE TABLES NAMES CURRENTLY ACTIVE IN CURRENT DATABASE PYTHON IS LINKED TO
def SQL_database_all_table_names(con,cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names_list_tuples=cur.fetchall()
    con.commit()
    table_names=list()
    for tuple_table in table_names_list_tuples:
        table_names.append(tuple_table[0])

    return table_names

#RETRIEVES ALL FILES NAMES IN SPECIFIC TABLE
def SQL_file_names_in_table(con,cur,table_name):
    select_statement=("SELECT DISTINCT file_name FROM {} ;".format(table_name))
    cur.execute(select_statement)
    file_names_list_tuples=cur.fetchall()
    con.commit()
    files_names=list()
    for file_tuple in  file_names_list_tuples:
        files_names.append(file_tuple[0])
    
    return files_names
        
#CREATES SQL TABLE IN CURRENT ACTIVE PYTHON DATABASE
#USED FOR BOTH AMINO TABLES; USES A DATAFRAME(DF)
def SQL_build_amino_table_by_df(df,con,cur,table_name):
    df.to_sql(table_name,con,if_exists="replace")
    
#OBTAINS PRIMARY KEY ID FROM  READING_FRAMES TABLE BASED ON DNA_FILE_NAME,STRAND_TYPE,READING_FRAME, sequence type
def SQL_reading_frames_primary_ID(readingFrames_table_name,DNA_FILE_NAME,STRAND_TYPE,READING_FRAME,cur,con,sequence_type):
#    print("DEBUGGING:",readingFrames_table_name,DNA_FILE_NAME,STRAND_TYPE,READING_FRAME,cur,con,sequence_type)
    
    select_statement=("SELECT id FROM "+ readingFrames_table_name  +" WHERE (file_name=? AND strand_type=? AND reading_frame=? AND sequence_type=? );")
    
#    print("DEBUGGING: ",select_statement)
    cur.execute(select_statement,(DNA_FILE_NAME,STRAND_TYPE,READING_FRAME,sequence_type))
    tuple_readingFrames_id=cur.fetchone()
#    print("DEBUGGING: ",tuple_readingFrames_id)
    readingFrames_id=tuple_readingFrames_id[0]
    con.commit()
    return readingFrames_id

#CREATES A TABLE TO STORE ALL THE SEQUENCES THAT WILL BE FOUND WITH A START CODON FOR A SPECIFIC DNA FILE
#WILL STORE IN ACTIVE PYTHON DATABASE
#COLUMNS THAT WILL BE ACTIVE ARE THE FOLLWOING: file_name TEXT NOT NULL,sequence_type TEXT NOT NULL,strand_type text NOT NULL,reading_frame text NOT NULL,readingFrames_id_DNA_ORGINAL integer NOT NULL,
#start_index integer NOT NULL,end_index integer,protein_sequence text NOT NULL,protein_sequence_index_length integer,file_protein_sequence_indicator integer NOT NULL,found_stop integer NOT NULL                                     
def SQL_CREATE_TABLE_sequenes(DNA,con,cur,DNA_FILE_NAME,database_name):
 
    create_new_table_choice=user_table_input_loop(con,cur,"SEQUENCES",DNA_FILE_NAME,database_name)
    while(create_new_table_choice==None):
        create_new_table_choice=user_table_input_loop(con,cur,"SEQUENCES",DNA_FILE_NAME,database_name)
        
    
    if create_new_table_choice!='y':
        return create_new_table_choice

    

    if create_new_table_choice=='y':
        table_name_sequence_database=input('What would you like to call the Table that will contain all sequences found in DNA file {}: '.format(DNA_FILE_NAME))
                
        if not(SQL_TABLE_EXISTS_in_database(con,cur,table_name_sequence_database)):    
            sql_create_Sequence_Table = """CREATE TABLE IF NOT EXISTS """+table_name_sequence_database+""" (
                                            id INTEGER PRIMARY KEY,
                                            file_name TEXT NOT NULL,
                                            sequence_type TEXT NOT NULL,
                                            strand_type text NOT NULL,
                                            reading_frame text NOT NULL,
                                            readingFrames_id integer NOT NULL,
                                            start_index integer NOT NULL,
                                            end_index integer,
                                            protein_sequence text NOT NULL,
                                            protein_sequence_index_length integer,
                                            file_protein_sequence_indicator integer NOT NULL,
                                            found_stop integer NOT NULL
                                            );"""
                                        
            cur.execute(sql_create_Sequence_Table)
            con.commit()
    else:
       print("\n"+ table_name_sequence_database+" WILL BE USED")   
        
    return table_name_sequence_database

#checks to see if sqlite table exists in database; NEEDED for reading_frames; TO SEE IF WE MAY HAVE DATABASE ALREADY TO RETRIEVE PRIMARY KEY ID NUMBERS
#Returns true if exists, false if doesn't
def SQL_TABLE_EXISTS_in_database(con,cur,table_name):
    select_statement="SELECT count(*) FROM sqlite_master WHERE (type='table' and name=(?));"
    cur.execute(select_statement,(table_name,))
    table_exists=cur.fetchone()
    con.commit()
    if table_exists[0]==1:
        return True
    else:
        return False

#CREATES A TABLE TO HOLD ALL THE READING FRAMES (12 ORFS -6 DNA and 6 RNA CODING AND TEMPLATE STRANDS)
#WILL INCREMENT CORRECTLY IN TABLE AND HAVE UNIQUE PRIMARY KEY ID FOR EACH ORF FOR EACH DNA FILE NAME; 
#PRIMARY KEY MANUALLY DONE BY FINDING LAST ENTRY IN TABLE; CHECKS TO SEE IF TABLE NAME IS ACTIVE BEFORE INPUTING KEY NUMBERS*     
def SQL_CREATE_TABLE_reading_rames(DNA,con,cur,DNA_FILE_NAME,database_name):
        
        create_new_table_choice=user_table_input_loop(con,cur,"READING FRAMES",DNA_FILE_NAME,database_name)
    
        table_name=create_new_table_choice
        if create_new_table_choice=='y' or create_new_table_choice=='n':
            table_name = input('Enter Table name for SQL lite Database for READING FRAMES TEMPLATE AND CODING(Contains 6 Open Reading Frames): ')
        
        if SQL_TABLE_EXISTS_in_database(con,cur,table_name):
                select_statement=("SELECT * FROM "+table_name+" WHERE (file_name=?);")
                cur.execute(select_statement,(DNA_FILE_NAME,))
                entry=cur.fetchone()
                if entry is None:
                    dna_data_list=list()
                    
                    select_statement=("SELECT max(id) FROM "+table_name+" ;")
                    cur.execute(select_statement)
                    entry=cur.fetchone()
                    primary_id=entry[0]+1
                    for sequence_type in DNA.READING_FRAMES:
                        for strand_type in DNA.READING_FRAMES[sequence_type]:
                            for reading_frame in DNA.READING_FRAMES[sequence_type][strand_type]:
                                strand_list=[primary_id]
                                primary_id=primary_id+1
                                strand_list.append(DNA_FILE_NAME)
                                strand_list.append(sequence_type)
                                strand_list.append(strand_type)
                                strand_list.append(reading_frame)
                                strand_list.append(DNA.READING_FRAMES[sequence_type][strand_type][reading_frame])
                                strand_list.append(len(DNA.READING_FRAMES[sequence_type][strand_type][reading_frame]))
                                dna_data_list.append(strand_list)
        
                else:
                    print("\n\n"+ table_name+" is ALREADY IN FILE")
                    return(table_name)
        else:

            dna_data_list=list()
            primary_id=0
            for sequence_type in DNA.READING_FRAMES:
    #            print(sequence_type)
    #            print(DNA.READING_FRAMES)
                for strand_type in DNA.READING_FRAMES[sequence_type]:
                        for reading_frame in DNA.READING_FRAMES[sequence_type][strand_type]:
                            strand_list=[primary_id]
                            primary_id=primary_id+1
                            strand_list.append(DNA_FILE_NAME)
                            strand_list.append(sequence_type)
                            strand_list.append(strand_type)
                            strand_list.append(reading_frame)
                            strand_list.append(DNA.READING_FRAMES[sequence_type][strand_type][reading_frame])
                            strand_list.append(len(DNA.READING_FRAMES[sequence_type][strand_type][reading_frame]))
                            dna_data_list.append(strand_list)
                             
        column_names=["id","file_name","sequence_type","strand_type","reading_frame","dna_sequence","dna_sequence_length"]
        df=pd.DataFrame(columns=column_names,data=dna_data_list)
     
        df.to_sql(table_name, con, if_exists="append",index=False)   
        return table_name
    
    
#CREATE TABLE THAT WILL HOLD ALL PROTEINS FOUND; SAVES SEQUENCE AND REDING FRAME ID NUMBERS AS WELL 
def SQL_CREATE_TABLE_proteins(con,cur,DNA_FILE_NAME,database_name):
    
    
    create_new_table_choice=user_table_input_loop(con,cur,"PROTEIN SEQUENCES",DNA_FILE_NAME,database_name)
    
    if create_new_table_choice=='y':
    
        table_name = input('Enter Table name for SQL lite Database for PROTIEN SEQUENCE INFORMATION Database(Contains all start-stop iterations in Sequence): ')
        
        if not(SQL_TABLE_EXISTS_in_database(con,cur,table_name)):
            
            sql_create_Sequence_Table = """CREATE TABLE IF NOT EXISTS """+table_name+""" (
                                            id INTEGER PRIMARY KEY,
                                            file_name TEXT NOT NULL,
                                            readingFrames_id integer NOT NULL,
                                            sequences_id integer NOT NULL,
                                            rna_sequence text NOT NULL,
                                            protein_sequence_one_letter text NOT NULL,
                                            protein_sequence_three_letter text NOT NULL,
                                            protein_sequence_name text NOT NULL,
                                            molecular_weight integer NOT NULL,
                                            amino_acids_count integer NOT NULL
                                            );"""
                                                    
            cur.execute(sql_create_Sequence_Table)
            con.commit()
    else:
        
        DNA_FILES_IN_TABLE=SQL_file_names_in_table(con,cur,create_new_table_choice)
        
        if DNA_FILE_NAME in DNA_FILES_IN_TABLE:
            sys.exit("ERROR TRYING TO PROCCESS SAME DNA FILE NAME {} ALREADY EXISTS IN {} TABLE CHECK DATABASE".format(DNA_FILE_NAME,create_new_table_choice))
        
        
        print("\n"+ table_name+" WILL BE USED FOR PROTEIN TABLE")   
                    
    return table_name

#JOINS AMINO ACIDS TABLES TOGETHER AND SENDS BACK THE JOIN FOR USE IN PROTEIN SEQUENCE BUILDING
#ASKS USER WHAT THE TABLE NAME SHOULD BE  AND THAN
#changes 3-letter-codons to be lower case for comparison in protein sequence finding
def SQL_JOIN_amino_acids(con,cur):
    
 
    amino_acids_table="amino_acids"
    amino_acids_detailed_table="amino_acids_detailed"
    
    select_statement=("SELECT {}.*, {}.molecular_weight FROM {} LEFT JOIN {} ON {}.one_letter_symbol={}.one_letter_symbol;".format(amino_acids_table,amino_acids_detailed_table,amino_acids_table, amino_acids_detailed_table,amino_acids_table,amino_acids_detailed_table))
#    print(select_statement)
    cur.execute(select_statement)
    amino_details=cur.fetchall()
    con.commit()
#    print (amino_details)
    
    new_aminos=list()
    for tups in amino_details:
        counter=0
        new_entries=list()
        for entry in tups:
            if counter==1:
                new_entries.append(entry.lower())
            else:
                new_entries.append(entry)
                
            counter+=1
            
        new_aminos.append(new_entries)
  
    return new_aminos
#--------------------------------------

#DNA PROCESSING; FIND PROTEIN SEQUENCE

#--------------------------------------

#LOOPS THROUGH A DNA OBJECT FOR EACH EADING FRAME; BUT WILL ONLY DO OPTION SELECTED BY USER DNA, RNA, OR BOTH
#WILL ALSO FIND THE PROTEIN SEQUENCES AT END OF FOR LOOP.
def sequence_finder(DNA,STOP_CODONS,START_CODON,con,cur,sequence_table_name,readingFrames_table_name,DNA_FILE_NAME,sequence_type):
    database_entries=int(0)
    for dna_rna_type in DNA:
        if dna_rna_type==sequence_type:
            for strand_type in DNA[dna_rna_type]:
                        for reading_frame in DNA[dna_rna_type][strand_type]:
                            database_entries+=find_start_codon(strand_type,reading_frame,DNA[dna_rna_type][strand_type][reading_frame],STOP_CODONS,START_CODON,con,cur,sequence_table_name,readingFrames_table_name,DNA_FILE_NAME,dna_rna_type)
            
    find_protein_sequence(con,cur,sequence_table_name,DNA_FILE_NAME,sequence_type)
    print("{} DATABASE FOR FILE_NAME {} FOR SEQUENCE_TYPE {} HAS BEEN UPDATED BY {} ENTRIES".format(sequence_table_name,DNA_FILE_NAME,sequence_type,database_entries))
    
#LOOPS THROUGH OPEN READING FRAME UNTIL IT FINDS A START CODON THAN WILL SEND TO FIND STOP CODON
def find_start_codon (STRAND_TYPE,READING_FRAME,DNA,STOP_CODONS,START_CODON,con,cur,sequence_table_name,readingFrames_table_name,DNA_FILE_NAME,sequence_type):
    index=0
    database_entry=int(0)
 
    while index<len(DNA):
        if DNA[index:index+3]in START_CODON:
            database_entry+=find_stop_codon(STRAND_TYPE,READING_FRAME,DNA,STOP_CODONS,START_CODON,index,con,cur,sequence_table_name,readingFrames_table_name,DNA_FILE_NAME,sequence_type)
            
        index=index+3

    return database_entry


#LOOPS THORUGH SEQUENCE UNTIL IT FINDS A STOP CODON AND THAN STORES IN SEQUENCES TABLE; IF NO STOP FOUND STILL SAVE IN SEQUENCES BUT WITH NULL MULTIPLE COLUMNS
#loops through entires indexed sequence until it finds a stop codon, once found inputs into sequence table in database
#if stop not found inputs none type into end_index and dna_indexed and indexed_length, inputs 0 for all in file_protein_sequence
def find_stop_codon(STRAND_TYPE,READING_FRAME,DNA,STOP_CODONS,START_CODON,INDEX_START,con,cur,sequence_table_name,readingFrames_table_name,DNA_FILE_NAME,sequence_type):
    
    index=INDEX_START
    
#OBTAINS PRIMARY KEY ID FROM 

#   Checks to see if entry is already in sequence; can't have duplicate sequences with same unique id of DNA_FILE_NAME,STRAND_TYPE,INDEX_START; ONLY ONE ENTRY AT EACH START INDEX
#   if nothing found than will go through sequence and input in sequences table     
    select_statement=("SELECT * FROM "+sequence_table_name+" WHERE (file_name=? AND strand_type=? AND reading_frame=? AND start_index=? AND sequence_type=?);")
    cur.execute(select_statement,(DNA_FILE_NAME,STRAND_TYPE,READING_FRAME,INDEX_START,sequence_type))
    entryFound=cur.fetchone()   
    con.commit()
    if entryFound==None:
        while index<len(DNA):
            if DNA[index:index+3] in STOP_CODONS:
#                    data={"STRAND_TYPE":STRAND_TYPE,"READING_FRAME":READING_FRAME,"DNA":DNA,"DNA_ORGINAL_LENGTH":len(DNA),"START_INDEX":INDEX_START,"END_INDEX":index+3,"DNA_INDEXED":DNA[INDEX_START:index+3],"DNA_INDEXED_LENGTH":(index+3)-INDEX_START}
#                    print(data)
                    readingFrames_id=SQL_reading_frames_primary_ID(readingFrames_table_name,DNA_FILE_NAME,STRAND_TYPE,READING_FRAME,cur,con,sequence_type)
                    insert_sql="INSERT INTO """ +sequence_table_name+ """(file_name,sequence_type,strand_type,reading_frame,readingFrames_id,start_index,end_index,protein_sequence,protein_sequence_index_length,file_protein_sequence_indicator,found_stop)"""+ " " +"""VALUES(?,?,?,?,?,?,?,?,?,?,?);"""
                    cur.execute(insert_sql,(DNA_FILE_NAME,sequence_type,STRAND_TYPE,READING_FRAME,readingFrames_id,INDEX_START,(index+3),DNA[INDEX_START:index+3],((index+3)-INDEX_START),0,1))
                    con.commit()
                    return int(1)
                
            index=index+3
            
#STOP CODON WAS NOT FOUND SO INPUTS DATA WITH NULL OR 0 IN end_index, protein_sequence, p         
#        print("/nNEW ENTRY;STOP NOT FOUND/n/")
        readingFrames_id=SQL_reading_frames_primary_ID(readingFrames_table_name,DNA_FILE_NAME,STRAND_TYPE,READING_FRAME,cur,con,sequence_type)
        insert_sql="INSERT INTO """ +sequence_table_name+ """(file_name,sequence_type,strand_type,reading_frame,readingFrames_id,start_index,end_index,protein_sequence,protein_sequence_index_length,file_protein_sequence_indicator,found_stop)"""+ " " +"""VALUES(?,?,?,?,?,?,?,?,?,?,?);"""
        cur.execute(insert_sql,(DNA_FILE_NAME,sequence_type,STRAND_TYPE,READING_FRAME,readingFrames_id,INDEX_START,None,DNA[INDEX_START:],None,0,0))
        con.commit()
        return int(1)
    else:
        return int(0) 
    
#INPUTS ONE FOR MAXIMUM SEQUENCE LENGHT FOR ANY SEQUENCE TYPE(DNA||RNA) FOR A SPECIFIC FILE
#WILL ALWAYS UPDATE REGARDLESS IF DATABASE ALREADY HAS A SEQUENCE SELECTED; WILL INFORM USER ON DUPLICATE AND TIL THEM TO DETERMINE WHICH IS TRUE
def find_protein_sequence(con,cur,sequence_table_name,DNA_FILE_NAME,sequence_type):
    
    select_statement=("SELECT id,file_protein_sequence_indicator,max(protein_sequence_index_length) FROM "+ sequence_table_name +" WHERE file_name=? AND sequence_type=? AND found_stop=?;")
    cur.execute(select_statement,(DNA_FILE_NAME,sequence_type,1))
    select_tuple=cur.fetchone()
    PROTEIN_SEQUENCE_ID_NUMBER=select_tuple[0]
    file_protein_sequence_indicator_check=select_tuple[1]
    con.commit()
    
    if file_protein_sequence_indicator_check==0:
        update_statement=("UPDATE "+sequence_table_name+" SET file_protein_sequence_indicator=? WHERE id=?;")
        cur.execute(update_statement,(1,PROTEIN_SEQUENCE_ID_NUMBER))
        con.commit()
        print(' ')
        print ("Update {} at location {} marking for file_protein_sequence_indicator as 1".format(sequence_table_name,PROTEIN_SEQUENCE_ID_NUMBER))
     
    else:
        print(' ')
        print ("DID NOT UPDATE {} at location {}, BECAUSE file_protein_sequence_indicator={} ".format(sequence_table_name,PROTEIN_SEQUENCE_ID_NUMBER,file_protein_sequence_indicator_check))
    
    select_statement=("SELECT id,file_protein_sequence_indicator,sum(file_protein_sequence_indicator) FROM "+ sequence_table_name +" WHERE file_name=? AND sequence_type=? AND found_stop=?;")
    cur.execute(select_statement,(DNA_FILE_NAME,sequence_type,1))
    select_tuple=cur.fetchone()
    con.commit()
    summation=select_tuple[2]
    if summation!=1:
        print('=================================================================================================== ')
        print('ERROR MESSAGE')
        print("ERROR IN INPUTTING PROTEIN SEQUENCE into {} DATABASE FOR FILE {} ON SEQUENCE TYPE {} ;".format(sequence_table_name,DNA_FILE_NAME,sequence_type))
        print("LOOKS LIKE THERE ARE MULTIPLE SELECTIONS FOR {} ON {} PLEASE DETERMINE WHICH IS CORRECT, WITH HAVE UPDATED THE DATABASE REGARDLESS OF DUPLICATES AS IT BE EASIER TO DETERMINE IN PERSON".format(DNA_FILE_NAME,sequence_type))
        print("PLEASE DOUBLE CHECK THAT DNA PRIME END SELECTION WAS CORRECT AND STRAND TYPE IS CORRECT; INPUTTING INCORRECTLEY WILL CAUSE THIS ERROR")
        print("MAY NEED TO DELETE DNA FILE NAME {} FROM TABLE {} AND RE-RUN PROGRAM ON DATABASE".format(DNA_FILE_NAME,sequence_table_name))
        print('=================================================================================================== ')
        
        
#--------------------------------------

#Protein PROCESSING; create Amino Acid Sequence

#--------------------------------------

#FINDS THE SEQUENCE THAT WILL CONTAIN RNA OR CREATES AND RNA STRAND FROM EXISTING DNA SEQUENCE TO RETURN
#RETURNS IF IT FOUND A RESULT THAT CAN BE INPUTTED INTO THE PROTEINS TABLE WITHA BOOLEAN, RETURNS LIST WITH ALL DETAILS ON SEQUENCE, AND RETURNS RNA SEQUENCE
#CHECKS FOR ERRRORS:#1. NOT POSSIBLE FOR TWO PROTEIN STRANDS BE SAME SEQUENCE TYPE SO CHECKS IF 2 SEQUENCES ARE THE SAME
#CHECKS FOR ERRORS:#2. CHECKS TO SEE IF THERE ARE 2 IF ONE IS RNA CONTAINING IF NOT SENDS ERROR MESSAGE
#CHECKS FOR ERRORS:#3. CHECKS TO SEE IF THERE MORE THAN 2 OR NO SEQUENCES WERE SENT TO GET RNA.     
def get_RNA_sequence(sequences_containing_protein):

# #1. ERROR CHECK    
        if len(sequences_containing_protein)== 2:
            if sequences_containing_protein[0][2]==sequences_containing_protein[1][2]:
#                print('Error in FINIDING Protein Sequence; AS THERE ARE 2 PROTEIN SEQUENCES AND BOTH OF SAME STRAND TYPE')
#                print('PLEASE MAKE SURE DATABASE TABLE IS CORRECT')
                sys.exit('Error in FINIDING Protein Sequence; AS THERE ARE 2 PROTEIN SEQUENCES AND BOTH OF SAME STRAND TYPE PLEASE MAKE SURE DATABASE TABLE IS CORRECT')
                return False,False,False
                
            for hit in sequences_containing_protein:
                if 'RNA' in hit:
                    return True, hit,hit[8]
# #2. ERROR CHECK
            else:
#                 print('Error in FINIDING Protein Sequence, AS THERE ARE MORE THAN 2 Protein Sequences and None are RNA Containing')
#                 print('PLEASE MAKE SURE DATABASE TABLE IS CORRECT')
                 sys.exit('Error in FINIDING Protein Sequence, AS THERE ARE MORE THAN 2 OR NO PROTEIN SEQUENCES FOUND IN TABLE PLEASE MAKE SURE DATABASE TABLE IS CORRECT')
                 return False,False,False
                
        elif len(sequences_containing_protein)==1:

            if 'RNA' in sequences_containing_protein[0]:
                    return True, sequences_containing_protein,sequences_containing_protein[0][8]
                
            else:

               rna_sequence=rna_t_changer(DNA=sequences_containing_protein[0][8])
               return True, sequences_containing_protein, rna_sequence
                
# #2. ERROR CHECK           
        else:
#            print('Error in FINIDING Protein Sequence, AS THERE ARE MORE THAN 2 OR NO PROTEIN SEQUENCES FOUND IN TABLE')
#            print('PLEASE MAKE SURE DATABASE TABLE IS CORRECT')
            sys.exit('Error in FINIDING Protein Sequence, AS THERE ARE MORE THAN 2 OR NO PROTEIN SEQUENCES FOUND IN TABLE PLEASE MAKE SURE DATABASE TABLE IS CORRECT')
            return False,False,False


#CHANGES A DNA SEQUNCE TO HAVE U INSTEAD OF T, NEEDED FOR get_RNA_sequence IF DNA FILE IS ONLY FOUND
def rna_t_changer(DNA):
    
    rna=list()
    dna_matcher={'a':'a','t':'u','c':'c','g':'g'}
    
    for nucleotide in DNA:
        rna.append(dna_matcher[nucleotide])
        
    rna="".join(rna)
    return rna

#SQL INSERTS AMINO ACIDS SEQUENCE INTO PROTEINS TABLE
def SQL_INSERT_protein(cur,con,table_list,rna_sequence,amino_acids,protein_table_name):
    
#   """CREATE TABLE IF NOT EXISTS """+table_name+""" (
#                                            id INTEGER PRIMARY KEY,
#                                            file_name TEXT NOT NULL,
#                                            readingFrames_id integer NOT NULL,
#                                            sequences_id integer NOT NULL,
#                                            rna_sequence text NOT NULL,
#                                            protein_sequence_one_letter text NOT NULL,
#                                            protein_sequence_three_letter text NOT NULL,
#                                            protein_sequence_name text NOT NULL,
#                                            molecular_weight integer NOT NULL
#                                            );""" 
    
    
    protein_list=list()
    protein_list.append(table_list[1])
    protein_list.append(table_list[5])
    protein_list.append(table_list[0])
    protein_list.append(rna_sequence)
    
    protein_sequence_one_letter=list()
    protein_sequence_three_letter=list()
    protein_sequence_name=list()
    molecular_weight=0
    amino_acids_count=0
    
    index=0
    
    while index < len(rna_sequence):
#        print("DEBUG:",rna_sequence[index:index+3], index,len(rna_sequence),amino_acids_count)
        for amino in amino_acids:
            if rna_sequence[index:index+3]==amino[1]:
                protein_sequence_one_letter.append(amino[4])
                protein_sequence_three_letter.append(amino[3])
                protein_sequence_name.append(amino[2])
                if amino[5]!=None:
                    molecular_weight+=amino[5]
                amino_acids_count+=1
        index+=3 
                
    protein_list.append(" ".join(protein_sequence_one_letter))
    protein_list.append(" ".join(protein_sequence_three_letter))
    protein_list.append(" ".join(protein_sequence_name))
    protein_list.append(molecular_weight)
    protein_list.append(amino_acids_count)
 
    
#    print (protein_list)
    
    insert_sql="INSERT INTO """ +protein_table_name+ """(file_name, readingFrames_id,sequences_id,rna_sequence,protein_sequence_one_letter,protein_sequence_three_letter,protein_sequence_name,molecular_weight,amino_acids_count)"""+" " +"""VALUES(?,?,?,?,?,?,?,?,?);"""
    cur.execute(insert_sql,(protein_list[0],protein_list[1],protein_list[2],protein_list[3],protein_list[4],protein_list[5],protein_list[6],protein_list[7],protein_list[8]))
    con.commit()
    
    return protein_list


#--------------------------------------

#SQL PROCESSING; 4/5 on UI CHOICE

#--------------------------------------
#UI SCREEN FOR SELECTION ON UI PROCESSING
def SQL_ui(con,cur,database_name):
    
     while True:
        print("\n")
        print("SQL LIST OF OPTIONS: ")
        print("===============================================================================")
        print("1. TABLES - LIST OF CURRENT TABLES IN {}".format(database_name))
        print("2. COLUMN NAMES - LIST OF COLUMNS NAMES")
        print("3. TABLE DETAILED - GIVE STATS AND INFORMATION ON A TABLE")
        print("4. DATABASE DETAILED - GIVE STATS AND INFORMATION FOR ALL TABLES IN {}".format(database_name))
        print("5. SQL- PERFORM ANY SQL STATEMENT FOR DATABASE")
        print("6. DATAFRAME - CREATE A DATAFRAME AND PERFORM STATISTICS")
        print("===============================================================================")
        try:
            user_choice=int(input("Please select an OPTION above (-1 to exit program): "))
            if((user_choice>0 and user_choice<7) or user_choice==-1):
                return user_choice
            else:
                print("INVALID OPTION PLEASE TYPE A CHOICE OF '1' THRU '6' OR -1 TO EXIT PROGRAM!")
        except:
            print("ONLY NUMBERS # ARE VALID OPTIONS; PLEASE TYPE A CHOICE OF '1' THRU '6' OR -1 TO EXIT PROGRAM!")
    

#PRINTS OUT ALL THE COLUMNS FIELDS FOUND ON A TABLE SELECTED
def SQL_column_names(con,cur,database_name,table_name):
    print("\n")
    print("COLUMN NAMES FOR {}".format(table_name))
    print("===============================================================================")
    SQL_statement=("SELECT * FROM {} ;".format(table_name))
    cur.execute(SQL_statement)
    names = list(map(lambda x: x[0], cur.description))
    con.commit()
    
    ui_number=0
    for name in names:
        print("{}. {}".format(ui_number+1,name))
        ui_number+=1    
    print("===============================================================================")

#CREATES A DATAFRAME FOR ALL FIELDS IN A TABLE AND OUTPUTS INFORMATION
#PANDAS DESCRIBE (SUMMARY STATS), BOX_PLOTS, HISTORGRAMS, SCATTER MATRIX    
def SQL_table_detailed(con,cur,database_name,table_name):
   try:
        SQL_statement=("SELECT * FROM {} ;".format(table_name))
        cur.execute(SQL_statement)
        SQL_output=cur.fetchall()
        con.commit()
        names = list(map(lambda x: x[0], cur.description))
        df=pd.DataFrame(SQL_output, columns=list(names))
        print("{} IS DETAILED BELOW:".format(table_name))
        print("*******************************************************************************")
        DATAFRAME_PRINT_head(df,table_name,5)
        DATAFRAME_PRINT_summary_stats(df,table_name)
        DATAFRAME_PRINT_box_plots(df,table_name)
        DATAFRAME_PRINT_histograms(df,table_name)
        DATAFRAME_PRINT_scatter_matrix(df,table_name)
   except:
        print("ERROR COULDN'T GIVE DETAILED INFORMAT FOR {}".format(table_name))
   print("*******************************************************************************") 

#LOOPS THROUGH EVERY TABLE IN DATABASE AND OUTPUTS DETAILS FOR EACH TABLE BY ABOVE FUNCTION
def SQL_database_detailed(con,cur,database_name):
    table_names=SQL_database_all_table_names(con,cur)
    for table in table_names:
        SQL_table_detailed(con,cur,database_name,table)

#ALLOWS USER TO OUTPUT ANY STATEMENT THEY WANT IN A SQL STATEMENT
def SQL_any_statement(con,cur,database_name):
    query=input("PLEASE TYPE YOUR SQL QUERY: ")
    
    try:
        cur.execute(query)
        SQL_output=cur.fetchall()
        names = list(map(lambda x: x[0], cur.description))
        df=pd.DataFrame(SQL_output, columns=list(names))
        con.commit()
        user_choice=input("Would you like to print out the full ouput?: 'y' or 'n'").lower()
        while(user_choice!='y' and user_choice!='n'):
            user_choice=input("Would you like to print out the full ouput?: 'y' or 'n'").lower()
        if user_choice=='y':
            print("FULL SQL QUERY OUTPUT")
            print("===============================================================================")
            print(df)
            print("===============================================================================")
        else:
            print("FIRST 10 FROM SQL QUERY")
            print("===============================================================================")
            print(df.head(10))
            print("===============================================================================")
    except:
        print("ERROR IN SQL STATEMENT PLEASE CHECK BELOW STATEMENT FOR ERRORS")
        print(query)
        
    con.commit()
    
    
    
#PRINTS OUT FEW ENTRIES IN DATAFRAME BASED OFF LIMIT PROVIDED
def DATAFRAME_PRINT_head(df,table_name,limit):
    print("\n")
    print("FIRST {} DATA POINTS FOR {}".format(limit,table_name))
    print("===============================================================================")
    print(df.head(limit))
    print("===============================================================================")
 
#PRINTS OUT SUMMARY STATS FOR DATAFRAME SETN
def DATAFRAME_PRINT_summary_stats(df,table_name):   
    print("\n") 
    print("SUMMARY STATISTICS FOR {}".format(table_name))

    print("===============================================================================")
    print(df.describe())
    print("===============================================================================")
    
#       PRINTS OUT BOX PLOT FOR DATAFRAME SENT 
def DATAFRAME_PRINT_box_plots(df,table_name):   
   
    plt.style.use('ggplot')
    print("\n")
    print("BOXPLOTS FOR {}".format(table_name))
    try:
        fig,ax=plt.subplots()
        ax.boxplot()
        plt.show()
    except:
        print("{} COULDN'T HAVE BOX PLOTS".format(table_name))
#PRINTS OUT HISTOGRAM FOR DATAFRAME SETN        
def DATAFRAME_PRINT_histograms(df,table_name):   
   
    plt.style.use('ggplot')
    print("\n")
    print("\n")
    print("HISTORGRAMS FOR {}".format(table_name))
    print("===============================================================================")
    try:
        df.hist()
        plt.show()
    except:
        print("{} COULDN'T HAVE HISTOGRAMS".format(table_name)) 
    print("===============================================================================")
    
#PRINTS OUT SCATTER MATRIX FOR DATA FRAME SENT
def DATAFRAME_PRINT_scatter_matrix(df,table_name):   
   
    plt.style.use('ggplot')
    print("\n")
    print("\n")
    print("SCATTER MATRIX FOR {}".format(table_name))
    print("===============================================================================")
    try:
        scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
        plt.show()
    except:
        print("{} COULDN'T HAVE scatter_matrix".format(table_name))
    print("===============================================================================")
    
    
#MAIN PROCESSING FROM UI BASED ON SELECTION OF USER; WILL TRIGGER SELECTED FUNCITONS ABOVE BASED OF USER CHOICE    
def SQL_main(con,cur,database_name):
    
    user_choice=None
    while(user_choice != -1 ):
        user_choice=SQL_ui(con,cur,database_name)
        if user_choice==1:
            print("Database {} has the following Information:".format(database_name))
            current_table_names(con,cur)
        elif user_choice==2:
            table_name=table_name_selection(con,cur,'y')
            while (table_name!=None):
                SQL_column_names(con,cur,database_name,table_name)
                table_name=table_name_selection(con,cur,'y')
        elif user_choice==3:
            table_name=table_name_selection(con,cur,'y')
            while (table_name!=None):
                SQL_table_detailed(con,cur,database_name,table_name)
                table_name=table_name_selection(con,cur,'y')
        elif user_choice==4:
            SQL_database_detailed(con,cur,database_name)
        elif user_choice==5:
#            table_name=table_name_selection(con,cur,'y')
#            while (table_name!=None):
            print("Database {} has the following Information:".format(database_name))
            current_table_names(con,cur)
            SQL_any_statement (con,cur,database_name)
        elif user_choice==6:
#            database_name = input('Enter the SQLITE database name: ').lower()
#            con=sqlite3.connect(database_name)
#            cur = con.cursor()
            print('WAIT FOR GGPLOT')
    
    
    
    
#    choice=input("WOULD YOU LIKE TO SEE THE LIST OF TABLES IN {}: 4".format(database_name)).lower()
#    while (choice!='y' and choice!='n'):
#        choice=input("WOULD YOU LIKE TO SEE THE LIST OF TABLES IN {}: ".format(database_name)).lower()
#    
#    if(choice=='y'):
#        print("Database {} has the following Information:".format(database_name))
#        current_table_names(con,cur)
#        
#   
    
    
    
if __name__ == '__main__':
    main()
    
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:48:16 2019

@author: karapet
"""


#Def:
#DNA Object that hold information on DNA sample that is being used to identify protein Sequence
# contains all 3 reading frames and a raw file as it was sent
#Function: createes a dictionary that contains each 3 reading frames;
# reading frame one is orginal 5' prime to 3' of DNA sequence sent

import string


def codon_dictionary_builder(self,match_type):
    
    codons=dict()
    
    if match_type=="DNA":
        codons['START']=['atg']
        codons['STOP']=['tag','taa','tga']
        return codons
    elif match_type=='RNA':
        codons['START']=['aug']
        codons['STOP']=['uag','uaa','uga']
        return codons
    else:
        print("ERROR IN CREATING CODONS DICTIONARIES, PLEASE CHECK DNA OBJECT INITIALIZER")
        return None

def dna_matcher_dictionary_builder(self,matcher_type):
    
    if matcher_type=="DNA": 
        dna_matcher={'a':'t','t':'a','c':'g','g':'c'}
        return dna_matcher
    elif matcher_type=="RNA":
        rna_matcher={'a':'u','t':'a','c':'g','g':'c'}
        return rna_matcher
    elif matcher_type=="RNA_U_CHANGER":
        dna_matcher={'a':'a','t':'u','c':'c','g':'g'}
        return dna_matcher
    else:
        print("ERROR IN CREATING MATHCING DICTIONARIES, PLEASE CHECK DNA OBJECT INITIALIZER")
        return None

#builds 3 reading frames for dna sequence; HAVE TO CALL EACH CODING AND TEMPLATE SEPERATELY
def reading_frames(self,DNA):
        
        frames=dict()
        frames['READING_FRAME_ONE']=DNA
        frames['READING_FRAME_TWO']=DNA[1:]
        frames['READING_FRAME_THREE']=DNA[2:]
        
        return frames

#finds matching rna sequence for template or coding strand; is a mirror copy of strand type is not what RNA is coded from it is what
#what the dna sequence is
#example: DNA: ATCGTTA
#RNA WOULD BE: AUCGUUA
#EXACT COPY JUST T'S REPLACED WITH U'S SO IN DATABASE THAT IS WHAT IT WILL BE STORED AS
def rna_reading_frames(self):

    rna_frames=dict()
    for sequence_type in self.READING_FRAMES:
        if sequence_type=="DNA":
            for strand_type in self.READING_FRAMES[sequence_type]:
                rna_frames[strand_type]=dict()
                for reading_frame in self.READING_FRAMES[sequence_type][strand_type]:
                    rna_frames[strand_type][reading_frame]=rna_t_changer(self,self.READING_FRAMES[sequence_type][strand_type][reading_frame])
    return rna_frames
    
    
def rna_t_changer(self,DNA):
    
    rna=list()
    for nucleotide in DNA:
        rna.append(self.matcher['RNA_U_CHANGER'][nucleotide])
        
    rna="".join(rna)
    return rna

#creates the affilated strand for main dna sequence in file
#if file contained template strand will create coding strand
#and vice versa; 
#Function: reverses DNA SEQUENCE SENT SO IT WILL BE 3 PRIME END
#Than tranverses through the sequence and matches the opposite nucletide creating a 5' to 3' affilated sequence
def affilated_strand(self,DNA):
#    GETS THREE PRIME OF DNA SEQUENCE
    dna_three_prime=DNA[::-1]
    
    dna_affiliated=list()
    
    for nucleotide in dna_three_prime:
            dna_affiliated.append(self.matcher['DNA'][nucleotide])
    
    dna_affiliated="".join(dna_affiliated)   
#    print("DNA_3: ",dna_3_prime)
#    print("DNA_AFFILATIATED: ",dna_affiliated)
    return dna_affiliated
        


class DNA_STRAND():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    
    def __init__(self,DNA_STRAND,STRAND_TYPE):
        
        #MAIN STRAND DATA ARCHIVE; WILL BE USED TO 6 MAKE READING FRAMES FROM 5' TO 3'
        self.DNA_SEQUENCE_RAW=DNA_STRAND.lower()
        self.DNA_TEMPLATE_STRAND=DNA_STRAND
        self.DNA_CODING_STRAND=DNA_STRAND[::-1]
        self.DNA_LENGTH=len(DNA_STRAND)
        
        self.READING_FRAMES={'DNA':dict(),'RNA':dict()}
        self.significant_codons=dict()
        self.codons=dict()
        
        self.codons["DNA"]=codon_dictionary_builder(self,"DNA")
        self.codons["RNA"]=codon_dictionary_builder(self,"RNA")
        
        self.matcher=dict()
        self.matcher["DNA"]=dna_matcher_dictionary_builder(self,"DNA")
        self.matcher["RNA"]=dna_matcher_dictionary_builder(self,"RNA")
        self.matcher["RNA_U_CHANGER"]=dna_matcher_dictionary_builder(self,"RNA_U_CHANGER")
        if(STRAND_TYPE=='t'or STRAND_TYPE=='n'):
            self.READING_FRAMES['DNA']['TEMPLATE_STRAND']=reading_frames(self,DNA_STRAND)
            self.DNA_SEQUENCE_RAW_AFFILIATED=affilated_strand(self,DNA_STRAND)
            self.READING_FRAMES['DNA']['CODING_STRAND']=reading_frames(self,self.DNA_SEQUENCE_RAW_AFFILIATED)
        elif (STRAND_TYPE=='c'):
            self.READING_FRAMES['CODING_STRAND']=reading_frames(self,DNA_STRAND)
            self.DNA_SEQUENCE_RAW_AFFILIATED=affilated_strand(self,DNA_STRAND)
            self.READING_FRAMES['TEMPLATE_STRAND']=reading_frames(self,self.DNA_SEQUENCE_RAW_AFFILIATED)
        
        self.READING_FRAMES['RNA']=rna_reading_frames(self)
        
#        self.DNA_STRAND_READING_FRAME_ONE=self.DNA_SEQUENCE
#        self.DNA_STRAND_READING_FRAME_TWO=self.DNA_SEQUENCE[1:]
#        self.DNA_STRAND_READING_FRAME_THREE=self.DNA_SEQUENCE[2:]
        
        
    
#prints out length of dna strand, or reading frame based of integer inputted
    def find_length(self,strand_type='TEMPLATE_STRAND',frame='READING_FRAME_ONE',new_strand=None):
        
            if new_strand!=None:
                return len(new_strand)
            else:
                return(len(self.DNA_READING_FRAMES[strand_type][frame]))
        

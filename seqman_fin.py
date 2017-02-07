# -*- coding: utf-8 -*-
"""
Zac Carver 
Assignment1 "SequenceManipulation"
01/23/17
--------
- Create a new Python script (text file)
- At the beginning of the script, define a DNA sequence (taken from
https://github.com/jembrown/CompPhylo_Spr17/blob/master/CodingSeq.txt)
- Print the length of the sequence to the screen along with text explaining
the value
- Create and store the RNA equivalent of the sequence, then print to screen.
- Create and store the reverse complement of your sequence, then print to
screen.
- Extract the bases corresponding to the 13rd and 14th codons from the
sequence, then print them to the screen.
- Create a function to translate the nucleotide sequence to amino acids
using the vertebrate mitochondrial genetic code (available from
https://github.com/jembrown/CompPhylo_Spr17/blob/master/VertMitTransTable.txt).
- Translate the sequence and print it to the screen.
- Be sure you've added comments to explain what this script is and what the
different bits of code mean.
"""

from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from collections import OrderedDict


def transcribe_seq(dnaseq):
	"""DNA sequence is capitalized(for preference) and each T is replaced by a U"""
	rnaseq = dnaseq.replace('T','U')
	return(rnaseq)


def reverse_seq(dnaseq):
	"""converted to a list, reversed and then each element is joined back together into a string object."""
	rev_seq = list(dnaseq)
	rev_seq.reverse()
	return(''.join(rev_seq))#returns the seq as a string


def codons(dnaseq):
	"""Here the sequence string is split into triplets, where elements are composed of 3 bases. Modified step from http://stackoverflow.com/questions/19521905/translation-dna-to-protein. In the MAIN function, 13th and the 14th codon are found by searching between indecies 12 to 14."""
	c = [dnaseq[i:i+3] for i in range(0, len(dnaseq), 3)]#referenced oneliner here: http://stackoverflow.com/questions/19521905/translation-dna-to-protein
	return(c)


def translate_seq(c):
	"""each element in c (list of codons) is matched to the respective aa in AAs string by iterating over the first char. of each Base line...returning a new & translated sequence string"""
	#print(c) #checking 'format' of variable/argument
	AAs = "FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIMMTTTTNNKKSS**VVVVAAAADDEEGGGG"
	#Starts = "--------------------------------MMMM---------------M------------"
	Base1 = "TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG"
	Base2 = "TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG"
	Base3 = "TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG"
	codon_aa_dict = {}#empty dictionary to hold the key-value/codon-aa pairs generated in the following.
	tran_seq = []#empty list brackets to capture the series of codon matches using the above bases and corresponding AAs.
	#the following components referenced from stackoverflow postings
	for i in range(len(AAs)):#as each character is iterated over the length of the strings.....
		codon_aa_dict['{}{}{}'.format(Base1[i], Base2[i], Base3[i])] = AAs[i]#they are placed into set positions using .format method then are set equal to the respective AA.
		#print(codon_aa_dict) #checking correct match
	for seqcodon in c:
		if len(seqcodon) == 3:#if the codon is 3 characters in length the loop will continue to add the matched AA to the open list as a new element.
			aminoacid = codon_aa_dict[seqcodon]
			tran_seq.append(aminoacid)
		else:#yet if the length of the codon is less than 3, the loop will through iteration.
			continue
	return(''.join(tran_seq))#returns the seq as a string


def translate_seq2(dnaseq):
	"""Utilizing the imported module Seq from Biopython and keeping with IUPAC convention, the sequence is simply translated according to the Vertebrate Mitochondrial Code Table. See Biopython guide."""
	dnaseq = Seq(dnaseq, IUPAC.unambiguous_dna)#signaling that there is no ambiguous characters present in the sequence given.
	return(dnaseq.translate(table="Vertebrate Mitochondrial", to_stop=True))#translation will stop at the first stop codon and is returned as a string.


def main():
	"""Although not defined at the begining of the script, the DNA sequence is definded as the variable dnaseq and is passed to the above functions (to keep the overall script clean and 'atomated'). Each value from the above functions are returned and printed below."""
	dnaseq = "aaaagctatcgggcccataccccaaacatgttggttaaaccccttcctttgctaattaatccttacgctatctccatcattatctccagcttagccctgggaactattactaccctatcaagctaccattgaatgttagcctgaatcggccttgaaattaacactctagcaattattcctctaataactaaaacacctcaccctcgagcaattgaagccgcaactaaatacttcttaacacaagcagcagcatctgccttaattctatttgcaagcacaatgaatgcttgactactaggagaatgagccattaatacccacattagttatattccatctatcctcctctccatcgccctagcgataaaactgggaattgccccctttcacttctgacttcctgaagtcctacaaggattaaccttacaaaccgggttaatcttatcaacatgacaaaaaatcgccccaatagttttacttattcaactatcccaatctgtagaccttaatctaatattattcctcggcttactttctacagttattggcggatgaggaggtattaaccaaacccaaattcgtaaagtcctagcattttcatcaatcgcccacctaggctg"
	dnaseq = dnaseq.upper()
	rnaseq = transcribe_seq(dnaseq)
	c = codons(dnaseq)
	tran_seq = translate_seq(c)
	biotran_seq = translate_seq2(dnaseq)
	"""the following statement will print the returned results of the body fucntions neatly and doublespaced."""
	print("Length of original seq. is...", len(dnaseq),
		  "\n\nReverse complement:\n", reverse_seq(dnaseq.upper()),
		  "\n\nRNA equivalent:\n", transcribe_seq(dnaseq),
		  "\n\nThe 13th and 14th codons are...", c[12:14], type(c),
		  "\n\nTranslation of original DNA sequence using Vertebrat_Mitochondrial_Code_Table:\n", tran_seq,
		  "\n\nBiopython CHECK translation of the 'translate_seq' using Vertebrat_Mitochondrial_Code_Table\n", biotran_seq)
	if tran_seq == biotran_seq:#statement will compare the Biopython method and the 'manual' method of dna translation.
		print('Check Matched')
	else:
		print('Check Fail')

if __name__ == '__main__':
	main()

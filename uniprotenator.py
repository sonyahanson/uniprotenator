# Sonya Hanson - December 17, 2014

# Get all PDB's for a given uniprot accession number.

#    USAGE: python uniprotenator.py P68400
#   output: *.pdb and P68400.xml

# Import needed libraries
import sys
from urllib2 import urlopen
from lxml import objectify
from Bio import PDB

# Define our uniprot accession ID of preference.
input = sys.argv[1]

# Define url from which to download xml.
url='http://www.uniprot.org/uniprot/'
r1 = urlopen(url+'%s' % input +'.xml')

# Read xml file.
my_xml = r1.read()
# Take out annoying head that makes xml file difficult to parse.
my_xml = my_xml.replace('<uniprot xmlns="http://uniprot.org/uniprot" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://uniprot.org/uniprot http://www.uniprot.org/support/docs/uniprot.xsd">','<uniprot>', 1)

# Write xml file.
with open("%s.xml" % input,"w") as file:
     file.write(my_xml)
     
     
# Define list of PDBs from uniprot xml.
root = objectify.fromstring(my_xml)
structures = [dbReference.attrib['id'] for dbReference in root.findall('.//dbReference[@type="PDB"]')]
structures = [s.lower() for s in structures]
print structures

for s in structures:
    
    dir = s[1:3]

    pdb1=PDB.PDBList()
    pdb1.retrieve_pdb_file(s)
    parser = PDB.PDBParser(PERMISSIVE=1)
    structure = parser.get_structure(s,"%s/pdb%s.ent" % (dir,s))
    io = PDB.PDBIO()
    io.set_structure(structure)
    io.save('%s.pdb' % s)

# Write pymol alignment file.
# Usage  'open -a MacPyMOL *.pdb' and then @P68400_align.pml in pymol.

ref = structures[0]

f=open('%s_align.pml' % input,'w')

for struct in structures[1:]:
    f.write ('align %s, %s ;\r' % (struct,ref))

f.close()

# Automatically remove non-kinase domains
# generate alignment text file to ID gaps and N and C termini of PDBs
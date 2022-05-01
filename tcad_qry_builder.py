import csv
file = open('test_query_simple.csv')

csvreader = csv.reader(file)

headers = next(csvreader)

rows = []
entree = []
sortie = []
for row in csvreader:
  rows.append(row)
  if row[4] == '1': #entree
    entree.append((row[1],row[2]))
  else:
    sortie.append((row[1],row[2]))

file.close()

#create functions to define recurrent statements
def xmlhead():
  print('<?xml version="1.0"?>')
  print("\n")
  print("<critical_link_queries>")

def printqueryentr(injecteur):
  global entree
  global sortie
  ei = injecteur[1]
  notent = [' and not Link'+sens+'('+ej+')' for ej,sens in entree if ej != ei]
  notsort = [' and not Link'+sens+'('+sj+')' for sj,sens in sortie ]
  texte = 'Link'+injecteur[2]+'('+ei+')'
  for i in notent:
    texte = texte+i
  for i in notsort:
    texte = texte+i

  print('\t\t\t'+texte)

def printqueryensort(injecteur):
  global entree
  global sortie
  si = injecteur[1]
  notent = [' and not Link'+sens+'('+ej+')' for ej,sens in entree]
  notsort = [' and not Link'+sens+'('+sj+')' for sj,sens in sortie if sj != si]
  texte1 = ''
  texte2 = ''
  texte3 = ' and Link'+injecteur[2]+'('+si+')'
  for i in notent:
    texte1 = texte1+i
  for i in notsort:
    texte2 = texte2+i
  texte1 = texte1[5:]
  print('\t\t\t'+texte1+texte3+texte2)

def debutquery():
  print('\t<query>')
  print("\t\t<name>"+" "+"Inj"+str(injecteur[0])+" "+"<\\name>")
  print("\t\t<text>")

def finquery():
  print("\t\t<\\text>")
  print('\t<\\query>')
  print('\n')

def printtale():
  print('<\\critical_link_queries>')

#assemble the different functions
xmlhead()

for injecteur in rows:
    debutquery()
    if injecteur[4] == '1': #Column entrée
      printqueryentr(injecteur)
    else:
      printqueryensort(injecteur)
    finquery()
printtale()
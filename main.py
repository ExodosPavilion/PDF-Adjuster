# importing the required modules 
import PyPDF2 
from pick import pick
from pick import Picker


#link to refer to
#	https://www.geeksforgeeks.org/working-with-pdf-files-in-python/


def PdfRotateSet(orignalFileName, newFileName, rotation, pages):
		# creating a pdf File object of original pdf 
	originalPdfFileObj = open(orignalFileName, 'rb') 
	
	# creating a pdf Reader object 
	pdfReader = PyPDF2.PdfFileReader(originalPdfFileObj) 

	# creating a pdf writer object for new pdf 
	pdfWriter = PyPDF2.PdfFileWriter() 
	
	if type(pages) == int:
		# rotating each page 
		for page in range(pdfReader.numPages): 
			# creating rotated page object 
			pageObj = pdfReader.getPage(page)
			
			if page == (pages - 1):
				pageObj.rotateClockwise(rotation) 

			# adding rotated page object to pdf writer 
			pdfWriter.addPage(pageObj)
	else:
		# rotating each page 
		for page in range(pdfReader.numPages): 

			# creating rotated page object 
			pageObj = pdfReader.getPage(page)
			
			if page in pages:
				pageObj.rotateClockwise(rotation) 

			# adding rotated page object to pdf writer 
			pdfWriter.addPage(pageObj)

	# new pdf file object 
	newFile = open(newFileName, 'wb') 
	
	# writing rotated pages to new file 
	pdfWriter.write(newFile) 

	# closing the original pdf file object 
	originalPdfFileObj.close() 
	
	# closing the new pdf file object 
	newFile.close() 


def PDFmerge(pdfs, output):  
	# creating pdf file merger object 
	pdfMerger = PyPDF2.PdfFileMerger() 
	
	pdfFiles = []
	
	#Doing it like so to ensure that the file stay open while PdfFileMerger does its work
	for file in pdfs:
		pdfFiles.append( open(file, 'rb') )
	
	# appending pdfs one by one 
	for pdf in pdfFiles: 
		pdfMerger.append(pdf) 
          
	# writing combined pdf to output pdf file 
	with open(output, 'wb') as f: 
		pdfMerger.write(f) 
	
	for file in pdfFiles:
		file.close()
		
	
def getNumberOfPages(fileName):
	# creating a pdf File object of pdf 
	pdfFileObj = open(fileName, 'rb') 
	
	# creating a pdf Reader object 
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	
	#return the number of pages in the pdf
	return pdfReader.numPages
	
	

def getIntInput(prompt):
	while True:
		try:
			value = int(input(prompt).strip())
			break
		except ValueError:
			print("Please enter a valid integer\n")
		
	return value
	

def optionSelector(title, options, multi=False, minimumSelection=1, outputOption=0):
	selectedOptionNames = []
	selectedIndexes = []
	selectedOption = None
	selectedIndex = None
	
	if type(title) != str or type(options) != list or type(multi) != bool or type(minimumSelection) != int or type(outputOption) != int:
		raise TypeError
	else:
		selected = pick(options, title, multiselect=multi, min_selection_count=minimumSelection)
		
		if multi:
			for i in selected:
				selectedOptionNames.append(i[0])
				selectedIndexes.append(i[1])
		else:
			selectedOption = selected[0]
			selectedIndex = selected[1]
		
		if outputOption == 1:
			if multi:
				return selectedIndexes
			else:
				return selectedIndex
		elif outputOption == 2:
			if multi:
				return selectedOptionNames
			else:
				return selectedOption
		else:
			if multi:
				return selectedOptionNames, selectedIndexes
			else:
				return selectedOption, selectedIndex
			

def rotate():
	print("Please enter how much you want to rotate the page(s) by")
	print("Note that the script will only accept values in increments of 90 degrees")
	print("Using a negative ( - ) will rotate the page(s) counter-clockwise")
	print("Generally: ")
	print("\t90: rotate page(s) right\n\t180: turn page(s) around\n\t-270: rotate page(s) right 3 times (basically rotates the page left")
	print("\t-90: rotate page(s) left\n\t-180: turn page(s) around\n\t-270: rotate page(s) left 3 times (basically rotates the page right\n")
	
	while True:
		rotationAngle = getIntInput("Rotation amount (in degrees): ")
		
		if (rotationAngle % 90) != 0:
			print("Please enter a multiple of 90\n")
		else:
			break
			
	print("\nPlease enter the name of the file you wish to rotate")
	print("(Note that the file needs to be in the same directory as the script [for now]")
	print("The file NEEDS TO BE A PDF, the script requires that you enter the name with the .pdf extension\n")
	
	while True:
		originalFileName = input("File name: ").strip()
		
		if originalFileName[-4:] == '.pdf':
			break
		else:
			print("Please make sure the file name has the .pdf extension at the end\n")
	
	print("\nPlease enter the new name you wish to give the file")
	print("(Note: no name will simply use the original name and add '-rotated-[degree]' at the end)\n")
	newFileName = input("New file name: ").strip()
	
	if newFileName == '':
		newFileName += originalFileName[:-4] + "-rotated-" + str(rotationAngle) + '.pdf'
		print("No name entered, using " + newFileName + " as the new file's name")
	elif newFileName[-4:] != '.pdf':
		newFileName += '.pdf'
		print("Name does not contain .pdf extension, adding the extension through the scirpt so '" + newFileName + "' will be the new file's name")
	
	
	selectOptionTitle = 'Would you like to (go to option and press enter):'
	options = ['Rotate a set of pages (e.g rotate only pages 1-5 and not the rest)', 'Rotate only one page', 'Rotate all the pages']
	selectedOption, selectedIndex = optionSelector(selectOptionTitle, options)
	
	if selectedIndex == 0:
		numPages = getNumberOfPages(originalFileName)
		#Setting outputOption = 1 since pdfReader.getPage uses list / array style to refer to pages
		pageList = optionSelector('Please choose pages you want to rotate (press SPACE to mark, ENTER to continue): ', list(range(1, numPages+1)), True, 1, 1)
		PdfRotateSet(originalFileName, newFileName, rotationAngle, pageList)
		
	elif selectedIndex == 1:
		numPages = getNumberOfPages(originalFileName)
		page = getIntInput('Please enter a number between 1 and ' + str(numPages) + ' : ')
		PdfRotateSet(originalFileName, newFileName, rotationAngle, page)
		
	elif selectedIndex == 2:
		numPages = getNumberOfPages(originalFileName)
		PdfRotateSet(originalFileName, newFileName, rotationAngle, list(range(0, numPages+1)))
	
	print("\nDone rotation")



def merge():
	mergeNum = None
	fileNames = []
	
	while True:
		print('How many PDF\'s are you merging?')
		print('[Minimum of 2 (ofcorse)]')
		mergeNum = getIntInput('')
	
		confirmation = optionSelector( ('You want to merge ' + str(mergeNum) + ' PDF\'s?'), ['Yes', 'No'], outputOption = 2)
		
		if confirmation == 'Yes':
			break
			
	if mergeNum != None:
		index = 0
		
		print('\nPlease enter the names of the ' + str(mergeNum) + ' files you wish to merge')
		print('The files will be merged in the order you enter them. (e.g. if you enter "file1.pdf" then "file2.pdf" then the merge order will be "file1" then "file2"')
		print("(Note that the files need to be in the same directory as the script [for now]")
		print("The file NEEDS TO BE A PDF, the script requires that you enter the name with the .pdf extension\n")
	
		while index < mergeNum:
			while True:
				fileName = input('File number ' + str(index + 1) + ' : ').strip()
			
				if fileName[-4:] == '.pdf':
					fileNames.append(fileName)
					index += 1
					break
				else:
					print("Please make sure the file name has the .pdf extension at the end\n")
					
		allFileNamesString = ''
		
		for i in range(len(fileNames)):
			if ( i == (len(fileNames) + 1) ):
				allFileNamesString += fileNames[i]
			else:
				allFileNamesString += fileNames[i] + ', '
				
		print('The following files will be merged: ')
		print('\t' + allFileNamesString)
				
		print("\nPlease enter the new name you wish to give to the merged file")
		print("(Note: no name will simply use the name of the first file followed by '-merged' at the end)\n")
		newFileName = input("New file name: ").strip()
		
		if newFileName == '':
			newFileName += fileNames[0][:-4] + '-merged' + '.pdf'
			print("No name entered, using " + newFileName + " as the new file's name")
		elif newFileName[-4:] != '.pdf':
			newFileName += '.pdf'
			print("Name does not contain .pdf extension, adding the extension through the scirpt so '" + newFileName + "' will be the new file's name")
			
		PDFmerge(fileNames, newFileName)
		
		print("\nDone merging")
	
	
def testPick():
	selectOptionTitle = 'Would you like to (go to option and press enter):'
	options = ['Rotate a set of pages (e.g rotate only pages 1-5 and not the rest)', 'Rotate only one page', 'Rotate all the pages']
	selectedOption, selectedIndex = pick(options, selectOptionTitle)
	print(type(selectedIndex))
	print(selectedIndex)



def main():
	getMergeInfo()

if __name__ == "__main__": 
	# calling the main function 
	main() 

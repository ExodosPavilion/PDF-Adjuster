# importing the required modules 
import PyPDF2 


#link to refer to
#	https://www.geeksforgeeks.org/working-with-pdf-files-in-python/


def PdfRotateAll(origFileName, newFileName, rotation): 
	# creating a pdf File object of original pdf 
	originalPdfFileObj = open(origFileName, 'rb') 
	
	# creating a pdf Reader object 
	pdfReader = PyPDF2.PdfFileReader(originalPdfFileObj) 

	# creating a pdf writer object for new pdf 
	pdfWriter = PyPDF2.PdfFileWriter() 
	
	# rotating each page 
	for page in range(pdfReader.numPages): 

		# creating rotated page object 
		pageObj = pdfReader.getPage(page) 
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
	

def getIntInput(prompt):
	while True:
		try:
			value = int(input(prompt).strip())
			break
		except ValueError:
			print("Please enter a valid integer\n")
		
	return value
	

def getRotationInfo():
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
		print("Name does not contain .pdf extension, adding the extension through scirpt so '" + newFileName + "' will be the new file's name")
		
	PdfRotateAll(originalFileName, newFileName, rotationAngle)
	
	print("\nDone rotation")

def main():
	getRotationInfo()

if __name__ == "__main__": 
	# calling the main function 
	main() 

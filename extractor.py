import sys
import os
import argparse
import signal

magic = {'jpg':
			{
			'header':[0xFF, 0xD8, 0xFF],
			'trailer': [0xFF, 0xD9]
			}
		}
fileSize = 0

def signalHandler(sig, frame):
	if sig == signal.SIGINT:
		print('\nExiting...')
		sys.exit(0)

def findStartSequence(file, fileType):
	index = 0
	while True:
	
		# check if it matches
		if index == len(magic[fileType]['header']):
			break
			
		# read 1 byte at a time
		buf = file.read(1)
		
		# check if EOF is reached
		if not buf:
			break
			
		# byte value, in decimal
		byte = ord(buf)
		
		sys.stdout.write("\rRead {:,} bytes; {:.1f}%".format(file.tell(), 100.0*file.tell()/fileSize))
		sys.stdout.flush()		
		
		if byte == magic[fileType]['header'][index]:
			index += 1
		else:
			index = 0
	# print newline
	print ''

def findEndSequence(file, fileIndex, fileType):
	with open('image{}.{}'.format(fileIndex, fileType), 'wb') as outputFile:
		
		index = 0
		while index < len(magic[fileType]['trailer']):
			buf = ord(file.read(1))
			outputFile.write(chr(buf))
			
			if (buf == magic[fileType]['trailer'][index]):
				index += 1
			else:
				index = 0
	
	print 'Written file image{}.{}'.format(fileIndex, fileType)

def main(args):

	# intercept CTRL+C
	signal.signal(signal.SIGINT, signalHandler)

	parser = argparse.ArgumentParser(description="Extract JPEG images from a file (e.g. a disk image)")
	parser.add_argument('file', nargs=1, help='The name of the file to scan')
	parser.add_argument('type', nargs=1, help='The file format to find. Currently only jpg works')
	parser.add_argument('-s', '--start', nargs=1, dest='start', help='Position from which start the search')

	args = parser.parse_args()		
	
	file = args.file[0]
	fileType = args.type[0]
	startIndex = int(args.start[0]) if args.start else None
	
	global fileSize
	try:
		fileSize = os.path.getsize(file)
	except OSError as e:
		print str(e)
	 	return
		
	print 'File size: {:,d} byte(s)'.format(fileSize)
	
	fileIndex = 0
	with open(file, 'rb') as file:
	
		if startIndex:
			if startIndex > fileSize:
				print 'Start index is greater than file size'
				return
			if startIndex < 0:
				startIndex = 0
			
			file.seek(startIndex)
		while file.tell() < fileSize:
			findStartSequence(file, fileType)
			if file.tell() >= fileSize:
				break
			print 'An image is found. Extracting it...'
			fileIndex += 1
			# go back to the beginning of magic numbers
			file.seek(-len(magic[fileType]['header']), os.SEEK_CUR)
			findEndSequence(file, fileIndex, fileType)
				
if __name__ == '__main__':
	main(sys.argv)
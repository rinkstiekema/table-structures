import cv2
import pytesseract
from bs4 import BeautifulSoup as bs4

def get_bbox(element):
	title = element['title']
	bbox_string = title.split(';')[0]
	str_array = bbox_string.split("bbox ")[1]
	return list(map(int,str_array.split(" ")))

def get_words(element):
	result = []
	words = element.findAll("span", {"class": "ocrx_word"})
	for word in words:
		x = word.contents[0]
		try:
			result.append(x.contents[0])
		except:
			result.append(x)

	result = " ".join(result)
	return result;

filename = '../data/output-images/Multilingual document recognition research and its application in China-Table2-1.png'
print(pytesseract.image_to_string(filename, config='-psm 6 -dpi 10'))
exit()
soup = bs4(hocr, features="lxml")

ocr_areas = soup.findAll("span", {"class": "ocr_line"})
columns = []

for area in ocr_areas:
	columns.append({'bbox': get_bbox(area), 'content': get_words(area)})
	print({'bbox': get_bbox(area), 'content': get_words(area)})
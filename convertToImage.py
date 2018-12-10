from pdf2image import convert_from_path
pages = convert_from_path('../reading/DeepDive.pdf')

counter = 0
for page in pages[50:60]:
    page.save('./in/in'+str(counter)+'.jpg', 'JPEG')
    counter += 1
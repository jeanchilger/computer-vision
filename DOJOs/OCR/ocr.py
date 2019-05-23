# Python: OCR for PDF or Compare textract, pytesseract, and pyocr
# https://medium.com/@winston.smith.spb/python-ocr-for-pdf-or-compare-textract-pytesseract-and-pyocr-acb19122f38c
# https://stackabuse.com/pytesseract-simple-python-optical-character-recognition/

imgs = {
    # 'eng-1.jpg':'eng',
    # 'ptbr-1.png':'por',
    'jpn-1.png':'jpn',
    # 'kor-1.jpg':'kor',
}

for img_src,lang in imgs.items():
    print(img_src)

    print("PyTesseract")
    # https://pypi.org/project/pytesseract/
    import cv2
    import pytesseract as tesseract

    img = cv2.imread(f"input/{img_src}")
    text = tesseract.image_to_string(img, lang=lang)
    pdf = tesseract.image_to_pdf_or_hocr(img, lang=lang, extension="pdf")
    hocr = tesseract.image_to_pdf_or_hocr(img, lang=lang, extension="hocr")
    print(text)
    print(None)
    print(None)
    print(tesseract.image_to_boxes(img))
    # Treino do Tesseract
    # https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00



    # print("\n\nPyORC")
    # # https://gitlab.gnome.org/World/OpenPaperwork/pyocr
    # from PIL import Image
    # import codecs
    #
    # import pyocr
    # import pyocr.builders
    #
    # ocr = pyocr.get_available_tools()[0]
    # lang = ocr.get_available_languages()[0]
    # img = Image.open(f'input/{img_src}')
    #
    # txt = ocr.image_to_string(
    #     img,
    #     lang=lang,
    #     builder=pyocr.builders.TextBuilder()
    # )
    #
    # print(txt)
    #
    # # Escrita txt
    # with codecs.open(f"output/{img_src}.txt", 'w', encoding='utf-8') as file_descriptor:
    #     pyocr.builders.TextBuilder().write_file(file_descriptor, txt)
    #
    # txt = ocr.image_to_string(
    #     img,
    #     lang=lang,
    #     builder=pyocr.builders.LineBoxBuilder()
    # )
    #
    #
    # #HOCR
    # # https://en.wikipedia.org/wiki/HOCR
    # with codecs.open(f"output/{img_src}.html", 'w', encoding='utf-8') as file_descriptor:
    #     pyocr.builders.LineBoxBuilder().write_file(file_descriptor, txt)
    #
    # # PDF
    #
    # pyocr.libtesseract.image_to_pdf(img, f'output/{img_src}.pdf')
    #
    # ori = ocr.detect_orientation(img, lang=lang)
    # print(ori)
    # https://github.com/the-paperless-project/paperless#readme
    # https://docs.mayan-edms.com/
    # https://gitlab.gnome.org/World/OpenPaperwork/paperwork#readme

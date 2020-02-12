__Start projektu__
1. Pobrać program tesseract ze strony https://tesseract-ocr.github.io/tessdoc/Downloads
2. Pobrać plik pol.traineddata ze strony https://github.com/tesseract-ocr/tessdata i umieścić go w folderze tessdata w lokalizacji programu tesseract
3. `start venv\Scripts\activate.bat` na Windows
4. `pip install -r "requirements.txt"`
5. W pliku settings.py w zmiennej TESSERACT_PATH ustawić link do programu tesseract 
np. 'C:\Program Files\Tesseract-OCR\tesseract.exe'
6. `python manage.py runserver`

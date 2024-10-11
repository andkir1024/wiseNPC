 (Ctrl+Shift+P) Python: Create Environment
инициализхация виртуального окружения !
python -m venv .venv
.\.venv\Scripts\activate
deactivate

установка необходимых зависимостей
pip install -r Requirements.txt

сохранение необходимых зависимостей 
pip freeze > Requirements.txt

git config --global user.email "andkir@mail.ru"
git config --global user.name "andkir1024"

генерация exe
auto-py-to-exe

под ubuntu установка opencv
sudo apt install libgl1-mesa-glx -y
sudo apt-get install libzbar0
sudo apt-get install tesseract-ocr-rus -y

под ubuntu переход в venv
akirpichnikov@claudette:/home/chatbot/manual$ source .venv/bin/activate

размещение бота
/home/chatbot

установка моделей
python -m spacy download ru_core_news_sm
  
start - запуск без параметров 
start=1395522 - запуск на проект (?start=1395522)
https://t.me/WiseDimensionsbot?start=test=1234


pyuic5 test.ui -o design.py
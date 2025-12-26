# Веб-приложение для автоматического ответа на вопросы по документу

Приложение обрабатывает текстовый документ и отвечает на вопросы пользователя по его содержимому с помощью RAG-системы.

## Функции приложения:
- Излечение текста из файлов с применением OCR
- Создание векторной базы документа
- Поиск релевантных запросу чанков по векторному сходству с FAISS
- Генерация ответа LLM на основе выделенных чанков

## Содержание

- [Обработка документа](#Обработка-документа)
- [Векторизация](#Векторизация)
- [Подключение LLM](#Подключение-LLM)
- [Интерфейс](#Интерфейс)

## Обработка документа
- Поддерживаемые форматы файлов: PDF, DOCX, DOC, TXT, JPG, JPEG, PNG, BMP, TIFF
- OCR реализован на [pytesseract](https://pypi.org/project/pytesseract/), поддерживается русский и английский язык

### Инструкция по установке Tesseract-OCR и Poppler для распознавания PDF и изображений
#### Windows
1. Загрузите установочный пакет [Tesseract v5.5.0.20241111](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe) и установите программу в директорию `C:/Program Files/Tesseract-OCR`
2. Загрузите архив [Poppler v25.12.0-0](https://github.com/oschwartz10612/poppler-windows/releases/tag/v25.12.0-0) и распакуйте его в директорию `C:/Program Files/poppler-25.12.0`

#### Linux
1. Установите программы с помощью команд:
```
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt install poppler-utils
```
2. 
#### Mac
1. Установите программы с помощью команд:
```
brew install poppler
```

## Векторизация
- Эмбеддинги
- FAISS

## Подключение LLM
- Модель, параметры: 
- ollama

## Интерфейс
Реализован с применением Flask

Метрики оценки на задаче **Q&A**

| Модель | Метрика |
| ------ | ------- |
| Llama  | 90%     |

<img width="2587" height="964" alt="image" src="https://github.com/user-attachments/assets/bf984433-8c2b-4f3e-b309-2c5e67f30300" />

Блок-схема с описанием архитектуры решения ([источник изображения](https://alvinntnu.github.io/python-notes/_images/nlp-pipeline.png))

> Важный факт про ПО

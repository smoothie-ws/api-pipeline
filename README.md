# API Pipeline

Простой скрипт, который:

1. читает отзывы из `input.csv`
2. отправляет каждый отзыв в LLM через API
3. получает ответ в формате JSON
4. сохраняет результат в `output.json`

В этом варианте используется задача классификации отзывов:

- `sentiment`: `positive`, `negative` или `neutral`
- `topic`: тема отзыва

По умолчанию скрипт настроен на `Groq`, потому что у него есть бесплатный план и OpenAI-compatible API.

## Файлы

- `script.py` — основной скрипт
- `input.csv` — входной CSV-файл
- `output.json` — выходной JSON-файл

## Входные данные

CSV должен содержать две колонки:

- `id`
- `review`

Пример:

```csv
id,review
1,Телефон работает быстро и батарея держит заряд целый день
2,Доставка задержалась на неделю и коробка пришла помятая
3,Качество звука у наушников отличное и бас очень приятный
```

## Выходные данные

Пример:

```json
[
  {
    "id": "1",
    "review": "Телефон работает быстро и батарея держит заряд целый день",
    "result": {
      "sentiment": "positive",
      "topic": "смартфон"
    }
  },
  {
    "id": "2",
    "review": "Доставка задержалась на неделю и коробка пришла помятая",
    "result": {
      "sentiment": "negative",
      "topic": "доставка"
    }
  }
]
```

## Установка

```bash
pip install requests python-dotenv
```

## .env

Создай рядом с `script.py` файл `.env`:

```env
API_KEY=your_groq_api_key
BASE_URL=https://api.groq.com/openai/v1
MODEL=llama-3.1-8b-instant
```

## Запуск

```bash
python script.py input.csv output.json
```

Если аргументы не переданы, используются значения по умолчанию:

- вход: `input.csv`
- выход: `output.json`

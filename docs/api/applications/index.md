# Applications

## Получение структуры формы

```http
GET /api/v0/application/schema/
```

В качестве ответа возвращается список полей анкеты. Каждое поле анкеты имеет следующее представление:

```python
key: str
label: str
type: FieldType
required: bool = False
options: list[OptionSchema] | None = None
depends_on: DependencySchema | None = None
```

Вспомогательнын классы:

```python
class OptionSchema(msgspec.Struct):
    value: str
    label: str


class DependencySchema(msgspec.Struct):
    field: str
    contains: str
```

Пример ответа:

```json
[
    {
        "key": "full_name",
        "label": "ФИО",
        "type": "text",
        "required": true,
        "options": null,
        "depends_on": null
    },
    {
        "key": "group",
        "label": "Учебная группа",
        "type": "text",
        "required": true,
        "options": null,
        "depends_on": null
    },
    {
        "key": "birth_date",
        "label": "Дата рождения",
        "type": "date",
        "required": true,
        "options": null,
        "depends_on": null
    },
    {
        "key": "telegram_url",
        "label": "Ссылка на Telegram",
        "type": "url",
        "required": true,
        "options": null,
        "depends_on": null
    },
    {
        "key": "vk_url",
        "label": "Ссылка на профиль в VK",
        "type": "url",
        "required": true,
        "options": null,
        "depends_on": null
    },
    {
        "key": "github_url",
        "label": "Профиль на GitHub",
        "type": "url",
        "required": true,
        "options": null,
        "depends_on": {
        "field": "categories",
        "contains": "programming"
        }
    },
    {
        "key": "portfolio_url",
        "label": "Ссылка на портфолио",
        "type": "url",
        "required": false,
        "options": null,
        "depends_on": {
        "field": "categories",
        "contains": "content_creation"
        }
    },
    {
        "key": "categories",
        "label": "Какой из следующих видов деятельности вам наиболее интересен?",
        "type": "multiple_choice",
        "required": true,
        "options": [
        {
            "value": "programming",
            "label": "Решение сложных технических задач, завязанных на программировании"
        },
        {
            "value": "event_planning",
            "label": "Планирование и организация мероприятий"
        },
        {
            "value": "content_creation",
            "label": "Создание визуального контента (СММ, Фото, Видео, Клипмейкинг, Графика, Дизайн)"
        },
        {
            "value": "team_building",
            "label": "Работа с людьми и командообразование"
        },
        {
            "value": "partnership",
            "label": "Взаимодействие с партнерами, ведение деловых переговоров"
        },
        {
            "value": "event_tech_support",
            "label": "Поддержка и помощь в решении технических задач мероприятий (Настройка звука, модерация презентации, расстановка оборудования, т.д)"
        }
        ],
        "depends_on": null
    },
    {
        "key": "tech_tasks",
        "label": "В решении каких технических задач вы заинтересованы?",
        "type": "multiple_choice",
        "required": true,
        "options": [
        {
            "value": "web",
            "label": "Разработка сайтов"
        },
        {
            "value": "bots",
            "label": "Разработка ботов"
        },
        {
            "value": "games",
            "label": "Разработка игр"
        }
        ],
        "depends_on": {
        "field": "categories",
        "contains": "programming"
        }
    },
    {
        "key": "visual_content_types",
        "label": "Какой вид создания визуального контента вас интересует?",
        "type": "multiple_choice",
        "required": true,
        "options": [
        {
            "value": "smm",
            "label": "СММ"
        },
        {
            "value": "photo",
            "label": "Фото"
        },
        {
            "value": "video",
            "label": "Видео"
        },
        {
            "value": "design",
            "label": "Дизайн"
        }
        ],
        "depends_on": {
        "field": "categories",
        "contains": "content_creation"
        }
    }
]
```

## Получение списка всех сущностей Application

```http
GET /api/v0/application/
```

## Создание новой сущности Application

```http
POST /api/v0/application/
```

Пример входных значений:

```json
{
  "full_name": "string",
  "group": "string",
  "birth_date": "2026-08-29",
  "telegram_url": "string",
  "vk_url": "string",
  "github_url": "string",
  "portfolio_url": "string",
  "categories": [],
  "tech_tasks": [],
  "visual_content_types": []
}
```

В поля `categories`, `tech_tasks` и `visual_content_types` указывается список `value` выбранных элементов из раздела `options`. Например:

```json
"categories": ["programming", "partnership"],
```

## Получение сущности Application по её ID

```http
GET /api/v0/application/{application_id}/
```

## Обновление существубщей сущности Application по её ID

```http
POST /api/v0/application/{application_id}/
```

## Удаление сущности Application по её ID

```http
DELETE /api/v0/application/{application_id}/
```

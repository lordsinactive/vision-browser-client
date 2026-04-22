<div align="center">

# vision-client

**Асинхронный Python-клиент для API антидетект-браузера Vision**

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![httpx](https://img.shields.io/badge/httpx-%E2%89%A5%200.28-0a7cbf)
![pydantic](https://img.shields.io/badge/pydantic-%E2%89%A5%202.0-e92063?logo=pydantic&logoColor=white)
![status](https://img.shields.io/badge/status-alpha-orange)
![license](https://img.shields.io/badge/license-MIT-green)

</div>

---

## О проекте

`vision-client` — лёгкая обёртка над облачным API `api.browser.vision` и локальным демоном Vision (`127.0.0.1:3030`). Весь I/O построен на `httpx.AsyncClient`, все ответы строго валидируются через `pydantic`. Никаких синхронных веток, никакой магии — только явные `async/await`.

Покрытие API:

- **folders** — управление папками профилей
- **profiles** — CRUD профилей с фингерпринтами и прокси
- **proxies** — прокси-пулы с гео-инфо
- **tags**, **statuses** — метки и статусы в рамках папки
- **cookies** — экспорт/импорт cookies по профилю
- **fingerprints** — получение и варьирование фингерпринтов (languages / timezones / renderers)
- **local** — запуск/остановка профилей через локальный Vision
- **instant** — одноразовые instant-профили (GET / typed body / raw dict)

---

## Установка

```bash
pip install httpx pydantic
```

Либо из `requirements.txt`:

```bash
pip install -r requirements.txt
```

Клонирование и установка локально:

```bash
git clone <repo-url> vision-client
cd vision-client
pip install -e .
```

Требуется **Python 3.11+** (используются `StrEnum`, `X | Y` в аннотациях).

---

## Быстрый старт

```python
import asyncio
from vision_client import VisionClient
from vision_client.models import FolderIcons, FolderColors

async def main() -> None:
    async with VisionClient(x_token='YOUR_TOKEN') as client:
        folder = await client.create_folder(
            folder_name='accounts',
            folder_icon=FolderIcons.Google,
            folder_color=FolderColors.BLUE,
        )
        print(folder.id, folder.folder_name)

asyncio.run(main())
```

---

## Авторизация

Клиент принимает **ровно один** из двух токенов:

| Параметр         | Описание                              | Заголовок         |
|------------------|---------------------------------------|-------------------|
| `x_token`        | Персональный токен пользователя       | `X-Token`         |
| `x_team_token`   | Командный токен (team-пространство)   | `X-Team-Token`    |

```python
# персональный
client = VisionClient(x_token='...')

# командный
client = VisionClient(x_team_token='...')
```

Если передать оба или ни одного — `VisionClient` выбросит `ValueError` на старте.

Дополнительные параметры конструктора:

| Параметр     | По умолчанию                    | Назначение                    |
|--------------|---------------------------------|-------------------------------|
| `base_url`   | `https://api.browser.vision`    | Облачный API Vision           |
| `local_url`  | `http://127.0.0.1:3030`         | Локальный Vision-демон        |

---

## Архитектура

`VisionClient` собран из тематических миксинов — каждый отвечает за свой раздел API:

```
VisionClient
├── Folders        — папки
├── Profiles       — профили
├── Proxies        — прокси
├── Statuses       — статусы
├── Tags           — теги
├── Fingerprints   — фингерпринты и варианты
├── Cookies        — cookies по профилю
├── Local          — /start, /stop, /list локального демона
└── Instant        — /start/instant, /stop/instant
```

Единая `AsyncClient`-сессия, общий `base_url` / `local_url`, `async with` закрывает соединение через `close()`.

---

## Справочник методов

### Folders

| Метод                                    | HTTP   | Эндпоинт                               |
|------------------------------------------|--------|----------------------------------------|
| `get_folders()`                          | GET    | `/api/v1/folders`                      |
| `create_folder(name, icon, color)`       | POST   | `/api/v1/folders`                      |
| `edit_folder(id, name?, icon?, color?)`  | PATCH  | `/api/v1/folders/{id}`                 |
| `delete_folder(id)`                      | DELETE | `/api/v1/folders/{id}`                 |

### Profiles

| Метод                                              | HTTP   | Эндпоинт                                              |
|----------------------------------------------------|--------|-------------------------------------------------------|
| `get_profiles(folder_id)`                          | GET    | `/api/v1/folders/{fid}/profiles`                      |
| `get_profile(folder_id, profile_id)`               | GET    | `/api/v1/folders/{fid}/profiles/{pid}`                |
| `create_profile(folder_id, name, fingerprint, …)`  | POST   | `/api/v1/folders/{fid}/profiles`                      |
| `edit_profile(folder_id, profile_id, …)`           | PATCH  | `/api/v1/folders/{fid}/profiles/{pid}`                |
| `delete_profile(folder_id, profile_id)`            | DELETE | `/api/v1/folders/{fid}/profiles/{pid}`                |

### Proxies

| Метод                                              | HTTP   | Эндпоинт                                         |
|----------------------------------------------------|--------|--------------------------------------------------|
| `get_proxies(folder_id)`                           | GET    | `/api/v1/folders/{fid}/proxies`                  |
| `create_proxies(folder_id, proxies)`               | POST   | `/api/v1/folders/{fid}/proxies`                  |
| `edit_proxy(folder_id, proxy_id, …)`               | PUT    | `/api/v1/folders/{fid}/proxies/{pid}`            |
| `delete_proxies(folder_id, proxy_ids)`             | DELETE | `/api/v1/folders/{fid}/proxies`                  |

### Tags

| Метод                                         | HTTP   | Эндпоинт                                   |
|-----------------------------------------------|--------|--------------------------------------------|
| `get_tags(folder_id)`                         | GET    | `/api/v1/folders/{fid}/tags`               |
| `create_tags(folder_id, tags)`                | POST   | `/api/v1/folders/{fid}/tags`               |
| `edit_tag(folder_id, tag_id, name?, color?)`  | PUT    | `/api/v1/folders/{fid}/tags/{tid}`         |
| `delete_tags(folder_id, tag_ids)`             | DELETE | `/api/v1/folders/{fid}/tags`               |

### Statuses

| Метод                                                  | HTTP   | Эндпоинт                                         |
|--------------------------------------------------------|--------|--------------------------------------------------|
| `get_statuses(folder_id)`                              | GET    | `/api/v1/folders/{fid}/statuses`                 |
| `create_statuses(folder_id, statuses)`                 | POST   | `/api/v1/folders/{fid}/statuses`                 |
| `edit_status(folder_id, status_id, name?, color?)`     | PUT    | `/api/v1/folders/{fid}/statuses/{sid}`           |
| `delete_statuses(folder_id, status_ids)`               | DELETE | `/api/v1/folders/{fid}/statuses`                 |

### Cookies

| Метод                                                          | HTTP | Эндпоинт                                              |
|----------------------------------------------------------------|------|-------------------------------------------------------|
| `get_cookies(folder_id, profile_id)`                           | GET  | `/api/v1/cookies/{fid}/{pid}`                         |
| `import_cookies(folder_id, profile_id, cookies)`               | POST | `/api/v1/cookies/import/{fid}/{pid}`                  |

### Fingerprints

| Метод                                                | HTTP | Эндпоинт                                    |
|------------------------------------------------------|------|---------------------------------------------|
| `get_fingerprint(os, version='latest', crc?, mode?)` | GET  | `/api/v1/fingerprints/{os}/{version}`       |
| `get_languages()`                                    | GET  | `{local}/variations/language`               |
| `get_timezones()`                                    | GET  | `{local}/variations/timezone`               |
| `get_renderers(os, version='latest')`                | GET  | `{local}/variations/renderer`               |

### Local (локальный демон)

| Метод                                                  | HTTP | Эндпоинт                                   |
|--------------------------------------------------------|------|--------------------------------------------|
| `get_active_profiles()`                                | GET  | `{local}/list`                             |
| `start_profile(folder_id, profile_id, args?, proxy?)`  | POST | `{local}/start/{fid}/{pid}`                |
| `stop_profile(folder_id, profile_id)`                  | GET  | `{local}/stop/{fid}/{pid}`                 |

### Instant

| Метод                                        | HTTP       | Эндпоинт                                 |
|----------------------------------------------|------------|------------------------------------------|
| `start_instant_profile(config?)`             | GET / POST | `{local}/start/instant`                  |
| `stop_instant_profile(profile_id)`           | GET        | `{local}/stop/instant/{pid}`             |

---

## Примеры

### Создание и редактирование папки

```python
from vision_client.models import FolderIcons, FolderColors

folder = await client.create_folder(
    folder_name='fb-ads',
    folder_icon=FolderIcons.Facebook,
    folder_color=FolderColors.BLUE,
)

await client.edit_folder(
    folder_id=folder.id,
    folder_name='fb-ads-renamed',
    folder_color=FolderColors.GREEN,
)
```

### Добавление прокси (модель + сырой dict)

```python
from vision_client.models import ProxyCreateItem, ProxyType

proxies = await client.create_proxies(
    folder.id,
    proxies=[
        ProxyCreateItem(
            proxy_name='res-1',
            proxy_type=ProxyType.SOCKS5,
            proxy_ip='1.1.1.1',
            proxy_port=1080,
        ),
        {
            'proxy_name': 'res-2',
            'proxy_type': 'HTTP',
            'proxy_ip': '2.2.2.2',
            'proxy_port': 8080,
            'proxy_username': 'u',
            'proxy_password': 'p',
        },
    ],
)
```

### Получение фингерпринта и создание профиля

```python
from vision_client.models import OSType

fp = await client.get_fingerprint(OSType.WINDOWS)
fp.webrtc_pref = 'auto'
fp.canvas_pref = 'real'
fp.webgl_pref = 'real'
fp.ports_protection = [3389, 5900, 5901, 5800, 7070, 6568, 5938, 1080, 8080, 3128, 3030]

created = await client.create_profile(
    folder.id,
    profile_name='worker-01',
    fingerprint=fp,
    new_profile_tags=['auto-tag'],
)
profile_id = created.data.id
```

### Импорт cookies

```python
from vision_client.models import Cookie

await client.import_cookies(
    folder_id=folder.id,
    profile_id=profile_id,
    cookies=[
        Cookie(
            name='datr',
            value='abc',
            path='/',
            domain='.facebook.com',
            expires=1739638509,
        ),
        {
            'name': 'OTZ',
            'value': 'xyz',
            'path': '/',
            'domain': 'accounts.google.com',
            'expires': 1707670639,
        },
    ],
)
```

### Запуск профиля через локальный демон

```python
from vision_client.models import ProxyConfig, ProxyTypes

started = await client.start_profile(
    folder_id=folder.id,
    profile_id=profile_id,
    args=['--lang=en-US'],
    proxy=ProxyConfig(
        type=ProxyTypes.SOCKS5,
        address='1.1.1.1',
        port=1080,
    ),
)
print(started.port)

await client.stop_profile(folder.id, profile_id)
```

### Instant-профиль (три способа)

```python
from vision_client.models import InstantStartBody, InstantBehavior

# 1. GET без параметров
s1 = await client.start_instant_profile()

# 2. Типизированный body
s2 = await client.start_instant_profile(
    InstantStartBody(
        name='typed',
        behavior=InstantBehavior(headless=False),
    )
)

# 3. Сырой dict
s3 = await client.start_instant_profile({'name': 'raw'})

for s in (s1, s2, s3):
    await client.stop_instant_profile(s.profile_id)
```

---

## Обработка ошибок

Все методы вызывают `response.raise_for_status()` — при HTTP 4xx/5xx вылетает `httpx.HTTPStatusError` с исходным ответом внутри:

```python
import httpx

try:
    await client.get_folders()
except httpx.HTTPStatusError as e:
    print(e.response.status_code, e.response.text)
except httpx.RequestError as e:
    print('network error:', e)
```

Валидация ответа через `pydantic.ValidationError` — если API вернул неожиданную схему.

---

## Модели (pydantic)

Все модели экспортируются из `vision_client.models`:

```python
from vision_client.models import (
    # folders
    Folder, FolderDelete, FolderUsage, FolderIcons, FolderColors,
    # tags / statuses
    Tag, TagColors, Status, StatusColors,
    # proxy
    Proxy, ProxyCreateItem, ProxyType, ProxyTypes, ProxyConfig, Geolocation,
    # profiles
    Profile, ProfileListItem, ProfilesList, ProfileCreate, ProfileDelete,
    # fingerprint
    Fingerprint, FingerprintScreen, FingerprintHints, FingerprintNavigator,
    FingerprintMediaDevices, FingerprintWebgl, FingerprintWebglExtra,
    FingerprintWebgpu, FingerprintWebgpuLimits, FingerprintOptions,
    OSType, SmartMode,
    # cookies
    Cookie,
    # local
    LocalProfile, LocalProfilesList, LocalStart, LocalStop,
    # instant
    InstantStartBody, InstantStart, InstantStop,
    InstantFingerprint, InstantNavigator, InstantScreen,
    InstantMediaDevices, InstantGeolocation, InstantNoise,
    InstantBehavior, InstantCookie, SameSite,
)
```

Везде, где API принимает объект, клиент допускает **и** модель, **и** сырой `dict` — конвертация делается автоматически.

---

## Структура проекта

```
vision-browser-client/
├── vision_client/
│   ├── __init__.py              # экспорт VisionClient
│   ├── vision_client.py         # сам класс-композит с миксинами
│   ├── methods/                 # реализация эндпоинтов (миксины)
│   │   ├── folders.py
│   │   ├── profiles.py
│   │   ├── proxy.py
│   │   ├── statuses.py
│   │   ├── tags.py
│   │   ├── cookies.py
│   │   ├── fingerprint.py
│   │   ├── local.py
│   │   └── instant.py
│   └── models/                  # pydantic-модели
│       ├── folders.py
│       ├── profiles.py
│       ├── proxy.py
│       ├── statuses.py
│       ├── tags.py
│       ├── cookies.py
│       ├── fingerprint.py
│       ├── local.py
│       └── instant.py
├── tests.py                     # ручной прогон всех разделов API
├── pyproject.toml
└── requirements.txt
```

---

## Ручные тесты

`tests.py` — интерактивный харнесс: прогоняет все разделы API последовательно, создаёт и удаляет тестовые сущности, печатает результат в консоль. Для запуска подставить свой токен в `TOKEN`:

```bash
python tests.py
```

Секции: `folders`, `tags`, `statuses`, `proxies`, `profiles`, `cookies`, `fingerprints`, `local`, `instant`.

---

## Требования

- Python ≥ 3.11
- `httpx` ≥ 0.28
- `pydantic` ≥ 2.0
- Запущенный локальный Vision-демон на `127.0.0.1:3030` — для методов из разделов `Local`, `Instant` и `Fingerprints` (`get_languages`, `get_timezones`, `get_renderers`)

---
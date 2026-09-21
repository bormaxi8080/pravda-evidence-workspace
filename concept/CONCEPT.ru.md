# Provereno Evidence Workspace — CONCEPT

**Статус документа:** концепция и техническое видение базовой production-версии 1.0  
**Язык:** русский  
**Основание:** `README.md`, интерактивный HTML-прототип интерфейса и презентация `Provereno Evidence Workspace`  
**Назначение документа:** зафиксировать целевую продуктовую модель, архитектурные принципы, границы базовой версии, ключевые сущности и этапы реализации до production-ready v1.0.

---

## 1. Краткое резюме

**Provereno Evidence Workspace** — open-source self-hosted система сохранения, организации и публикации проверяемых веб-доказательств для независимых редакций, фактчекинговых команд, расследовательских проектов и НКО.

Система создаётся как редакционный слой поверх движка веб-архивации `opensanctions/pravda`, использующего Playwright. Она должна позволять редактору без терминала и специальных навыков:

1. передать URL страницы, публикации или списка URL;
2. выполнить управляемый capture в браузере;
3. сохранить несколько независимых представлений источника;
4. зафиксировать время, HTTP-метаданные и условия захвата;
5. вычислить криптографические контрольные суммы артефактов;
6. сохранить evidence-пакет локально в инфраструктуре редакции;
7. привязать его к коллекциям, тегам и редакционным заметкам;
8. провести редакционную проверку;
9. при необходимости опубликовать безопасную публичную evidence-ссылку;
10. экспортировать переносимый forensic package;
11. отслеживать дальнейшую доступность оригинального URL;
12. сохранить журнал действий пользователей и системы.

Ключевой принцип продукта:

> **Не просто архивировать страницу, а превращать её зафиксированное состояние в управляемое, проверяемое и пригодное для редакционного использования доказательство.**

Базовая архитектура должна оставаться простой для установки и сопровождения: **FastAPI + PostgreSQL + server-side UI + worker-процессы + Pravda/Playwright + локальное artifact storage + Nginx + Docker Compose**.

Для v1.0 приоритетом является не расширение набора функций, а перевод существующего прототипа в надёжный production-продукт: тесты, durable jobs, безопасность, backup/restore, WARC, аудит, изоляция browser capture, управляемые обновления и пилотирование в реальных редакциях.

---

# 2. Источники концепции и границы интерпретации

Документ основан на трёх материалах проекта.

### 2.1. README

README фиксирует следующие решения и функции:

- Python 3.11+;
- FastAPI;
- PostgreSQL 15;
- GitHub OAuth;
- роли `admin` и `editor`;
- capture через `opensanctions/pravda` / Playwright;
- PostgreSQL `LISTEN/NOTIFY` для фоновых jobs;
- SSE для отображения прогресса;
- collections и tags;
- CSV batch import до 500 URL;
- forensic receipt;
- PNG + MHTML + JSON metadata + SHA-256;
- public evidence viewer;
- URL monitoring;
- append-only audit log;
- Jinja2 SSR;
- Docker Compose + Nginx;
- AGPL-3.0.

### 2.2. HTML-прототип

Прототип подтверждает основную продуктовую структуру интерфейса:

- Dashboard;
- New Capture;
- Jobs Queue;
- Snapshots;
- Snapshot Detail;
- Collections & Tags;
- Public Viewer;
- Forensic Receipt;
- Settings.

Также прототип явно задаёт важные UX-решения:

- private-by-default;
- публикация evidence только после редакционного решения;
- безопасный просмотр screenshot вместо исполнения архивного HTML/MHTML;
- live job progress;
- batch workflow;
- статусы оригинального URL;
- светлая и тёмная темы;
- мобильная адаптация.

### 2.3. Pitch deck

Презентация уточняет продуктовую и организационную модель:

- целевой пользователь — редакция или НКО порядка 5–50 человек;
- self-hosting является частью ценностного предложения;
- проект решает проблему исчезновения и изменения веб-источников;
- private evidence особенно важно для чувствительных расследований;
- рабочий прототип уже существует;
- prototype → production является основным предметом дальнейшей разработки;
- обязательными production-задачами названы automated tests, CI/CD, security review, backup/restore и WARC;
- предполагается пилотирование в 3–5 редакциях;
- sustainability model: бесплатный AGPL-код + платные установка, managed hosting, обновления и поддержка.

### 2.4. Архитектурные выводы данного документа

Некоторые решения ниже являются **не прямыми требованиями исходных материалов, а инженерными рекомендациями**, вытекающими из заявленного назначения системы. К ним относятся, в частности:

- разделение `Source`, `Capture`, `Artifact`, `Publication`;
- durable queue через jobs table + `FOR UPDATE SKIP LOCKED`;
- использование `LISTEN/NOTIFY` только как wake-up signal;
- выделение web / worker / scheduler в отдельные процессы;
- отдельный `Evidence Manifest`;
- storage abstraction;
- SSRF-защита и сетевые ограничения для browser capture;
- отделение immutable evidence от изменяемой editorial metadata.

Эти рекомендации следует валидировать при ревью существующего прототипа.

---

# 3. Проблема

Веб-источник не является стабильным объектом.

Он может:

- быть удалён;
- быть отредактирован без уведомления;
- изменить URL;
- начать редиректить;
- стать недоступным без VPN;
- закрыться авторизацией;
- исчезнуть из соцсети;
- изменить содержимое при сохранении того же URL;
- блокировать внешних архивных роботов.

Для журналистики и фактчекинга это означает, что обычная ссылка не является достаточным доказательством того, что именно находилось по URL в момент проверки.

Типичная ситуация:

```text
Редакция публикует материал
        │
        ├── ссылается на источник
        │
        └── через несколько дней источник изменён или удалён
                         │
                         ▼
        читатель / юрист / редактор уже не может проверить
        первоначальный контекст
```

Public archives частично решают задачу, но имеют ограничения:

- чувствительный материал нельзя всегда отдавать третьей стороне;
- сохранение может быть невозможно технически;
- социальные платформы и тяжёлые JS-приложения могут архивироваться плохо;
- нет внутреннего editorial workflow;
- нет локального контроля доступа;
- нет единых коллекций, заметок, ролей и audit trail;
- нет гарантии, что внешний сервис останется доступен организации.

---

# 4. Продуктовая гипотеза

Целевой пользователь — небольшая или средняя редакция / НКО, которая:

- регулярно работает с изменяемыми или исчезающими источниками;
- хочет контролировать хранение evidence;
- не имеет отдельного archival engineer;
- не хочет самостоятельно собирать сложную инфраструктуру;
- нуждается в командной работе;
- периодически публикует evidence для читателей, партнёров или юридической проверки;
- предпочитает открытый код и возможность независимого self-hosting.

Основное конкурентное преимущество Provereno Evidence Workspace должно находиться **не в самом crawler**, а в простом редакционном workflow вокруг надёжного capture и preservation.

---

# 5. Product scope

## 5.1. Что входит в базовую версию 1.0

### Capture

- ручной capture одного URL;
- batch capture из CSV;
- очередь;
- повторные попытки;
- progress events;
- ограничение concurrency;
- захват через Pravda/Playwright.

### Evidence preservation

- screenshot PNG;
- MHTML;
- structured metadata JSON;
- WARC/WARC.GZ;
- SHA-256;
- evidence manifest;
- фиксирование capture provenance.

### Editorial workspace

- users;
- roles;
- collections;
- tags;
- notes;
- search/filter;
- review state;
- private-by-default.

### Publication

- отдельное действие Publish;
- публичная evidence page;
- screenshot preview;
- timestamp;
- source URL;
- hashes;
- origin availability state;
- безопасные downloads;
- unpublish/revoke.

### Forensic export

- ZIP package;
- receipt HTML;
- receipt PDF;
- screenshot;
- MHTML;
- WARC;
- metadata;
- manifest;
- SHA256SUMS.

### Operations

- Docker Compose;
- Nginx;
- HTTPS-ready deployment;
- migrations;
- backup;
- restore;
- upgrade procedure;
- health checks;
- structured logging.

### Security

- GitHub OAuth;
- RBAC;
- Secure/HttpOnly cookies;
- SSRF protection;
- safe artifact serving;
- browser isolation;
- input validation;
- rate/concurrency controls;
- security review.

### Quality

- unit tests;
- integration tests;
- E2E tests;
- security tests;
- CI/CD.

---

## 5.2. Что сознательно не является P0 для 1.0

Чтобы не превратить prototype-hardening в бесконечную платформенную разработку, в базовый scope не следует включать как обязательные:

- Kubernetes;
- microservices;
- multi-tenant SaaS;
- Elasticsearch/OpenSearch;
- RabbitMQ/Kafka;
- AI-анализ содержания;
- сложный semantic diff;
- browser extension;
- полноценный end-user CLI;
- application-level encryption каждого артефакта;
- обязательные цифровые подписи manifest;
- распределённый capture cluster;
- отдельный frontend SPA.

Архитектура не должна запрещать эти функции в будущем, но не должна зависеть от них сейчас.

---

# 6. Основные архитектурные принципы

## 6.1. Modular monolith

Базовая версия должна оставаться **модульным монолитом**, а не набором микросервисов.

Один Python package и одна основная PostgreSQL database, но несколько runtime-процессов:

```text
web
worker
scheduler
```

Это даёт изоляцию фоновых задач без распределённой архитектурной сложности.

## 6.2. Private by default

Созданный capture **никогда не становится публичным автоматически**.

```text
Capture completed
      │
      ▼
   PRIVATE
      │
      ▼
Editorial review
      │
      ├── remain private
      │
      └── publish
```

## 6.3. Immutable evidence, mutable editorial context

Необходимо разделять:

### Immutable

- URL capture;
- timestamps;
- HTTP metadata;
- browser/capture provenance;
- artifacts;
- hashes;
- manifest.

### Mutable

- title;
- note;
- tags;
- collections;
- review state;
- publication status.

Редакторская правка не должна изменять forensic core capture.

## 6.4. Safe rendering

Никогда не исполнять архивированный MHTML/HTML в public viewer.

Показывать:

- screenshot;
- текстовые metadata;
- hashes;
- download links.

MHTML/WARC должны скачиваться как attachments.

## 6.5. Durable state

Все критические состояния jobs хранятся в PostgreSQL. `LISTEN/NOTIFY` не должен быть единственным механизмом очереди.

## 6.6. Self-hosting first

One newsroom → one deployment является предпочтительной моделью 1.0.

---

# 7. Высокоуровневая архитектура

```text
                              INTERNET
                                  │
                                  ▼
                           ┌─────────────┐
                           │    Nginx    │
                           │ TLS / proxy │
                           └──────┬──────┘
                                  │
                                  ▼
                    ┌────────────────────────┐
                    │       FastAPI          │
                    │                        │
                    │ SSR pages + REST API   │
                    │ Auth / RBAC            │
                    │ SSE endpoints          │
                    └───────────┬────────────┘
                                │
                   ┌────────────▼────────────┐
                   │      PostgreSQL         │
                   │                         │
                   │ Users / Sources         │
                   │ Captures / Artifacts    │
                   │ Jobs / Batches          │
                   │ Collections / Tags      │
                   │ Publications            │
                   │ Audit                   │
                   └────────────┬────────────┘
                                │
              ┌─────────────────┼────────────────┐
              │                 │                │
              ▼                 ▼                ▼
       ┌─────────────┐   ┌─────────────┐  ┌─────────────┐
       │ Capture     │   │ Scheduler   │  │ Export      │
       │ worker      │   │ / monitor   │  │ worker      │
       └──────┬──────┘   └─────────────┘  └─────────────┘
              │
              ▼
       ┌─────────────┐
       │   Pravda    │
       │ Playwright  │
       └──────┬──────┘
              │
              ▼
         External Web

                 Artifacts
                    │
                    ▼
             ┌──────────────┐
             │ Filesystem   │
             │ Evidence     │
             │ Storage      │
             └──────────────┘
```

---

# 8. Компоненты

## 8.1. Nginx

Ответственность:

- TLS termination;
- HTTP → HTTPS redirect;
- proxy к FastAPI;
- ограничение размера uploads;
- security headers;
- отдельные cache policies;
- безопасная раздача разрешённых static assets.

Не должен напрямую отдавать evidence directories.

## 8.2. FastAPI application

Ответственность:

- server-side pages;
- REST API;
- authentication;
- sessions;
- permissions;
- CRUD editorial metadata;
- создание jobs;
- public evidence pages;
- SSE streams;
- audit event recording.

FastAPI не должен сам выполнять тяжёлые browser captures в request process.

## 8.3. PostgreSQL

Хранит:

- пользователей;
- editorial state;
- capture metadata;
- artifact metadata;
- durable jobs;
- batches;
- audit;
- publication state;
- monitoring state.

Не хранит бинарные MHTML/WARC/PNG как primary storage.

## 8.4. Capture worker

Получает job, вызывает capture engine, формирует evidence и сохраняет результат.

## 8.5. Scheduler / monitor

Отвечает за:

- URL probes;
- retry recovery;
- stale-job detection;
- scheduled maintenance;
- периодические integrity checks при необходимости.

## 8.6. Pravda adapter

Pravda должен быть инкапсулирован через внутренний интерфейс capture engine.

```python
class CaptureEngine:
    async def capture(self, request: CaptureRequest) -> CaptureResult:
        ...
```

Это позволит в будущем заменить или дополнить Pravda без изменения domain model.

## 8.7. Artifact Store

Для 1.0 реализация — local filesystem volume.

Внутренний интерфейс:

```python
class ArtifactStore:
    async def put(...): ...
    async def open(...): ...
    async def exists(...): ...
```

S3-compatible backend может быть добавлен позже.

---

# 9. Доменная модель

## 9.1. Source

Логический веб-источник.

```text
Source
------
id
canonical_url
domain
source_type
created_at
```

Один Source может иметь несколько captures.

```text
Source
 ├── Capture 1
 ├── Capture 2
 └── Capture 3
```

## 9.2. Capture

Зафиксированное состояние Source в конкретный момент.

```text
Capture
-------
id
source_id
requested_by
requested_at
started_at
captured_at
finished_at
status
engine
engine_version
browser
browser_version
http_status
final_url
capture_condition
condition_met
error_code
error_message
manifest_sha256
```

Capture после успешного завершения рассматривается как immutable forensic record.

## 9.3. Artifact

```text
Artifact
--------
id
capture_id
type
storage_backend
storage_key
mime_type
size_bytes
sha256
created_at
```

Типы для v1.0:

- screenshot;
- mhtml;
- warc;
- metadata;
- manifest;
- receipt_html;
- receipt_pdf.

## 9.4. Editorial Metadata

Отдельная сущность или набор связанных таблиц.

```text
CaptureEditorial
----------------
capture_id
title
note
review_state
updated_by
updated_at
```

## 9.5. Collection

Группа evidence по расследованию/проекту.

Связь capture ↔ collection должна быть many-to-many.

## 9.6. Tag

Нормализованный тег.

Следует использовать canonical name/slug и уникальный индекс.

## 9.7. Publication

Публичность — не поле capture, а отдельная сущность.

```text
Publication
-----------
id
capture_id
public_slug
status
published_at
published_by
revoked_at
revoked_by
```

Состояния:

```text
draft
published
revoked
```

## 9.8. Job

```text
Job
---
id
type
entity_id
status
priority
attempt_count
max_attempts
available_at
worker_id
heartbeat_at
created_at
started_at
finished_at
last_error
```

## 9.9. Batch

Объединяет набор jobs после CSV import.

## 9.10. Audit Event

```text
AuditEvent
----------
id
timestamp
actor_type
actor_id
action
entity_type
entity_id
request_id
ip_address
user_agent
data_json
```

Audit events нельзя удалять через UI.

---

# 10. Основные связи данных

```text
User
 │
 ├──────── requests ────────┐
 │                           ▼
 │                        Capture
 │                           │
 │                           ├──────── Artifact
 │                           │
 │                           ├──────── Editorial Metadata
 │                           │
 │                           ├──────── Collection (*)
 │                           │
 │                           ├──────── Tag (*)
 │                           │
 │                           └──────── Publication (0..n)
 │
 └──────── AuditEvent

Source
  │
  └──────── Capture (*)

Batch
  │
  └──────── Job (*)
```

---

# 11. Capture workflow

## 11.1. Single URL

```text
Editor submits URL
        │
        ▼
Normalize URL
        │
        ▼
Security validation
        │
        ▼
Create/reuse Source
        │
        ▼
Create Capture
        │
        ▼
Create durable Job
        │
        ▼
Notify worker
        │
        ▼
Worker claims Job
        │
        ▼
Pravda / Playwright capture
        │
        ▼
Persist raw artifacts
        │
        ▼
Generate WARC / metadata
        │
        ▼
Compute SHA-256
        │
        ▼
Generate manifest
        │
        ▼
Persist artifact records
        │
        ▼
Capture = DONE
        │
        ▼
Editorial review
```

## 11.2. Job state machine

```text
created
   │
   ▼
queued
   │
   ▼
claimed
   │
   ▼
capturing
   │
   ▼
processing
   │
   ▼
hashing
   │
   ▼
persisting
   │
   ├────────────► failed
   │                 │
   │                 ▼
   │             retry_wait
   │                 │
   └─────────────────┘
   │
   ▼
done
```

Final states:

- `done`;
- `failed`;
- `cancelled`.

## 11.3. Heartbeat и orphan recovery

Worker обновляет `heartbeat_at`.

Scheduler ищет зависшие jobs:

```text
status in (claimed, capturing, processing)
AND heartbeat_at older than threshold
```

После проверки job возвращается в retry или переводится в failed.

---

# 12. Durable queue на PostgreSQL

README предлагает PostgreSQL `LISTEN/NOTIFY`. Для production следует использовать двухуровневую схему:

```text
Jobs table = источник истины
LISTEN/NOTIFY = быстрый wake-up signal
```

Получение job:

```sql
SELECT *
FROM jobs
WHERE status = 'queued'
  AND available_at <= now()
ORDER BY priority DESC, created_at
FOR UPDATE SKIP LOCKED
LIMIT 1;
```

Преимущества:

- notification можно потерять без потери job;
- restart worker не ломает очередь;
- несколько workers безопасно конкурируют;
- легко реализовать retry;
- не нужен Redis/RabbitMQ для базовой нагрузки.

---

# 13. Batch import

CSV import до 500 URL должен быть двухэтапным.

```text
Upload CSV
   │
   ▼
Parse
   │
   ▼
Preview
   │
   ▼
Validate
   │
   ▼
Confirm
   │
   ▼
Create Batch + Jobs
```

Preview должен показывать:

- valid URL;
- malformed URL;
- duplicate;
- unsupported scheme;
- blocked/private target;
- parsed tags/collection.

Импорт 500 URL **не означает 500 одновременных Chromium sessions**.

Concurrency должен задаваться конфигурацией.

---

# 14. Evidence artifacts

## 14.1. Screenshot PNG

Назначение:

- визуальная проверка человеком;
- безопасный public preview;
- быстрый редакционный просмотр.

## 14.2. MHTML

Назначение:

- browser-oriented page representation;
- сохранение DOM/resources в удобном portable browser формате.

Не должен исполняться inline на public site.

## 14.3. WARC/WARC.GZ

Назначение:

- устойчивое архивное представление;
- interoperability с web-archiving ecosystem;
- долгосрочное preservation.

WARC становится обязательной production-задачей согласно pitch deck.

## 14.4. Metadata JSON

Должен включать:

- source URL;
- final URL;
- timestamps;
- HTTP status;
- headers;
- redirect chain;
- capture condition;
- engine version;
- browser version;
- viewport;
- locale/timezone при наличии;
- ошибки/предупреждения.

## 14.5. Manifest

Центральный индекс evidence package.

Пример:

```json
{
  "schema": "provereno-evidence/1",
  "capture_id": "01K...",
  "source_url": "https://example.org/article",
  "captured_at": "2027-03-17T18:43:11Z",
  "engine": {
    "name": "pravda",
    "version": "x.y.z"
  },
  "artifacts": [
    {
      "path": "screenshot.png",
      "sha256": "..."
    },
    {
      "path": "page.mhtml",
      "sha256": "..."
    },
    {
      "path": "archive.warc.gz",
      "sha256": "..."
    }
  ]
}
```

Для 1.0 достаточно canonical manifest + SHA-256. Цифровая подпись может быть добавлена позже.

---

# 15. Artifact storage

Рекомендуемая структура:

```text
data/
└── captures/
    └── <capture-id>/
        ├── evidence/
        │   ├── screenshot.png
        │   ├── page.mhtml
        │   └── archive.warc.gz
        ├── metadata/
        │   ├── capture.json
        │   └── http.json
        └── integrity/
            ├── manifest.json
            └── SHA256SUMS
```

В БД хранится `storage_key`, а не абсолютный host path.

---

# 16. Forensic export

Экспортируемый пакет:

```text
evidence-<id>.zip
├── README.txt
├── receipt.html
├── receipt.pdf
├── evidence/
│   ├── screenshot.png
│   ├── page.mhtml
│   └── archive.warc.gz
├── metadata/
│   ├── capture.json
│   └── http.json
├── manifest.json
└── SHA256SUMS
```

Проверка:

```bash
sha256sum -c SHA256SUMS
```

Receipt должен объяснять человеку:

- какой URL был сохранён;
- когда;
- кем/какой системой;
- какие артефакты входят в пакет;
- как проверить контрольные суммы;
- какова текущая доступность оригинала на момент генерации receipt.

---

# 17. Public Evidence Viewer

Public viewer — отдельный read-only presentation layer.

## Показывает

- source URL;
- captured at;
- publisher/organisation;
- screenshot;
- hash/manifest information;
- current origin state;
- разрешённые downloads;
- идентификатор evidence.

## Не делает

- не исполняет MHTML;
- не встраивает сохранённый HTML в iframe;
- не показывает private notes;
- не раскрывает внутренние usernames без явного решения продукта;
- не открывает admin API.

## HTTP hardening

Для MHTML/WARC:

```http
Content-Disposition: attachment
X-Content-Type-Options: nosniff
```

Для public viewer требуется жёсткий CSP.

---

# 18. URL monitoring

Monitoring должен рассматриваться как вспомогательная функция, а не как основной archiver.

Базовые состояния:

```text
online
redirected
deleted
blocked
unreachable
unknown
```

Порядок проверки:

```text
HEAD
 │
 ├── usable response → store status
 │
 └── unsupported/ambiguous
          │
          ▼
     bounded GET probe
```

Для 1.0 достаточно availability/status monitoring. Надёжный semantic change detection можно отложить.

---

# 19. Search and filtering

Фильтры:

- URL/domain;
- collection;
- tag;
- author;
- capture date;
- capture status;
- review state;
- publication state;
- origin state.

Для ожидаемого масштаба достаточно PostgreSQL:

- B-tree indices;
- GIN;
- `pg_trgm`;
- `tsvector` при необходимости.

Elasticsearch для 1.0 не требуется.

---

# 20. Authentication and RBAC

## 20.1. GitHub OAuth

README задаёт:

- allowed organisations;
- allowed logins.

ENV должен определять admission policy, а пользователь должен существовать в БД.

```text
User
----
id
github_id
github_login
display_name
avatar_url
role
enabled
last_login_at
```

## 20.2. Роли v1.0

Чтобы не переусложнять MVP:

### admin

- users/settings;
- all captures;
- publish/unpublish;
- delete policies;
- audit;
- system operations.

### editor

- create capture;
- collections/tags;
- notes;
- review;
- publish, если текущая продуктовая политика это допускает.

Если пилоты покажут потребность в separation-of-duties, позже можно добавить `reviewer`.

---

# 21. Audit log

Audit должен быть append-only на уровне приложения.

Минимальные events:

```text
user.login
user.logout
capture.requested
capture.completed
capture.failed
capture.exported
collection.created
tag.added
tag.removed
publication.created
publication.revoked
settings.changed
backup.created
restore.performed
```

Audit UI доступен admin.

Опционально в будущей версии можно добавить hash chaining audit events.

---

# 22. Security model

Это один из критических разделов продукта, потому что система намеренно открывает недоверенные URL.

## 22.1. SSRF

Запрещать access к:

```text
127.0.0.0/8
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
169.254.0.0/16
::1
fc00::/7
fe80::/10
```

Проверка должна выполняться:

- перед capture;
- после DNS resolution;
- после каждого redirect.

## 22.2. Schemes

По умолчанию разрешать только:

```text
http
https
```

Запрещать:

```text
file:
ftp:
data:
javascript:
chrome:
```

## 22.3. Browser isolation

Pravda/Playwright container:

- non-root;
- no Docker socket;
- no host network;
- no access к database network, если возможно;
- CPU/memory/PID limits;
- read-only filesystem где возможно;
- выделенный writable volume/temp.

## 22.4. Application security

- CSRF protection для state-changing SSR forms;
- secure sessions;
- HTTPS;
- permission checks на backend;
- path traversal protection;
- filename normalization;
- CSP;
- safe content disposition;
- dependency scanning.

## 22.5. Sensitive evidence

Private capture никогда не должен становиться доступным по знанию UUID без авторизации.

Public links должны ссылаться только на `Publication` records.

---

# 23. Deployment

Production deployment:

```text
server/
├── docker-compose.yml
├── .env
├── data/
├── backups/
└── nginx/
```

Services:

```text
nginx
app
worker
scheduler
postgres
pravda
```

`worker` и `scheduler` могут использовать тот же Docker image, что и application, но запускаться с разными commands.

---

# 24. Backup and restore

Backup — P0-функция production readiness.

Он должен включать:

- PostgreSQL dump;
- artifacts;
- system metadata;
- checksums;
- version information.

Пример:

```text
backup-2027-03-17/
├── database.dump
├── artifacts.tar.zst
├── backup-manifest.json
└── SHA256SUMS
```

Ключевой критерий качества:

> **Наличие backup script недостаточно. Restore должен регулярно проверяться.**

Integration scenario:

```text
create capture
    ↓
backup
    ↓
restore into clean environment
    ↓
verify DB records
    ↓
verify artifact SHA-256
```

---

# 25. Upgrade model

Нужны:

- semantic versioning;
- Alembic migrations;
- pre-upgrade backup;
- migration validation;
- release notes;
- documented rollback limitations.

Deployment support должен уметь определить:

```text
Application version
Database schema version
Pravda version
Storage backend
```

---

# 26. Health and observability

Endpoints:

```text
/health/live
/health/ready
```

`ready` проверяет минимум:

- database;
- artifact store;
- Pravda;
- worker heartbeat.

Structured logs должны включать correlation fields:

```text
request_id
user_id
job_id
capture_id
batch_id
```

Пример:

```json
{
  "level": "INFO",
  "event": "capture.completed",
  "capture_id": "01K...",
  "duration_ms": 8241
}
```

---

# 27. UI architecture

Для базовой версии предпочтительно сохранить server-side rendering.

Рекомендуемый стек:

```text
FastAPI
Jinja2
HTML/CSS design system из prototype
небольшой JavaScript
SSE
опционально HTMX/Alpine.js
```

React/Next/Vue не требуются для текущего набора задач.

Структура templates:

```text
templates/
├── base.html
├── dashboard.html
├── capture.html
├── jobs.html
├── snapshots.html
├── snapshot_detail.html
├── collections.html
├── settings.html
├── public/
│   └── evidence.html
└── components/
    ├── badge.html
    ├── job_row.html
    ├── snapshot_row.html
    └── pagination.html
```

Текущий HTML mockup следует использовать как design/UI baseline, а не выбрасывать.

---

# 28. API outline

Внутренний/public API должен иметь version prefix.

```text
/api/v1/
```

Пример endpoints:

```text
POST   /api/v1/captures
GET    /api/v1/captures/{id}
GET    /api/v1/captures

GET    /api/v1/jobs
GET    /api/v1/jobs/{id}
GET    /api/v1/jobs/{id}/events

POST   /api/v1/batches
GET    /api/v1/batches/{id}

POST   /api/v1/collections
PATCH  /api/v1/collections/{id}

POST   /api/v1/captures/{id}/tags
DELETE /api/v1/captures/{id}/tags/{tag}

POST   /api/v1/captures/{id}/publish
POST   /api/v1/captures/{id}/unpublish

GET    /api/v1/captures/{id}/export
```

Server-rendered pages могут вызывать application services напрямую, не обязательно через loopback HTTP API.

---

# 29. Предлагаемая структура репозитория

```text
provereno/
├── pyproject.toml
├── alembic.ini
├── docker-compose.yml
├── .env.example
│
├── src/provereno/
│   ├── main.py
│   ├── config.py
│   │
│   ├── domain/
│   │   ├── sources.py
│   │   ├── captures.py
│   │   ├── artifacts.py
│   │   ├── collections.py
│   │   ├── publications.py
│   │   └── audit.py
│   │
│   ├── db/
│   │   ├── models.py
│   │   ├── session.py
│   │   └── repositories/
│   │
│   ├── capture/
│   │   ├── base.py
│   │   ├── pravda.py
│   │   ├── pipeline.py
│   │   └── warc.py
│   │
│   ├── storage/
│   │   ├── base.py
│   │   └── filesystem.py
│   │
│   ├── jobs/
│   │   ├── queue.py
│   │   ├── worker.py
│   │   └── events.py
│   │
│   ├── forensic/
│   │   ├── manifest.py
│   │   ├── receipt.py
│   │   └── export.py
│   │
│   ├── monitoring/
│   │   └── urls.py
│   │
│   ├── security/
│   │   ├── auth.py
│   │   ├── permissions.py
│   │   ├── sessions.py
│   │   └── urls.py
│   │
│   ├── api/
│   ├── pages/
│   ├── templates/
│   └── static/
│
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── security/
│
├── deploy/
│   ├── nginx/
│   └── docker/
│
└── scripts/
    ├── install.sh
    ├── upgrade.sh
    ├── backup.sh
    ├── restore.sh
    └── healthcheck.sh
```

---

# 30. Testing strategy

## Unit

- URL normalization;
- SSRF checks;
- permissions;
- hash generation;
- manifest generation;
- state transitions;
- retry policy.

## Integration

- PostgreSQL repositories;
- queue locking;
- Pravda adapter;
- artifact storage;
- WARC generation;
- export package;
- audit persistence.

## E2E

```text
login
→ create capture
→ wait for job
→ inspect evidence
→ add tags
→ publish
→ open public page
→ download package
→ verify hashes
```

## Security tests

- localhost/private-IP targets;
- DNS rebinding/redirect to private network;
- path traversal;
- unauthorised evidence access;
- dangerous MIME types;
- malformed CSV;
- session/RBAC bypass;
- artifact filename injection.

---

# 31. CI/CD

Pipeline:

```text
commit / PR
     │
     ▼
format/lint
     │
     ▼
type checks
     │
     ▼
unit tests
     │
     ▼
integration tests
     │
     ▼
Docker build
     │
     ▼
dependency/container scan
     │
     ▼
E2E
     │
     ▼
release candidate
```

Перед v1.0 должен существовать migration test с prototype schema/data.

---

# 32. Этапы реализации до базовой версии

## Этап 0. Audit существующего prototype

**Цель:** понять, что сохраняется, что требует refactor.

### Задачи

- inventory текущих modules;
- DB schema review;
- auth review;
- audit log review;
- Pravda integration review;
- filesystem layout review;
- background task review;
- threat model;
- dependency audit;
- зафиксировать current user flows.

### Результат

- Architecture Decision Record;
- migration plan;
- список prototype shortcuts;
- baseline test fixtures.

---

## Этап 1. Domain/data model

### Задачи

- ввести Source;
- нормализовать Capture;
- ввести Artifact;
- отделить Editorial Metadata;
- many-to-many Collections;
- Tags;
- Publication;
- Job/Batch;
- AuditEvent;
- Alembic migrations.

### Acceptance criteria

- existing prototype data мигрируется;
- evidence metadata не зависит от UI metadata;
- capture имеет стабильный ID;
- publication отделена от capture.

---

## Этап 2. Durable jobs and workers

### Задачи

- jobs table;
- claim через `SKIP LOCKED`;
- retry policy;
- worker heartbeat;
- orphan recovery;
- LISTEN/NOTIFY wakeup;
- SSE job events;
- batch states;
- concurrency config.

### Acceptance criteria

- restart worker не теряет jobs;
- failed capture можно безопасно retry;
- два worker не выполняют одну job;
- UI видит progress.

---

## Этап 3. Evidence pipeline

### Задачи

- Pravda adapter;
- screenshot persistence;
- MHTML persistence;
- metadata normalization;
- WARC export/generation;
- SHA-256;
- manifest;
- filesystem storage abstraction;
- integrity verification command/service.

### Acceptance criteria

- каждый успешный capture создаёт полный минимальный evidence set;
- SHA-256 воспроизводим;
- manifest однозначно ссылается на artifacts;
- WARC включён в export.

---

## Этап 4. Editorial workspace

### Задачи

- Dashboard;
- capture form;
- jobs queue;
- snapshot list;
- snapshot detail;
- collections;
- tags;
- notes;
- review state;
- filters/search;
- batch import preview.

### Acceptance criteria

- основной workflow выполняется без CLI;
- UI соответствует mockup;
- все state-changing operations permission-checked.

---

## Этап 5. Publication and forensic export

### Задачи

- Publication model;
- publish/unpublish workflow;
- public viewer;
- OpenGraph metadata;
- safe downloads;
- receipt HTML;
- receipt PDF;
- ZIP generation;
- SHA256SUMS;
- public/private access tests.

### Acceptance criteria

- private capture невозможно открыть публично;
- public viewer не исполняет archived active content;
- exported package проходит hash verification.

---

## Этап 6. Authentication, RBAC, audit

### Задачи

- GitHub OAuth hardening;
- allowed org/logins;
- user DB;
- admin/editor permissions;
- session security;
- complete audit coverage;
- audit CSV export.

### Acceptance criteria

- unauthorized user не может войти;
- editor/admin boundaries работают;
- важные actions появляются в audit;
- audit не удаляется через UI.

---

## Этап 7. Security hardening

### Задачи

- SSRF defenses;
- redirect validation;
- DNS/IP checks;
- browser container isolation;
- resource limits;
- CSP/security headers;
- upload validation;
- safe Content-Disposition;
- secret handling;
- dependency/container scan.

### Acceptance criteria

- private/internal targets блокируются;
- archived HTML не может выполнить JS в public viewer;
- capture container не получает доступ к host-sensitive resources.

---

## Этап 8. Operations

### Задачи

- production Docker Compose;
- Nginx config;
- TLS documentation;
- health endpoints;
- structured logs;
- backup script;
- restore script;
- restore test;
- upgrade script;
- migration checks.

### Acceptance criteria

- чистая установка документирована;
- backup восстанавливается в новой среде;
- upgrade не требует ручного редактирования БД.

---

## Этап 9. Automated quality

### Задачи

- unit suite;
- integration suite;
- E2E suite;
- security regression suite;
- CI;
- release builds;
- test coverage critical paths.

### Acceptance criteria

- PR не может пройти при broken core workflow;
- capture/export/public access проверяются автоматически.

---

## Этап 10. Release Candidate

### Задачи

- external/internal security review;
- documentation;
- admin runbook;
- disaster recovery runbook;
- onboarding guide;
- known limitations;
- release checklist.

### Результат

`v1.0.0-rc1`.

---

## Этап 11. Pilots

3–5 редакций.

Измерять:

- capture success rate;
- median/p95 capture duration;
- failed jobs;
- number of captures;
- batches;
- public evidence links;
- exported packages;
- later deleted/changed origins;
- deployment time;
- backup/restore failures;
- support incidents;
- usability issues.

---

## Этап 12. Baseline v1.0

После пилотов:

- исправить P0/P1 defects;
- заморозить schema v1;
- финализировать upgrade process;
- финализировать docs;
- выпустить stable Docker images;
- опубликовать v1.0.

---

# 33. Критерии готовности базовой версии 1.0

Версия не должна считаться production-ready, пока не выполнены все условия:

### Capture

- jobs durable;
- retries predictable;
- browser isolation работает;
- batch import не перегружает систему.

### Evidence

- PNG/MHTML/WARC/metadata;
- SHA-256;
- manifest;
- reproducible verification.

### Privacy

- private by default;
- no public access without Publication;
- correct RBAC.

### Public viewer

- safe rendering;
- no active archive execution;
- hashes/timestamp visible.

### Operations

- install documented;
- backup works;
- restore tested;
- upgrade documented;
- migrations automated.

### Security

- SSRF controls;
- secure sessions;
- security headers;
- browser resource limits;
- dependency review.

### Quality

- automated tests;
- CI;
- E2E core flow;
- security regression suite.

---

# 34. Архитектурные риски

## 34.1. Capture engine reliability

Современные сайты могут требовать login, anti-bot bypass или platform-specific treatment.

**Подход:** не обещать универсальный capture; фиксировать ошибки и engine limitations; проектировать adapter boundary.

## 34.2. WARC generation complexity

MHTML → WARC не обязательно эквивалентно полноценному network capture.

**Подход:** отдельно определить, какой именно WARC создаёт v1.0 и какие данные он гарантирует.

## 34.3. Disk growth

PNG + MHTML + WARC могут быстро занимать storage.

**Подход:** metrics, configurable retention, disk warnings, documented capacity planning.

## 34.4. Browser attack surface

Capture engine открывает hostile content.

**Подход:** isolation, SSRF checks, resource limits, timely Chromium updates.

## 34.5. False forensic claims

SHA-256 доказывает неизменность файла после вычисления hash, но сам по себе не доказывает юридически время или автора capture.

**Подход:** аккуратная терминология. Для более сильных гарантий в будущем — signatures/timestamping.

## 34.6. Scope creep

Есть риск превратить продукт в crawler + CMS + OSINT platform + AI fact-checker.

**Подход:** держать ядро продукта узким:

```text
capture
→ preserve
→ organize
→ review
→ publish/export
```

---

# 35. Решения, которые желательно зафиксировать ADR-документами

До активной реализации стоит создать Architecture Decision Records:

1. **ADR-001:** Modular monolith vs microservices.
2. **ADR-002:** PostgreSQL durable queue.
3. **ADR-003:** Capture engine adapter boundary.
4. **ADR-004:** Evidence artifact set: PNG/MHTML/WARC/JSON.
5. **ADR-005:** Immutable Capture vs mutable Editorial Metadata.
6. **ADR-006:** Publication as separate entity.
7. **ADR-007:** Filesystem artifact storage for v1.0.
8. **ADR-008:** Private-by-default policy.
9. **ADR-009:** WARC implementation strategy.
10. **ADR-010:** Backup/restore format.

---

# 36. Будущие расширения после v1.0

После стабилизации core можно рассмотреть:

- S3-compatible artifact storage;
- browser extension;
- command-line capture client;
- cryptographic manifest signatures;
- trusted timestamping;
- semantic content diff;
- scheduled recapture;
- notifications;
- platform-specific capture adapters;
- evidence API tokens;
- organisation-specific SSO;
- encryption policies;
- optional managed multi-instance control plane;
- external archival replication.

Эти функции не должны задерживать basic production release.

---

# 37. Итоговая формула продукта

Provereno Evidence Workspace следует реализовывать не как «GUI для Pravda», а как **редакционный evidence lifecycle system**.

```text
        FIND
         │
         ▼
      CAPTURE
         │
         ▼
      PRESERVE
         │
         ▼
       VERIFY
         │
         ▼
      ORGANIZE
         │
         ▼
       REVIEW
         │
         ├──────────────► KEEP PRIVATE
         │
         ▼
      PUBLISH
         │
         ▼
       EXPORT
         │
         ▼
      PRESERVE
      LONG-TERM
```

`Pravda/Playwright` является capture engine.  
`PostgreSQL` хранит состояние workflow.  
`Artifact Store` хранит evidence.  
`FastAPI UI` предоставляет редакционный интерфейс.  
`Audit`, `hashes`, `manifest`, `backup` и `WARC` обеспечивают проверяемость и устойчивость.

Главная задача до v1.0 — **не добавить максимум возможностей, а добиться того, чтобы существующий прототип можно было безопасно установить в реальной редакции, доверить ему важные доказательства, восстановить после сбоя и использовать без постоянного участия разработчика.**

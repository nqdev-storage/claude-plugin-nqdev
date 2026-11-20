# Gợi ý tìm entry point theo framework

Xác định stack qua file dấu hiệu ở root (`*.csproj`, `package.json`, `pom.xml`, `go.mod`, `composer.json`, `pyproject.toml`...), rồi tìm điểm bắt đầu theo bảng. Đây là gợi ý để bắt đầu tìm, không phải bằng chứng; luôn mở file để xác nhận.

| Stack | Màn hình / API | Job, consumer, sự kiện | Truy cập dữ liệu |
|---|---|---|---|
| ASP.NET MVC / Web API | `Controllers/*Controller.cs`, attribute `[Route]`, `[Http*]`; view `Views/<Controller>/*.cshtml` | `IHostedService`, `BackgroundService`, Hangfire `RecurringJob`, Quartz `IJob`, MassTransit `IConsumer<T>` | `DbContext`, repository, Dapper, stored procedure (`CommandType.StoredProcedure`) |
| ASP.NET Core Minimal API | `app.Map*` trong `Program.cs` | như trên | như trên |
| Node.js (Express, NestJS, Fastify) | `router.get/post`, `app.use`, decorator `@Controller`, `@Get` | `@Cron`, BullMQ `Worker`, `@EventPattern`, `@MessagePattern` | Prisma, TypeORM, Sequelize, Mongoose |
| Next.js / React | `app/**/page.tsx`, `pages/**`, `app/api/**/route.ts`; form `onSubmit` | — | gọi API qua `fetch`/axios, server action |
| Java Spring | `@RestController`, `@RequestMapping`, `@GetMapping` | `@Scheduled`, `@KafkaListener`, `@RabbitListener` | `JpaRepository`, `@Query`, MyBatis mapper |
| PHP Laravel | `routes/web.php`, `routes/api.php` → controller | `app/Console/Kernel.php`, `app/Jobs`, listener | Eloquent model, `DB::` |
| Python (Django, FastAPI, Flask) | `urls.py`, `@app.get`, `@router.post`, `@app.route` | Celery `@shared_task`, APScheduler | Django ORM, SQLAlchemy |
| Go | `http.HandleFunc`, `gin`/`echo`/`chi` router | goroutine worker, consumer Kafka/NATS | `database/sql`, GORM, sqlc |

Khi người dùng chỉ đưa tên tính năng: tìm theo từ khoá nghiệp vụ trong tên route, tên màn hình, chuỗi hiển thị và resource đa ngôn ngữ (`*.resx`, `i18n/*.json`), rồi lần ngược về controller hoặc handler.

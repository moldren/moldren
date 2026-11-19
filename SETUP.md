# Профиль-сайт: как загрузить

## Что лежит в папке

| Файл | Зачем |
|---|---|
| `README.md` | сам профиль: баннер, статистика, змейка |
| `assets/banner.png` | широкая шапка 1600×640, она и стоит вверху README |
| `assets/waifu-round.png` | круглая аватарка под профиль GitHub |
| `assets/waifu.jpg` | оригинал картинки |
| `assets/fonts/` | шрифты баннера (Unbounded, Manrope) + лицензии OFL |
| `scripts/make-banner.py` | генератор баннера, если захочешь поменять текст |
| `.github/workflows/snake.yml` | змейка по контрибуциям |

## Сначала главное

У GitHub **нет настройки «обложка профиля»**. Баннер показывается только потому, что лежит в README-репозитории,
имя которого совпадает с ником: `moldren`. Аватар ставится отдельно, в настройках.

## Загрузка через сайт (без терминала)

1. Открой [github.com/new](https://github.com/new)
2. **Repository name**: `moldren` (ровно так, без пробелов)
3. **Public** → **Create repository**
4. На странице пустого репозитория: **Add file → Upload files**
5. Перетащи в окно **содержимое** папки `github-profile`: `README.md`, папку `assets`, папку `.github`
   - Важно: `README.md` должен оказаться в корне репозитория, а не внутри вложенной папки `github-profile`
   - Finder по умолчанию прячет папки на точку: нажми `Cmd + Shift + .`, чтобы увидеть `.github`
6. Внизу: **Commit changes**
7. Открой `github.com/moldren` — баннер уже на месте

Если `.github` не хочешь тащить вручную, залей пока без него: профиль будет работать, змейка просто не появится.

## Загрузка через терминал

```bash
cd github-profile
git init -b main
git add .
git commit -m "feat: профиль-сайт 🌸"
git remote add origin https://github.com/moldren/moldren.git
git push -u origin main
```

Репозиторий `moldren/moldren` должен быть уже создан на GitHub и пустой.

## Включи змейку

1. **Settings → Actions → General → Workflow permissions → Read and write permissions → Save**
2. Вкладка **Actions** → слева **Generate snake** → **Run workflow**
3. Через минуту появится ветка `output` — змейка начнёт рисоваться в README
4. Дальше обновляется сама каждые 12 часов, ничего делать не нужно

## Как поставить круглую аватарку

**Settings → Public profile → Avatar → Upload** → выбери `assets/waifu-round.png`.
Она уже круглая и с розовым кольцом, GitHub просто впишет её в свой круг.

## Как поменять баннер

- **Быстро**: замени `assets/banner.png` на свой файл с тем же именем — README подхватит автоматически
- **По-честному**: отредактируй `scripts/make-banner.py` (тексты, пилюли, цвета) и пересобери:

```bash
python3 -m pip install pillow
python3 scripts/make-banner.py
```

В скрипте легко меняются: имя, подпись, список технологий, фраза внизу, цвета `PINK / VIOLET / INDIGO`.

## Если что-то не отобразилось

- **Баннер не видно** — проверь, что файл лежит ровно в `assets/banner.png` (регистр букв важен) и что в README путь `./assets/banner.png`
- **Карточки статистики пустые** — это нормально для `github-readme-stats`: первый запрос «холодный». Открой ссылку карточки в браузере, подожди 10–20 секунд
- **Змейка не рисуется** — проверь, что workflow отработал и появилась ветка `output`
- **Трофеи** — блок в README закомментирован: сервис иногда отдаёт ошибку 402. Раскомментируй, когда оживёт

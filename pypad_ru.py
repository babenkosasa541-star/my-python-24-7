import os
from flask import Flask, render_template_string, redirect, url_for, request

app = Flask(__name__)

# --- БАЗА ДАННЫХ (Добавлено больше фильмов для теста фильтров) ---
media_data = {
    "ivan-vasilyevich-menyaet-professiyu": {
        "title": "Иван Васильевич меняет профессию",
        "full_title": "Иван Васильевич меняет профессию (1973)",
        "category": "Фильмы",
        "rating": "8.8",
        "year": "1973",
        "director": "Леонид Гайдай",
        "country": "СССР",
        "genre": "Комедия",
        "poster_url": "https://ru-images-s.kinorium.com/movie/1080/65324.jpg?1613476278",
        "description": "Советская комедия о машине времени.",
        "video_stream_url": "http://localhost:8090/stream/ivan_vasilyevich.mkv"
    },
    "brilliantovaya-ruka": {
        "title": "Бриллиантовая рука",
        "full_title": "Бриллиантовая рука (1968)",
        "category": "Фильмы",
        "rating": "8.5",
        "year": "1968",
        "director": "Леонид Гайдай",
        "country": "СССР",
        "genre": "Комедия",
        "poster_url": "https://ru-images-s.kinorium.com/movie/1080/65133.jpg",
        "description": "История о контрабандистах и примерном семьянине.",
        "video_stream_url": "#"
    },
    "interstellar": {
        "title": "Интерстеллар",
        "full_title": "Интерстеллар (2014)",
        "category": "Фильмы",
        "rating": "8.6",
        "year": "2014",
        "director": "Кристофер Нолан",
        "country": "США",
        "genre": "Фантастика",
        "poster_url": "https://ru-images-s.kinorium.com/movie/1080/681755.jpg",
        "description": "Путешествие через черную дыру.",
        "video_stream_url": "#"
    }
}

# --- ШАБЛОНЫ ---

# Общий CSS для всех страниц
common_style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body { font-family: 'Roboto', sans-serif; margin: 0; background: #0a0a0a; color: #fff; }
    .container { max-width: 1200px; margin: auto; padding: 20px; }
    a { text-decoration: none; color: inherit; }
    
    /* Шапка и поиск */
    .header { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid #222; }
    .search-box { display: flex; gap: 10px; }
    .search-box input, .search-box select { padding: 10px; border-radius: 5px; border: 1px solid #333; background: #1a1a1a; color: white; }
    .btn-search { background: #00adef; border: none; padding: 10px 20px; border-radius: 5px; color: white; cursor: pointer; }

    /* Сетка фильмов */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 25px; margin-top: 30px; }
    .card { background: #1a1a1a; border-radius: 12px; overflow: hidden; transition: 0.3s; border: 1px solid #222; }
    .card:hover { transform: translateY(-5px); border-color: #00adef; }
    .card img { width: 100%; height: 320px; object-fit: cover; }
    .card-info { padding: 15px; }
    .card-title { font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }
    .card-meta { color: #888; font-size: 0.9em; }
</style>
"""

main_template = f"""
<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Медиатека 24</title>{common_style}</head>
<body>
<div class="container">
    <div class="header">
        <h1 style="color: #00adef;">Медиатека 24</h1>
        <form action="/search" method="GET" class="search-box">
            <input type="text" name="q" placeholder="Поиск фильма...">
            <select name="genre">
                <option value="">Все жанры</option>
                <option value="Комедия">Комедия</option>
                <option value="Фантастика">Фантастика</option>
            </select>
            <select name="year">
                <option value="">Все годы</option>
                <option value="1973">1973</option>
                <option value="2014">2014</option>
            </select>
            <button type="submit" class="btn-search">Найти</button>
        </form>
    </div>

    <h2>Категории</h2>
    <div style="display: flex; gap: 20px;">
        <a href="/category/Фильмы" style="padding: 20px; background: #1a1a1a; border-radius: 10px; flex: 1; text-align: center; border: 1px solid #333;">🎬 Фильмы</a>
        <a href="#" style="padding: 20px; background: #1a1a1a; border-radius: 10px; flex: 1; text-align: center; border: 1px solid #333; color: #555;">📺 Сериалы (Пусто)</a>
    </div>

    <h2>Рекомендуем</h2>
    <div class="grid">
        {% for id, item in items.items() %}
        <a href="/media/{{ id }}" class="card">
            <img src="{{ item.poster_url }}">
            <div class="card-info">
                <div class="card-title">{{ item.title }}</div>
                <div class="card-meta">{{ item.year }} • {{ item.country }} • {{ item.genre }}</div>
                <div style="color: #f39c12; margin-top: 5px;">★ {{ item.rating }}</div>
            </div>
        </a>
        {% endfor %}
    </div>
</div>
</body>
</html>
"""

# Плеер остается из предыдущего ответа, но вписывается в общий дизайн
media_template = f"""
<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>{{{{ media.full_title }}}}</title>{common_style}
<link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
<style>:root {{ --plyr-color-main: #00adef; }}</style>
</head>
<body style="background: #000;">
<div class="container">
    <a href="/" style="color: #00adef;">← Назад на главную</a>
    <div style="margin-top: 20px; border-radius: 15px; overflow: hidden;">
        <video id="player" playsinline controls data-poster="{{{{ media.poster_url }}}}">
            <source src="{{{{ media.video_stream_url }}}}" type="video/mp4" />
        </video>
    </div>
    <div style="display: flex; gap: 40px; margin-top: 30px; background: #111; padding: 30px; border-radius: 15px;">
        <img src="{{{{ media.poster_url }}}}" style="width: 200px; border-radius: 10px;">
        <div>
            <h1>{{{{ media.full_title }}}}</h1>
            <p><strong>Страна:</strong> {{{{ media.country }}}}</p>
            <p><strong>Жанр:</strong> {{{{ media.genre }}}}</p>
            <p style="color: #ccc;">{{{{ media.description }}}}</p>
        </div>
    </div>
</div>
<script src="https://cdn.plyr.io/3.7.8/plyr.js"></script>
<script>const player = new Plyr('#player');</script>
</body>
</html>
"""

# --- ЛОГИКА ---

@app.route('/')
def index():
    return render_template_string(main_template, items=media_data)

@app.route('/category/<name>')
def category_page(name):
    filtered = {k: v for k, v in media_data.items() if v['category'] == name}
    return render_template_string(main_template, items=filtered)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    genre = request.args.get('genre', '')
    year = request.args.get('year', '')
    
    results = {}
    for k, v in media_data.items():
        match_q = query in v['title'].lower() or query in v['description'].lower()
        match_genre = genre == '' or v['genre'] == genre
        match_year = year == '' or v['year'] == year
        
        if match_q and match_genre and match_year:
            results[k] = v
            
    return render_template_string(main_template, items=results)

@app.route('/media/<id>')
def media_page(id):
    media = media_data.get(id)
    if not media: return redirect('/')
    return render_template_string(media_template, media=media)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

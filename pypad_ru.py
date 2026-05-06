from flask import Flask, render_template_string, request

app = Flask(__name__)

# ТВОЯ БАЗА ДАННЫХ СО ВСЕМИ РОЛИКАМИ
media_library = [
    {
        "blogger": "Дюшес",
        "title": "ДОБЫВАЕМ 1 ЛИТР ПИТЬЕВОЙ ВОДЫ ИЗ КАКТУСОВ",
        "iframe": '<iframe src="https://vk.com/video_ext.php?oid=-162096641&id=456239470&hash=df6a2a1f04da367d" width="100%" height="400" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>'
    },
    {
        "blogger": "Дюшес",
        "title": "ПРОЙДИ УЗКИЙ ТОННЕЛЬ С КУЧЕЙ КАКТУСОВ С ЗАКРЫТЫМИ ГЛАЗАМИ!",
        "iframe": '<iframe src="https://vk.com/video_ext.php?oid=-162096641&id=456239469&hash=362d640954b83a6b" width="100%" height="400" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>'
    },
    {
        "blogger": "Дюшес",
        "title": "Команда Дюшес VS Повар Мишлен! Кто приготовит лучше?",
        "iframe": '<iframe src="https://vk.com/video_ext.php?oid=-162096641&id=456239616&hash=e8964d47663f7f63" width="100%" height="400" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>'
    },
    {
        "blogger": "Дюшес",
        "title": "ПРОПИТАЛИ ВОЛОСЫ ФИКСИРУЮЩИМ ЛАКОМ, ЧТОБЫ ПРОБИТЬ АРБУЗ!",
        "iframe": '<iframe src="https://vk.com/video_ext.php?oid=-162096641&id=456239468&hash=2909403e4811a7f0" width="100%" height="400" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>'
    },
    {
        "blogger": "Дюшес",
        "title": "Кто Пройдет 50 УЖАСНЫХ БАССЕЙНОВ - ЗАБЕРЕТ iPhone 17 ЧЕЛЛЕНДЖ!",
        "iframe": '<iframe src="https://vk.com/video_ext.php?oid=-213022244&id=456244296&hash=731e843c0047545e" width="100%" height="400" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>'
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 МОЯ МЕДИАТЕКА</title>
    <style>
        :root {
            --bg-color: #0f0f0f;
            --card-bg: #1e1e1e;
            --accent-color: #00d1ff;
            --text-color: #eeeeee;
            --secondary-text: #aaaaaa;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            padding: 30px 0;
        }
        h1 {
            color: var(--accent-color);
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .filter-section {
            background: var(--card-bg);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
            border: 1px solid #333;
        }
        .filter-link {
            display: inline-block;
            padding: 8px 18px;
            margin: 5px;
            background: #333;
            color: var(--accent-color);
            text-decoration: none;
            border-radius: 20px;
            transition: 0.3s;
        }
        .filter-link:hover, .filter-link.active {
            background: var(--accent-color);
            color: #000;
        }
        .card {
            background: var(--card-bg);
            border-radius: 15px;
            margin-bottom: 30px;
            overflow: hidden;
            border: 1px solid #333;
            box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        }
        .card-info { padding: 20px; }
        .blogger-name { color: var(--accent-color); font-weight: bold; font-size: 0.9em; }
        .video-title { margin: 10px 0 0 0; font-size: 1.3em; }
        .video-box { background: #000; line-height: 0; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎬 МОЯ МЕДИАТЕКА</h1>
        </header>

        <div class="filter-section">
            <a href="/" class="filter-link {% if not current_blogger %}active{% endif %}">ВСЕ</a>
            {% for blogger in bloggers %}
            <a href="/?blogger={{ blogger }}" class="filter-link {% if current_blogger == blogger %}active{% endif %}">
                {{ blogger }}
            </a>
            {% endfor %}
        </div>

        {% for item in items %}
        <div class="card">
            <div class="card-info">
                <div class="blogger-name">{{ item.blogger }}</div>
                <h2 class="video-title">{{ item.title }}</h2>
            </div>
            <div class="video-box">
                {{ item.iframe | safe }}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    bloggers = sorted(list(set(item['blogger'] for item in media_library)))
    selected_blogger = request.args.get('blogger')
    
    if selected_blogger:
        filtered_items = [i for i in media_library if i['blogger'] == selected_blogger]
    else:
        filtered_items = media_library

    return render_template_string(
        HTML_TEMPLATE, 
        items=filtered_items, 
        bloggers=bloggers, 
        current_blogger=selected_blogger
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

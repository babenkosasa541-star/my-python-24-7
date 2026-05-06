from flask import Flask, render_template_string

app = Flask(__name__)

# ТВОЯ МЕДИАТЕКА (Сюда просто добавляем новые блоки)
media_library = [
    {
        "author": "Дюшес",
        "title": "ДОБЫВАЕМ 1 ЛИТР ПИТЬЕВОЙ ВОДЫ ИЗ КАКТУСОВ",
        "iframe": '<iframe src="https://vk.com/video_ext.php?oid=-162096641&id=456239470&hash=df6a2a1f04da367d" width="100%" height="400" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>'
    }
]

# Красивый дизайн сайта
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Media Library</title>
    <style>
        body { 
            background-color: #0f0f0f; 
            color: #ffffff; 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
        }
        header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid #333;
            margin-bottom: 40px;
        }
        h1 { font-size: 2.5em; color: #00d1ff; margin: 0; }
        .card { 
            background: #1e1e1e; 
            border-radius: 16px; 
            overflow: hidden; 
            margin-bottom: 40px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid #333;
        }
        .card-content { padding: 20px; }
        .author { 
            color: #aaa; 
            font-size: 0.9em; 
            font-weight: bold; 
            text-transform: uppercase;
        }
        .title { 
            font-size: 1.5em; 
            margin: 10px 0 20px 0; 
            line-height: 1.3;
        }
        .video-container {
            background: #000;
            line-height: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎬 МОЯ МЕДИАТЕКА</h1>
            <p>Личный архив избранного контента</p>
        </header>

        {% for item in library %}
        <div class="card">
            <div class="card-content">
                <div class="author">{{ item.author }}</div>
                <div class="title">{{ item.title }}</div>
            </div>
            <div class="video-container">
                {{ item.iframe | safe }}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, library=media_library)

if __name__ == '__main__':
    # Запуск сервера
    # host='0.0.0.0' позволяет подключаться извне
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# قائمة ديناميكية لتخزين الخدمات (تتحدث فوراً عند استلام بيانات من واتساب)
services_data = [
    {
        "title": "مكتب خدمات إقامات وتثبيت نفوس",
        "category": "معاملات",
        "details": "الموقع: مركز مرسين (شارع أتاتورك).\nالخدمات: حجز مواعيد إقامات، تثبيت عنوان النفوس.",
        "timestamp": "محدث اليوم"
    }
]

html_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة مرسين للخدمات - الدليل الشامل</title>
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #10b981;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-color: #1e293b;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
        }
        header {
            background-color: var(--primary-color);
            color: white;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .container {
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .ad-banner {
            background: #e2e8f0;
            border: 2px dashed #cbd5e1;
            text-align: center;
            padding: 15px;
            margin-bottom: 2rem;
            border-radius: 8px;
            color: #64748b;
            font-size: 14px;
        }
        .controls-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 10px;
        }
        .filter-buttons {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 5px;
            flex: 1;
        }
        .filter-btn {
            background: white;
            border: 1px solid #cbd5e1;
            padding: 8px 14px;
            border-radius: 20px;
            cursor: pointer;
            white-space: nowrap;
            font-size: 14px;
            color: #475569;
        }
        .filter-btn:hover, .filter-btn.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
        .btn-refresh {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
        }
        .job-card {
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
            border-right: 5px solid var(--primary-color);
            white-space: pre-line;
        }
        .job-title {
            font-size: 1.25rem;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        .job-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        .btn-action {
            background-color: var(--secondary-color);
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
            display: inline-block;
        }
        .btn-share {
            background-color: #64748b;
        }
        .job-time {
            font-size: 0.85rem;
            color: #64748b;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <header>
        <h1>منصة مرسين للخدمات</h1>
        <p>البوابة المحدثة تلقائياً من مجموعات واتساب</p>
    </header>

    <div class="container">
        <!-- 💰 مساحة إعلانية علوية -->
        <div class="ad-banner">
            <span>[مساحة إعلانية - AdBanner Header]</span>
        </div>

        <!-- شريط التحكم والتصفية -->
        <div class="controls-bar">
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterServices('all', this)">الكل</button>
                <button class="filter-btn" onclick="filterServices('معاملات', this)">معاملات وإقامات</button>
                <button class="filter-btn" onclick="filterServices('صيانة', this)">صيانة منزلية</button>
                <button class="filter-btn" onclick="filterServices('توصيل', this)">توصيل ونقل</button>
                <button class="filter-btn" onclick="filterServices('عام', this)">خدمات عامة</button>
            </div>
            <button class="btn-refresh" onclick="fetchServices()">🔄 تحديث القائمة</button>
        </div>

        <div id="servicesList">
            <p style="text-align: center; color: #64748b;">جاري تحميل الخدمات...</p>
        </div>

        <!-- 💰 م��احة إعلانية سفلية -->
        <div class="ad-banner" style="margin-top: 2rem;">
            <span>[مساحة إعلانية - AdBanner Footer]</span>
        </div>
    </div>

    <script>
        let allServices = [];

        async function fetchServices() {
            try {
                const response = await fetch('/api/services');
                allServices = await response.json();
                displayServices(allServices);
            } catch (e) {
                console.error('Error fetching services:', e);
            }
        }

        function displayServices(services) {
            const container = document.getElementById('servicesList');
            
            if (!services || services.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #64748b;">لا توجد خدمات مضافة حالياً...</p>';
                return;
            }

            container.innerHTML = '';
            services.forEach(service => {
                const card = document.createElement('div');
                card.className = 'job-card';
                card.innerHTML = `
                    <div class="job-title">${service.title}</div>
                    <div>${service.details}</div>
                    <div class="job-time">📅 التوقيت: ${service.timestamp}</div>
                    <div class="job-actions">
                        <a href="https://wa.me/?text=` + encodeURIComponent('خدمة عبر منصة مرسين:\n' + service.title + '\n' + service.details) + `" class="btn-action btn-share" target="_blank">📤 مشاركة</a>
                        <a href="https://wa.me/" class="btn-action" target="_blank">💬 التواصل</a>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function filterServices(category, btn) {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            if (category === 'all') {
                displayServices(allServices);
            } else {
                const filtered = allServices.filter(service => service.category === category);
                displayServices(filtered);
            }
        }

        fetchServices();
        setInterval(fetchServices, 10000); // تحديث تلقائي كل 10 ثوانٍ
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/api/services', methods=['GET'])
def get_services():
    return jsonify(services_data)

@app.route('/api/add-service', methods=['POST'])
def add_service():
    data = request.json
    if data and 'title' in data and 'details' in data:
        new_item = {
            "title": data['title'],
            "category": data.get('category', 'عام'),
            "details": data['details'],
            "timestamp": "مباشرة من واتساب"
        }
        services_data.insert(0, new_item) # إضافة الإعلان الجديد في أعلى القائمة
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

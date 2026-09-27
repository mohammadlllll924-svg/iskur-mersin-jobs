from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

jobs_data = [
    {
        "title": "مطلوب شيف مشويات كفء للعمل في مطعم بمرسين",
        "details": "الموقع: مركز مرسين (مزيتلي).\nالخبرة: سنتان على الأقل.\nالراتب: جيد ويقاس بالمقابلة.",
        "timestamp": "اليوم - 12:00 م"
    },
    {
        "title": "مطلوب موظف مبيعات وتسويق",
        "details": "الموقع: مرسين - مركز المدينة.\nالمتطلبات: إجادة اللغة التركية.",
        "timestamp": "اليوم - 10:30 ص"
    }
]

html_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة مرسين للخدمات - فرص العمل اليومية</title>
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
        <p>البوابة الرسمية لجلب أحدث الوظائف والخدمات في مرسين</p>
    </header>

    <div class="container">
        <!-- 💰 مساحة إعلانية علوية -->
        <div class="ad-banner">
            <span>[مساحة إعلانية - AdBanner Header]</span>
        </div>

        <!-- شريط التحكم والتصفية -->
        <div class="controls-bar">
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterJobs('all', this)">الكل</button>
                <button class="filter-btn" onclick="filterJobs('مطعم', this)">مطاعم ومقاهي</button>
                <button class="filter-btn" onclick="filterJobs('مبيعات', this)">مبيعات وتسويق</button>
                <button class="filter-btn" onclick="filterJobs('عامل', this)">عمالة ومهن</button>
            </div>
            <button class="btn-refresh" onclick="fetchJobs()">🔄 تحديث الوظائف</button>
        </div>

        <div id="jobsList">
            <p style="text-align: center; color: #64748b;">جاري تحميل أحدث الوظائف...</p>
        </div>

        <!-- 💰 مساحة إعلانية سفلية -->
        <div class="ad-banner" style="margin-top: 2rem;">
            <span>[مساحة إعلانية - AdBanner Footer]</span>
        </div>
    </div>

    <script>
        let allJobs = [];

        async function fetchJobs() {
            try {
                const response = await fetch('/api/jobs');
                allJobs = await response.json();
                displayJobs(allJobs);
            } catch (e) {
                console.error('Error fetching jobs:', e);
            }
        }

        function displayJobs(jobs) {
            const container = document.getElementById('jobsList');
            
            if (!jobs || jobs.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #64748b;">لا توجد وظائف مضافة حالياً...</p>';
                return;
            }

            container.innerHTML = '';
            jobs.forEach(job => {
                const card = document.createElement('div');
                card.className = 'job-card';
                card.innerHTML = `
                    <div class="job-title">${job.title}</div>
                    <div>${job.details}</div>
                    <div class="job-time">📅 وقت النشر: ${job.timestamp}</div>
                    <div class="job-actions">
                        <a href="https://wa.me/?text=` + encodeURIComponent('فرصة عمل جديدة عبر منصة مرسين للخدمات:\n' + job.title + '\n' + job.details) + `" class="btn-action btn-share" target="_blank">📤 مشاركة الإعلان</a>
                        <a href="https://wa.me/" class="btn-action" target="_blank">💬 التواصل السريع</a>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function filterJobs(keyword, btn) {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            if (keyword === 'all') {
                displayJobs(allJobs);
            } else {
                const filtered = allJobs.filter(job => job.details.includes(keyword) || job.title.includes(keyword));
                displayJobs(filtered);
            }
        }

        fetchJobs();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/api/jobs')
def get_jobs():
    return jsonify(jobs_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

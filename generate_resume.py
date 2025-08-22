

import yaml
from bs4 import BeautifulSoup

# Read the YAML file
with open('resume.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# Start HTML string
html = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 900px;
            margin: 20px auto;
            padding: 25px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        h1, h2, h3 {
            color: #0056b3;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 8px;
            margin-top: 20px;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 0;
        }
        .contact-info {
            text-align: center;
            margin-bottom: 25px;
            color: #555;
        }
        .contact-info a {
            color: #0056b3;
            text-decoration: none;
            margin: 0 10px;
        }
        .contact-info a:hover {
            text-decoration: underline;
        }
        .section {
            margin-bottom: 20px;
        }
        ul {
            padding-left: 20px;
            list-style-type: disc;
        }
        li {
            margin-bottom: 8px;
        }
        .job, .education, .project, .patent {
            margin-bottom: 15px;
            padding-left: 15px;
            border-left: 3px solid #0056b3;
        }
        .job-title, .school-name {
            font-weight: bold;
            font-size: 1.1em;
        }
        .duration {
            font-style: italic;
            color: #666;
            float: right;
        }
        .company-name, .department-name {
            font-weight: bold;
            color: #444;
        }
        .project-summary {
            font-weight: bold;
            font-size: 1.05em;
        }
        .keywords {
            font-size: 0.9em;
            color: #555;
            background-color: #e9ecef;
            padding: 2px 6px;
            border-radius: 4px;
            display: inline-block;
            margin-right: 5px;
            margin-top: 5px;
        }
        .clear {
            clear: both;
        }
        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .skill-category {
            flex: 1 1 200px;
            min-width: 180px;
        }
        .skill-category h3 {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="container">
"""

# --- Header ---
html += f"<h1>{data['name']['zh']}</h1>"
html += "<div class=\"contact-info\">"
html += f"<a href=\"mailto:{data['mail']}\">{data['mail']}</a>"
if 'phones' in data and data['phones']:
    html += f" | <span>{' / '.join(data['phones'])}</span>"
if 'github' in data and data['github']:
    full_url = data['github']
    html += f' | <a href="{full_url}" target="_blank">{full_url}</a>'
html += "</div>"


# --- Profile ---
html += "<div class=\"section\"><h2>個人簡介</h2>"
profile_text = ' '.join(data['profile']['zh'])
html += f"<p>{profile_text}</p></div>"

# --- Work Experience & Projects ---
html += "<div class=\"section\"><h2>工作經歷 & 專案成就</h2>"

all_projects = [p for p in data['attainments']['items'] if p.get('display', False)]
displayed_projects = []

for company in data['companies']:
    html += "<div class=\"job\">"
    html += f"<span class=\"duration\">{company['duration']}</span>"
    html += f"<div class=\"company-name\">{company['name']['zh']}</div>"
    html += f"<div class=\"job-title\">{company['position']['zh']}</div>"
    if company.get('description') and company['description'].get('zh'):
        html += "<ul>"
        for desc_item in company['description']['zh']:
             html += f"<li>{desc_item}</li>"
        html += "</ul>"

    if company.get('reason') and company['reason'].get('zh'):
        html += f"<p><strong>離職原因：</strong> {company['reason']['zh']}</p>"

    company_projects = [p for p in all_projects if p['company']['zh'] == company['name']['zh'] or (company['name']['zh'] == 'Uitox電子商務' and p['company']['zh'] == 'Uitox')]
    if company_projects:
        html += "<h4>主要專案:</h4>"
        for project in company_projects:
            html += "<div class=\"project\">"
            html += f"<div class=\"project-summary\">{project['summary']['zh']}</div>"
            if project.get('description') and project['description'].get('zh'):
                project_desc_text = ' '.join(project['description']['zh'])
                html += f"<p>{project_desc_text}</p>"
            if project.get('keywords'):
                html += "<div>"
                for keyword in project['keywords']:
                    html += f"<span class=\"keywords\">{keyword}</span>"
                html += "</div>"
            html += "</div>"
            displayed_projects.append(project)

    html += "</div>"

remaining_projects = [p for p in all_projects if p not in displayed_projects]
if remaining_projects:
    html += "<h3>其他專案</h3>"
    if data['attainments'].get('comment', {}).get('zh'):
        html += f"<p><em>{data['attainments']['comment']['zh']}</em></p>"
    for project in remaining_projects:
        html += "<div class=\"project\">"
        html += f"<div class=\"project-summary\">{project['summary']['zh']}</div>"
        html += f"<div class=\"company-name\">{project['company']['zh']}</div>"
        if project.get('description') and project['description'].get('zh'):
            project_desc_text = ' '.join(project['description']['zh'])
            html += f"<p>{project_desc_text}</p>"
        if project.get('keywords'):
            html += "<div>"
            for keyword in project['keywords']:
                html += f"<span class=\"keywords\">{keyword}</span>"
            html += "</div>"
        html += "</div>"

html += "</div>"


# --- Skills ---
html += "<div class=\"section\"><h2>專業技能</h2>"
html += "<div class=\"skills-container\">"

if 'programs' in data and data['programs']:
    html += "<div class=\"skill-category\">"
    html += "<h3>程式語言</h3><ul>"
    for skill in data['programs']:
        html += f"<li>{skill['name']}</li>"
    html += "</ul></div>"

if 'libraries' in data and data['libraries']:
    html += "<div class=\"skill-category\">"
    html += "<h3>函式庫／框架</h3><ul>"
    for skill in data['libraries']:
        html += f"<li>{skill}</li>"
    html += "</ul></div>"

if 'databases' in data and data['databases']:
    html += "<div class=\"skill-category\">"
    html += "<h3>資料庫</h3><ul>"
    for skill in data['databases']:
        html += f"<li>{skill}</li>"
    html += "</ul></div>"

if 'vsersion controlls' in data and data['vsersion controlls']:
    html += "<div class=\"skill-category\">"
    html += "<h3>版本控制</h3><ul>"
    for skill in data['vsersion controlls']:
        html += f"<li>{skill}</li>"
    html += "</ul></div>"

if 'os' in data and data['os']:
    html += "<div class=\"skill-category\">"
    html += "<h3>作業系統</h3><ul>"
    for skill in data['os']:
        html += f"<li>{skill}</li>"
    html += "</ul></div>"

if 'special experiences and knowledge' in data and data['special experiences and knowledge']:
    html += "<div class=\"skill-category\">"
    html += "<h3>其他</h3><ul>"
    for skill in data['special experiences and knowledge']:
        html += f"<li>{skill}</li>"
    html += "</ul></div>"

html += "</div></div>"

# --- Patents ---
html += "<div class=\"section\"><h2>專利</h2>"
for patent in data['patents']:
    html += "<div class=\"patent\">"
    html += f"<div class=\"job-title\">{patent['name']['zh']}</div>"
    html += "<ul>"
    html += f"<li>類型：{patent['type']}</li>"
    html += f"<li>專利權人：{patent['company']['zh']}</li>"
    html += "</ul>"
    html += "</div>"
html += "</div>"


# --- Education ---
html += "<div class=\"section\"><h2>學歷</h2>"
for edu in data['educations']:
    html += "<div class=\"education\">"
    html += f"<span class=\"duration\">{edu['duration']}</span>"
    html += f"<div class=\"school-name\">{edu['school']['zh']}</div>"
    html += f"<div class=\"department-name\">{edu['department']['zh']}</div>"
    html += "<div class=\"clear\"></div></div>"
html += "</div>"

# --- Licenses ---
html += "<div class=\"section\"><h2>專業證照</h2>"
html += "<ul>"
for license in reversed(data['licenses']):
    html += f"<li>{license['name']}</li>"
html += "</ul></div>"


# --- Footer ---
html += """
    </div>
</body>
</html>
"""

# Write the HTML to a file
soup = BeautifulSoup(html, 'lxml')
pretty_html = soup.prettify()
with open('resume_zh.html', 'w', encoding='utf-8') as f:
    f.write(pretty_html)

print("履歷 'resume_zh.html' 已成功產生。")

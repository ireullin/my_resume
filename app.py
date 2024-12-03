from flask import Flask, render_template, jsonify, send_from_directory
import yaml
import os

app = Flask(__name__, template_folder=os.path.abspath('.'))

@app.route('/')
def index():
    return render_template('result.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resume')
def resume_json():
    with open('./resume.yaml', 'r') as file:
        resume_data = yaml.safe_load(file)
    return jsonify(resume_data)

@app.route('/photos/<path:filename>')
def photos(filename):
    return send_from_directory('photos', filename)

if __name__ == '__main__':
    app.run(debug=True)
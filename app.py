from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)   #In the case of any error try it 

# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('D:/HTML/.vscode/Ai_project/Flask/app/templates/index.html') or use only index.html

# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=False)
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

FILE_PATH = "appointments.txt"

# Rota para o formulário (página inicial)
@app.route('/')
def index():
    return render_template('form.html')

# Rota para processar a submissão do formulário
@app.route('/schedule', methods=['POST'])
def schedule():
    name = request.form.get('name')
    email = request.form.get('email')
    date = request.form.get('date')
    time = request.form.get('time')
    
    if name and email and date and time:
        with open(FILE_PATH, "a", encoding="utf-8") as file:
            file.write(f"{name};{email};{date};{time}\n")
            
    return redirect(url_for('list_appointments'))

# Rota para ler o ficheiro e mostrar a lista
@app.route('/appointments')
def list_appointments():
    appointments_list = []
    
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(';')
                    if len(parts) == 4:
                        appointments_list.append({
                            'name': parts[0],
                            'email': parts[1],
                            'date': parts[2],
                            'time': parts[3]
                        })
                    
    return render_template('list.html', appointments=appointments_list)

if __name__ == '__main__':
    app.run(debug=True)

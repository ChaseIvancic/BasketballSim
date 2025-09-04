from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
import shutil

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

# Create sims directory if it doesn't exist
SIM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sims')
STATS_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'Stats_Templates')
if not os.path.exists(SIM_DIR):
    os.makedirs(SIM_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play')
def play():
    # Get list of existing simulations
    simulations = [d for d in os.listdir(SIM_DIR) if os.path.isdir(os.path.join(SIM_DIR, d))]
    return render_template('play.html', simulations=simulations)

@app.route('/create_sim', methods=['POST'])
def create_sim():
    sim_name = request.form.get('sim_name')
    if sim_name:
        # Check if simulation already exists
        sim_path = os.path.join(SIM_DIR, sim_name)
        if os.path.exists(sim_path):
            flash('This simulation name already exists. Please choose a different name.', 'error')
        else:
            # Create the simulation directory
            os.makedirs(sim_path)
            
            # Create date file with January 1st of current year
            current_year = datetime.now().year
            date_file_path = os.path.join(sim_path, 'date.txt')
            with open(date_file_path, 'w') as f:
                f.write(f'January 1, {current_year}')
            
            # Create stats folder and copy CSV templates
            stats_folder = os.path.join(sim_path, 'stats')
            os.makedirs(stats_folder)
            if os.path.exists(STATS_TEMPLATE_DIR):
                for filename in os.listdir(STATS_TEMPLATE_DIR):
                    if filename.lower().endswith('.csv'):
                        src = os.path.join(STATS_TEMPLATE_DIR, filename)
                        dst = os.path.join(stats_folder, filename)
                        shutil.copy2(src, dst)
            
            flash('Simulation created successfully!', 'success')
    return redirect(url_for('play'))

@app.route('/delete_sim/<sim_name>')
def delete_sim(sim_name):
    sim_path = os.path.join(SIM_DIR, sim_name)
    if os.path.exists(sim_path):
        # Remove the simulation directory and all its contents
        for root, dirs, files in os.walk(sim_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(sim_path)
        flash('Simulation deleted successfully!', 'success')
    return redirect(url_for('play'))

# Helper to get sim date
def get_sim_date(sim_name):
    sim_path = os.path.join(SIM_DIR, sim_name)
    date_file_path = os.path.join(sim_path, 'date.txt')
    current_date = "Date not found"
    if os.path.exists(date_file_path):
        with open(date_file_path, 'r') as f:
            current_date = f.read().strip()
    return current_date

@app.route('/play_sim/<sim_name>')
def play_sim(sim_name):
    sim_path = os.path.join(SIM_DIR, sim_name)
    if os.path.exists(sim_path):
        current_date = get_sim_date(sim_name)
        return render_template('sim_index.html', sim_name=sim_name, current_date=current_date, active_page='home')
    return redirect(url_for('play'))

@app.route('/play_sim/<sim_name>/simulate')
def simulate_sim(sim_name):
    sim_path = os.path.join(SIM_DIR, sim_name)
    if os.path.exists(sim_path):
        current_date = get_sim_date(sim_name)
        return render_template('sim_simulate.html', sim_name=sim_name, current_date=current_date, active_page='simulate')
    return redirect(url_for('play'))

@app.route('/play_sim/<sim_name>/news')
def news_sim(sim_name):
    sim_path = os.path.join(SIM_DIR, sim_name)
    if os.path.exists(sim_path):
        current_date = get_sim_date(sim_name)
        return render_template('sim_news.html', sim_name=sim_name, current_date=current_date, active_page='news')
    return redirect(url_for('play'))

@app.route('/play_sim/<sim_name>/stats')
def stats_sim(sim_name):
    sim_path = os.path.join(SIM_DIR, sim_name)
    if os.path.exists(sim_path):
        current_date = get_sim_date(sim_name)
        return render_template('sim_stats.html', sim_name=sim_name, current_date=current_date, active_page='stats')
    return redirect(url_for('play'))

@app.route('/play_sim/<sim_name>/rosters')
def rosters_sim(sim_name):
    sim_path = os.path.join(SIM_DIR, sim_name)
    if os.path.exists(sim_path):
        current_date = get_sim_date(sim_name)
        return render_template('sim_rosters.html', sim_name=sim_name, current_date=current_date, active_page='rosters')
    return redirect(url_for('play'))

@app.route('/about')
def about():
    return "About Page - Coming Soon"

if __name__ == '__main__':
    app.run(debug=True) 
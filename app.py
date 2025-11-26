import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from data_engine import DataEngine

app = Flask(__name__)
app.secret_key = 'enterprise_ml_secret_key_change_in_prod'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Data Engine
engine = DataEngine(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            success, msg = engine.load_data(filename)
            if success:
                flash('File uploaded and analyzed successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(f'Error loading file: {msg}', 'danger')
        else:
            flash('Only CSV files are allowed.', 'warning')

    return render_template('base.html', page='home')


@app.route('/dashboard')
def dashboard():
    if engine.df is None:
        flash('Please upload a dataset first.', 'info')
        return redirect(url_for('index'))

    summary = engine.get_summary()
    # Get first 5 rows for preview
    preview = engine.df.head().to_html(classes='table table-striped table-hover', index=False)

    return render_template('dashboard.html', summary=summary, preview=preview)


@app.route('/cleaning', methods=['GET', 'POST'])
def cleaning():
    if engine.df is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form.get('action')
        target = request.form.get('target')

        # Map form actions to engine strategies
        success = False
        msg = ""

        if action == 'drop_rows':
            success, msg = engine.clean_data('drop_na_rows')
        elif action == 'drop_cols':
            success, msg = engine.clean_data('drop_na_cols')
        elif action == 'drop_specific':
            success, msg = engine.clean_data('drop_col', target_col=target)
        elif action == 'fill_mean':
            success, msg = engine.clean_data('fill_mean', target_col=target)
        elif action == 'fill_zero':
            success, msg = engine.clean_data('fill_zero', target_col=target)
        elif action == 'fill_mode':
            success, msg = engine.clean_data('fill_mode', target_col=target)

        if success:
            flash(msg, 'success')
        else:
            flash(msg, 'danger')

        return redirect(url_for('cleaning'))

    columns = engine.df.columns.tolist()
    numeric_columns = engine.df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    return render_template('cleaning.html', columns=columns, numeric_columns=numeric_columns)


@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    if engine.df is None:
        return redirect(url_for('index'))

    plot_content = None  # Generic name for plot output (image or HTML)
    is_interactive = False  # Flag to determine if it's an interactive Plotly HTML chart

    columns = engine.df.columns.tolist()
    numeric_columns = engine.df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if request.method == 'POST':
        plot_type = request.form.get('plot_type')
        x_col = request.form.get('x_col')
        y_col = request.form.get('y_col')
        z_col = request.form.get('z_col')
        color_col = request.form.get('color_col')
        theme = request.form.get('theme')

        # Treat "None" strings as actual None
        if y_col == "None": y_col = None
        if z_col == "None": z_col = None
        if color_col == "None": color_col = None

        # Updated call: Expecting 3 return values (content, message, is_interactive)
        content, msg, is_html = engine.visualize(plot_type, x_col, y_col, z_col, color_col, theme=theme)

        if content:
            plot_content = content
            is_interactive = is_html
        else:
            flash(msg, 'danger')

    return render_template('visualize.html',
                           columns=columns,
                           numeric_columns=numeric_columns,
                           plot_content=plot_content,  # Pass the content string
                           is_interactive=is_interactive)  # Pass the interactive flag


@app.route('/download')
def download():
    if engine.df is None:
        return redirect(url_for('index'))

    # Save current state to a temp file
    filename = "modified_dataset.csv"
    engine.save_data(filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, request, render_template_string
from stress_analysis import parse_brain_log, BrainRegion, StressAnalyzer, save_analysis_report

app = Flask(__name__)

TEMPLATE = '''
<h1>Deteksi Stres Otak</h1>
<form method="post">
    <textarea name="log" rows="10" cols="60" placeholder="Masukkan log aktivasi otak di sini...">{{ log }}</textarea><br>
    <button type="submit">Analisis</button>
</form>
{% if report %}
    <h2>Hasil Analisis</h2>
    <pre>{{ report }}</pre>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def analyze():
    report = ''
    log = ''
    if request.method == 'POST':
        log = request.form.get('log', '')
        data = parse_brain_log(log)
        if data:
            brain_regions = []
            for name, role, val in data:
                region = BrainRegion(name, role)
                region.set_activation(val)
                brain_regions.append(region)

            analyzer = StressAnalyzer(brain_regions)
            report = analyzer.get_report()
            save_analysis_report(brain_regions, report)
            report = "\n".join([r.get_info() for r in brain_regions]) + "\n\n" + report
        else:
            report = "Log tidak valid."

    return render_template_string(TEMPLATE, report=report, log=log)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# webhook_receiver.py
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
latest_readings = []

# … tus rutas /webhook y /readings …

DASHBOARD_HTML = """
<!doctype html>
<html>
<head>
  <title>Dashboard Sensores</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <h2>Lecturas de Corriente (últimos 20 puntos)</h2>
  <canvas id="sensorChart" width="800" height="400"></canvas>
  <script>
    const ctx = document.getElementById('sensorChart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [],              // llenadas en JS
        datasets: [
          { label: 'Fase U', data: [], fill: false },
          { label: 'Fase V', data: [], fill: false },
          { label: 'Fase W', data: [], fill: false },
          { label: 'Promedio', data: [], fill: false },
        ]
      },
      options: {
        animation: false,
        scales: { x: { display: true }, y: { beginAtZero: true } }
      }
    });

    async function updateChart() {
      const resp = await fetch('/readings');
      const readings = await resp.json();
      // solo los últimos 20
      const last = readings.slice(-20);
      chart.data.labels = last.map(r => r.hora);
      chart.data.datasets[0].data = last.map(r => r.corr1);
      chart.data.datasets[1].data = last.map(r => r.corr2);
      chart.data.datasets[2].data = last.map(r => r.corr3);
      chart.data.datasets[3].data = last.map(r => r.prom);
      chart.update();
    }

    // refresca cada 10s
    setInterval(updateChart, 10000);
    updateChart();
  </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

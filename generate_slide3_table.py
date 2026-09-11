import os
from playwright.sync_api import sync_playwright

html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  
  body {
    margin: 0;
    padding: 20px;
    background-color: transparent;
    font-family: 'Inter', Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  
  .container {
    width: 1100px;
    background: #ffffff;
    padding: 24px;
    border-radius: 12px;
    box-sizing: border-box;
  }

  .subtitle {
    text-align: center;
    color: #1b5e20;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 18px;
    text-transform: uppercase;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    color: #1a1a1a;
  }

  th {
    background-color: #f0f4f1;
    color: #0d2b45;
    font-weight: 700;
    padding: 14px 12px;
    border: 1px solid #c8d6c9;
    text-align: center;
    font-size: 15px;
  }

  td {
    padding: 14px 12px;
    border: 1px solid #d0d7de;
    vertical-align: middle;
    line-height: 1.45;
  }

  tr:nth-child(even) {
    background-color: #f9fbf9;
  }

  tr:nth-child(odd) {
    background-color: #ffffff;
  }

  .col-feature {
    width: 16%;
    font-weight: 700;
    color: #0d2b45;
    text-align: center;
  }

  .col-input {
    width: 18%;
    font-size: 13.5px;
  }

  .col-output {
    width: 18%;
    font-weight: 600;
    color: #c8102e;
    font-size: 13.5px;
  }

  .col-method {
    width: 31%;
    font-size: 13.5px;
  }

  .col-tools {
    width: 17%;
    font-weight: 600;
    color: #1b5e20;
    font-size: 13.5px;
  }
</style>
</head>
<body>
  <div class="container">
    <div class="subtitle">TECHNOLOGY USED AND METHODOLOGY</div>
    <table>
      <thead>
        <tr>
          <th>Feature</th>
          <th>Input</th>
          <th>Output</th>
          <th>How We Do It (Methodology)</th>
          <th>APIs / Open-Source Tools</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="col-feature">Joint Block Optimizer</td>
          <td class="col-input">P-Way, TRD & S&T maintenance requests</td>
          <td class="col-output">1 Consolidated 4h Joint Maintenance Window</td>
          <td class="col-method">MILP constraint solver algorithm grouping overlapping track section requests across departments.</td>
          <td class="col-tools">Google OR-Tools, PuLP, Python</td>
        </tr>
        <tr>
          <td class="col-feature">AI Train Dispatcher</td>
          <td class="col-input">Live train speeds, priority & telemetry feeds</td>
          <td class="col-output">Loop Line Overtake Directive (PWL Siding)</td>
          <td class="col-method">Spatio-temporal graph modeling & priority speed vector analysis to hold slow freight trains.</td>
          <td class="col-tools">FastAPI, NetworkX, Redis</td>
        </tr>
        <tr>
          <td class="col-feature">Track Capacity Engine</td>
          <td class="col-input">Section downtime logs & historical timetable</td>
          <td class="col-output">42.9% Capacity Recovery & Zero Domino Delay</td>
          <td class="col-method">Dynamic track availability modeling & section uptime calculation formulas.</td>
          <td class="col-tools">Pandas, NumPy, SciPy</td>
        </tr>
        <tr>
          <td class="col-feature">Live Route Dashboard</td>
          <td class="col-input">Route Selection (NDLS → GWL)</td>
          <td class="col-output">Live "Where Is My Track" Interactive Portal</td>
          <td class="col-method">Real-time web portal rendering section tracks, loop siding status & timetable alerts.</td>
          <td class="col-tools">HTML5, Tailwind CSS, Chart.js</td>
        </tr>
        <tr>
          <td class="col-feature">CRIS System Gateway</td>
          <td class="col-input">COA & BDMS railway system feeds</td>
          <td class="col-output">Automated Controller Approval Directive</td>
          <td class="col-method">REST API synchronization with Human-in-the-Loop controller click approval workflow.</td>
          <td class="col-tools">CRIS Open APIs, WebSocket, JSON</td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
"""

with open("slide3_table.html", "w") as f:
    f.write(html_content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=2) # high DPI for crisp quality
    page.goto(f"file://{os.path.abspath('slide3_table.html')}")
    container = page.query_selector(".container")
    container.screenshot(path="slide3_table.png")
    browser.close()

print("Image slide3_table.png successfully created!")

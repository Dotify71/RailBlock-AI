import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

# Data for Slide 3 Table
data = [
    ["Joint Block\nOptimizer", "P-Way, TRD & S&T\nmaintenance requests", "1 Consolidated 4h\nJoint Block Window", "MILP constraint solver groups overlapping section requests across departments.", "Google OR-Tools,\nPuLP, Python"],
    ["AI Train\nDispatcher", "Live train speeds,\npriority & telemetry", "Loop Line Overtake\nDirective (PWL Siding)", "Spatio-temporal graph modeling & priority speed vector analysis to hold slow trains.", "FastAPI, NetworkX,\nRedis"],
    ["Track Capacity\nEngine", "Section downtime logs &\nhistorical timetable", "42.9% Capacity Recovery &\nZero Domino Delay", "Dynamic track availability modeling & section uptime calculation formulas.", "Pandas, NumPy,\nSciPy"],
    ["Live Route\nDashboard", "Route Selection\n(NDLS → GWL)", "Live 'Where Is My Track'\nInteractive Portal", "Real-time web portal rendering section tracks, loop siding status & timetable alerts.", "HTML5, Tailwind CSS,\nChart.js"],
    ["CRIS System\nGateway", "COA & BDMS railway\nsystem feeds", "Automated Controller\nApproval Directive", "REST API sync with Human-in-the-Loop controller click approval workflow.", "CRIS Open APIs,\nWebSocket, JSON"]
]

columns = ["Feature", "Input", "Output", "How We Do It (Methodology)", "APIs / Open-Source Tools"]

fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
ax.axis('off')

# Title above table
plt.title("TECHNOLOGY USED AND METHODOLOGY", fontsize=18, fontweight='bold', color='#1B5E20', pad=20)

# Table layout
table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')

table.auto_set_font_size(False)
table.set_fontsize(10.5)
table.scale(1.2, 2.6)

# Styling cells
for (row, col), cell in table.get_celld().items():
    cell.set_linewidth(1.2)
    cell.set_edgecolor('#B0BEC5')
    if row == 0:
        cell.set_facecolor('#E8F5E9')
        cell.set_text_props(weight='bold', color='#0D2B45', fontsize=11.5)
    else:
        if row % 2 == 0:
            cell.set_facecolor('#F9FBF9')
        else:
            cell.set_facecolor('#FFFFFF')
        
        # Highlight specific columns
        if col == 0:
            cell.set_text_props(weight='bold', color='#0D2B45')
        elif col == 2:
            cell.set_text_props(weight='bold', color='#C8102E')
        elif col == 4:
            cell.set_text_props(weight='bold', color='#1B5E20')

plt.tight_layout()
output_path = "slide3_table_matplotlib.png"
plt.savefig(output_path, bbox_inches='tight', dpi=300, facecolor='white', transparent=False)
print("Matplotlib table generated successfully:", output_path)

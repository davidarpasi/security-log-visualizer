# Security Log Visualizer

**Parse and visualize failed SSH login attempts from auth logs.**  
A practical log parser and plotter for analyzing brute-force patterns.

---

![Failed Login Graph](output/failed-login-plot.png)

---

## Project Structure

```bash
security-log-visualizer/
├── logs/                    # Sample log files
│   └── sample_auth.log
├── src/                     # Log parsing + plotting script
│   └── parse_failed_logins.py
├── output/                  # Generated plot
│   └── failed_login_plot.png
└── requirements.txt

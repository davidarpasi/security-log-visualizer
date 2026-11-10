"""Plot hourly failed SSH logins from a traditional syslog file."""

import argparse
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

PATTERN = re.compile(r'^(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+.*\bsshd\[\d+\]: Failed password\b')
MONTHS = {name: i for i, name in enumerate(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), 1)}
ROOT = Path(__file__).resolve().parents[1]


def parse_failed_logins(log_path, year):
    counts = Counter()
    with Path(log_path).open(encoding='utf-8') as handle:
        for line in handle:
            match = PATTERN.match(line)
            if match:
                try:
                    hour, minute, second = map(int, match['time'].split(':'))
                    timestamp = datetime(year, MONTHS[match['month']], int(match['day']), hour, minute, second)
                except (ValueError, KeyError):
                    continue
                counts[timestamp.replace(minute=0, second=0)] += 1
    return counts


def plot_attempts(counts, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    times = sorted(counts)
    figure, axis = plt.subplots(figsize=(10, 5))
    axis.plot(times, [counts[t] for t in times], marker='o', color='crimson')
    axis.set(title='Failed Login Attempts per Hour', xlabel='Time (log-local)', ylabel='Failed Attempts')
    figure.autofmt_xdate()
    figure.tight_layout()
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'logs/sample_auth.log')
    parser.add_argument('--output', type=Path, default=ROOT / 'output/failed_login_plot.png')
    parser.add_argument('--year', type=int, required=True)
    args = parser.parse_args()
    if not 1 <= args.year <= 9999:
        parser.error('year must be between 1 and 9999')
    try:
        counts = parse_failed_logins(args.input, args.year)
        if not counts:
            parser.error('no valid failed SSH login events found')
        plot_attempts(counts, args.output)
    except OSError:
        parser.exit(2, 'Could not read the log or write the plot.\n')
    print(f'Parsed {sum(counts.values())} events; plot saved to {args.output}')


if __name__ == '__main__':
    main()

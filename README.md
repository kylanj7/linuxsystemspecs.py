# Laptop System Information Gatherer

A Python script that collects comprehensive system information from Linux-based laptops, including hardware specifications, performance metrics, and health statistics.

## Features

- Complete system information gathering
- Detailed hardware specifications
- Battery health monitoring
- I/O device enumeration
- Automated report generation

## Information Collected

- System details (OS, manufacturer, model, serial)
- CPU specifications and performance
- Memory configuration and usage
- GPU information
- I/O devices (USB, Network, Audio)
- Storage details
- Battery health status

## Prerequisites

- Linux-based operating system
- Python 3.x
- Required packages:
```bash
pip install psutil
```

- System utilities:
```bash
sudo apt-get install dmidecode lsusb upower
```

## Installation

1. Clone or download the script
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with sudo privileges for full information:
```bash
sudo python laptop_info.py
```

## Output

- Creates timestamped report in Documents folder
- Filename format: `laptop_info_YYYYMMDD_HHMMSS.txt`
- Displays summary on console
- Saves detailed report to file

## Permissions

Some features require elevated privileges:
- Detailed memory information (dmidecode)
- Some hardware specifications
- Battery information

## Error Handling

- Graceful handling of missing permissions
- Alternative information paths
- Clear error reporting
- Continues execution on non-critical failures

## Limitations

- Some features Linux-specific
- Full information requires root access
- Battery info requires laptop hardware

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Specify your license here]

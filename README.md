# Advanced CPU & Memory Stress Tester

A comprehensive system stress testing tool with real-time monitoring capabilities.

## Features

🔥 **CPU Stress Testing**
- Multi-core CPU stress testing
- Configurable intensity levels
- Real-time CPU usage monitoring per core

🧠 **Memory Stress Testing** 
- Configurable memory allocation and manipulation
- Multiple memory stress processes
- Memory usage monitoring

📊 **Real-time Dashboard**
- Live CPU usage per core with visual bars
- Memory usage monitoring with visual indicators
- Temperature monitoring (cross-platform compatible)
- Comprehensive system information

🛠️ **Advanced Features**
- Graceful shutdown with Ctrl+C handling
- Comprehensive logging to timestamped log files
- Input validation with warnings
- Cross-platform compatibility
- Legacy mode for backward compatibility

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic CPU Stress Test
```bash
python cpu.py -c 4 -t 30 -i 2
```
- `-c 4`: Use 4 CPU cores
- `-t 30`: Run for 30 seconds  
- `-i 2`: Use intensity level 2

### CPU + Memory Stress Test
```bash
python cpu.py -c 4 -t 60 -i 1 -m 2 -s 200
```
- `-m 2`: Start 2 memory stress processes
- `-s 200`: Allocate 200MB per memory process

### All Available Options
```bash
python cpu.py --help
```

### Legacy Mode (Original Behavior)
```bash
python cpu.py --cpu-only -c 4 -t 30 -i 1
```

## Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--cores` | `-c` | Number of CPU cores to stress | All cores |
| `--time` | `-t` | Duration in seconds | 10 |
| `--intensity` | `-i` | CPU workload intensity factor | 1 |
| `--memory-processes` | `-m` | Number of memory stress processes | 0 |
| `--memory-size` | `-s` | Memory allocation per process (MB) | 100 |
| `--cpu-only` | | Run in legacy CPU-only mode | False |

## Safety Features

- **Graceful Shutdown**: Press Ctrl+C to stop safely
- **Input Validation**: Prevents invalid configurations
- **Process Cleanup**: Ensures all processes are terminated
- **Resource Warnings**: Alerts for potentially dangerous configurations
- **Comprehensive Logging**: All activities logged with timestamps

## Dashboard Features

The real-time dashboard shows:
- ⏱️ Elapsed time
- 🖥️ Overall CPU usage percentage
- 📊 Per-core CPU usage with visual bars
- 🧠 Memory usage with visual indicators
- 🌡️ Temperature information (if available)
- 📈 System specifications

## Log Files

Each test run creates a timestamped log file:
- Format: `stress_test_YYYYMMDD_HHMMSS.log`
- Contains detailed execution information
- Includes error messages and system metrics

## Platform Compatibility

- ✅ Windows
- ✅ Linux  
- ✅ macOS

## Warning ⚠️

This tool intentionally stresses your system to its limits. Use responsibly:
- Monitor temperatures to prevent overheating
- Start with lower intensity and shorter durations
- Ensure adequate cooling
- Save your work before running stress tests

## Examples

### Light CPU Test
```bash
python cpu.py -c 2 -t 10 -i 1
```

### Heavy CPU + Memory Test
```bash
python cpu.py -c 8 -t 300 -i 3 -m 4 -s 500
```

### Quick System Check
```bash
python cpu.py -t 5
```
import multiprocessing
import time
import argparse
import psutil   # install with: pip install psutil
import signal
import sys
import os
import logging
import threading
import random
from datetime import datetime


def cpu_burn(intensity=1):
    """CPU-intensive workload function"""
    while True:
        x = 1.0
        for _ in range(100000 * intensity):
            x *= 1.000001
            x /= 1.000001
            # Add some variety to prevent optimization
            if _ % 10000 == 0:
                x += random.random() * 0.001


def memory_burn(size_mb=100):
    """Memory-intensive workload function"""
    try:
        # Allocate and manipulate memory
        data = []
        chunk_size = 1024 * 1024  # 1MB chunks
        
        while True:
            # Allocate memory
            for _ in range(size_mb):
                chunk = bytearray(chunk_size)
                # Fill with random data to prevent optimization
                for i in range(0, len(chunk), 1000):
                    chunk[i] = random.randint(0, 255)
                data.append(chunk)
            
            # Modify existing data
            if data:
                for chunk in random.sample(data, min(10, len(data))):
                    for i in range(0, len(chunk), 5000):
                        chunk[i] = random.randint(0, 255)
            
            # Occasionally clear some data to prevent infinite growth
            if len(data) > size_mb * 2:
                data = data[size_mb:]
                
            time.sleep(0.1)  # Small delay to prevent complete system freeze
            
    except Exception as e:
        print(f"Memory stress error: {e}")


def get_system_info():
    """Get comprehensive system information"""
    info = {
        'cpu_count': psutil.cpu_count(logical=False),
        'cpu_count_logical': psutil.cpu_count(logical=True),
        'memory_total': psutil.virtual_memory().total / (1024**3),  # GB
        'memory_available': psutil.virtual_memory().available / (1024**3),  # GB
        'platform': sys.platform
    }
    return info


class CPUStressTester:
    def __init__(self):
        self.processes = []
        self.memory_processes = []
        self.running = True
        self.setup_logging()
        self.setup_signal_handlers()
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_filename = f"stress_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Log file created: {log_filename}")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle interrupt signals gracefully"""
        print("\n🛑 Interrupt received. Shutting down gracefully...")
        self.logger.info("Interrupt signal received, initiating shutdown")
        self.running = False
        self.cleanup_processes()
        sys.exit(0)

    def cleanup_processes(self):
        """Clean up all running processes"""
        all_processes = self.processes + self.memory_processes
        
        for p in all_processes:
            if p.is_alive():
                try:
                    p.terminate()
                    p.join(timeout=2)  # Wait up to 2 seconds
                    if p.is_alive():
                        p.kill()  # Force kill if terminate didn't work
                        p.join()
                except Exception as e:
                    self.logger.error(f"Error cleaning up process: {e}")
        
        self.processes.clear()
        self.memory_processes.clear()
        self.logger.info("All processes cleaned up")

    def get_temperature_info(self):
        """Get temperature information with cross-platform compatibility"""
        temp_info = []
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            if entry.current:
                                temp_info.append(f"Temp ({name}): {entry.current:.1f}°C")
                else:
                    temp_info.append("Temperature sensors not available")
            else:
                temp_info.append("Temperature monitoring not supported on this platform")
        except Exception as e:
            temp_info.append(f"Temperature reading error: {e}")
        
        return temp_info

    def display_dashboard(self, start_time, cpu_cores, memory_size, intensity):
        """Display a comprehensive monitoring dashboard"""
        elapsed = time.time() - start_time
        
        # Get system metrics
        try:
            cpu_usage = psutil.cpu_percent(interval=0.1)
            cpu_per_core = psutil.cpu_percent(percpu=True, interval=0.1)
            memory = psutil.virtual_memory()
            
            # Clear screen for dashboard effect (cross-platform)
            if os.name == 'nt':  # Windows
                os.system('cls')
            else:  # Unix/Linux/macOS
                os.system('clear')
            
            print("=" * 60)
            print("🔥 CPU & MEMORY STRESS TESTER DASHBOARD 🔥")
            print("=" * 60)
            print(f"⏱️  Elapsed Time: {elapsed:.1f}s")
            print(f"🔧 CPU Cores Stressed: {cpu_cores}")
            print(f"💾 Memory Stress Size: {memory_size}MB per process")
            print(f"⚡ Intensity Level: {intensity}")
            print("-" * 60)
            
            # CPU Information
            print(f"🖥️  Overall CPU Usage: {cpu_usage:.1f}%")
            print("📊 Per-Core Usage:")
            for i, usage in enumerate(cpu_per_core):
                bar_length = int(usage / 5)  # Scale to 20 chars max
                bar = "█" * bar_length + "░" * (20 - bar_length)
                print(f"   Core {i:2d}: [{bar}] {usage:5.1f}%")
            
            print("-" * 60)
            
            # Memory Information
            print(f"🧠 Memory Usage: {memory.percent:.1f}%")
            print(f"📈 Used: {memory.used / (1024**3):.2f}GB / {memory.total / (1024**3):.2f}GB")
            memory_bar_length = int(memory.percent / 5)
            memory_bar = "█" * memory_bar_length + "░" * (20 - memory_bar_length)
            print(f"   Memory: [{memory_bar}] {memory.percent:.1f}%")
            
            print("-" * 60)
            
            # Temperature Information
            temp_info = self.get_temperature_info()
            print("🌡️  Temperature Information:")
            for temp in temp_info:
                print(f"   {temp}")
            
            print("-" * 60)
            print("Press Ctrl+C to stop the stress test gracefully")
            print("=" * 60)
            
            # Log metrics
            self.logger.info(f"Elapsed: {elapsed:.1f}s, CPU: {cpu_usage:.1f}%, Memory: {memory.percent:.1f}%")
            
        except Exception as e:
            print(f"Dashboard error: {e}")
            self.logger.error(f"Dashboard error: {e}")

    def stress_cpu(self, cores, duration, intensity):
        """Start CPU stress testing"""
        try:
            for _ in range(cores):
                p = multiprocessing.Process(target=cpu_burn, args=(intensity,))
                p.start()
                self.processes.append(p)
            
            self.logger.info(f"Started {cores} CPU stress processes with intensity {intensity}")
            
        except Exception as e:
            self.logger.error(f"Error starting CPU stress: {e}")
            raise

    def stress_memory(self, processes, size_mb):
        """Start memory stress testing"""
        try:
            for _ in range(processes):
                p = multiprocessing.Process(target=memory_burn, args=(size_mb,))
                p.start()
                self.memory_processes.append(p)
            
            self.logger.info(f"Started {processes} memory stress processes, {size_mb}MB each")
            
        except Exception as e:
            self.logger.error(f"Error starting memory stress: {e}")
            raise

    def run_stress_test(self, cpu_cores, duration, intensity, memory_processes=0, memory_size=100):
        """Main stress test execution"""
        try:
            # Display system info
            sys_info = get_system_info()
            print(f"🖥️  System: {sys_info['cpu_count']} cores ({sys_info['cpu_count_logical']} logical)")
            print(f"🧠 Memory: {sys_info['memory_total']:.1f}GB total, {sys_info['memory_available']:.1f}GB available")
            print(f"🔥 Starting stress test...")
            
            self.logger.info(f"Starting stress test: CPU cores={cpu_cores}, duration={duration}s, intensity={intensity}")
            
            # Start CPU stress
            self.stress_cpu(cpu_cores, duration, intensity)
            
            # Start memory stress if requested
            if memory_processes > 0:
                self.stress_memory(memory_processes, memory_size)
            
            start_time = time.time()
            
            # Monitoring loop
            while self.running and (time.time() - start_time) < duration:
                self.display_dashboard(start_time, cpu_cores, memory_size if memory_processes > 0 else 0, intensity)
                time.sleep(1)
            
            if self.running:  # Test completed normally
                print("\n✅ Stress test completed successfully!")
                self.logger.info("Stress test completed successfully")
            
        except KeyboardInterrupt:
            print("\n🛑 Test interrupted by user")
            self.logger.info("Test interrupted by user")
        except Exception as e:
            print(f"\n❌ Error during stress test: {e}")
            self.logger.error(f"Error during stress test: {e}")
        finally:
            self.cleanup_processes()


def validate_args(args):
    """Validate command line arguments"""
    if args.cores <= 0:
        raise ValueError("Number of cores must be positive")
    if args.time <= 0:
        raise ValueError("Duration must be positive")
    if args.intensity <= 0:
        raise ValueError("Intensity must be positive")
    if args.memory_processes < 0:
        raise ValueError("Memory processes cannot be negative")
    if args.memory_size <= 0:
        raise ValueError("Memory size must be positive")
    
    # Warn about high values
    if args.cores > multiprocessing.cpu_count():
        print(f"⚠️  Warning: Requesting {args.cores} cores but system has {multiprocessing.cpu_count()}")
    if args.memory_processes > 0 and args.memory_size > 1000:
        print(f"⚠️  Warning: Large memory allocation ({args.memory_size}MB per process)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced CPU & Memory Stress Tester with Real-time Monitoring")
    parser.add_argument("-c", "--cores", type=int, default=multiprocessing.cpu_count(),
                        help="Number of CPU cores to stress (default: all)")
    parser.add_argument("-t", "--time", type=int, default=10,
                        help="Duration in seconds (default: 10s)")
    parser.add_argument("-i", "--intensity", type=int, default=1,
                        help="CPU workload intensity factor (default: 1)")
    parser.add_argument("-m", "--memory-processes", type=int, default=0,
                        help="Number of memory stress processes (default: 0 - no memory stress)")
    parser.add_argument("-s", "--memory-size", type=int, default=100,
                        help="Memory allocation size per process in MB (default: 100MB)")
    parser.add_argument("--cpu-only", action="store_true",
                        help="Run CPU stress test only (legacy mode)")

    try:
        args = parser.parse_args()
        validate_args(args)
        
        if args.cpu_only:
            # Legacy mode for backward compatibility
            print(f"🔥 Legacy mode: Stressing {args.cores} cores for {args.time}s at intensity {args.intensity}...")
            tester = CPUStressTester()
            tester.stress_cpu(args.cores, args.time, args.intensity)
            
            start_time = time.time()
            while tester.running and (time.time() - start_time) < args.time:
                usage = psutil.cpu_percent(interval=1)
                print(f"CPU Usage: {usage:.1f}%")
                temp_info = tester.get_temperature_info()
                for temp in temp_info:
                    print(temp)
                print("-" * 20)
            
            tester.cleanup_processes()
            print("✅ Legacy test finished")
        else:
            # Advanced mode with dashboard
            tester = CPUStressTester()
            
            print("🚀 Advanced CPU & Memory Stress Tester")
            print(f"📊 Configuration:")
            print(f"   • CPU cores: {args.cores}")
            print(f"   • Duration: {args.time}s")
            print(f"   • CPU intensity: {args.intensity}")
            if args.memory_processes > 0:
                print(f"   • Memory processes: {args.memory_processes}")
                print(f"   • Memory size: {args.memory_size}MB per process")
            print()
            
            tester.run_stress_test(
                cpu_cores=args.cores,
                duration=args.time,
                intensity=args.intensity,
                memory_processes=args.memory_processes,
                memory_size=args.memory_size
            )
    
    except ValueError as e:
        print(f"❌ Invalid argument: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
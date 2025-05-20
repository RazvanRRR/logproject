import re
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler()
    ]
)

class LogMonitor:
    def __init__(self, log_file, warning_threshold_minutes=5, error_threshold_minutes=10):
        """
        Initialize LogMonitor with thresholds for warnings and errors
        
        Args:
            log_file (str): Path to the log file
            warning_threshold_minutes (int): Threshold in minutes for warning alerts
            error_threshold_minutes (int): Threshold in minutes for error alerts
        """
        self.log_file = log_file
        self.warning_threshold = warning_threshold_minutes * 60  # Convert to seconds
        self.error_threshold = error_threshold_minutes * 60  # Convert to seconds
        self.jobs = {}  # Dictionary to track jobs: {pid_jobname: {'start': timestamp, 'end': timestamp}}
        self.job_durations = {}  # Store calculated durations
        
    def parse_log_line(self, line):
        """
        Parse a log line into its components
        
        Args:
            line (str): A line from the log file
            
        Returns:
            tuple: (timestamp, job_description, status, pid) or None if parsing fails
        """
        # Pattern matches: HH:MM:SS, job description, START/END, PID
        pattern = r"(\d{2}:\d{2}:\d{2}),(.+), (START|END),(\d+)"
        match = re.match(pattern, line)
        
        if match:
            timestamp_str, job_description, status, pid = match.groups()
            # Create a job key combining PID and job name to handle cases where PIDs might be reused
            job_key = f"{pid}_{job_description.strip()}"
            
            # Parse timestamp
            timestamp = datetime.strptime(timestamp_str, "%H:%M:%S")
            
            return timestamp, job_description.strip(), status, pid, job_key
        return None

    def process_logs(self):
        """
        Process the log file, tracking start and end times for each job
        """
        with open(self.log_file, "r") as file:
            for line in file:
                parsed = self.parse_log_line(line.strip())
                if parsed:
                    timestamp, job_description, status, pid, job_key = parsed
                    
                    if job_key not in self.jobs:
                        self.jobs[job_key] = {'description': job_description, 'pid': pid}
                    
                    if status == "START":
                        self.jobs[job_key]['start'] = timestamp
                    elif status == "END":
                        self.jobs[job_key]['end'] = timestamp
    def calculate_durations(self):
        """
        Calculate the duration of each job and store it in self.job_durations
        """
        for job_key, job_info in self.jobs.items():
            if 'start' in job_info and 'end' in job_info:
                duration = job_info['end'] - job_info['start']
                self.job_durations[job_key] = duration
                print(self.job_durations[job_key])
        
    
            

    

    def run(self):
        """
        Run the complete monitoring process
        """
        logging.info(f"Starting log monitoring of {self.log_file}")
        self.process_logs()
        self.calculate_durations()
        logging.info(f"Log monitoring complete.")


if __name__ == "__main__":
    monitor = LogMonitor("logs.log")
    monitor.run()
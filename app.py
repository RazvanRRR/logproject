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
            
            # Parse timestamp
            timestamp = datetime.strptime(timestamp_str, "%H:%M:%S")
            
            return timestamp, job_description.strip(), status, pid
        return None

    def process_logs(self):
        """
        Process the log file, tracking start and end times for each job
        """
        with open(self.log_file, "r") as file:
            for line in file:
                parsed = self.parse_log_line(line.strip())
                if parsed:
                    timestamp, job_description, status, pid = parsed
                    
                    if pid not in self.jobs:
                        self.jobs[pid] = {'description': job_description}
                    
                    if status == "START":
                        self.jobs[pid]['start'] = timestamp
                    elif status == "END":
                        self.jobs[pid]['end'] = timestamp
                
    def calculate_durations(self):
        """
        Calculate the duration of each job and store it in self.job_durations
        """
        for pid, job_info in self.jobs.items():
            if 'start' in job_info and 'end' in job_info:
                duration = job_info['end'] - job_info['start']
                self.job_durations[pid] = duration
                
                
    def save_results(self):
        """
        Save the results to a CSV file
        """
        with open("job_durations.csv", "w") as file:
            file.write("Type,PID,Job Name,Duration\n")
            for pid, duration in self.job_durations.items():
                
                duration_seconds = duration.total_seconds()
                if self.error_threshold > duration_seconds > self.warning_threshold :
                    file.write(f"WARNING,{pid},{self.jobs[pid]['description']},{duration}\n")
                elif duration_seconds > self.error_threshold:
                    file.write(f"ERROR,{pid},{self.jobs[pid]['description']},{duration}\n")

    

    def run(self):
        """
        Run the complete monitoring process
        """
        logging.info(f"Starting log monitoring of {self.log_file}")
        self.process_logs()
        self.calculate_durations()
        self.save_results()
        logging.info(f"Log monitoring complete.")


if __name__ == "__main__":
    monitor = LogMonitor("logs.log")
    monitor.run()
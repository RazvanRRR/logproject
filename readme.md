Python3 project for parsing logs from file logs.log
1.Create regexp pattern to parse logs.log file
2.Create function that will parse the each log line and return timestamp, job_description.strip(), status, pid, job_key
3.Create function that will process the log file, tracking start and end times for each job and return a dictionary with the following structure:
{
    "job_key": {
        "description": "job description",
        "pid": "PID",
        "start": "start time",
        "end": "end time"
    }
}


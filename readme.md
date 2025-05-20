Python3 project for parsing logs from file logs.log
1.Create regexp pattern to parse logs.log file
2.Create function that will parse the each log line and return timestamp, job_description.strip(), status, pid
3.Create function that will process the log file, tracking start and end times for each job and return a dictionary with the following structure:
{
    "pid":
        "description": "job description",
        "start": "start time",
        "end": "end time"
    }
}
4.Create function that will calculate the duration of each job and store it in self.job_durations
5.Create function that will save and filter the results to a csv file

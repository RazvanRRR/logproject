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
6 Create unit tests for 2 functions

Running the app:
python3 app.py logs.log

Running the tests:
python3 unit_testing.py

Future Improvements:
1. Add logging to the unit tests
2. Add more unit tests
3. Add integration tests
4. Add black box testing
5. Add more logging to the app.
6. Add custom colums for the csv file like (background job wmy) 
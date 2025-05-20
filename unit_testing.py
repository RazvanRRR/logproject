#!/usr/bin/env python3
import unittest
import os
import tempfile
from app import LogMonitor

class LogMonitorTest(unittest.TestCase):
    def setUp(self):
        # Create simple test data with just the essentials:
        # - One short job (33s)
        # - One job that triggers warning (3m 33s)
        # - One job that triggers error (14m 46s)
        test_log = """11:35:23,short job, START,10001
11:35:56,short job, END,10001
11:50:09,warning job, START,10002
11:56:42,warning job, END,10002
11:36:58,error job, START,10003
11:51:44,error job, END,10003
"""
        # Create a temporary test file
        self.temp_fd, self.temp_path = tempfile.mkstemp(suffix='.log')
        os.write(self.temp_fd, test_log.encode('utf-8'))
        
        # Create a monitor with specific thresholds for testing
        self.monitor = LogMonitor(self.temp_path, 
                                 warning_threshold_minutes=5, 
                                 error_threshold_minutes=10)
        
        # Process logs and calculate durations
        self.monitor.process_logs()
        self.monitor.calculate_durations()
        
    def tearDown(self):
        os.close(self.temp_fd)
        os.unlink(self.temp_path)
    
    def test_duration_calculation(self):
        """Test job duration calculation is accurate"""
        # Check we have 3 job durations
        self.assertEqual(len(self.monitor.job_durations), 3)
        
        # Verify specific durations
        self.assertIn('10001', self.monitor.job_durations)  # Short job
        self.assertIn('10002', self.monitor.job_durations)  # Warning job
        self.assertIn('10003', self.monitor.job_durations)  # Error job
        
        # Check durations match expected values (within 1 second tolerance)
        short_duration = self.monitor.job_durations['10001'].total_seconds()
        warning_duration = self.monitor.job_durations['10002'].total_seconds()
        error_duration = self.monitor.job_durations['10003'].total_seconds()
        
        self.assertEqual(short_duration, 33)
        self.assertEqual(warning_duration, 6*60 + 33)
        self.assertEqual(error_duration, 14*60 + 46)
    
    def test_threshold_detection(self):
        """Test threshold detection for warnings and errors"""
        # Get durations
        short_duration = self.monitor.job_durations['10001'].total_seconds()
        warning_duration = self.monitor.job_durations['10002'].total_seconds()
        error_duration = self.monitor.job_durations['10003'].total_seconds()
        
        # Short job should be below warning threshold
        self.assertLess(short_duration, self.monitor.warning_threshold)
        
        # Warning job should exceed warning but not error threshold
        self.assertGreater(warning_duration, self.monitor.warning_threshold)
        self.assertLess(warning_duration, self.monitor.error_threshold)
        
        # Error job should exceed error threshold
        self.assertGreater(error_duration, self.monitor.error_threshold)

if __name__ == '__main__':
    unittest.main()

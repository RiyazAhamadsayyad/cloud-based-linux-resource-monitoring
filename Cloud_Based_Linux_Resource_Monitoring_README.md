# Cloud-Based Linux Resource Monitoring and Auto-Scaling

A Linux-based resource monitoring and auto-scaling project that collects CPU, memory, and disk usage, stores monitoring data, detects resource thresholds, generates usage graphs, and provides a Flask web dashboard. The project can be tested locally on Linux and later deployed to AWS EC2 with CloudWatch and Auto Scaling.

## 1. Project Overview

Modern cloud applications need to monitor server resources continuously and respond when resource utilization becomes too high or too low.

This project implements a monitoring and scaling workflow:

```text
Linux Server
     |
     v
Python Resource Monitor
     |
     +---- CPU
     +---- Memory
     +---- Disk
     |
     v
CSV Logs
     |
     v
Threshold Detection
     |
     +---- High Usage ---> Scale Up
     |
     +---- Low Usage ----> Scale Down
     |
     v
Flask Web Dashboard
```

For the cloud version, the architecture can be extended with:

```text
                    Internet
                       |
                       v
                Load Balancer
                       |
             +---------+---------+
             |                   |
             v                   v
          EC2 #1              EC2 #2
             |                   |
             +---------+---------+
                       |
                       v
                   CloudWatch
                       |
                       v
                Auto Scaling
                       |
                       v
                  New EC2
```

## 2. Objectives

- Monitor Linux CPU utilization.
- Monitor RAM utilization.
- Monitor disk utilization.
- Store resource metrics in CSV format.
- Detect high and low resource utilization.
- Generate CPU, memory, and disk graphs.
- Provide a browser-based monitoring dashboard.
- Test scaling decisions using controlled CPU load.
- Deploy the application on a Linux cloud server.
- Extend the system to AWS CloudWatch and EC2 Auto Scaling.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Linux/Ubuntu | Operating system and server environment |
| Python 3 | Application development |
| psutil | System resource monitoring |
| Pandas | Data processing |
| Matplotlib | Graph generation |
| Flask | Web dashboard |
| Git/GitHub | Version control and project management |
| AWS EC2 | Cloud Linux server |
| AWS CloudWatch | Cloud monitoring |
| AWS Auto Scaling | Automatic instance scaling |
| AWS Load Balancer | Traffic distribution |

## 4. Project Structure

```text
linux-monitoring/
|
+-- monitor/
|   +-- system_monitor.py
|   +-- autoscaler.py
|   +-- create_graph.py
|
+-- dashboard/
|   +-- app.py
|   +-- templates/
|       +-- index.html
|
+-- logs/
|   +-- metrics.csv
|
+-- graphs/
|   +-- cpu_usage.png
|   +-- memory_usage.png
|   +-- disk_usage.png
|
+-- venv/
|
+-- requirements.txt
+-- README.md
```

## 5. Requirements

Recommended:

- Ubuntu or another Debian-based Linux distribution
- Python 3
- pip
- Python virtual environment support
- Git
- At least 2 GB RAM for comfortable development
- Internet connection
- AWS account for the optional cloud deployment stage

## 6. Installation on Linux

### Step 1: Update the system

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install required Linux packages

```bash
sudo apt install python3 python3-pip python3-venv git htop sysstat stress -y
```

Verify:

```bash
python3 --version
pip3 --version
git --version
stress --version
```

### Step 3: Create the project

```bash
mkdir -p ~/linux-monitoring/{monitor,dashboard,logs,graphs}
cd ~/linux-monitoring
```

### Step 4: Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

When activated, the terminal should show `(venv)`.

### Step 5: Install Python dependencies

```bash
pip install psutil pandas matplotlib flask
```

Save the dependencies:

```bash
pip freeze > requirements.txt
```

## 7. System Monitoring

The `system_monitor.py` program reads CPU, memory, and disk utilization using `psutil`.

Run:

```bash
cd ~/linux-monitoring
source venv/bin/activate
python3 monitor/system_monitor.py
```

Example output:

```text
Linux Resource Monitor Started
Press Ctrl+C to stop

2026-09-20 15:00:01 | CPU: 18.0% | RAM: 42.3% | Disk: 36.1%
2026-09-20 15:00:04 | CPU: 21.0% | RAM: 42.5% | Disk: 36.1%
2026-09-20 15:00:07 | CPU: 16.0% | RAM: 42.4% | Disk: 36.1%
```

Metrics are stored in:

```text
logs/metrics.csv
```

View the data:

```bash
cat logs/metrics.csv
```

Stop the monitor with:

```text
Ctrl + C
```

## 8. Auto-Scaling Logic

The `autoscaler.py` program checks CPU and RAM utilization against configured thresholds.

Default thresholds:

```text
CPU > 80%  -> Scale Up
RAM > 80%  -> Scale Up
CPU < 30%  -> Scale Down
Otherwise  -> Normal
```

Run:

```bash
python3 monitor/autoscaler.py
```

Example:

```text
CPU: 22.0% | RAM: 43.0%
LOW RESOURCE USAGE
SCALE DOWN TRIGGERED
```

or:

```text
CPU: 91.0% | RAM: 45.0%
HIGH RESOURCE USAGE
SCALE UP TRIGGERED
```

### Important note

In the local implementation, "scale up" and "scale down" are monitoring decisions/logical triggers. They do not create or terminate physical machines on your laptop.

Actual cloud instance scaling is handled in the AWS deployment stage using services such as EC2 Auto Scaling and CloudWatch.

## 9. Testing High CPU Usage

Open a second terminal.

Run:

```bash
stress --cpu 4 --timeout 30
```

While the stress test is running, execute:

```bash
python3 monitor/autoscaler.py
```

The CPU utilization should increase and the application should eventually report:

```text
HIGH RESOURCE USAGE
SCALE UP TRIGGERED
```

This provides a simple demonstration of threshold-based scaling logic.

## 10. Generate Resource Graphs

After collecting monitoring data, run:

```bash
python3 monitor/create_graph.py
```

The application generates:

```text
graphs/cpu_usage.png
graphs/memory_usage.png
graphs/disk_usage.png
```

These graphs can be included in the project report.

## 11. Run the Flask Dashboard

Start the dashboard:

```bash
python3 dashboard/app.py
```

The application runs on:

```text
http://127.0.0.1:5000
```

Open that address in a browser.

The dashboard displays:

- CPU utilization
- Memory utilization
- Disk utilization
- Current resource status

For example:

```text
Linux Resource Monitoring Dashboard

CPU       22%
Memory    43%
Disk      36%

Status: NORMAL
```

## 12. Running the Complete Local Project

Use separate terminal windows.

### Terminal 1 - Resource Monitor

```bash
cd ~/linux-monitoring
source venv/bin/activate
python3 monitor/system_monitor.py
```

### Terminal 2 - Auto-Scaler

```bash
cd ~/linux-monitoring
source venv/bin/activate
python3 monitor/autoscaler.py
```

### Terminal 3 - Flask Dashboard

```bash
cd ~/linux-monitoring
source venv/bin/activate
python3 dashboard/app.py
```

### Terminal 4 - Optional CPU stress test

```bash
stress --cpu 4 --timeout 30
```

Open the dashboard:

```text
http://127.0.0.1:5000
```

## 13. AWS Cloud Deployment

The local version can be deployed to an AWS EC2 Linux server.

### Step 1: Create an EC2 instance

In the AWS Console:

1. Open EC2.
2. Choose "Launch instance".
3. Select an Ubuntu Server AMI.
4. Select an instance type appropriate for your account and current AWS pricing/free-tier eligibility.
5. Create or select an SSH key pair.
6. Configure the security group.
7. Launch the instance.

For direct Flask testing, port `5000` can be allowed from your own IP address. SSH uses port `22`.

For production-style deployment, it is preferable to put the application behind a web server/load balancer rather than exposing Flask's development server directly.

### Step 2: Connect through SSH

AWS provides an SSH command similar to:

```bash
ssh -i "your-key.pem" ubuntu@YOUR_PUBLIC_IP
```

If required:

```bash
chmod 400 your-key.pem
```

### Step 3: Install dependencies on EC2

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

Clone the project:

```bash
git clone YOUR_GITHUB_REPOSITORY
cd linux-monitoring
```

Create the environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Start the dashboard

```bash
python3 dashboard/app.py
```

For development/testing, access:

```text
http://YOUR_PUBLIC_IP:5000
```

## 14. AWS Auto-Scaling Extension

For the full cloud implementation, the recommended architecture is:

```text
                         Internet
                            |
                            v
                    Application Load
                        Balancer
                            |
               +------------+------------+
               |                         |
               v                         v
            EC2 #1                    EC2 #2
               |                         |
               +------------+------------+
                            |
                            v
                        CloudWatch
                            |
                    CPU utilization
                            |
                            v
                    Auto Scaling Group
                            |
                            v
                      EC2 #3 / etc.
```

AWS CloudWatch can monitor instance metrics such as CPU utilization. An EC2 Auto Scaling Group can then add or remove instances according to configured policies.

The Python local auto-scaler remains useful as the project's custom monitoring and threshold demonstration, while AWS services perform actual infrastructure scaling.

## 15. Suggested Auto-Scaling Policy

A simple demonstration policy can be:

```text
CPU >= 80%
    |
    +--> Scale Out

CPU <= 30%
    |
    +--> Scale In
```

For a real deployment, use cooldown/stabilization behavior and appropriate minimum/maximum instance counts to avoid rapid scaling oscillations.

## 16. Testing Plan

### Test 1: Normal usage

Expected:

```text
CPU < 80%
RAM < 80%
Status = NORMAL
```

### Test 2: High CPU

Command:

```bash
stress --cpu 4 --timeout 30
```

Expected:

```text
CPU > 80%
SCALE UP TRIGGERED
```

### Test 3: Low CPU

Stop heavy workloads.

Expected:

```text
CPU < 30%
SCALE DOWN TRIGGERED
```

### Test 4: Dashboard

Open:

```text
http://127.0.0.1:5000
```

Expected:

- CPU value displayed
- Memory value displayed
- Disk value displayed
- Status displayed

### Test 5: Cloud deployment

Expected:

- EC2 instance is running.
- Application is reachable.
- Monitoring data is collected.
- CloudWatch receives metrics.
- Auto Scaling responds according to the configured policy.

## 17. Expected Results

The completed project should demonstrate:

1. Real-time Linux CPU monitoring.
2. Real-time memory monitoring.
3. Disk utilization monitoring.
4. Persistent metric logging.
5. Resource utilization graphs.
6. Threshold-based scaling decisions.
7. Browser-based monitoring.
8. Linux cloud-server deployment.
9. Cloud monitoring through AWS.
10. Automatic instance scaling using AWS Auto Scaling.

## 18. Advantages

- Lightweight Python implementation.
- Easy to understand and demonstrate.
- Works directly on Linux.
- Can be extended to cloud environments.
- Provides both command-line and web-based monitoring.
- Useful for learning Linux administration, Python automation, cloud computing, and DevOps concepts.

## 19. Limitations

- The local version does not create or remove physical machines.
- Flask's built-in server is intended for development/testing, not production.
- CSV storage is suitable for a student project but not ideal for large-scale monitoring.
- Production systems should use a dedicated metrics/monitoring stack and secure service deployment.
- AWS resources can incur charges; monitor and remove resources after testing.

## 20. Future Enhancements

Possible extensions include:

- Prometheus and Grafana integration.
- Real-time charts using JavaScript.
- Email or notification alerts.
- Database storage instead of CSV.
- Docker containerization.
- Kubernetes deployment.
- AWS CloudWatch dashboards.
- Application Load Balancer integration.
- HTTPS/TLS.
- Authentication for the dashboard.
- More advanced scaling policies.
- Monitoring multiple Linux servers.

## 21. Useful Commands

Activate the project:

```bash
cd ~/linux-monitoring
source venv/bin/activate
```

Run monitor:

```bash
python3 monitor/system_monitor.py
```

Run auto-scaler:

```bash
python3 monitor/autoscaler.py
```

Generate graphs:

```bash
python3 monitor/create_graph.py
```

Run dashboard:

```bash
python3 dashboard/app.py
```

View metrics:

```bash
cat logs/metrics.csv
```

Check Linux CPU/RAM interactively:

```bash
htop
```

Check memory:

```bash
free -h
```

Check disk:

```bash
df -h
```

Test CPU load:

```bash
stress --cpu 4 --timeout 30
```

Stop a running Python application:

```text
Ctrl + C
```

Deactivate virtual environment:

```bash
deactivate
```

## 22. Conclusion

The Cloud-Based Linux Resource Monitoring and Auto-Scaling project demonstrates how Linux system resources can be monitored programmatically and how resource thresholds can be used to make scaling decisions.

The local implementation provides the foundation for CPU, memory, disk monitoring, logging, visualization, and dashboard development. The cloud extension uses AWS EC2, CloudWatch, and Auto Scaling to demonstrate how the same concept can be applied to scalable cloud infrastructure.

## 23. Author

**Project:** Cloud-Based Linux Resource Monitoring and Auto-Scaling

**Platform:** Linux / Ubuntu

**Language:** Python

**Cloud Platform:** AWS

**Academic Project:** M.Tech Project

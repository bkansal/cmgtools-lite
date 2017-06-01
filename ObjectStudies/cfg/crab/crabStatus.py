#!/usr/bin/env python2.6

# crabStatus.py <options> DIRECTORY
# Wrapper around crab status which allows to use filters on output and automatic resubmissions

import os
from optparse import OptionParser

#Option parser
parser = OptionParser()
parser.add_option("-n", "--noStatusCheck", action="store_false", dest="checkCrab", default = True, help="Crab status is not re-checked (fast debug option)")
parser.add_option("-j", "--job", dest="jobs", default = "All", help="filter on job numbers")
parser.add_option("-s", "--state", dest="state", default="All", help="filter on state")
parser.add_option("-e", "--exitCode", dest="exitCode", default="All", help="filter on exitCode")
#parser.add_option("-b", "--blacklist", dest="blacklist", default="", help="blacklist E_HOST")
#parser.add_option("-k", "--kill", action="store_true", dest="kill", default = False, help="Kill the (selected) jobs")
#parser.add_option("-r", "--resubmit", action="store_true", dest="resubmit", default = False, help="Resubmit the (selected) jobs")
#parser.add_option("-f", "--forceResubmit", action="store_true", dest="forceResubmit", default = False, help="Force resubmit the (selected) jobs")
(options, args) = parser.parse_args()

# changing python list to crab list
def jobsToCrabList(jobs):
  crabList = ""
  for i in jobs:
    if crabList == "": crabList = format(i) 
    else:
      pythonRange = crabList.split(',')[-1]
      last = pythonRange.split('-')[-1]
      if i == int(last) + 1: 
        if pythonRange.split('-')[0] == last: crabList += '-' + format(i)
        else: crabList = crabList.replace(last, format(i))
      else: crabList += "," + format(i)
  return crabList

# changing crab list to python list
def jobsToPythonList(jobs):
  pythonList = []
  for crabRange in jobs.split(','):
    i = int(crabRange.split('-')[0])
    j = int(crabRange.split('-')[-1])
    while i <= j:
      pythonList.append(i)
      i+=1
  return pythonList

if options.checkCrab: 
  print "Getting the crab status..."
  if len(args) > 0: os.system("crab status --long " + args[0] + "> .status.txt")
  else:             os.system("crab status --long > .status.txt")
  

statusFile = open(".status.txt")
jobs = []
for str in statusFile:
  if 'jobs' in str: continue
  if len(str.split()) and str.split()[0].isdigit():
     jobs.append({ 'Job' : int(str.split()[0]), 'State' : str.split()[1], 'Exit code' : str.split()[-1], 'Str' : str})

# Filter on job numbers
if options.jobs != 'All':
  jobsToKeep = jobsToPythonList(options.jobs)
  jobs = [job for job in jobs if job['Job'] in jobsToKeep]

# Filter on state
if options.state != 'All':
  print options.state
  jobs = [job for job in jobs if job['State'] in options.state]

# Filter on exit code
if options.exitCode != 'All':
  jobs = [job for job in jobs if job['Exit code'] in options.exitCode]

# Print out
print " Job State        Most Recent Site        Runtime   Mem (MB)      CPU %    Retries   Restarts      Waste       Exit Code"
for job in jobs: print job['Str'],

# Automatic resubmissions
jobsToResubmit = []
for job in jobs:
  if job['Exit code'] in ['60317','60307','60302','10030','10040','50115']: jobsToResubmit.append(job['Job'])
  if job['State'] == 'failed' and job['Exit code'] == '0':                  jobsToResubmit.append(job['Job'])

if len(jobsToResubmit) > 0:
  print "Resubmitting " + jobsToCrabList(jobsToResubmit)
  if len(args) > 0: os.system("crab resubmit --jobids=" + jobsToCrabList(jobsToResubmit) + " " +  args[0])
  else:             os.system("crab resubmit --jobids=" + jobsToCrabList(jobsToResubmit))

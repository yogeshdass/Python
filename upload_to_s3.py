from imgkit import from_file
import boto3
import os
import magic

# to be removed
BUILD_NUMBER = 104

bucket = boto3.resource('s3').Bucket('cucumberpoc')
fname = "CucumberexecutionReport_BuildNo_"+str(BUILD_NUMBER)
buildIndex = "/endtoend_cucumberframework/target/site/cucumber-reports/cucumber-html-reports/overview-features.html"

build = set()
timestamp = dict()

# Upload New Directory recursively
for subdir, dirs, files in os.walk(fname):
    for file in files:
        full_path = os.path.join(subdir, file)
        with open(full_path, 'rb') as data:
            key = fname+"/"+full_path[len(fname)+1:]
            print(F"Uploading {key}")
            print(magic.from_file(key, mime=True))
            bucket.put_object(Key=key, Body=data, ContentType=magic.from_file(key, mime=True))

# Get all Directories in the Bucket
for _ in bucket.objects.all():
    element = _.key.split('/')[0]
    if "." not in element:
        build.add(element)

# Get all Directories Timestamp
for i in build:
    for _ in bucket.objects.all():
        if _.key in i+buildIndex:
            timestamp.update({i: _.last_modified})

print(F"ALL Builds are: {build}")
print(F"Respective Timestamps are: {timestamp}")

# Base template
contents = [
    '<table style="width:50%"><tr><th>Cucumber-Reports</th><th>TimeStamp</th></tr>',
    '</table>',
    '<style>table, th, td {border: 1px solid black;}</style>',
]

# Genrate the index.html
for _ in build:
    contents.insert(1, F"<tr><td><a href=\"{_+buildIndex}\">{_}</a></td><td>{timestamp[_]}</td></tr>")
print(F"Generated index.html :--> {contents}")

# Create the index.html
f = open("index.html", "w")
contents = "".join(contents)
f.write(contents)
f.close()

# Upload the New index.html
bucket.put_object(Key='index.html', Body=contents, ContentType='text/html')
# Create the JPEG to be sent in email body
from_file(fname+buildIndex, 'out.jpg')

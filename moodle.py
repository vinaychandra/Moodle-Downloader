import cookielib
import urllib2
import urllib
import os
import os.path
import re

from bs4 import BeautifulSoup


root_directory = "<Root Directory full path>"
username = "<LDAP Username>"
password = "<LDAP Password>"
authentication_url = "http://moodle.iitb.ac.in/login/index.php"

# Store the cookies and create an opener that will hold them
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# Add our headers
opener.addheaders = [('User-agent', 'Moodle-Crawler')]

# Install our opener (note that this changes the global opener to the one
# we just made, but you can also just call opener.open() if you want)
urllib2.install_opener(opener)


# Input parameters we are going to send
payload = {
    'username': username,
    'password': password
}

# Use urllib to encode the payload
data = urllib.urlencode(payload)

# Build our Request object (supplying 'data' makes it a POST)
req = urllib2.Request(authentication_url, data)

# Make the request and read the response
response = urllib2.urlopen(req)
contents = response.read()

# Verify the contents
if "My courses" not in contents:
    print "Cannot connect to moodle"
    exit(1)

courses = contents.split("<h2>My courses</h2>")[1].split('<aside id="block-region-side-pre" ')[0]

regex = re.compile('<h3 class="coursename">(.*?)</h3>')
course_list = regex.findall(courses)
courses = []

for course_string in course_list:
    soup = BeautifulSoup(course_string)
    a = soup.find('a')
    course_name = a.text
    course_link = a.get('href')
    courses.append([course_name, course_link])

for course in courses:
    if not os.path.isdir(root_directory + course[0]):
        os.mkdir(root_directory+course[0])
    response1 = urllib2.urlopen(course[1])
    scrap = response1.read()
    soup = BeautifulSoup(scrap)

    course_links = soup.find(class_="course-content").find(class_="weeks").find_all('a')

    for link in course_links:
        current_dir = root_directory + course[0] + "/"
        href = link.get('href')

        # Checking only resources... Ignoring forum and folders, etc
        if "resource" in href:
            cj1 = cookielib.CookieJar()
            opener1 = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj1))

            # Add our headers
            opener1.addheaders = [('User-agent', 'Moodle-Crawler')]

            # Install our opener (note that this changes the global opener to the one
            # we just made, but you can also just call opener.open() if you want)
            urllib2.install_opener(opener1)

            # The action/ target from the form
            authentication_url1 = href

            # Build our Request object (supplying 'data' makes it a POST)
            req1 = urllib2.Request(authentication_url, data)

            # Make the request and read the response
            resp = urllib2.urlopen(req1)

            webFile = urllib2.urlopen(href)
            url = current_dir + webFile.geturl().split('/')[-1].split('?')[0]
            file_name = urllib.unquote(url).decode('utf8')
            if os.path.isfile(file_name):
                print "File found : ", file_name
                continue
            print "Creating file : ", file_name
            pdfFile = open(file_name, 'wb')
            pdfFile.write(webFile.read())
            webFile.close()
            pdfFile.close()
print "Update Complete"

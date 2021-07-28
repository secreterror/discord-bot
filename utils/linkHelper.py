from pysondb import db
a=db.getDb("db.json")


#links for courses
courses=['ml','adsa','bm','hci','oe','pe']
labCourse=['ml-lab','adsa-lab']


#commands
GET_LINK="!getLink"
UPDATE_LINK='!updateLink'

#Sections
ITA='it-a'
ITB='it-b'
NOSECTION='NO-SECTION-ASSIGNED'

subsections=['it-1','it-2','it-3','it-4','it-5','it-6']
sections=['it-a','it-b']

def isValidCommand(message,command):
    messageContent=message.content.split()
    messageLength=len(command)

    if command==GET_LINK:
        if len(messageContent)!=2:
            return False
        #for one white space
        messageLength=messageLength+1
        course=messageContent[1]
        messageLength=messageLength+len(course)

        if len(message.content)!=messageLength:
            return False
        return True
    else:
        if len(messageContent)!=3:
            return False
        messageLength=messageLength+3
        course=messageContent[1]
        link=messageContent[2]
        messageLength=messageLength+len(course)+len(link)
        
        if len(message.content)!=messageLength:
            return False
        return True

def isValidCourse(course):
    if course in courses:
        return True
    return False
def isValidLabCourse(course):
    if course in labCourse:
        return True
    return False

def isCourseInDb(course,section,subsection):
    courses=a.getBy({"course":course,"section":section,"subsection":subsection})
    if len(courses)==0:
        return False
    return True

def isCr(roles):
    cr='admin'
    for role in roles:
        if role.name==cr:
            return True
    return True

def getSection(roles):
    for role in roles:
        if role.name in sections:
            return role.name
    return NOSECTION

def isCallFromSection(channel):
    if channel in sections:
        return True

def isCallFromSubSection(channel):
    if channel in subsections:
        return True

def getSubsection(roles):
    for role in roles:
        if role.name in subsections:
            return role.name
    return NOSECTION

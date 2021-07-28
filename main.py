import os

import discord
from dotenv import load_dotenv
from pysondb import db

a=db.getDb("db.json")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

from utils.linkHelper import GET_LINK,UPDATE_LINK
from utils.linkHelper import isCourseInDb,isValidCommand,isCr,isValidCourse,getSection,isCallFromSection,isCallFromSubSection,getSubsection,isValidLabCourse
from utils.linkHelper import ITA,ITB,NOSECTION
from utils.linkConstant import NOT_A_VALID_COURSE,YOU_ARE_NOT_A_CR,SUBSECTION_NOT_ASSIGNED,SECTION_NOT_ASSIGNED,LINK_ADDED,LINK_UPDATED,NO_LINKS_AVAILABLE




@client.event
async def on_message(message):

    messageContent=message.content.split()
    roles=message.author.roles
    channel=message.channel.name

    if isCallFromSection(channel) or isCallFromSubSection(channel):

        if message.content.startswith(GET_LINK):

            if isValidCommand(message,GET_LINK):

                course=messageContent[1]
                section=channel

                if isValidCourse(course) or isValidLabCourse(course):

                    if isCallFromSection(channel):
                        if isValidLabCourse(course):
                            return await message.channel.send('Please ask for this link in your subsection channel')
                        link=a.getBy({"section":section,"course":course})
                    else:
                        if isValidCourse(course):
                            return await message.channel.send('Please ask for this link in your section channel')
                        link=a.getBy({"subsection":section,"course":course})
                    if len(link)!=0:
                        print('here')
                        return await message.channel.send("hey, {} your {} link is {}".format(message.author.mention,course,link[0]['link']))
                    else:
                        return await message.channel.send(NO_LINKS_AVAILABLE)
                else:
                    return await message.channel.send(NOT_A_VALID_COURSE)
    
        elif message.content.startswith(UPDATE_LINK):
            
            if isValidCommand(message,UPDATE_LINK):
                course=messageContent[1]
                link=messageContent[2]
                section=getSection(roles)
                subsection=getSubsection(roles)

                if isCr(roles)==False:
                    return await message.channel.send(YOU_ARE_NOT_A_CR)
                if section==NOSECTION:
                    return await message.channel.send(SECTION_NOT_ASSIGNED)
                if subsection==NOSECTION:
                    return await message.channel.send(SUBSECTION_NOT_ASSIGNED)
                
                
                if isValidCourse(course) or isValidLabCourse(course):
                    if isCourseInDb(course,section,subsection):
                        #update
                        a.update({
                            "subsection":subsection,
                            "section":section,
                            "course":course
                        },{
                            "link":link
                        })
                        return await message.channel.send(LINK_UPDATED)
                    else:
                        a.add({
                            "subsection":subsection,
                            "section":section,
                            "course":course,
                            "link":link
                        })
                        return await message.channel.send(LINK_UPDATED)
                else:
                    return await message.channel.send(NOT_A_VALID_COURSE)



  
client.run(TOKEN)
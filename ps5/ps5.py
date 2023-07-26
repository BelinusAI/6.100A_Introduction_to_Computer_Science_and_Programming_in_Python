# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
            pubdate = pubdate.astimezone(pytz.timezone('EST'))
            pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory():
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase) :
        Trigger.__init__(self)
        self.phrase = phrase.lower()
    
    def get_phrase(self):
        return self.phrase
    
    def is_phrase_in(self, text):
        unwanted = string.punctuation
        for i in unwanted:
            text = text.replace(i, " ")
        text = text.split()
        text = " ".join(text).lower() + " "

        return (self.get_phrase() + " ") in text
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError
      

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS
# Problem 5
class TimeTrigger(Trigger):
    # Constructor:
    #Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
    #Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, time) :
        Trigger.__init__(self)
        self.time = datetime.strptime(time, "%d %b %Y %X").replace(tzinfo=pytz.timezone("EST"))
 

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError



# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) < self.time

class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) > self.time

# COMPOSITE TRIGGERS
# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger) :
        Trigger.__init__(self)
        self.trigger = trigger

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2) :
        Trigger.__init__(self)
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2) :
        Trigger.__init__(self)
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    stories_filtered = []
    for story in stories:
        for trigger in triggerlist:
            if(trigger.evaluate(story)):
                stories_filtered.append(story)
    return stories_filtered

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    triggers = {}  
    result = []   
    for line in lines:
        arguments = line.split(',')  
        if arguments[0] == 'ADD':
            for trigger_name in arguments[1:]:
                result.append(triggers[trigger_name])
        elif arguments[1] == 'TITLE':
            triggers[arguments[0]] = TitleTrigger(arguments[2])
        elif arguments[1] == 'DESCRIPTION':
            triggers[arguments[0]] = DescriptionTrigger(arguments[2])
        elif arguments[1] == 'AFTER':
            triggers[arguments[0]] = AfterTrigger(arguments[2])
        elif arguments[1] == 'BEFORE':
            triggers[arguments[0]] = BeforeTrigger(arguments[2])
        elif arguments[1] == 'NOT':
            triggers[arguments[0]] = NotTrigger(triggers[arguments[2]])
        elif arguments[1] == 'AND':
            triggers[arguments[0]] = AndTrigger(triggers[arguments[2]], triggers[arguments[3]])
        elif arguments[1] == 'OR':
            triggers[arguments[0]] = OrTrigger(triggers[arguments[2]], triggers[arguments[3]])
            
    return result

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("Abortion")
        # t2 = DescriptionTrigger("Colombia")
        # t3 = DescriptionTrigger("Petro")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]
        
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()



    
    
        
    
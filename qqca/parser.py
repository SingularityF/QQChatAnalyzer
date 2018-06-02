from dateutil import parser as dateparser
import re

def read_chat_log(filename):
    file=open(filename,"r",encoding="utf-8")
    content=file.read()
    file.close()
    return content

# Is this string the info line preceding a message
def is_info_format(str):
    return True if re.search(r"\d{4}-\d{2}-\d{2} \d+:\d{2}:\d{2} \wM",str) else False

# Extract the year, month and day from a info line
def get_date(str):
    (year,month,day)=re.findall(r"(\d{4})-(\d{2})-(\d{2})",str)[0]
    return (int(year),int(month),int(day))

# Get the LOCAL time from a info line
def get_time(str):
    datetime=dateparser.parse(re.findall(r"(\d+:\d{2}:\d{2} \wM)",str)[0])
    return (datetime.hour,datetime.minute,datetime.second)

# Likewise
def get_qq_id(str):
    return re.findall(r"\((\d+)\)",str)[0]

# Likewise
def get_nickname(str):
    nickname=re.findall(r"M(.*?)\(",str)[0]
    return nickname.strip()

def filter_by_month(year,month,content):
    isinside=False
    subcontent=""
    for line in content.split("\n"):
        if is_info_format(line):
            if get_date(line)[0]==year and get_date(line)[1]==month:
                subcontent+=line
                subcontent+="\n"
                isinside=True
            else:
                isinside=False
        elif isinside:
            subcontent+=line
            subcontent+="\n"
    return subcontent

# Construct info and message list
def get_info_msg(content):
    first=True
    info_msg=[]
    info_cache=""
    msg_cache=""
    for line in content.split("\n"):
        if is_info_format(line):
            if not first:
                info_msg.append({"date":get_date(info_cache),"time":get_time(info_cache),"nickname":get_nickname(info_cache),"qqid":get_qq_id(info_cache),"message":msg_cache.strip()})
            else:
                first=False
            info_cache=line
            msg_cache=""
        else:
            msg_cache+=line
    if len(content)>0:
        info_msg.append({"date":get_date(info_cache),"time":get_time(info_cache),"nickname":get_nickname(info_cache),"qqid":get_qq_id(info_cache),"message":msg_cache.strip()})
    return info_msg

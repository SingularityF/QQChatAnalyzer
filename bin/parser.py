from dateutil import parser as dateparser

def read_chat_log(filename):
    file=open(filename,"r",encoding="utf-8")
    content=file.read()
    file.close()
    return(content)

# Is this string the info line preceding a message
def is_info_format(str):
    # Length AT LEAST 20
    if len(str)<20:
        return(False)
    if str[4]=="-" and str[7]=="-":
        for i in [0,1,2,3,5,6,8,9]:
            if not str[i].isdigit():
                return(False)
    else:
        return(False)
    return(True)

# Extract the year, month and day from a info line
def get_date(str):
    year=0
    month=0
    day=0
    if is_info_format(str):
        year=int(str[0:4])
        month=int(str[5:7])
        day=int(str[8:10])
    return (year,month,day)

# Get the LOCAL time from a info line
def get_time(str):
    hour=0
    minute=0
    second=0
    if is_info_format(str):
        substr=str[11:22]
        datetime=dateparser.parse(substr)
        hour=datetime.hour
        minute=datetime.minute
        second=datetime.second
    return (hour,minute,second)

# Likewise
def get_qq_id(str):
    qqid=0
    if is_info_format(str):
        substr=str[(str.index("(")+1):-1]
        qqid=int(substr)
    return(qqid)

# Likewise
def get_nickname(str):
    nickname=""
    if is_info_format(str) and 22!=str.index("("):
        substr=str[22:str.index("(")]
        nickname=substr.strip()
    return(nickname)

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
    return(subcontent)

# Construct info dictionary
def get_info_dict(content):
    infos=[]
    for line in content.split("\n"):
        if is_info_format(line):
            infos.append({"date":get_date(line),"time":get_time(line),"nickname":get_nickname(line),"qqid":get_qq_id(line)})
    return infos

import codecs
import requests
import re
from termcolor import colored

dict_data = [
        {'url': 'http://testinsane.com/', 'SOL': '<script', 'EOL': '</script>', 'block': 'file1.txt', 'keyword': ['www.google-analytics.com/analytics.js', 'GoogleAnalyticsObject']},
        {'url': 'http://testinsane.com/', 'SOL': '<li', 'EOL': '</li>',  'block': 'file2.txt', 'keyword': ['http://www.linkedin.com/company/test-insane']},
        {'url': 'http://testinsane.com/', 'SOL': '<nav>', 'EOL': '</nav>', 'keyword': ['sales@testinsane.com']},
        {'url': 'http://testinsane.com/', 'SOL': '<!', 'EOL': '>', 'keyword': ['Settings'], 'logall': True},
]

print(colored(
        "Guidelines\n"+
        "L1 : Exact match was found as recorded in the text file specified by the block field in test data\n"+
        "L2 : Match was found as recorded in the text file specified by the block field in test data but with some "
        "space and new line characters missing or added in fetched html data\n"+
        "L3 : No exact or almost Exact matches found. However the words specified by keyword field in test data were "
        "found in html fetched\n"+
        "No L1/L2/L3 : No matches were found\n",
        'red')
)

for entry in dict_data:
    Found = False
    LOGALL = False
    text = ''
    print('-----------------------------------------------------------------------------------------------------------')
    print('Test data entry : '+str(entry))

    url= entry['url']
    r = requests.get(url)
    if r.status_code == 200:
        print("HTML encoding : "+r.encoding)
        html =r.content.decode(encoding='utf-8',errors='replace')
        all_keys = entry.keys()
        if 'logall' in all_keys and entry['logall'] is True:
            LOGALL = True
        pattern = entry['SOL']+'.*?'+entry['EOL']
        script = re.compile(pattern, re.DOTALL | re.MULTILINE)
        if 'block' in all_keys:
            g=codecs.open(entry['block'],'rb',encoding='utf-8')
            text = g.read()
            g.close()
        res = script.findall(str(html))
        print("Matches Found with regular expression "+pattern+" : "+str(len(res)))
        for s in res:
            if LOGALL is True:
                print(s)
            if text != '' and s.find(text) != -1:
                print(colored('L1: Found match', 'green'))
                Found = True
                break
            s = re.sub('[\r\n\s]', '', s)
            temp = re.sub('[\r\n\s]', '', text)
            if text != '' and temp == s:
                print(colored("L2: Found match", 'blue'))
                Found = True
                break
            cnt = 0
            for keyword in entry['keyword']:
                if s.find(keyword) != -1:
                    print("Found "+str(keyword))
                    cnt+=1
            if cnt == len(entry['keyword']):
                print(colored("L3: Found match", 'yellow'))
                Found= True
                break
        if Found is True:
            print (colored("The exact or space and new line stripped html block which matched is :", 'magenta'))
            print (colored(s, 'cyan'))
        else:
            print (colored("L4 : No Match Found",'red'))

    else:
        print ('URL Error     :'+str(url))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import string
import requests
import time 
from datetime import date
from duplicate_text_extractor_from_link import *
from pdf_selector_update1 import *
# from fine_tuned import *
# from text_to_pdf import *

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 

def extension_for_url(country):
    df = pd.read_csv("D:\\Infoware\\Cyber_WebScrap_Oct\\May2023\\webscrap_try\\utils\\WebScrap.csv")
    key =[]
    for i in df['Country']:
        if country.replace(" ",'').lower() in i.lower().replace(" ",''):
            x = (df.loc[(df['Country'] == i )]).values.tolist()
            url_kwy = [i for i in x[0][1:] if str(i) != 'nan']
            key += url_kwy
    ke = list(set(key))
    return ke

def filter1(links,country_name):  
    https_links = [link for link in links if 'https://' in link.lower()] 
    authentic_site_extension = extension_for_url(country_name)
    print("extension name : ",authentic_site_extension)
    com_ex = ['.gov','.org','.eu','itu']
    c_ex = [i for i in authentic_site_extension if i not in com_ex]
    if len(c_ex) == 0:
        c_ex = ['.eu']
    first_stage_filter = [link for i in authentic_site_extension for link in https_links if i.lower() in link.lower()]
    first_stage_filter = https_links if len(first_stage_filter) == 0 else first_stage_filter
    filter1_links = list(set(first_stage_filter))
    return filter1_links,c_ex

def filter_sublinks(sublink_list,main_extension):
    df = pd.read_excel("D:\\Infoware\\Cyber_WebScrap_Oct\\May2023\\webscrap_try\\utils\\Regulator.xlsx", sheet_name='keywords')
    keyword_list = [i for i in df['Url_keywords'].tolist() if str(i) != 'nan']
    filter2_sublinks = []
    for keyword in keyword_list:
        y = keyword.translate(str.maketrans('', '', string.punctuation))
        for each_sublink in sublink_list:
            if main_extension in each_sublink:
                 filter2_sublinks.append(each_sublink)            
            x = each_sublink.translate(str.maketrans('', '', string.punctuation))
            if y.lower() in x.lower():
                filter2_sublinks.append(each_sublink)
    filter2_sublinks = list(set(filter2_sublinks))
    return filter2_sublinks

def filter3(link_list): 
    l = ['linkedin','facebook','twitter','youtube','instagram','wiki','contact','yahoo','whatsapp','login','signin','unodc','cyberwiser.eu']
    q = [link for link in link_list if any(ext in link for ext in l)]
    links = [i for i in link_list if i not in q]
    return links

def find_site_name(x):
    site_name = [j for j in x.split("/") if 'www' in j]
    return site_name

def unique_filter_links(list_of_links):
    un_web_site = []
    for i in list_of_links:
        site_name = find_site_name(i)
        res = any(site_name[0] in sub for sub in un_web_site)
        if res == False:
            un_web_site.append(i)
    return un_web_site

cwd = os.getcwd()

text_dir = 'D:\\Infoware\\Cyber_WebScrap_Oct\\May2023\\webscrap_try\\summary.txt'
with open(text_dir,'a') as document:
    raw_links=[]
    country_name = ''

    ans=int(input("Please Enter (1) for Google Search or (2) for direct link : "))
    if(ans==1):
        try:
            from googlesearch import search
        except ImportError:
            print("No module named 'google' found")
        print("Enter Country Name : ")
        user_response = input()                                                          
        country_name = user_response
        user_response = "cyber security policy/strategy in "+user_response
        print("user_responce >>> ",user_response)
        for j in search(user_response, tld="co.in", num=1, stop=10, pause=2):
            raw_links.append(j)    
    elif (ans==2):
        li=input("Please Enter The Link  : ")
        print("Enter country Name : ")
        country_name = input()
        raw_links.append(li)

    print("raw links >>>>>>>>>>>>>>>>>>>>>>>>>>>>> ",raw_links)

    filter1links,c_ex = filter1(raw_links,country_name)
    print("filter1links : ",filter1links)
    print("c_ex : ",c_ex)
    filter2links = filter_sublinks(filter1links,c_ex[0])

    filter3links = filter3(filter2links)
    # try:
    #     links = unique_filter_links(filter3links)
    # except:
    links = filter3links
    print("filter links >>>>>>>>>>>>>>>>>>>>>> ",links)

    # raw link filter out using authentic site extension corresponding country.


    main_flder = country_name.replace(" ","_")
    #subflder='CyberSecurity'
    try:
        path1 = f'D:\\Infoware\\Cyber_WebScrap_Oct\\May2023\\webscrap_try\\utils\\{main_flder}'
        isExistmain = os.path.exists(path1)
        if not isExistmain:
            os.mkdir(path1) 
        #path2 = f'/home/moka/Infoware/policy_pdf_scrapping/output/{main_flder}/{subflder}'
       # isExistsub = os.path.exists(path2)
        #if not isExistsub:
        #    os.mkdir(path2)  
        path3 = f'D:\\Infoware\\Cyber_WebScrap_Oct\\May2023\\webscrap_try\\utils\\{main_flder}\\policy'
        isExistsub_policy = os.path.exists(path3)
        if not isExistsub_policy:
            os.mkdir(path3)
        path4 = f'D:\\Infoware\\Cyber_WebScrap_Oct\\May2023\\webscrap_try\\utils\\{main_flder}\\strategy'
        isExistsub_strategy = os.path.exists(path4)
        if not isExistsub_strategy:
            os.mkdir(path4)
        path5 = f'D:\\Infoware\\Cyber_WebScrap_Oct\\May2023\\webscrap_try\\utils\\{main_flder}\\guildlines'
        isExistsub_guidlines = os.path.exists(path5)
        if not isExistsub_guidlines:
            os.mkdir(path5)         
    except:
        pass



    ## create a organised folder for different counrty and filed name "cybersecurity".
    link_pdf = {}
    for link in links:
        print("URL for policy ------------------>>>>>>> ",link)

        pdf_name_list = []
        pdf_from_sub_link = []
        name = str(link[8:]).replace("/","_")
        text_dir = f"{path1}/{name}.txt"

        driver = webdriver.Chrome('/home/moka/Infoware/policy_pdf_scrapping/Driver/chromedriver_linux64/chromedriver', options=options)
        driver.maximize_window()
        driver.get(link)
        time.sleep(10)
        current_link = driver.current_url

        if 'pdf' in current_link.lower():
            x = pdf_selector(link,path1,country_name)
            print("x >>>",x)
            if '.pdf' in x.lower():
                pdf_name_list.append(x)
            driver.quit()

        else:

            list_=[] 
            lnk=driver.find_elements(By.XPATH, "//a[@href]")
            try:
                for i in lnk:
                    list_.append(str(i.get_attribute('href'))) 
            except:
                pass
            final_list = [link]+list_
            sublink_list = list(set(final_list))
            driver.quit()

            # print("raw_sublink >>> ",sublink_list)
            print("sublink list :",len(sublink_list))
            Filter_Sublinks = filter_sublinks(sublink_list,c_ex[0])
            u_filter_sublinks = filter3(Filter_Sublinks)
            https_filtersublinks = [sublink for sublink in u_filter_sublinks if 'https://' in sublink.lower()]

            print("sublinks after filter >>>>>>>>>>>>>>> ",https_filtersublinks)
            print("len of filter sublink :",len(https_filtersublinks))

            pdf_from_sub_link = create_text_for_each_link(text_dir,https_filtersublinks,path1,country_name)

        pdf_for_link = pdf_name_list + pdf_from_sub_link
        if len(pdf_for_link)>0:
            link_pdf[link] = pdf_for_link

        print("-----------@----------@-----------@------------@----------@-----------@------------")

    print("summary >>>>>>>>>>> ",link_pdf)
    
    day = date.today()    
    document.write(str(day))
    document.write("\n\n")
    document.write(str(country_name))
    document.write("\n\n")
    document.write(f"Raw_link : {str(raw_links)}")
    document.write("\n\n")
    document.write(f"filter_link : {str(links)}")
    document.write("\n\n")
    document.write(f"pdf download summary from url : {str(link_pdf)}")
    document.write("\n\n\n\n")

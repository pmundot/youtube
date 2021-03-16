import numpy as np
import pandas as pd
import requests
import os, glob, sys
import matplotlib.pyplot as plt
import itertools
import more_itertools
from google_trans_new import google_translator
import argparse
import logging

rootlogger = logging.getLogger()
rootlogger.setLevel(logging.DEBUG)

fh = logging.FileHandler('autolog.log','w')
fh.setLevel(logging.DEBUG)
rootlogger.addHandler(fh)

sh = logging.StreamHandler()
sh.setLevel(logging.WARNING)
rootlogger.addHandler(sh)

class youtube:

    def __init__(self,files,given_country=None):
        logging.debug("initializing the class")
        self.given_country = given_country
        self.current = files
        self.cat = {2:"Autos & Vehicles",
        1:"Film & Animation",
        10:"Music",
        15:"Pets & Animals",
        17:"Sports",
        18:"Short Movies",
        19:"Travel & Events",
        20:"Gaming",
        21:"Videoblogging",
        22:"People & Blogs",
        23:"Comedy",
        24:"Entertainment",
        25:"News & Politics",
        26:"Howto & Style",
        27:"Education",
        28:"Science & Technology",
        29:"Nonprofits & Activism",
        30:"Movies",
        31:"Anime/Animation",
        32:"Action/Adventure",
        33:"Classics",
        34:"Comedy",
        35:"Documentary",
        36:"Drama",
        37:"Family",
        38:"Foreign",
        39:"Horror",
        40:"Sci-Fi/Fantasy",
        41:"Thriller",
        42:"Shorts",
        43:"Shows",
        44:"Trailers"}
        self.population = {
            'CA':37799407,
            'BR':212821986,
            'DE':5792202,
            'FR':65273511,
            'GB':67886011,
            'IN':1380004385,
            'JP':126476461,
            'KR':51276977,
            'MX':129166028,
            'RU':145945524,
            'US':331341050
        }
        self.colors = {
            'BR':'Green',
            'CA':'Red',
            'DE':'Blue',
            'FR':'Purple',
            'GB':'Brown',
            'IN':'Orange',
            'KR':'Black',
            'MX':'Teal',
            'RU':'Yellow',
            'US':'Crismson'}
    
    def files(self):
        logging.debug('getting files from current directory')
        os.chdir(self.current)
        self.li = []
        for file in glob.glob("*.csv", recursive = True):
            self.li.append(file)

    def reader(self,file):
        data = pd.read_csv(file)
        data['country']=[file[:2] for f in data['title']]
        data['catagory']=[self.cat[c] if c in self.cat else'Na' for c in data['categoryId']]
        data['color']=[self.colors[c] if c in self.cat else'White' for c in data['country']]
        return(data)

    def combine(self):
        self.files()

        comb = []
        size = 0
        for name in self.li:
            comb.append(self.reader(name))
            #print(name,'------',len(self.reader(name).index),'lines')
            #size += len(self.reader(name).index)
        #print("total size for top 30 videos in 11 countries is "+str(size)+" lines")
        self.result = pd.concat(comb, axis=0, ignore_index=True)
        logging.debug('getting files combined')
    
    def no_group(self):
        self.combine()
        logging.debug('No group has been called')
        return(self.result)

    def by_country(self):
        self.combine()
        logging.debug('by_country has been called')
        return(self.result.groupby(['country']).mean())

    def by_catagory(self):
        self.combine()
        logging.debug('by_catagory has been called')
        return(self.result.groupby(['catagory']).mean())

    def by_country_catagory(self):
        self.combine()
        logging.debug('by_country catagory has been called')
        return(self.result.groupby(['country','catagory']).mean())
    
    def country_tags_dic_sort(self):
        self.combine()
        country_tags_sublist = self.result.loc[self.result['country'] == self.given_country, 'tags'].tolist()
        for i in range(len(country_tags_sublist)):
            country_tags_sublist[i] = country_tags_sublist[i].split('|')
        country_tags_list = list(itertools.chain.from_iterable(country_tags_sublist))
        country_tags_dic = {}
        for j in country_tags_list:
            country_tags_dic[j] = country_tags_dic.get(j, 0) + 1
        country_tags_dic_sorted = dict(sorted(country_tags_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse = True))
        del country_tags_dic_sorted['[None]']
        return(country_tags_dic_sorted)
    
    def top_10_country_tags(self):
        if self.given_country is None:
            logging.info("given_country is none")
            self.files()
            tags = []
            names = [cout[0:2] for cout in self.li]
            for n in names:
                self.given_country = n
                tags.append(more_itertools.take(10, self.country_tags_dic_sort().items()))
            return(tags)
        self.combine()
        logging.info("given_country is  not none")
        logging.debug("top ten tags")
        return more_itertools.take(10, self.country_tags_dic_sort().items())
    
    def display_top_country_tags(self):
        logging.debug('calling country histogram')
        self.files()
        list1 = self.top_10_country_tags()
        for i,c in enumerate(list1):
            word, frequency = zip(*c)
            word = list(word)
            indices = np.arange(len(c))
            plt.bar(indices, frequency, color = 'r')
            plt.xticks(indices, word, rotation ='vertical')
            plt.title("Frequency of Top 10 Tags-%s"%self.li[i][:2])
            plt.tight_layout()
            plt.show()
            print(word)
    
    def display_country_tagpercentage(self):
        self.files()
        logging.debug('calling country pie chart')
        list1 = self.top_10_country_tags()
        for i,c in enumerate(list1):
            labels, size = zip(*c)
            fig1, ax1 = plt.subplots() 
            ax1.pie(size, labels=labels, autopct='%1.1f%%', shadow=True)
            ax1.set(aspect = 'equal', title = "Top Tags - %s"%self.li[i][:2])
            plt.show()
    
    def population_plot(self):
        logging.debug('calling population histogram')
        self.combine()
        Views_by_country=self.result.groupby(['country']).mean()
        co =  Views_by_country.index.tolist()
        view = Views_by_country['view_count'].tolist()
        d= {}
        for i,c in enumerate(co):
            if c in self.population.keys():
                d[c]=(view[i]/self.population[c])*100
        plt.bar(d.keys(), d.values(), color='g')
        plt.title('Population to Views')
        plt.xlabel('Country')
        plt.ylabel('% population watching')
        plt.show()
    
    def correlation(self):
        self.combine()
        logging.debug('calling correlation scatter matrix')
        new_columns=['categoryId','view_count','likes','dislikes','comment_count']
        analyze=self.result[new_columns]
        pd.plotting.scatter_matrix(analyze,alpha = 0.2,range_padding=0.3,figsize = (9,9))
        plt.suptitle('Youtube Correlation')
        plt.show()

def plotting():
    if args.do_plot == 'corr':
        youtube(os.getcwd()).correlation()
    elif args.do_plot == 'pie_tag':
        youtube(os.getcwd()).display_country_tagpercentage()
    elif args.do_plot == 'hist_tag':
        youtube(os.getcwd()).display_top_country_tags()
    elif args.do_plot == 'pop':
        youtube(os.getcwd()).population_plot()
    else:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Youtube Analyzer")
    parser.add_argument('Command', metavar='<command>', choices = ['print'], type=str, help='command to execute: only choice is print')
    parser.add_argument('-g','--group',dest = 'do_group',metavar = '<grouping>', default = 'default',choices=['default','Data','country','catagory','country/catagory'], help= 'command to execute: Data,country,catagory,country/catagory')
    parser.add_argument('-t','--tags', dest = 'do_tag', metavar = '<tags>',  default = 'default',choices=['default','Data','BR','CA','DE','FR','GB','IN','JP','KR','MX','RU','US'], help= 'command to execute: Data,BR,CA,DE,FR,GB,IN,JP,KR,MX,RU,US')
    parser.add_argument('-p','--plot', dest = 'do_plot', action = 'store', metavar = '<plot>',choices=['default','corr','pie_tag','hist_tag','pop'], help= 'command to execute: corr, pie_tag, hist_tag, pop')
    args = parser.parse_args()
    
    if args.do_group.lower() == 'data':
        print(youtube(os.getcwd()).no_group())
    elif args.do_group.lower() == 'country':
        print(youtube(os.getcwd()).by_country())
    elif args.do_group.lower() == 'catagory':
        print(youtube(os.getcwd()).by_catagory())
    elif args.do_group.lower() == 'country/catagory':
        print(youtube(os.getcwd()).by_country_catagory())
    else:
        pass

    if args.do_tag.lower() == 'default':
        pass
    elif args.do_tag == 'Data':
        country = [c[:2] for c in youtube(os.getcwd()).by_country().index]
        lst = youtube(os.getcwd()).top_10_country_tags()
        for i,j in enumerate(country):
            print(j,lst[i])
    else:
        lst = youtube(os.getcwd(),given_country=args.do_tag).top_10_country_tags()
        print(args.do_tag,lst)
    
    if args.do_plot == 'corr':
        youtube(os.getcwd()).correlation()
    elif args.do_plot == 'pie_tag':
        youtube(os.getcwd()).display_country_tagpercentage()
    elif args.do_plot == 'hist_tag':
        youtube(os.getcwd()).display_top_country_tags()
    elif args.do_plot == 'pop':
        youtube(os.getcwd()).population_plot()
    else:
        pass

    

    
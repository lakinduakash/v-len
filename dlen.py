#!/usr/local/bin/python3
import subprocess
import shlex
import json
import glob
import sys

# This depend on ffmpeg

def findVideoMetada(pathToInputVideo):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(pathToInputVideo)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)

    #prints all the metadata available:
    #import pprint
    #pp = pprint.PrettyPrinter(indent=2)
    #pp.pprint(ffprobeOutput)

    #find duration property in metadata
    duration = ffprobeOutput['streams'][0]['duration']
    return duration
    
def count_all_d(d_path,format='mp4'):

    s=0
    #add files in specified format to list
    lis = glob.glob(d_path+'/*.'+format)
    for i in lis:
        s=s+float(findVideoMetada(i))
    return s
        
def __main__():
    args=sys.argv
    
    if len(args)<=1:
        print('Total length of videos (h): ',count_all_d('.')/60/60)
    elif args[1] == '-h' or args[1] == '--help':
        help()
        
    elif args[1] == '-p':
        if len(args) >= 3:
            c=0
            t=0
            for i in args:
                if c>1:
                    if(args[len(args)-2] == '-t' ):
                        t=t+count_all_d(i,args[len(args)-1])
                    else:    
                        t=t+count_all_d(i)
                c=c+1
            print('Total length of videos (sec): ',t)
        else:
            help() 
    else:
        help()
            
            
def help():
    print(
        '''
        usage: dlen [option]
        
        options:
            -p folderpath(s) -Folder path to calculate length
            -t filetype(s)   -File type (default mp4)
        '''
        )

__main__()
    

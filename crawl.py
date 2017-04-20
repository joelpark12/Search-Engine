import os
import sys
import subprocess

def main():
    ''' Take first 5 arguments and execute scrapy spider '''
    # obtain current working directory from the path of this script
    cwd = os.path.dirname(os.path.realpath(__file__))

    # get commmand line arguments
    if len(sys.argv) < 5:
        print 'not enough arguments'
        return
    start_urls = sys.argv[1]
    num_page = sys.argv[2]
    dest_dir = sys.argv[3]
    algo = sys.argv[4]

    # call scrapy in cwd with specific arguments
    args = ' '.join(['scrapy', 'crawl', 'IUB-I427-jgpark',
            '-a', 'algo=%s' % algo,
            '-a', 'num=%s' % num_page,
            '-a', 'directory=%s' % dest_dir,
            '-a', 'urls=%s' % start_urls])
    subprocess.call(args, cwd=cwd, shell=True)


if __name__ == '__main__':
    main()

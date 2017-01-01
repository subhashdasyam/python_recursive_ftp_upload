import sys,os,zipfile,ftplib, configargparse
from os.path import basename

def ftp_login(user,passwd,host,port=21,timeout=30):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout)
        ftp.login(user, passwd)
        return ftp
    except ftplib.all_errors as e:
        print e
        return False

def ftp_makedirs(ftp_conn,path):
    path = path.lstrip('/')
    _path = path.split('/')
    ftp_conn.cwd('/')
    for _p in _path:
        if not directory_exists(ftp_conn,_p):
            ftp_conn.mkd(_p)
        ftp_conn.cwd(_p)
    return True


def ftp_dir_exists(ftp_conn,dir):
    if directory_exists(ftp_conn,dir) is False:
        print dir
        ftp_conn.mkd(dir)
    return True

def directory_exists(ftp_conn,dir):
    filelist = []
    ftp_conn.retrlines('LIST',filelist.append)
    for f in filelist:
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False

def ftp_upload_recursively(ftp_conn,common_dir,file_path):
    file_name = basename(file_path)
    ftp_conn.cwd('/')
    ftp_makedirs(ftp_conn,common_dir)
    #ftp_conn.cwd(common_dir)
    ftp_conn.storbinary('STOR '+file_name, open(file_path, 'rb'))
    return True
    

def scan_zip_extract_recursively(rootdir):
    #print rootdir
    for root_dir,sub_dir,files in os.walk(rootdir):
        for file in files:
            if file.lower().endswith('.zip'):
                zip_name = root_dir+'/'+file
                zip_basename = os.path.basename(zip_name)
                zip_basename = zip_basename.rstrip('.zip')
                extract_dir = root_dir+'/'+zip_basename
                if not os.path.exists(extract_dir):        
                    os.makedirs(extract_dir)
                if zipfile.is_zipfile(zip_name):
                    print 'zipfile'
                    zip_ref = zipfile.ZipFile(zip_name, 'r')            
                    zip_ref.extractall(extract_dir)
                    zip_ref.close()

def scan_upload_ftp(ftp_conn,rootdir):
    for root_dir,sub_dir,files in os.walk(rootdir):
        for file in files:
            _rootdir = root_dir.lstrip('/')
            file_path = root_dir+'/'+file
            print 'Uploading '+ file_path
            ftp_upload_recursively(ftp_conn,_rootdir,file_path)
    return True

if __name__ == "__main__":
    p = configargparse.ArgParser()
    p.add('-u', '--username', required=True, help='FTP Username', metavar='')
    p.add('-p', '--password', default='', help='FTP Password', metavar='')
    p.add('-s', '--host', required=True, help='FTP Host', metavar='')
    p.add('-po', '--port', required=False, type=int, default=21, help='FTP Port', metavar='')
    p.add('-r', '--path', required=True, help='local path', metavar='')
    options = p.parse_args()
    ftp_conn = ftp_login(options.username,options.password,options.host,options.port)
    if ftp_conn:
        scan_zip_extract_recursively(options.path)
        scan_upload_ftp(ftp_conn, options.path)
    else:
        print 'Error opening connection with FTP, please check the options and try again'

# python_recursive_ftp_upload

Tested in Ubuntu

Instructions

Python 2.7

sudo apt-get install python-pip -y

sudo pip install configargparse zipfile

save the code in ftp_sol.py or some_file_name.py

```
python ftp_sol.py -u subhash_username -p password -s 192.168.5.5 -po 5555 -r /var/www/html/test
```

**Full Help**

```
python ftp_sol.py --help

usage: ftp_sol.py [-h] -u [-p] -s [-po] -r

optional arguments:

-h, --help show this help message and exit

-u , --username FTP Username

-p , --password FTP Password

-s , --host FTP Host

-po , --port FTP Port Default 21

-r , --path local path

```

It will recursively create directories in FTP Server and upload the files 
It also scan the zip files in local path unzip under same zip name then upload files by creating folders

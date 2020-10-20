
import os

class FileReader:

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def get(self, filepath, cookies):
        '''
        Returns a binary string of the file contents, or None.
        '''
        fileContents = '' 
        try:
            if os.path.isdir(self.dir_path + filepath):
                fileContents = '<html><body><h1>'+ filepath +'</h1></body></html>'
            else:
                with open(self.dir_path + filepath, "rb") as f: 
                    if not f: 
                        fileContents = None
                    else: 
                        fileContents = f.read()
                f.close()
        except Exception as e:
            print(e) 
        return fileContents

    def head(self, filepath, cookies):
        '''
        Returns the size to be returned, or None.
        '''
        headerContents = ''
        try:
            if os.path.isdir(self.dir_path + filepath):
                dirResposne = '<html><body><h1>'+ filepath +'</h1></body></html>'
                headerContents += "Server sg3gj"
                headerContents += "Content-length:", str(len(dirResposne.encode()))+"\r\n"
            else:
                headerContents += "Content-length:" + str(os.path.getsize(self.dir_path + filepath))+"\r\n" 

                filetype = filepath[filepath.rfind('.'):]
                if filetype == ".html":
                    headerContents += "Content-type: text/html\r\n"
                elif filetype == ".css":
                    headerContents += "Content-type: text/css\r\n"
                elif filetype == ".png":
                    headerContents += "Content-type: image/png\r\n"
                elif filetype == ".jpg" or filetype == ".jpeg":
                    headerContents += "Content-type: image/jpeg\r\n"
                elif filetype == ".gif":
                    headerContents += "Content-type: image/gif\r\n"
        except Exception as e:
            print(e)
            return None

        return headerContents

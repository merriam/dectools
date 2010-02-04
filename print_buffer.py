class print_buffer(object):
    def __init__(self):
        self.lines = []
    
    def clear(self):
        self.lines = []
        
    def rint(self, *msgs):
        line = " ".join([str(msg) for msg in msgs])
        self.lines.append(line)
        print line
    record_line = rint
    
    def rinted(self, line, back=-1):
        if line != self.lines[back]:
            error = "\n".join(["UNEXPECTED!", "  Got", ':' + self.lines[-1] + ':', 
                                "  but expected", ':' + line + ':'])
            print error
            raise StandardError(error)
    expect = rinted

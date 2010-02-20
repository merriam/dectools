class print_buffer(object):
    def __init__(self):
        self.lines = []
    
    def clear(self):
        self.lines = []
        
    def rint(self, *msgs):
        """ Print line into buffer and then on screen.  Takes any number
            of arguments. """
        line = " ".join([str(msg) for msg in msgs])
        self.lines.append(line)
        print line
    record_line = rint
    
    def rinted(self, line, back=-1):
        """ Verify the line passed in is exactly as printed, with argument
            of how many lines to go back. """
        if line != self.lines[back]:
            error = "\n".join(["UNEXPECTED!", "  Got", ':' + self.lines[back] + ':', 
                                "  but expected", ':' + line + ':'])
            print error
            raise StandardError(error)
    expect = rinted
    
    def rinted_lines(self, lines_string):
        """ Verify all lines given were last ones printed """
        lines = lines_string.split("\n")
        for num, the_line in enumerate(lines):
            self.rinted(the_line, back=num - len(lines))

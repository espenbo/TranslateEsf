#!/usr/bin/python

import os

max_lines_per_file = 250
found_no_type = 'FoundNoAppropriateType'

def getName(name):
    resultingName = ''
    if name[0].isdigit():
        resultingName = '_'
    for i in name:
        if i.isalnum():
            resultingName += i
        else:
            resultingName += '_'
    return resultingName

def getNormalName(n, t):
    if '(1 Bit)' in t:
        return n + '1B'
    return n + '1R'

class OutputFile(object):
    def __init__(self, filename):
        self.basename = filename[0:filename.rfind('.')]
        self.filecounter = 1
        self.linecounter = 1
        self.outfile = self.getOutFile()

    def getOutFileName(self):
        return '%s.ou%d' % (self.basename, self.filecounter)

    def getOutFile(self):
        return open(self.getOutFileName(), 'w')

    def getNormalType(self, t):
        if '(1 Bit)' in t:
            return 'BOOL'
        if '(1 Byte)' in t or '(2 Byte)' in t:
            return 'REAL'
        return found_no_type

    def getSpecialType(self, n, t):
        if '(1 Bit)' in t:
            return 'FbDPT_Bool'
        if '(2 Byte)' in t:
            return 'FbDPT_Value_Temp'
        if '(1 Byte)' in t:
            return 'FbDPT_Scaling'
        print '%s:%d: No matching type found for %s' % (self.getOutFileName(), (self.linecounter*2)-1, n)
        return found_no_type

    def write(self, n, t):
        if self.linecounter > max_lines_per_file:
            self.filecounter += 1
            self.linecounter = 1
            self.outfile.close()
            self.outfile = self.getOutFile()
        self.outfile.write('%s: %s;\n' % (n, self.getSpecialType(n, t)))
        self.outfile.write('%s: %s;\n' % (getNormalName(n, t), self.getNormalType(t)))
        self.linecounter += 1

    def close(self):
        self.outfile.close()

class UniqueFilenameChecker(object):
    def __init__(self):
        self.varnames = {}

    def check(self, name):
        if name in self.varnames.keys():
            return self.makeunique(name)
        self.varnames[name] = True
        return name

    def makeunique(self, name):
        newid = 1
        newname = '%s_%d' % (name, newid)
        while newname in self.varnames.keys():
            newid += 1
            newname = '%s_%d' % (name, newid)
        self.varnames[newname] = True
        return newname

def translateFile(filename):
    outfile = OutputFile(filename)
    for line in open(filename).readlines():
        splitted = line.split('\t')
        if len(splitted) < 4:
            continue
        name = uniqueFilename.check(getName(splitted[1]))
        outfile.write(name, splitted[2])
    outfile.close()

def getAllFiles():
    return [ x for x in os.listdir('.') if x.endswith('.esf') ]

uniqueFilename = UniqueFilenameChecker()

for f in getAllFiles():
    translateFile(f)

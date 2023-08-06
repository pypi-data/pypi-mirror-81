import sys
import os
import shutil
import subprocess
from . import output
from . import constants
from . import RAO
import re
import pyscores2
import pyscores2.indata


class Calculation():
    def __init__(self, outDataDirectory):

        self.outDataDirectory = outDataDirectory

        self.standardIndataFile = "scores.in"
        self.standardOutdataFile = "SCORES.OUT"
        self.standardCoeffFile = "COEFF.OUT"
        self.exe_file_path = pyscores2.exe_file_path

        self.errorDescriptions = {}
        self.errorDescriptions["unknown"] = r'Unknown error'
        self.errorDescriptions[
            "  0"] = r'Too many sections, wave lengths, wave angles, etc.'
        self.errorDescriptions[
            "  1"] = r'Sum of weight distribution does not equal the displacement'
        self.errorDescriptions[
            "  2"] = r'The calculated displacement differs from the given nominal displacement (max 2% deviation alowed)'
        self.errorDescriptions[
            "  3"] = r'The calculated longitudinal centre of bouyancy differ from the nomonal value ((LCB-LCG)/L max 0.5%)'
        self.errorDescriptions[
            "  4"] = r'Error in range or increment of variable conditions'
        self.errorDescriptions["  5"] = r'TDP calculation incomplete'
        self.errorDescriptions[
            "  6"] = r'TDP file label does not equal title data, col. 1-30'

        self.outDataPath = ''

    def run(self, indata_file_path=None, indata=None, check_errors=True):
        """
		run Scores2
		You can run it either by specifying the indata file path or provide an Indata object.
		:param indata_file_path: path to the indata file
		:param indata: pyscores2.indata.Indata object
		:param check_errors: look for error messages in the result file.
		:return:
		"""

        # Remove old indata and result files:
        if os.path.exists(self.standardIndataFile):
            os.remove(self.standardIndataFile)

        if os.path.exists(self.standardOutdataFile):
            os.remove(self.standardOutdataFile)

        if os.path.exists(self.standardCoeffFile):
            os.remove(self.standardCoeffFile)

        if indata_file_path is None:
            assert isinstance(indata, pyscores2.indata.Indata)
            self.indataFileName = indata.projectName
            indata.save(indataPath=self.standardIndataFile)

        else:
            assert isinstance(indata_file_path, str)
            head, tail = os.path.split(indata_file_path)
            self.indataFileName = os.path.splitext(tail)[0]
            # Copy and rename indatafile:
            shutil.copyfile(indata_file_path, self.standardIndataFile)

        self.outDataPath = os.path.join(self.outDataDirectory,
                                        self.indataFileName + ".out")
        self.indata_path = os.path.join(self.outDataDirectory,
                                        self.indataFileName + ".in")
        self.coeffPath = os.path.join(self.outDataDirectory,
                                      self.indataFileName + "-COEFF.out")

        self.TDPFIL_path = os.path.join(self.outDataDirectory, "TDPFIL")

        #run Scores2:
        print("Running Scores2 for %s" % self.indataFileName)
        #	os.system('scores2.exe ' + self.standardIndataFile)

        if not os.path.exists(self.exe_file_path):
            raise ValueError('Cannot find the executable for Scores2 in:%s' %
                             self.exe_file_path)

        process = subprocess.Popen(self.exe_file_path, stderr=subprocess.PIPE)
        process.wait()

        #Copy the resultfiles to the outDataDirectory:
        shutil.move(self.standardOutdataFile, self.outDataPath)
        shutil.move(self.standardCoeffFile, self.coeffPath)
        shutil.move(self.standardIndataFile, self.indata_path)
        shutil.move('TDPFIL', self.TDPFIL_path)

        if check_errors:
            errorCode, errorDescription = self.parse_error()
            if not errorCode=='unknown':
                raise ValueError(errorDescription)

    @property
    def is_successfull_run(self):
        return os.path.exists(self.outDataPath)

    def getResult(self):

        if not self.is_successfull_run:
            raise ValueError('Please run a successfull calculation first')

        self.scoresFile = output.OutputFile(self.outDataPath)

        #Apply high wave frequency correction on the added resistance according to Bystrom:
        self.bystromCorrection()

        self.addedResistanceRAOs = self.scoresFile.getAddedResistanceRAOs(
            constants.rho, self.scoresFile.geometry.B,
            self.scoresFile.geometry.Lpp)
        return self.addedResistanceRAOs

    def bystromCorrection(self):

        #Apply bystrom correction to all results:
        for results in self.scoresFile.results.values():
            for result in results.values():
                result.addedResistance.bystromCorrection(
                    constants.rho, self.scoresFile.geometry.B,
                    self.scoresFile.geometry.Lpp)

    def calculateAddedResistanceInIrregularWaves(self, Tz):

        addedResistanceRAO = self.addedResistanceRAOs[12.0][180.0]
        irregularSea = RAO.irregularSeaClass(addedResistanceRAO, constants.rho,
                                             self.scoresFile.geometry.B,
                                             self.scoresFile.geometry.Lpp, Tz)

        self.addedResistance = irregularSea.addedResistance

        return irregularSea.addedResistance

    def parse_error(self):

        with open(self.outDataPath, 'r') as file:
            s = file.read()

        result = re.search("ERROR NO.(.*)", s)
        if result:
            errorCode = result.group(1)
        else:
            errorCode = 'unknown'

        if errorCode in self.errorDescriptions:
            errorDescription = self.errorDescriptions[errorCode]
        else:
            errorDescription = 'unknown error'

        if errorCode == "  2":
            calculatedDisplacement = self.parse_calculated_displacement()
            if calculatedDisplacement != None:
                errorDescription += " Calculated displacement = %f m3" % calculatedDisplacement

        if errorCode == "  3":
            calculatedLCB = self.parse_calculated_LCB()
            if calculatedLCB != None:
                errorDescription += " Calculated LCB = %f m (FWD. OF MIDSHIPS)" % calculatedLCB

        GM = self.parseGM()
        if GM != None:
            if GM < 0:
                errorDescription += " GM is negative"

        return errorCode, errorDescription

    def parse_calculated_displacement(self):

        with open(self.outDataPath, 'r') as file:
            s = file.read()

        result = re.search("DISPL. =([^G]*)", s)

        if result:
            displacement = float(result.group(1))
        else:
            displacement = None

        return displacement

    def parse_calculated_LCB(self):

        with open(self.outDataPath, 'r') as file:
            s = file.read()

        result = re.search("LONG. C.B. =([^\(]*)", s)

        if result:
            LCB = float(result.group(1))
        else:
            LCB = None

        return LCB

    def parseGM(self):

        with open(self.outDataPath, 'r') as file:
            s = file.read()

        result = re.search("GM =(.*)", s)

        if result:
            GM = float(result.group(1))
        else:
            GM = None

        return GM


def batchRunScores2(indataDirectory, outDataDirectory):

    if not os.path.exists(outDataDirectory):
        print("Create: %s" % outDataDirectory)
        os.mkdir(outDataDirectory)

    indataFiles = os.listdir(indataDirectory)

    scores2Calculations = []
    for indataFile in indataFiles:
        fileName, fileExtension = os.path.splitext(indataFile)

        if fileExtension == ".in":
            calculation = Calculation(
                os.path.join(indataDirectory, indataFile), outDataDirectory)
            calculation.run()
            calculation.getResult()

            Tz = 10.0
            addedResistance = calculation.calculateAddedResistanceInIrregularWaves(
                Tz)

            scores2Calculations.append(calculation)
    a = 1


# If run interactively
if __name__ == "__main__":

    if len(sys.argv) == 3:

        inDataDirectory = sys.argv[1]
        outDataDirectory = sys.argv[2]

        if not os.path.exists(inDataDirectory):
            print('Error: The indataDirectory does not exist.')
            sys.exit(1)

        batchRunScores2(inDataDirectory, outDataDirectory)
        a = 1
    else:
        print(
            'Error: This program should be called like this: batchRunScores "inDataDirectory" "outDataDirectory'
        )

        sys.exit(1)

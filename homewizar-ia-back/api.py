
class API:
    def __init__(self, sanity_check=False, generate=False, train=False, test=False):
        self.works = True if sanity_check else self.runUnitTests() == 100

    def runUnitTests(self):
        """ Call unit tests and return score """
        score = 100
        return score

    def generateDBs(self):
        """ Run scrapping scripts + Organise files """
        pass

    def makeBackup(self):
        """ Backup all of the files to prevent overwrite with errors """
        pass

    def trainAIs(self): # Additionnal params may specify a specific AI to train
        """ Train all AIs """
        pass

    def testAIs(self): # Same as above
        """ Test all AIs """
        pass

    def modelFromImage(self, path):
        """ Main pipeline, will generate a model file from an image """
        pass

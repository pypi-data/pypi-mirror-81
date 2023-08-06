import wget
import os
import tarfile
import platform
import sys

#Data for Geant4
dataPackages = [
    "https://cern.ch/geant4-data/datasets/G4NDL.4.6.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4EMLOW.7.9.1.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4PhotonEvaporation.5.5.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4RadioactiveDecay.5.4.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4SAIDDATA.2.0.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4PARTICLEXS.2.1.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4ABLA.3.1.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4INCL.1.0.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.2.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4RealSurface.2.1.1.tar.gz"]

#Check and download Geant4 data if not present:
def checkGeant4Data():
    dataLocation = getGeant4DataFolder()
    if not os.path.exists(dataLocation):
        print("No Geant4 data available in: " + dataLocation)
        print("I download it for you.")
        downloadGeant4Data()
        print("")
        print("Done")

#Download Geant4 data:
def downloadGeant4Data():
    dataLocation = getGeant4DataFolder()
    os.mkdir(dataLocation)
    for package in dataPackages:
      packageArchive = wget.download(package, out=dataLocation)
      with tarfile.open(packageArchive) as tar:
        tar.extractall(path=dataLocation)
      os.remove(packageArchive)

#Return Geant4 data folder:
def getGeant4DataFolder():
    packageLocation = os.path.dirname(os.path.realpath(__file__))
    dataLocation = os.path.join(packageLocation, "geant4_data")
    return dataLocation

#Return Geant4 data path:
def getGeant4DataPath():
    dataLocation = getGeant4DataFolder()
    g4DataPath = {
          "G4NEUTRONHPDATA"  : os.path.join(dataLocation, 'G4NDL4.6'),
          "G4LEDATA"         : os.path.join(dataLocation, 'G4EMLOW7.9.1'),
          "G4LEVELGAMMADATA" : os.path.join(dataLocation, 'PhotonEvaporation5.5'),
          "G4RADIOACTIVEDATA": os.path.join(dataLocation, 'G4RadioactiveDecay5.4'),
          "G4SAIDXSDATA"     : os.path.join(dataLocation, 'G4SAIDDATA2.0'),
          "G4PARTICLEXSDATA" : os.path.join(dataLocation, 'G4PARTICLEXS2.1'),
          "G4ABLADATA"       : os.path.join(dataLocation, 'G4ABLA3.1'),
          "G4INCLDATA"       : os.path.join(dataLocation, 'G4INCL1.0'),
          "G4PIIDATA"        : os.path.join(dataLocation, 'G4PII1.3'),
          "G4ENSDFSTATEDATA" : os.path.join(dataLocation, 'G4ENSDFSTATE2.2'),
          "G4REALSURFACEDATA": os.path.join(dataLocation, 'G4RealSurface2.1.1')
    }
    return g4DataPath

#Set Geant4 data paths:
def setGeant4DataPath():
    g4DataPath = getGeant4DataPath()
    for key, value in g4DataPath.items():
        os.environ[key] = value

    g4libFolder = os.path.dirname(os.path.realpath(__file__)) + ".libs"
    print(g4libFolder)
    s = platform.system()
    if s == 'Windows':
        os.add_dll_directory(g4libFolder)
    else:
        sys.path.append(g4libFolder)
    #sys.path.append(gam_g4_folder)
    os.environ["LD_LIBRARY_PATH"] = g4libFolder


# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
import csv
import os
os.chdir(r"D:/Upload_GitHub/txt")#
filePath = "D:/Upload_GitHub/springback_process"#

for num in range(1,6): #
    Mdb()
    num=str(num)#
    session.openOdb(filePath+num+'.odb')
    odb = session.odbs[filePath+num+'.odb']

    p = mdb.models['Model-1'].PartFromOdb(name='PIPE-1', instance='PIPE-1', 
        odb=odb)
    p = mdb.models['Model-1'].parts['PIPE-1']
    odb.close()
    #blank tube
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['PIPE-1']
    a.Instance(name='PIPE-1-1', part=p, dependent=ON)
    #

    mdb.Job(name='sp'+num+'_1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=DOUBLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
        numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
        numCpus=1, numGPUs=0)

    mdb.jobs['sp'+num+'_1'].writeInput(consistencyChecking=OFF)
    #





    session.openOdb(filePath+num+'.odb')
    odb = session.odbs[filePath+num+'.odb']
    p = mdb.models['Model-1'].PartFromOdb(name='PIPE-1', instance='PIPE-1', 
        odb=odb, shape=DEFORMED, step=0, frame=0)
    p = mdb.models['Model-1'].parts['PIPE-1']
    odb.close()
    #after process
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    
    mdb.jobs.changeKey(fromName='sp'+num+'_1', toName='sp'+num+'_2')
    mdb.jobs['sp'+num+'_2'].writeInput(consistencyChecking=OFF)
    #


    session.openOdb(filePath+num+'.odb')
    odb = session.odbs[filePath+num+'.odb']
    p = mdb.models['Model-1'].PartFromOdb(name='PIPE-1', instance='PIPE-1', 
        odb=odb, shape=DEFORMED, step=0, frame=-1)#-1: last frame
    p = mdb.models['Model-1'].parts['PIPE-1']
    #springbacked
    odb.close()

    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    mdb.jobs.changeKey(fromName='sp'+num+'_2', toName='sp'+num+'_3')
    mdb.jobs['sp'+num+'_3'].writeInput(consistencyChecking=OFF)
    #

#mdb.saveAs(pathName='G:/pipe_abaqus/pipe_shell_batch/20210507_copper/singlecopperodb/txt/odbreadercopper')#

print 'End of programm'


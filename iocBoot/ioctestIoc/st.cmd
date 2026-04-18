#!../../bin/linux-x86_64/testIoc

#- SPDX-FileCopyrightText: 2000 Argonne National Laboratory
#-
#- SPDX-License-Identifier: EPICS

#- You may have to change testIoc to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"


## Register all support components
dbLoadDatabase "dbd/testIoc.dbd"
testIoc_registerRecordDeviceDriver pdbbase

drvAsynIPPortConfigure("PSU0", "127.0.0.1:24700",0,0,0)
asynOctetSetInputEos("PSU0", 0, "\r\n")
asynOctetSetOutputEos("PSU0", 0, "\r\n")

## Load record instances
dbLoadTemplate "db/user.substitutions"
#dbLoadRecords "db/testIocVersion.db", "user=epics-dev"
#dbLoadRecords "db/dbSubExample.db", "user=epics-dev"

#- Set this to see messages from mySub
#-var mySubDebug 1

#- Run this to trace the stages of iocInit
#-traceIocInit

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncExample, "user=epics-dev"

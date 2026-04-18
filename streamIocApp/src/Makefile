# SPDX-FileCopyrightText: 1998 Argonne National Laboratory
#
# SPDX-License-Identifier: EPICS

TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# Use typed rset structure (see 3.16.1 release notes)
USR_CPPFLAGS += -DUSE_TYPED_RSET

# xxxRecord.h will be created from xxxRecord.dbd
DBDINC += xxxRecord

# Install xxxSupport.dbd into <top>/dbd
DBD += xxxSupport.dbd

# Build an IOC support library
LIBRARY_IOC += testIocSupport

# Compile and add code to the support library
testIocSupport_SRCS += xxxRecord.c
testIocSupport_SRCS += devXxxSoft.c

# Link locally-provided code into the support library,
# rather than directly into the IOC application, that
# causes problems on Windows DLL builds
testIocSupport_SRCS += dbSubExample.c
testIocSupport_SRCS += devtestIocVersion.c
testIocSupport_SRCS += testIocHello.c
testIocSupport_SRCS += initTrace.c

testIocSupport_LIBS += $(EPICS_BASE_IOC_LIBS)

# Auto-generate a header file containing a version string.
# Version comes from the VCS if available, else date+time.
GENVERSION = testIocVersion.h
# Macro name
GENVERSIONMACRO = testIocVERSION

# Build the IOC application
PROD_IOC = testIoc

# testIoc.dbd will be created and installed
DBD += testIoc.dbd

# testIoc.dbd will include these files:
testIoc_DBD += base.dbd
testIoc_DBD += dbSubExample.dbd
testIoc_DBD += devtestIocVersion.dbd
testIoc_DBD += testIocHello.dbd
testIoc_DBD += initTrace.dbd
testIoc_DBD += asyn.dbd
testIoc_DBD += drvAsynSerialPort.dbd
testIoc_DBD += drvAsynIPPort.dbd
#testIoc_DBD += calc.dbd
testIoc_DBD += stream.dbd
testIoc_DBD += xxxSupport.dbd

# testIoc_registerRecordDeviceDriver.cpp derives from testIoc.dbd
testIoc_SRCS += testIoc_registerRecordDeviceDriver.cpp

# Build the main IOC entry point where needed
testIoc_SRCS_DEFAULT += testIocMain.cpp
testIoc_SRCS_vxWorks += -nil-

# Link in the code from our support library
testIoc_LIBS += testIocSupport
testIoc_LIBS += asyn
#testIoc_LIBS += calc
testIoc_LIBS += stream 

# To build SNL programs, SNCSEQ must be defined
# in the <top>/configure/RELEASE file
ifneq ($(SNCSEQ),)
    # Build sncExample into testIocSupport
    sncExample_SNCFLAGS += +r
    testIoc_DBD += sncExample.dbd
    # A .stt sequence program is *not* pre-processed:
    testIocSupport_SRCS += sncExample.stt
    testIocSupport_LIBS += seq pv
    testIoc_LIBS += seq pv

    # Build sncProgram as a standalone program
    PROD_HOST += sncProgram
    sncProgram_SNCFLAGS += +m
    # A .st sequence program *is* pre-processed:
    sncProgram_SRCS += sncProgram.st
    sncProgram_LIBS += seq pv
    sncProgram_LIBS += $(EPICS_BASE_HOST_LIBS)
endif

# Link QSRV (pvAccess Server) if available
ifdef EPICS_QSRV_MAJOR_VERSION
    testIoc_LIBS += qsrv
    testIoc_LIBS += $(EPICS_BASE_PVA_CORE_LIBS)
    testIoc_DBD += PVAServerRegister.dbd
    testIoc_DBD += qsrv.dbd
endif

# Finally link IOC to the EPICS Base libraries
testIoc_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE

# Explicit dependency needed for generated header file
devtestIocVersion$(DEP): $(COMMON_DIR)/$(GENVERSION)

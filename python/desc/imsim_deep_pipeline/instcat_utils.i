// -*- c++ -*-
%define instcat_utils_DOCSTRING
"Swig-exposed functions for imsim_deep_pipeline"
%enddef

%feature("autodoc", "1");
%module(package="instcat_utils", docstring=instcat_utils_DOCSTRING) instcat_utils

%include "lsst/p_lsstSwig.i"
%lsst_exceptions()

%{
#include "lsst/afw.h"
#include "desc/imsim_deep_pipeline/instcat_utils.h"
%}

%include "desc/imsim_deep_pipeline/instcat_utils.h"

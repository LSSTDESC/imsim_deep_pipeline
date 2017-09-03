#include "pybind11/pybind11.h"
#include "desc/imsim_deep_pipeline/InstcatUtils.h"

namespace py = pybind11;

namespace desc {
   namespace imsim_deep_pipeline {

      PYBIND11_PLUGIN(instcat_utils) {
         py::module mod("instcat_utils");

	 //         mod.doc() = "instance catalog filtering tools";

         mod.def("ang_sep", &ang_sep,
                 "Angular separation between two sky coordinates in degrees.");

         mod.def("sky_cone_select", &sky_cone_select,
                 "Stream filtering of an instance catalog.");

         return mod.ptr();
      }
   } // imsim_deep_pipeline
} // desc

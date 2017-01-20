#ifndef desc_imsim_deep_pipeline_instcat_utils_h
#define desc_imsim_deep_pipeline_instcat_utils_h

#include <string>

namespace desc {
   namespace imsim_deep_pipeline {

      double ang_sep(double ra0, double dec0, double ra1, double dec1);

      void sky_cone_select(const std::string & infile,
                           double ra, double dec, double radius,
                           const std::string & outfile);
   } // namespace imsim_deep_pipeline
} // namespace desc

#endif // desc_imsim_deep_pipeline_instcat_utils_h

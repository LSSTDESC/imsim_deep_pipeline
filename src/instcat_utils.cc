#include <fstream>
#include <sstream>

#include "lsst/afw/coord/Coord.h"
#include "lsst/afw/geom/Point.h"
#include "desc/imsim_deep_pipeline/instcat_utils.h"

namespace desc {
namespace imsim_deep_pipeline {

   double ang_sep(double ra0, double dec0, double ra1, double dec1) {
      lsst::afw::geom::Point2D p0(ra0, dec0);
      lsst::afw::geom::Point2D p1(ra1, dec1);
      lsst::afw::coord::Coord coord0(p0);
      lsst::afw::coord::Coord coord1(p1);
      return coord0.angularSeparation(coord1).asDegrees();
   }

   void sky_cone_select(const std::string & obs_par_file,
                        const std::string & object_file,
                        double ra, double dec, double radius,
                        const std::string & outfile) {
      std::ofstream output(outfile.c_str());
      std::string line;

      // Stream the observing parameters directly to the output file.
      std::ifstream obs_pars(obs_par_file.c_str());
      while (std::getline(obs_pars, line, '\n')) {
         if (line.substr(0, 6) == "object") {
            break;
         }
         output << line << std::endl;
      }
      obs_pars.close();

      // Stream the objects, filtering by the desired acceptance cone.
      std::ifstream objects(object_file.c_str());
      while (std::getline(objects, line, '\n')) {
         if (line.substr(0, 6) == "object") {
            std::string command;
            std::string objectID;
            double ra_obj, dec_obj;
            std::istringstream ss;
            ss.str(line);
            ss >> command >> objectID >> ra_obj >> dec_obj;
            if (ang_sep(ra, dec, ra_obj, dec_obj) <= radius) {
               output << line << std::endl;
            }
         }
      }
      objects.close();

      output.close();
   }
} // namespace imsim_deep_pipeline
} // namespace desc

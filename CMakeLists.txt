################################################################################
# Package: InDetAlignmentWebMonitor
################################################################################

# Declare the name of this package:
atlas_subdir( InDetAlignmentWebMonitor )

# Declare the package's dependencies:
atlas_depends_on_subdirs( PUBLIC InDetAlignmentMonitoring )

# Install user scripts and python modules
atlas_install_scripts( scripts/* )
atlas_install_python_modules( python/*.py )
############################################################################
#
# Library:   UltrasoundScoliosis
#
# Copyright 2010 Kitware Inc. 28 Corporate Drive,
# Clifton Park, NY, 12065, USA.
#
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
############################################################################
cmake_minimum_required( VERSION 3.5 )

project( UltrasoundScoliosis CXX )

#Required packages and libraries
find_package( IntersonArraySDKCxx REQUIRED )

#find_package( PlusLib REQUIRED )
#include( ${PlusLib_USE_FILE} )

find_package( ITK REQUIRED )

find_package( ITK COMPONENTS
  ITKBinaryMathematicalMorphology
  ITKCommon
  ITKDistanceMap
  ITKImageFilterBase
  ITKImageFunction
  ITKImageFusion
  ITKImageGrid
  ITKImageIntensity
  ITKLabelMap
  ITKMathematicalMorphology

  ITKSmoothing
  ITKSpatialObjects
  ITKThresholding
  ITKTransform
  ITKIOImageBase
  ITKIONRRD
)

include( ${ITK_USE_FILE} )

find_package( Qt5 COMPONENTS Core Widgets REQUIRED )

#For Scoliosis App


  if(NOT MSVC)
      add_compile_options(-std=c++11 -Wall -Wextra -Wsign-conversion)
  else()
      add_compile_options(/W1)
  endif()


#Common setup
include_directories( ${CMAKE_SOURCE_DIR} )

include_directories( ${CMAKE_CURRENT_BINARY_DIR} )

add_definitions( -DNOMINMAX )



#Scoliosis ui executable

  qt5_wrap_ui( ScoliosisUI_H Scoliosis.ui )
  qt5_wrap_cpp( scoliosis_source_files_moc ScoliosisUI.h )

  set( scoliosis_source_files
    ScoliosisDriver.cxx
    ScoliosisUI.cxx
  )

  add_executable( ScoliosisUI
    ${scoliosis_source_files}
    ${ScoliosisUI_H}
    ${scoliosis_source_files_moc}
  )

  target_link_libraries( ScoliosisUI PUBLIC
    ${ITK_LIBRARIES}
    ${IntersonArraySDKCxx_LIBRARIES}
    Qt5::Widgets
  )


  install( TARGETS ScoliosisUI
    RUNTIME DESTINATION bin COMPONENT Runtime
    LIBRARY DESTINATION bin COMPONENT Runtime
    ARCHIVE DESTINATION lib COMPONENT Development
  )



#CPack setup

include( InstallRequiredSystemLibraries )

set( CPACK_MONOLITHIC_INSTALL ON )
set( CPACK_PACKAGE_VENDOR "Kitware, Inc." )
set( CPACK_GENERATOR "ZIP" )
set( CPACK_PACKAGE_VERSION "0.1.4" )
set( CPACK_PACKAGE_VERSION_MAJOR "0" )
set( CPACK_PACKAGE_VERSION_MINOR "1" )
set( CPACK_PACKAGE_VERSION_PATCH "4" )

set( CPACK_INSTALL_CMAKE_PROJECTS "${IntersonArraySDKCxx_DIR};IntersonArraySDKCxx;Runtime;/" )
set( CPACK_INSTALL_CMAKE_PROJECTS "${CPACK_INSTALL_CMAKE_PROJECTS};${CMAKE_BINARY_DIR};${PROJECT_NAME};ALL;/" )

# Get location of windeployqt.exe based on uic.exe location
get_target_property( uic_location Qt5::uic IMPORTED_LOCATION )
get_filename_component( _dir ${uic_location} DIRECTORY )
set( windeployqt "${_dir}/windeployqt.exe" )
if( NOT EXISTS ${windeployqt} )
  message( FATAL_ERROR "Failed to locate windeployqt executable: [${windeployqt}]" )
endif()
install( CODE "execute_process(COMMAND \"${windeployqt}\" \"\${CMAKE_INSTALL_PREFIX}/bin/OpticNerveUI.exe\")" )
#install( CODE "execute_process(COMMAND \"${windeployqt}\" \"\${CMAKE_INSTALL_PREFIX}/bin/PTXUI.exe\")" )

include( CPack )

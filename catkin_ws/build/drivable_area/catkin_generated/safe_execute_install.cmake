execute_process(COMMAND "/media/ankurrc/new_volume/usl/drivable_area_project/catkin_ws/build/drivable_area/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/media/ankurrc/new_volume/usl/drivable_area_project/catkin_ws/build/drivable_area/catkin_generated/python_distutils_install.sh) returned error code ")
endif()

project(LibModbusTest CXX)
cmake_minimum_required(VERSION 3.1.2)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(example example.cpp)
if(WIN32)
  target_link_libraries(example CONAN_PKG::libmodbus)
else()
  target_link_libraries(example CONAN_PKG::libmodbus)
endif()

#find_package(libmodbus REQUIRED)
#add_definitions(-DLIBMODBUS_STATICBUILD) # This should be obtained from library specification (pkg-config?)
#target_include_directories(example PRIVATE ${LIBMODBUS_INCLUDE_DIRS})
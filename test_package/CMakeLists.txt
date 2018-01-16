project(LibModbusTest CXX)
cmake_minimum_required(VERSION 3.1.2)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_definitions(-DLIBMODBUS_STATICBUILD) # This should be obtained from library specification (pkg-config?)
add_executable(example example.cpp)
if(WIN32)
  target_link_libraries(example CONAN_PKG::libmodbus ws2_32) # ws2_32 dependency should be included by CONAN_PKG::libmodbus, pkg-config or ?
else()
  target_link_libraries(example CONAN_PKG::libmodbus)
endif()

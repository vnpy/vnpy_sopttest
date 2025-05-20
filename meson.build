project(
  'vnpy_sopttest',
  'cpp',
  version: '3.7.1.0',
  license: 'MIT',
  meson_version: '>=1.7.0',
  default_options: [
    'buildtype=release',
    'cpp_std=c++17',
    'warning_level=2',
  ],
)

# 导入文件系统和Python模块
fs = import('fs')
py = import('python').find_installation(pure: false)
py_dep = py.dependency()

# 获取pybind11路径
python_cmd = host_machine.system() == 'windows' ? 'python' : 'python3'
pybind11_include_dir = run_command(python_cmd, '-c', 'import pybind11; print(pybind11.get_include())', check: true).stdout().strip()
message('使用pybind11路径: ' + pybind11_include_dir)

# 获取编译器信息
cpp = meson.get_compiler('cpp')
compiler_id = cpp.get_id()

# 输出构建目标系统信息
message('构建目标系统: ' + host_machine.system())

# 初始化变量
soptthostmduserapi_lib = []
soptthosttraderapi_lib = []
extra_cpp_args = []
extra_link_args = []

# 初始化库变量
soptthostmduserapi_lib = []
soptthosttraderapi_lib = []

# 初始化其他编译选项
install_rpath_value = ''

# 设置Windows特定编译选项
if host_machine.system() == 'windows'
  # Windows编译器设置
  add_project_arguments('/MT', language : 'cpp')
  
  # 设置库目录
  lib_dir = meson.current_source_dir() / 'vnpy_sopttest/api/libs'
  api_dir = meson.current_source_dir() / 'vnpy_sopttest/api'
  
  # 设置include目录
  include_dirs = include_directories(
    'vnpy_sopttest/api/include',
    'vnpy_sopttest/api/vnsopt',
    pybind11_include_dir,
  )
  
  # 定义CTP库
  soptthostmduserapi_lib = cpp.find_library('soptthostmduserapi_se', 
                                       dirs: [lib_dir, api_dir],
                                       required: true)
  soptthosttraderapi_lib = cpp.find_library('soptthosttraderapi_se', 
                                       dirs: [lib_dir, api_dir],
                                       required: true)

# 设置Linux特定编译选项
else  # Linux
  # Linux编译器设置
  extra_cpp_args = [
    '-std=c++17',
    '-O3',
    '-Wno-delete-incomplete',
    '-Wno-sign-compare',
  ]
  
  extra_link_args = [
    '-lstdc++',
    '-Wl,-rpath,$ORIGIN',  # 添加rpath设置，使库能在运行时找到同目录下的动态库
  ]
  
  # 设置库目录
  lib_dir = meson.current_source_dir() / 'vnpy_sopttest/api'
  
  # 设置include目录
  include_dirs = include_directories(
    'vnpy_sopttest/api/include',
    'vnpy_sopttest/api/vnsopt',
    pybind11_include_dir,
  )
  
  # 定义CTP库
  soptthostmduserapi_lib = cpp.find_library('soptthostmduserapi_se', 
                                       dirs: [lib_dir],
                                       required: true)
  soptthosttraderapi_lib = cpp.find_library('soptthosttraderapi_se', 
                                       dirs: [lib_dir],
                                       required: true)
endif

# 创建MD模块扩展
md_module = py.extension_module(
  'vnsoptmd',
  sources: ['vnpy_sopttest/api/vnsopt/vnsoptmd/vnsoptmd.cpp'],
  include_directories: include_dirs,
  dependencies: [py_dep, soptthostmduserapi_lib],
  cpp_args: extra_cpp_args,
  link_args: extra_link_args,
  install: true,
  subdir: 'vnpy_sopttest/api'
)

# 创建TD模块扩展
td_module = py.extension_module(
  'vnsopttd',
  sources: ['vnpy_sopttest/api/vnsopt/vnsopttd/vnsopttd.cpp'],
  include_directories: include_dirs,
  dependencies: [py_dep, soptthosttraderapi_lib],
  cpp_args: extra_cpp_args,
  link_args: extra_link_args,
  install: true,
  subdir: 'vnpy_sopttest/api'
)

# 安装Python源代码
python_files = [
  ['vnpy_sopttest/__init__.py', 'vnpy_sopttest'],
  ['vnpy_sopttest/api/__init__.py', 'vnpy_sopttest/api'],
  ['vnpy_sopttest/api/sopt_constant.py', 'vnpy_sopttest/api'],
  ['vnpy_sopttest/gateway/__init__.py', 'vnpy_sopttest/gateway'],
  ['vnpy_sopttest/gateway/sopttest_gateway.py', 'vnpy_sopttest/gateway'],
]

foreach file : python_files
  py.install_sources(
    [file[0]],
    pure: false,
    subdir: file[1]
  )
endforeach

# 安装API动态库文件
if host_machine.system() == 'windows'
  api_libs = [
    'vnpy_sopttest/api/soptthostmduserapi_se.dll',
    'vnpy_sopttest/api/soptthosttraderapi_se.dll',
  ]
  
  install_data(
    api_libs,
    install_dir: py.get_install_dir() / 'vnpy_sopttest/api'
  )
else  # Linux
  api_libs = [
    'vnpy_sopttest/api/libsoptthostmduserapi_se.so',
    'vnpy_sopttest/api/libsoptthosttraderapi_se.so',
  ]
  
  install_data(
    api_libs,
    install_dir: py.get_install_dir() / 'vnpy_sopttest/api'
  )
endif

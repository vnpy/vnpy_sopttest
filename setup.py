import platform

from setuptools import Extension, setup


def get_ext_modules() -> list:
    """
    获取三方模块

    Linux和Windows需要编译封装接口
    Mac由于缺乏二进制库支持无法使用
    """
    if platform.system() == "Linux":
        extra_compile_flags = [
            "-std=c++17",
            "-O3",
            "-Wno-delete-incomplete",
            "-Wno-sign-compare",
        ]
        extra_link_args = ["-lstdc++"]
        runtime_library_dirs = ["$ORIGIN"]
    else:
        extra_compile_flags = ["-O2", "-MT"]
        extra_link_args = []
        runtime_library_dirs = []

    vnsoptmd = Extension(
        "vnpy_sopttest.api.vnsoptmd",
        [
            "vnpy_sopttest/api/vnsopt/vnsoptmd/vnsoptmd.cpp",
        ],
        include_dirs=["vnpy_sopttest/api/include",
                      "vnpy_sopttest/api/vnsopt"],
        define_macros=[],
        undef_macros=[],
        library_dirs=["vnpy_sopttest/api/libs", "vnpy_sopttest/api"],
        libraries=["soptthostmduserapi_se", "soptthosttraderapi_se"],
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        depends=[],
        language="cpp",
    )

    vnsopttd = Extension(
        "vnpy_sopttest.api.vnsopttd",
        [
            "vnpy_sopttest/api/vnsopt/vnsopttd/vnsopttd.cpp",
        ],
        include_dirs=["vnpy_sopttest/api/include",
                      "vnpy_sopttest/api/vnsopt"],
        define_macros=[],
        undef_macros=[],
        library_dirs=["vnpy_sopttest/api/libs", "vnpy_sopttest/api"],
        libraries=["soptthostmduserapi_se", "soptthosttraderapi_se"],
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        depends=[],
        language="cpp",
    )

    return [vnsopttd, vnsoptmd]


setup(
    ext_modules=get_ext_modules(),
)

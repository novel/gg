try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
        name = "gg",
        version = "0.2.0",
        author = "Roman Bogorodskiy",
        author_email = "rbogorodskiy@griddynamics.com",
        url="http://github.com/novel/gg/tree",
        py_modules = ["GoGridClient", "GoGridManager"],
        scripts = ["gg-image-list", "gg-image-save", "gg-ip", "gg-lookup", 
            "gg-password", "gg-raw", "gg-server-add", 
            "gg-server-delete", "gg-server-delete-all", 
            "gg-server-list", "gg-server-power"]
)

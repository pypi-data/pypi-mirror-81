from setuptools import setup, find_packages

setup(
    name="hass-home-assistant-frontend",
    version="20200427.3",
    description="The HaaS version of Home Assistant frontend",
    url="https://gitlab.svccomp.de/svccomp-students/entwicklungsprojekt/2020/haas-human-as-a-sensor/home-assistant-frontend",
    author="The HaaS Project and Home Assistant Authors",
    author_email="author@email.com",
    license="Apache License 2.0",
    packages=find_packages(include=["hass_frontend", "hass_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)

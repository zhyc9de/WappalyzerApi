# coding=utf8
import os

from selenium import webdriver

from libs import get_root_path

ext_dir_path = get_root_path('libs/crawler/chrome_ext')


def add_ext(options, crx_name):
    crx_path = ext_dir_path + crx_name + '.crx'
    if not os.path.isfile(crx_path):
        raise FileNotFoundError('没有这个插件')
    options.add_extension(crx_path)


def chrome_new_session(show_image=True, incognito=False, proxy_server=None, ua=None, mobile=False,
                       extensions=None):
    options = webdriver.ChromeOptions()

    if not show_image:
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    if incognito:
        options.add_argument("--incognito")

    if ua:
        options.add_argument("user-agent=" + ua)

    if proxy_server:
        options.add_argument('--proxy-server=' + proxy_server)

    if mobile:  # todo 自由设定device name
        mobile_emulation = {"deviceName": "Google Nexus 5"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

    if extensions:
        [add_ext(options, crx) for crx in extensions]

    return webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities=options.to_capabilities()
    ), options.arguments

# WappalyzerApi

由于找到的开源版Wappalyzer都没chrome插件探测出来的准确

所以基于chrome插件修改了这么个版本出来

## 原理

[下载crx源文件](http://chrome-extension-downloader.com/)，直接解压，添加代码使其探测完成后传回服务器

利用selenium，装载插件访问网页得到数据

通过API进行数据传输

## 安装

环境：python3.6 redis chrome node selenium
目前Wappalyzer插件版本： 2.51

```bash
# 安装selenium
npm install -g selenium-standalone
selenium-standalone install
# 国内请使用
selenium-standalone install --drivers.chrome.baseURL=https://npm.taobao.org/mirrors/chromedriver --baseURL=https://npm.taobao.org/mirrors/selenium --drivers.firefox.baseURL=https://npm.taobao.org/mirrors/geckodriver
# 开启selenium
selenium-standalone start

# 安装python3依赖
pip3 install -r requirements.txt

# 后台启动
./start.sh
```

## TODO

- [ ] 打包docker
- [ ] 添加代理
- [ ] 多线程（是否有必要？
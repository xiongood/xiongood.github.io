@echo off
chcp 65001
cd ../../ && hexo clean && git add . && git commit -m zyx && git push && hexo d && hexo g && hexo d


@echo off
F:\Python27WorkSp\WebService_PDC
pyinstaller SDWebService_PDC.py

CD F:\Python27WorkSp\WebService_PDC\dist
copy /y F:\Python27WorkSp\WebService_PDC\dist\_mssql.pyd F:\Python27WorkSp\WebService_PDC\dist\SDWebService_PDC
copy /y F:\Python27WorkSp\WebService_PDC\dist\Config.ini F:\Python27WorkSp\WebService_PDC\dist\SDWebService_PDC
md F:\Python27WorkSp\WebService_PDC\dist\SDWebService_PDC\log
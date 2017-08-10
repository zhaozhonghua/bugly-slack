# Bugly 接入 Slack

将 Bugly 的消息发送到 Slack 上。

### Bugly josn data
```
{
  "eventType": "bugly_crash_trend",
  "timestamp": 1462780713515,
  "isEncrypt": 0,
  "eventContent": {
    "datas": [
      {
        "accessUser": 12972,//联网用户数
        "crashCount": 21,//crash次数
        "crashUser": 20,//crash影响用户数
        "version": "1.2.3",//app版本号
        "url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
      },
      {
        "accessUser": 15019,
        "crashCount": 66,
        "crashUser": 64,
        "version": "1.2.4",
        "url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
      },
      {
        "accessUser": 15120,
        "crashCount": 1430,
        "crashUser": 1423,
        "version": "1.2.4",
        "url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
      }
    ],
    "appId": "1104512706", //appId
    "platformId": 1   //平台
"appName": "AF", //app名称
    "date": "20160508",
"appUrl":"http://bugly.qq.com/issueIndex?app=1104512706&pid=1&ptag=1005-10000" 
  },
  "signature": "ACE346A4AE13A23A52A0D0D19350B466AF51728A"
}

```

slack 接收json格式
```
{"text": ""}
```
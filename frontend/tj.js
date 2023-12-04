(function() {
    // 获取流量来源信息
    var referrer = document.referrer || 'Direct';

    // 发送数据到服务器
    var xhr = new XMLHttpRequest();
    var url = "https://tab.jordonfbi.uk";
    var data = {
        referrer: referrer,
        // 其他需要发送的统计数据
    };

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // 请求成功的处理
            console.log(xhr.responseText);
        }
    };

    xhr.send(JSON.stringify(data));
})();

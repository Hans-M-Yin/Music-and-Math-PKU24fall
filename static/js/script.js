document.getElementById('musicStyleForm').onsubmit = function(event) {
    event.preventDefault();  // 阻止默认表单提交

    const img = document.getElementById('result');
    const statusMessage = document.getElementById('statusMessage');
    
    img.style.display = 'none';  // 隐藏图像
    statusMessage.style.display = 'block';  // 显示状态消息

    // 使用 Fetch API 发送 POST 请求
    fetch('/generate_image', {
        method: 'POST',
        body: new URLSearchParams(new FormData(this)),  // 将表单数据发送到服务器
    })
    .then(response => {
        if (response.ok) {
            return response.blob();  // 获取图像blob
        }
        throw new Error('网络错误');
    })
    .then(blob => {
        const imgUrl = URL.createObjectURL(blob);  // 创建图像URL
        img.src = imgUrl;  // 设置图像源
        img.style.display = 'block';  // 显示图像
        statusMessage.style.display = 'none';  // 隐藏状态消息
    })
    .catch(error => {
        console.error('错误:', error);
        statusMessage.textContent = '生成图像时出错。请重试。';  // 更新状态消息
    });
};
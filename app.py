from flask import Flask, render_template, request, send_file
from main import generate_png  # 导入你的生成图像函数
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def create_image():
    style = request.form.get('style')
    
    # 调用 main.py 中的函数生成乐谱
    # image_file = generate_png(style)
    generate_png(style)

    # 发送生成的乐谱图像文件
    response = send_file('output_1.png', mimetype='image/png')
    response.headers['Cache-Control'] = 'no-store'  # 禁用缓存
    return response

# Linux
# if __name__ == '__main__':
#     app.run(debug=True)
# 在Windows上需要改ip地址和端口号
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
### 运行环境
以下方法选择一个：
- Linux下运行setup.sh并且手动运行source musicMath/bin/activate激活虚拟环境
- Linux或Windows下安装flask, lilypond, music21, python=3.10.11或更高版本

保证lilypond添加至Path变量，或手动修改main.py中lilypond的位置

运行app.py生成本地网页

### 功能
根据选择的选项(classical, pop, rock, electric, jazz)传入相应style参数到(main.py)generate_png(style), 在对应的style-music.txt中**随机**(music_to_vector.py中musicTxt_to_vector(style)改为了用random)抽取一行音符，传入run_generic_algorithm()，将输出以.ly格式写入output_1文件，调用lilypond将.ly文件转为.png的乐谱图片，显示在网页上
- 把museScore换成了lilypond来呈现乐谱，因为后者不需要图形界面可以直接导出png

### to be modified
1. music_data/目录下对应各个style的旋律，有的需要补充一些
2. generate_png(style)可以把随机抽取对应风格的旋律改进为更合适的方法
3. 网页功能可以增加比如播放旋律、生成多条旋律、标注生成旋律所用的原曲等
4. 如果需要搭建外部可访问的网站，需要一个域名或者托管
5. 网页格式太简陋了，可以找点html template套一下

### generic_algs.py
#### run_generic_algorithm
1. questions:
- 把原有的melody也添加到population中，可能导致最后生成的曲子是原曲？
- population的排序，即population = sorted(population, key=lambda x: x.score)这一行应该放在操作的后面，否则iterations=1时新加入的元素不会参与排序？
2. changes:
- 把population排序放到了循环末尾
- 最后的stream_list循环for i in range(10)改为了挑分最高的一个instead of十个；为了提升速度把2000次变换暂时改为了200次

### 网页的搭建过程
- 设计思路：为了更方便地与用户交互，我们想搭建一个动态网页，使得用户点击生成按键后即可自动生成乐谱和可播放的旋律。尽管由于时间等因素最终只搭建了一个本地网页（即用本地主机当作服务器的网页），但相对来说也大幅提升了用户操作的简便性，也请期待后续我们可能进一步将它升级为可外部访问的网站。
- 具体实现：分为下述三个步骤
  - 1. 编写index.html文件，搭建简单的交互主页；在app.py中调用Flask库接受用户点击按键的请求
  - 2. 收到客户端请求后，app.py调用相应的基于music21库的生成函数，生成music21格式的旋律，接着调用lilypond将其转换为图片格式
  - 3. 编写script.js呈现生成乐谱或在生成出现错误时显示生成错误
- 过程与改进：
  - 在搭建网页初期，我们发现之前用于呈现乐谱的museScore软件由于图形界面不适合用作被请求的服务，于是更换为更简便的命令行程序lilypond来生成图片格式乐谱。
  - 另外，最初设想根据不同音乐类型分类，用户选择音乐类型后生成相应风格的旋律，但我们发现由于数据量的限制，分类后的生成效果不尽如人意，于是又转而采用所有类型的整体数据集，实现效果上的进步。
  - 除此之外，我们发现手动安装Flask, lilypond, music21等运行环境对用户不友好，于是编写了setup.sh的shell脚本，帮助Linux系统的用户配置环境。当然，最理想的情况是客户端可以使用域名访问我们的远程服务器来请求服务，如此一来便不用配置环境，但受限于时间和域名获取等因素目前没有实现，请期待我们后续的改进。
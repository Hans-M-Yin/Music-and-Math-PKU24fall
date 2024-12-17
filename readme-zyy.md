### 运行环境
以下方法选择一个：
- Linux下运行setup.sh即可
- Linux或Windows下安装flask, lilypond, music21, python=3.10.11或更高版本
添加lilypond至Path变量，或手动修改main.py中lilypond的位置

运行app.py生成本地网页

### 功能
根据选择的选项(classical, pop, rock, electric, jazz)传入相应style参数到(main.py)generate_png(style), 在对应的style-music.txt中**随机**抽取一行音符，传入run_generic_algorithm()，将输出以.ly格式写入output_1文件，调用lilypond将.ly文件转为.png的乐谱图片，显示在网页上
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
- 最后的stream_list循环for i in range(10)，改为了挑分最高的一个instead of十个
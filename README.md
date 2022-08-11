# Dataset-
这是我自己的 一个处理数据集的一些文件，这里只包含代码，里面的一些文件，例如数据集的json，xml等文件还有图片自己可以从网上自行下载。
在这里我是使用的TT100k数据集，你可以使用自己的数据集，修改其中的代码来运行。

1.2_json2xml.py是将TT100k数据集提供的json格式文件通过其路径将其分成train和test两个数据集，然后生成xml文件并按照路径放入数据集中

2.alldetect.py是负责处理将不在45类的xml的object给剔除掉

3.classnum.py可以获取所以xml文件中的包含的所有类别

4.coco2images.py 将json标签文件根据coco格式将符合满足条件的图片放入一个文件夹中

5.createtxt.py将类别文件转成label_list.txt

6.imagetxt.py根据训练集和测试集将图片也进行分类

7.json2coco.py将json总文件分成训练集和测试集的coco格式的标签文件

8.json2txt.py将coco格式的json文件转成多个yolo格式的txt文件

9.lenclasses.py将根据总的json文件生成state.json文件（json2coco根据生成的文件来进行划分）

10.randomnum.py对标签文件和图片进行重命名

11.txt2json1.py将yolo格式转为json格式的步骤1

12.txt2json2.py是步骤2

13.txt2xml，xml2odgt，xml2txt也都是进行格式转换的文件


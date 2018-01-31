分割手写数字并得到.npy文件提供给MNIST识别

    先看处理数字图片结果流程图,以下图片的顺序为:原始图->去噪->像素反转->查找数字目标->切割
 ![](https://user-images.githubusercontent.com/29486192/35605796-13ec19f2-0686-11e8-8163-cd64fe138a2b.png)  
 ![](https://user-images.githubusercontent.com/29486192/35605582-a2527de6-0684-11e8-97d8-dd44062720bb.png)
 ![](https://user-images.githubusercontent.com/29486192/35605583-a2f3ba58-0684-11e8-98b0-d10ad164e24c.png)
 ![](https://user-images.githubusercontent.com/29486192/35605584-a32cd6c6-0684-11e8-8657-fa039dcbff10.png)
 ![](https://user-images.githubusercontent.com/29486192/35605585-a3ba66bc-0684-11e8-8015-2cfc17a82b4b.png)
 ![](https://user-images.githubusercontent.com/29486192/35605586-a3f1b55e-0684-11e8-92f4-92ed11784678.png)
 ![](https://user-images.githubusercontent.com/29486192/35605587-a4920f7c-0684-11e8-887c-4c8403105789.png)
 ![](https://user-images.githubusercontent.com/29486192/35605588-a4cdeaec-0684-11e8-9cec-868ea55c40fe.png)
 ![](https://user-images.githubusercontent.com/29486192/35605589-a50681a4-0684-11e8-82dd-4f46a6595752.png)
 ![](https://user-images.githubusercontent.com/29486192/35605590-a540e9de-0684-11e8-88e7-330f8298c794.png)
 ![](https://user-images.githubusercontent.com/29486192/35605591-a5765222-0684-11e8-98f1-98268fd3d004.png)
 ![](https://user-images.githubusercontent.com/29486192/35605592-a5af7b24-0684-11e8-991b-ec2293039731.png)
 ![](https://user-images.githubusercontent.com/29486192/35605594-a5fafcf2-0684-11e8-97ea-3df775173708.png)
 ![](https://user-images.githubusercontent.com/29486192/35605595-a66adc3e-0684-11e8-9458-ec4cd9fd7a35.png)
 
 最后的分割结果只是展示，具体内容是保存在image_data.npy文件中（保存顺序为从上往下，从左到右），这样只要得到了image_data.npy文件，便可以作为输入数据feed给神经网络模型，和MNIST训练结果比对，得到最终识别结果

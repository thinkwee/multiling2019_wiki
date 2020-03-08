# multiling2019_wiki

- Multiling 2019 维基百科词条提取任务
- 基于BERT，用CRF/NMT微调
- 论文见[Multilingual Wikipedia Summarization and Title Generation On Low Resource Corpus](https://www.aclweb.org/anthology/W19-8904.pdf)
- 代码基于sberbank-ai的实现[ner-bert](https://github.com/sberbank-ai/ner-bert)	

# Description

- 见[任务说明](http://multiling.iit.demokritos.gr/pages/view/1651/task-headline-generation)
- 数据请从[此处下载](https://drive.google.com/open?id=1a2p5ZfnFVLp2JfYgqQQSkCndzqEztIK0)
- 测试集请从[此处下载](https://drive.google.com/open?id=1B-r7lJYJ7Kk5qmoy0WUzk4O045Lurai5)
- 已经处理好的测试集摘要见```/WikiTrain19/processed_summary```，和测试集一起解压到```/WikiTrain19/test/```下

# Methods
- [x] Baseline1: Spacy多语言模型（七种）进行命名实体识别，直接挑选实体作为词条
- [x] Baseline2: Spacy单语言模型（八种）进行依存剖析，提取主语作为词条
- [x] Model1: [BERT多语言模型+BiLSTM+Attn+CRF](https://github.com/sberbank-ai/ner-bert),对词条位置进行序列标注
- [x] Model2: [BERT多语言模型+BiLSTM+Attn+NMT](https://github.com/sberbank-ai/ner-bert),对词条位置进行序列标注(Seq2Seq)
- [ ] Model3: [MUSE](https://github.com/facebookresearch/MUSE)+BiLSTM+CRF，对词条位置进行序列标注

# Data Pipeline
- 下载数据集，解压到```./WikiTrain19/full   ./WikiTrain19/clipped```
- 运行```./preprocess.py```，得到标注好的数据```./WikiTrain19/tagged_data```和纯语料```./WikiTrain19/raw_data```
- 纯语料可以直接跑baseline```./simple_method.ipynb```
- 若要使用标注数据，运行```./combine_shuffle_divide.sh```进行后处理，并下载[BERT预训练多语言模型](https://storage.googleapis.com/bert_models/2018_11_23/multi_cased_L-12_H-768_A-12.zip)到```./ner-bert/datadrive/multi_cased_L-12_H-768_A-12```
- 运行```./ner-bert/examples/multiling-2019.ipynb ./ner-bert/examples/multiling-2019-nmt.ipynb```进行BERT模型的训练，模型保存在```./ner-bert/datadrive/models/multiling-2019/```下

# Results
- Baseline1
    - en: 0.105
    - de: 0.48
    - es: 0.013
    - fr: 0.397
    - it: 0.021
    - pt: 0.404
    - ru: 0.25
    
- Baseline2
    - en: 0.507
    - de: 0.490
    - fr: 0.4
    - es: 0.451
    - el: 0.4
    - pt: 0.433
    - it: 0.523
    - nl: 0.567
    
- Model1（迭代十次）

```
              precision    recall  f1-score   support

      B_MISC      0.665     0.443     0.532      1788
      I_MISC      0.733     0.379     0.500      1348

   micro avg      0.690     0.415     0.519      3136
   macro avg      0.699     0.411     0.516      3136
weighted avg      0.694     0.415     0.518      3136

              precision    recall  f1-score   support

           O      0.972     0.985     0.979     35451
        MISC      0.601     0.447     0.513      1788

    accuracy                          0.959     37239
   macro avg      0.787     0.716     0.746     37239
weighted avg      0.955     0.959     0.956     37239

```

- Model2（迭代十次）

```
              precision    recall  f1-score   support

      B_MISC      0.890     0.910     0.900      1802
      I_MISC      0.888     0.902     0.895      1339

   micro avg      0.889     0.907     0.898      3141
   macro avg      0.889     0.906     0.897      3141
weighted avg      0.889     0.907     0.898      3141

              precision    recall  f1-score   support

           O      0.996     0.994     0.995     34664
        MISC      0.888     0.916     0.902      1788

    accuracy                          0.990     36452
   macro avg      0.942     0.955     0.948     36452
weighted avg      0.990     0.990     0.990     36452
```
import xml.dom.minidom
import xml.etree.cElementTree as ET
import os
import re
import csv
# import jieba
root_path = './WikiTrain19/full'
train_path = './WikiTrain19/tagged_data'
raw_path = './WikiTrain19/raw_data'
TAG = 1

# 拿到语料的title

def get_title(dom):
    root = dom.documentElement
    title_list = root.getElementsByTagName('title')
    title = title_list[0].firstChild.data
    return title

def split_sentence(para, zh):
    if zh:
        return para.split('。')
    else:
        return para.split('.')

# 对每个p中的句子进行标注，标注样式为BIO，之后转为标准的B_MISC，I_MISC
# 返回值如[标注序列，原句]

def get_tag(title, sentence, zh):
    # print(title, sentence)
    title_len = len(title.split())  # 保存title的单词数
    if zh:
        title_len = len([w for w in title])
    sub_seq = ''
    # 用于替换的字符串，形如"B I O"，但为了防止与句子中原有的BIO错乱，使用#@代替BI
    for i in range(title_len):
        if i == 0:
            sub_seq += '#'
        else:
            sub_seq += '@'
        if not zh:
            sub_seq += ' '
    if not zh:
        sub_seq = sub_seq[:-1]
    title_pattern = re.compile(title, re.I)
    sub_sent = re.sub(title_pattern, sub_seq, sentence)
    if zh:
        # 对于中文，不用分词，按字分
        sentence_list = [word for word in sub_sent]
        raw_seq = ' '.join([word for word in sentence])
    else:
        sentence_list = sub_sent.split()
        raw_seq = sentence
    for index in range(len(sentence_list)):
        if '#' not in sentence_list[index] and '@' not in sentence_list[index]:
            sentence_list[index] = 'O'
        else:
            if len(sentence_list[index]) > 1:
                if sentence_list[index][1] != ',' or sentence_list[index][1] != '.' or sentence_list[index][1] != '，' or sentence_list[index][1] != '。':
                    sentence_list[index] = 'O'
    tag_seq = ' '.join(sentence_list)
    if '#' in tag_seq:
        if len(sentence_list)>3:
            return [tag_seq, raw_seq]
    else:
        return False

def get_train_data(title, para_list, data_tag, data_raw, zh):
    for p in para_list:
        para = p.firstChild.data
        # 分句
        sentence_list = split_sentence(para, zh)
        for sentence in sentence_list:
            tmp = get_tag(title, sentence.strip(), zh)
            if tmp:
                data_tag.append(tmp)
                data_raw.append([title,sentence.strip()])
    return data_tag, data_raw

def get_train_data_more(title, para_list, data_tag, data_raw, zh):
    sentence_list = split_sentence(para_list, zh)
    for sentence in sentence_list:
        tmp = get_tag(title, sentence.strip(), zh)
        if tmp:
            data_tag.append(tmp)
            data_raw.append([title,sentence.strip()])
    return data_tag, data_raw

def get_more_samples(path):
    # 获取更多的子标题训练对
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    sec_list = []
    for section in root[2]:
        for sec in section:
            if sec.tag == "header" or sec.tag == "p":
                sec_list.append(sec)
    l = len(sec_list)
    idx = 0
    data = []
    while idx < l:
        while sec_list[idx].tag == "header":
            idx += 1
            if idx == l:
                break
        if idx == l:
            break
        header = sec_list[idx-1].text
        p_idx = idx
        while sec_list[p_idx].tag=="p":
            if header in sec_list[p_idx].text:
                data.append([header,sec_list[p_idx].text])
            p_idx += 1
            if p_idx==l:
                break
        idx = p_idx
    return data

def get_lang(lang_name, zh=False):
    data_tag = []
    data_raw = []
    lang_path = os.path.join(root_path, lang_name)
    lang_file_name = lang_name + '.csv' # 标注过的csv文件名
    raw_name = lang_name + '.txt' # 挑选出的训练集中的原始句子文件名
    files = os.listdir(lang_path)
    for file_name in files:
        dom = xml.dom.minidom.parse(os.path.join(lang_path, file_name))
        root = dom.documentElement
        # 拿到summary下的标签
        summary_list = root.getElementsByTagName('summary')
        # 拿到所有标签p，每个p都需要再分句
        para_list = summary_list[0].getElementsByTagName('p')
        data = get_more_samples(os.path.join(lang_path, file_name))
        for (header,text) in data:
            get_train_data_more(header,text,data_tag,data_raw,zh)
        title = get_title(dom)
        print('title:', title)
        get_train_data(title, para_list, data_tag, data_raw, zh)

    with open(os.path.join(train_path, lang_file_name), 'w', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data_tag)
    with open(os.path.join(raw_path, raw_name), 'w', encoding='utf-8', newline='') as f:
        for (title,line) in data_raw:
            f.write(title + '\t' + line + '\n')
    return None        

def get_langs():
    langs = os.listdir(root_path)
    for lang_name in langs:
        if lang_name == 'zh':
            get_lang(lang_name, True)
        else:
            get_lang(lang_name)

if __name__ == '__main__':
    get_langs()
    # data = get_lang('en')
    # print(data[0][1])
    # print(data[1][1])
    # with open('en.csv', 'w', encoding='utf-8', newline='') as f:
    #     f_csv = csv.writer(f)
    #     f_csv.writerows(data)
    # with open('en.csv',encoding="utf-8") as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         print(row[0])
    #         print(row[1])
    #         break

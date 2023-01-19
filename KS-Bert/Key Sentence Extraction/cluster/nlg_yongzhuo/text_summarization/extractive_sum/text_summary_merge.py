# -*- coding: utf-8 -*-


from nlg_yongzhuo import text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf
from multiprocessing import Manager, Process
import multiprocessing
import platform
if platform.system()=='Windows':
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn", force=True)


# 共享变量
def worker(i, text, num, fs, return_dict):
    """
        worker function
    :param i: int
    :param text: str
    :param fs: list
    :param return_dict: list<list> 
    :return: None
    """
    return_dict[i] = fs[i].summarize(text=text, num=num)


def summary_multi_preprocess(doc, num=None, fs=[text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf]):
    """
        len(fs) 个进程
    :param doc: str
    :return: list
    """
    manager = Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(len(fs)):
        p = Process(target=worker, args=(i, doc, num, fs, return_dict))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    return list(return_dict.values())


def summary_serial(doc, num=None, fs=[text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf]):
    """
        单独串行跑所有
    :param doc: str
    :return: list
    """
    res = []
    for fs_ in fs:
        res_fs = fs_.summarize(text=doc, num=num)
        res.append(res_fs)
    return res


def summary_post_preprocess(reses):
    """
        后处理
    :param reses: list<list>
    :return: list
    """
    res_dict = {}
    for res in reses:
        r_dict = {}
        sum_score = sum([r[0] for r in res])
        for score, sent in res:
            r_dict[sent] = score/sum_score
            if sent in res_dict:
                res_dict[sent] = res_dict[sent] + r_dict[sent]
            else:
                res_dict[sent] = r_dict[sent]
    score_sen = [(rc[1], rc[0]) for rc in sorted(res_dict.items(),
                                                 key=lambda d: d[1], reverse=True)]
    return score_sen


def text_summarize(doc, num=None, multi_process=False,
                   fs=[text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf]):
    """
        抽取式文本摘要, 汇总, 使用几个方法
    :param doc: str or list, 用户输入
    :param num: int, 返回的句子个数
    :param multi_process: bool, 是否使用多进程
    :return: res_score: list, sentences of doc with score
    """
    if type(doc)==list:
        doc = "。".join(doc)
    elif not doc or (type(doc) != str):
        raise RuntimeError(" type of doc must be 'list' or 'str' ")
    if not num:
        from nlg_yongzhuo.data_preprocess.text_preprocess import cut_sentence
        num = len(cut_sentence(doc))
    # 是否使用多进程, 注意: 当cpu数量不足或性能较差时, 多进程不一定比串行快
    if multi_process:
        res = summary_multi_preprocess(doc, num, fs)
    else:
        res = summary_serial(doc, num, fs)
    # 后处理
    res_score = summary_post_preprocess(res)
    return res_score


if __name__ == '__main__':
    doc = "看的心碎，也让人感动，愿一切安好。一个女孩子写在死里逃生后:今天郑州暴雨，下午四点物业通知要停电所以需要尽快下班，我和同事下楼后发现门口积水已到膝盖，同事说硬着头皮过吧，我犹豫了一下不敢过，所以没有过去。又等了一个多小时终究还是不想在公司留宿，还是淌着到大腿的水过去了，刚坐上地铁以为噩梦结束了，结果地铁刚过了一站，开往第二站的时候就停在中间了！走不动了，车厢就开始慢慢的往里渗水，但是还不太多，我们就在等怎么办？所有人都傻了，后来地铁的工作人员安排我们慢慢撤离，刚走了没多远，又要求我们回去，因为前方的水全部漫过来了。等全部人员上车后车厢的水已经到腰部了，可是噩梦还没有结束，车外面的水一直在涨，也一直在从门缝里往里渗着，慢慢的水越来越多，我们能站在座位上都站在座位上，最后站在座位上水都到胸口了。我真的害怕了，可是最恐怖的不是水而是车厢里的空气越来越少，好多人都出现了呼吸困难的症状。我听到一个阿姨给家人交代银行卡号，交代家里的事情，我想我是不是也要交代一下呢？当时想联系的人很多，想说的事情也很多，但是最后都没有说出口，只能妈妈发了一句，妈妈我可能快不行了，我有点害怕。但是妈妈回过来电话我也不知道说啥，只说还在等救援，就挂了。从六点到八点半一直都处在崩溃的边缘，慢慢的也不用崩溃了，因为我也因为缺氧晕倒了。就在这个时候我妈妈给我打个电话，手机的震动叫醒了我，和妈妈说了两句，有个救援队的叔叔联系上了，我告诉他我们缺氧快不能呼吸了，叔叔说救援队都到了正在想办法。就在这个时候车顶传来了救命的脚步声，有人来了，消防队的叔叔在使劲的砸车厢的玻璃，一下两下无数下，终于砸开了两扇玻璃，有空气了，我们可以恢复呼吸了！然后就听到车厢前面传来越来越多的声音，救援队终于来了。真正遇到生死的时刻才更能体现人性的美好，这么长时间肯定有很多人熬不住了，到处可以听见互相安慰的声音，有获救的机会了，每个人都在喊着让晕倒的人先走，两个男生架着一个晕倒的人，每个人都上去扶一把，把每个晕倒的人都先救出去。然后所有的男生说女生先走，然后男生真的站在两边等着让女生先走，即使是情侣都放开了彼此的手，让女生先走，男生们在后面一个拉着一个女生走，我头晕走不动了，不过停在哪里，不管男生女生都会说一句，你靠着我就可以，看看好多男生和消防员叔叔一直泡在水里，接应一个又一个女生出去，真的是觉得很庆幸，生在华夏生在一个有爱的国度，遇到善良可爱的人，这是我有生以来第一次离死亡那么近，原来只是嘴上说说谁知道明天和意外哪个先来，这次真的是遇到了，原来意外真的会来，真的是害怕了，如果今天真的出不来了，我会很后悔，后悔有太多的事情没有做，后悔太多人没有见，再也不能吃我最爱的麻辣火锅了，更后悔没有和爸爸妈妈奶奶弟弟说句我爱你们，死里逃生后这种感觉更加深刻，既然幸运的我活下来了，那么以后一定要好好的享受生活，好好的珍惜眼前的人和事！好多人发信息关心我，十万分的感谢大家！谢谢".replace(" ", "").replace('"', '')

    # fs可以填其中一个或几个 text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf
    res_score = text_summarize(doc, multi_process=True, fs=[lda])
    for rs in res_score:
        print(rs)


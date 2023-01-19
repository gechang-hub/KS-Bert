class Parameters(object):
    seq_length = 300         #max length of cnnsentence序列长度
    num_classes = 8         #number of labels

    keep_prob = 0.4          #droppout
    lr = 0.00004               #learning rate

    num_epochs = 25         #epochs
    batch_size = 16          #batch_size


    train_filename='./data/cnews.train.txt'  #train data
    test_filename='./data/cnews.test.txt'    #test data
    val_filename='./data/cnews.val.txt'      #validation data
    vocab_filename='./bert_model/chinese_L-12_H-768_A-12/vocab.txt'        #vocabulary
    bert_config_file = './bert_model/chinese_L-12_H-768_A-12/bert_config.json'
    init_checkpoint = './bert_model/chinese_L-12_H-768_A-12/bert_model.ckpt'
    # init_checkpoint = './checkpoints/bert_classify/best_validation-468'

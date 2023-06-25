from transformers import AutoTokenizer, AutoModel, AutoConfig
import time
import torch
import torch.nn as nn
import os


class Chat(nn.Module):
    def __init__(self, model_path="../models/chatglm-6b"):
        super(Chat, self).__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
        self.model.eval()

    def forward(self, text, history):
        start = time.time()
        response, history_new = self.model.chat(self.tokenizer, text, history=history)
        infer_time = round(time.time() - start, 3)
        return response, infer_time


class PtChat(nn.Module):
    def __init__(self, model_path, checkpoint_path, pre_seq_len):
        super(PtChat, self).__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        config = AutoConfig.from_pretrained("../models/chatglm-6b", trust_remote_code=True, pre_seq_len=pre_seq_len)
        self.model = AutoModel.from_pretrained("../models/chatglm-6b", config=config, trust_remote_code=True)
        prefix_state_dict = torch.load(os.path.join(checkpoint_path, "pytorch_model.bin"))
        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        self.model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)

        # model = model.quantize(4)
        self.model = self.model.half().cuda()
        self.model.transformer.prefix_encoder.float()
        self.model = self.model.eval()

    def forward(self, text, history):
        start = time.time()
        response, _ = self.model.chat(self.tokenizer, text, history=history)
        infer_time = round(time.time() - start, 3)
        return response, infer_time


if __name__ == '__main__':
    sentence = '肚子疼怎么办？'
    glm = Chat()
    res, time_ = glm(sentence, [])
    print(res)
    print(time_)

    glm_path = '../models/chatglm-6b'
    pt_path = 'output/adgen-chatglm-6b-pt-256-2e-2/checkpoint-3000'
    predict_max_len = 256
    pt_chat = PtChat(glm_path, pt_path, predict_max_len)
    res, time_ = pt_chat(sentence, [])
    print(res)
    print(time_)

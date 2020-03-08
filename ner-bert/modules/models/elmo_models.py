from modules.layers.encoders import *
from modules.layers.decoders import *
from modules.layers.embedders import *
import abc


class NerModel(nn.Module, metaclass=abc.ABCMeta):
    """Base class for all Models"""
    def __init__(self, encoder, decoder, use_cuda=True):
        super(NerModel, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        if use_cuda:
            self.cuda()

    @abc.abstractmethod
    def forward(self, *batch):
        # return self.decoder(self.encoder(batch))
        raise NotImplementedError("abstract method forward must be implemented")

    @abc.abstractmethod
    def score(self, *batch):
        # return self.decoder.score(self.encoder(batch))
        raise NotImplementedError("abstract method score must be implemented")

    @abc.abstractmethod
    def create(self, *args):
        raise NotImplementedError("abstract method create must be implemented")

    def get_n_trainable_params(self):
        pp = 0
        for p in list(self.parameters()):
            if p.requires_grad:
                num = 1
                for s in list(p.size()):
                    num = num * s
                pp += num
        return pp


class ElmoBiLSTMCRF(NerModel):

    def forward(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder(output, batch[-2])

    def score(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder.score(output, batch[-2], batch[-1])

    @classmethod
    def create(cls,
               label_size,
               # ElmoEmbedder params
               model_dir, config_name, embedding_dim=1024, elmo_mode="avg",
               freeze=True,
               # ElmoBiLSTMEncoder params
               enc_hidden_dim=128, rnn_layers=1,
               # CRFDecoder params
               input_dropout=0.5,
               # Global params
               use_cuda=True):
        embedder = ElmoEmbedder.create(
            model_dir, config_name, embedding_dim, use_cuda, elmo_mode, freeze)
        encoder = ElmoBiLSTMEncoder.create(embedder, enc_hidden_dim, rnn_layers, use_cuda)
        decoder = CRFDecoder.create(label_size, encoder.output_dim, input_dropout)
        return cls(encoder, decoder, use_cuda)


class ElmoBiLSTMAttnCRF(NerModel):

    def forward(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder(output, batch[-2])

    def score(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder.score(output, batch[-2], batch[-1])

    @classmethod
    def create(cls,
               label_size,
               # ElmoEmbedder params
               model_dir, config_name, embedding_dim=1024, elmo_mode="avg",
               freeze=True,
               # ElmoBiLSTMEncoder params
               enc_hidden_dim=128, rnn_layers=1,
               # AttnCRFDecoder params
               key_dim=64, val_dim=64, num_heads=3,
               input_dropout=0.5,
               # Global params
               use_cuda=True):
        embedder = ElmoEmbedder.create(
            model_dir, config_name, embedding_dim, use_cuda, elmo_mode, freeze)
        encoder = ElmoBiLSTMEncoder.create(embedder, enc_hidden_dim, rnn_layers, use_cuda)
        decoder = AttnCRFDecoder.create(
            label_size, encoder.output_dim, input_dropout, key_dim, val_dim, num_heads)
        return cls(encoder, decoder, use_cuda)


class ElmoBiLSTMAttnNMT(NerModel):
    """Reused from https://github.com/DSKSD/RNN-for-Joint-NLU"""

    def forward(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder(output, batch[-2])

    def score(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder.score(output, batch[-2], batch[-1])

    @classmethod
    def create(cls,
               label_size,
               # ElmoEmbedder params
               model_dir, config_name, embedding_dim=1024, elmo_mode="avg",
               freeze=True,
               # ElmoBiLSTMEncoder params
               enc_hidden_dim=128, rnn_layers=1,
               # NMTDecoder params
               dec_embedding_dim=64, dec_hidden_dim=256, dec_rnn_layers=1,
               input_dropout=0.5, pad_idx=0,
               # Global params
               use_cuda=True):
        embedder = ElmoEmbedder.create(
            model_dir, config_name, embedding_dim, use_cuda, elmo_mode, freeze)
        encoder = ElmoBiLSTMEncoder.create(embedder, enc_hidden_dim, rnn_layers, use_cuda)
        decoder = NMTDecoder.create(
            label_size, dec_embedding_dim, dec_hidden_dim,
            dec_rnn_layers, input_dropout, pad_idx, use_cuda)
        return cls(encoder, decoder, use_cuda)


class ElmoBiLSTMAttnNMTCRF(NerModel):

    def forward(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder(output, batch[-2])

    def score(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder.score(output, batch[-2], batch[-1])

    @classmethod
    def create(cls,
               label_size,
               # ElmoEmbedder params
               model_dir, config_name, embedding_dim=1024, elmo_mode="avg",
               freeze=True,
               # ElmoBiLSTMEncoder params
               enc_hidden_dim=128, rnn_layers=1,
               # NMTDecoder params
               dec_embedding_dim=64, dec_hidden_dim=256, dec_rnn_layers=1,
               input_dropout=0.5, pad_idx=0,
               # Global params
               use_cuda=True):
        embedder = ElmoEmbedder.create(
            model_dir, config_name, embedding_dim, use_cuda, elmo_mode, freeze)
        encoder = ElmoBiLSTMEncoder.create(embedder, enc_hidden_dim, rnn_layers, use_cuda)
        decoder = NMTCRFDecoder.create(
            label_size, dec_embedding_dim, dec_hidden_dim,
            dec_rnn_layers, input_dropout, pad_idx, use_cuda)
        return cls(encoder, decoder, use_cuda)


class ElmoBiLSTMAttnCRFJoint(NerModel):

    def forward(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder(output, batch[-2])

    def score(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder.score(output, batch[-2], batch[-1], batch[-3])

    @classmethod
    def create(cls,
               label_size, intent_size,
               # ElmoEmbedder params
               model_dir, config_name, embedding_dim=1024, elmo_mode="avg",
               freeze=True,
               # ElmoBiLSTMEncoder params
               enc_hidden_dim=128, rnn_layers=1,
               # AttnCRFDecoder params
               key_dim=64, val_dim=64, num_heads=3,
               input_dropout=0.5,
               # Global params
               use_cuda=True):
        embedder = ElmoEmbedder.create(
            model_dir, config_name, embedding_dim, use_cuda, elmo_mode, freeze)
        encoder = ElmoBiLSTMEncoder.create(embedder, enc_hidden_dim, rnn_layers, use_cuda)
        decoder = AttnCRFJointDecoder.create(
            label_size, encoder.output_dim, intent_size, input_dropout, key_dim, val_dim, num_heads)
        return cls(encoder, decoder, use_cuda)


class ElmoBiLSTMAttnNMTJoint(NerModel):
    """Reused from https://github.com/DSKSD/RNN-for-Joint-NLU"""

    def forward(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder(output, batch[-2])

    def score(self, batch):
        output, _ = self.encoder(batch)
        return self.decoder.score(output, batch[-2], batch[-1], batch[-3])

    @classmethod
    def create(cls,
               label_size, intent_size,
               # ElmoEmbedder params
               model_dir, config_name, embedding_dim=1024, elmo_mode="avg",
               freeze=True,
               # ElmoBiLSTMEncoder params
               enc_hidden_dim=128, rnn_layers=1,
               # NMTDecoder params
               dec_embedding_dim=64, dec_hidden_dim=256, dec_rnn_layers=1,
               input_dropout=0.5, pad_idx=0,
               # Global params
               use_cuda=True):
        embedder = ElmoEmbedder.create(
            model_dir, config_name, embedding_dim, use_cuda, elmo_mode, freeze)
        encoder = ElmoBiLSTMEncoder.create(embedder, enc_hidden_dim, rnn_layers, use_cuda)
        decoder = NMTJointDecoder.create(
            label_size, intent_size, dec_embedding_dim, dec_hidden_dim,
            dec_rnn_layers, input_dropout, pad_idx, use_cuda)
        return cls(encoder, decoder, use_cuda)

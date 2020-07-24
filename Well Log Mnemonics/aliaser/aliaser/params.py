from typing import Optional, Union, List


class Params:
    # Model architecture
    vocab_size: int = 30000
    hidden_size: int = 150  # of the encoder; default decoder size is doubled if encoder is bidi
    dec_hidden_size: Optional[
        int
    ] = 200  # if set, a matrix will transform enc state into dec state
    embed_size: int = 100
    enc_bidi: bool = True
    enc_attn: bool = True  # decoder has attention over encoder states?
    dec_attn: bool = False  # decoder has attention over previous decoder states?
    pointer: bool = True  # use pointer network (copy mechanism) in addition to word generator?
    out_embed_size: Optional[
        int
    ] = None  # if set, use an additional layer before decoder output
    tie_embed: bool = True  # tie the decoder output layer to the input embedding layer?

    # Coverage (to turn on/off, change both `enc_attn_cover` and `cover_loss`)
    enc_attn_cover: bool = True  # provide coverage as input when computing enc attn?
    cover_func: str = "max"  # how to aggregate previous attention distributions? sum or max
    cover_loss: float = 1  # add coverage loss if > 0; weight of coverage loss as compared to NLLLoss
    show_cover_loss: bool = False  # include coverage loss in the loss shown in the progress bar?

    # Regularization
    enc_rnn_dropout: float = 0
    dec_in_dropout: float = 0
    dec_rnn_dropout: float = 0
    dec_out_dropout: float = 0

    # Training
    optimizer: str = "Nadam"  # adam or adagrad
    lr: float = 0.001  # learning rate
    adagrad_accumulator: float = 0.1
    lr_decay_step: int = 5  # decay lr every how many epochs?
    lr_decay: Optional[float] = None  # decay lr by multiplying this factor
    batch_size: int = 32
    n_batches: int = 50  # how many batches per epoch CHANGED 1000
    val_batch_size: int = 32
    n_val_batches: int = 10  # how many validation batches per epoch CHANGED 100
    n_epochs: int = 10  # CHANGED 75
    pack_seq: bool = True  # use packed sequence to skip PAD inputs?
    forcing_ratio: float = 0.75  # initial percentage of using teacher forcing
    partial_forcing: bool = True  # in a seq, can some steps be teacher forced and some not?
    forcing_decay_type: Optional[str] = "exp"  # linear, exp, sigmoid, or None
    forcing_decay: float = 0.9999
    sample: bool = True  # are non-teacher forced inputs based on sampling or greedy selection?
    grad_norm: float = 1  # use gradient clipping if > 0; max gradient norm
    # note: enabling reinforcement learning can significantly slow down training
    rl_ratio: float = 0  # use mixed objective if > 0; ratio of RL in the loss function
    rl_ratio_power: float = 1  # increase rl_ratio by **= rl_ratio_power after each epoch; (0, 1]
    rl_start_epoch: int = 1  # start RL at which epoch (later start can ensure a strong baseline)?

    # Data
    embed_file: Optional[
        str
    ] = "data/.vector_cache/glove.6B.100d.txt"  # use pre-trained embeddings
    data_path: str = "data/mnem.gz"
    val_data_path: Optional[str] = "data/mnem.val.gz"
    max_src_len: int = 400  # exclusive of special tokens such as EOS
    max_tgt_len: int = 100  # exclusive of special tokens such as EOS
    truncate_src: bool = True  # truncate to max_src_len? if false, drop example if too long
    truncate_tgt: bool = True  # truncate to max_tgt_len? if false, drop example if too long

    # Saving model automatically during training
    model_path_prefix: Optional[str] = "weights"
    keep_every_epoch: bool = False  # save all epochs, or only the best and the latest one?

    # Testing
    beam_size: int = 4
    min_out_len: int = 60
    max_out_len: Optional[int] = 100
    out_len_in_words: bool = False
    test_data_path: str = "data/mnem.test.gz"
    test_sample_ratio: float = 1  # what portion of the test data is used? (1 for all data)
    test_save_results: bool = True

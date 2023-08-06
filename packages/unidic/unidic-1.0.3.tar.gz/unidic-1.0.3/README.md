# unidic-py

This is a version of [UniDic](https://unidic.ninjal.ac.jp/) packaged for use
with pip. 

Currently it supports 2.3.0, the latest version of UniDic. **Note this will
take up 1GB on disk after install and can take a long time to download.** If
you want a small package, try
[unidic-lite](https://github.com/polm/unidic-lite).

After installing via pip, you need to download the dictionary using the
following command:

    python -m unidic download

With [fugashi](https://github.com/polm/fugashi) or
[mecab-python3](https://github.com/samurait/mecab-python3) unidic will be used
automatically when installed, though if you want you can manually pass the
MeCab arguments:

    import fugashi
    import unidic
    tagger = fugashi.Tagger('-d "{}"'.format(unidic.DICDIR))
    # that's it!

## Differences from the Official UniDic Release

This has a few changes from the official UniDic release to make it easier to use.

- entries for 令和 have been added
- single-character numeric and alphabetic words have been deleted
- `unk.def` has been modified so unknown punctuation won't be marked as a noun

See the `extras` directory for details on how to replicate the build process.

# License

The modern Japanese UniDic is available under the GPL, LGPL, or BSD license,
[see here](https://unidic.ninjal.ac.jp/download#unidic_bccwj). UniDic is
developed by [NINJAL](https://www.ninjal.ac.jp/), the National Institute for
Japanese Language and Linguistics. UniDic is copyrighted by the UniDic
Consortium and is distributed here under the terms of the [BSD
License](./LICENSE.unidic).

The code in this repository is not written or maintained by NINJAL. The code is
available under the MIT or WTFPL License, as you prefer.

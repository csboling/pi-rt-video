On Windows I was able to get this working by installing a few
[Python extension packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/), namely I installed the following wheels:

* `Cython-0.28.1-cp36-cp36m-win32.whl`
* `numpy-1.14.2+mkl-cp36-cp36m-win32.whl`
* `PyOpenGL-3.1.2-cp36-cp36m-win32.whl`
Then I could install the other stuff with `pip install -r requirements.txt`.
I also needed a Freetype DLL on my PATH, I achieved this by building Freetype from
[source](https://www.freetype.org/download.html) but you might try
[here](https://github.com/ubawurinna/freetype-windows-binaries).
For audio I used the pyo installer. MME worked on my system, yours might need a different
audio backend, which you can edit in `pipeline/audio/capture.py`.

After all this I could:
``` bash
python3 __main__.py
```

You can pick from a couple different demos in `__main__.py`.

On Windows I was able to get this working by installing a few 
[Python extension packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/), namely I installed the following wheels:
* `Cython-0.28.1-cp36-cp36m-win_amd64.whl`
* `numpy-1.14.2+mkl-cp36-cp36m-win_amd64.whl`
* `PyOpenGL-3.1.2-cp36-cp36m-win_amd64.whl`
Then I could install the other stuff with `pip install -r requirements.txt`.
I also needed a 64-bit Freetype DLL on my PATH, I achieved this by building Freetype from 
[source](https://www.freetype.org/download.html) but you might try 
[here](https://github.com/ubawurinna/freetype-windows-binaries).

Finally, my platform did not have numpy.float128 or numpy.complex256 defined, so I had to 
edit the PyOpenGL source and comment them out (from 
`~/AppData/Local/Programs/Python/Python36/lib/site-packages/OpenGL/arrays/numpymodule.py`).
After all this I could:

``` bash
python3 __main__.py
```

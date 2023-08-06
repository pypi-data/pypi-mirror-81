# Offset
## - What is this?
To encode & decode by shift text(Symmetric encryption).

## - How to install
```bash
pip install Offset
```

## - How to use

### Module
1. Import
```python
from offset import Offset
```
2. Convert text through a public method
```python
Offset.convert(text, number)
```

### CLI

- Basic mode:
```bash
offset -n 10 -s 'Hello'
```

- File mode:
>The new file will be stored at '~/offset_export/filename_%Y%m%d_%H%M%S.ext'

```bash
offset -n 10 -f '/filepath/and/filename.ext'
```

- Interactive mode
> you can give it a default without enter a number every single time.

```bash
offset -i [-n int]
```

### GUI(IN PROGRESS)
![Screenshot](https://github.com/Ron-Chang/offset/blob/master/img/gui.png?raw=true)

If you like my work, please consider buying me a coffee or [PayPal](https://paypal.me/RonDevStudio?locale.x=zh_TW)
Thanks for your support! Cheers! 🎉
<a href="https://www.buymeacoffee.com/ronchang" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" align="right"></a>

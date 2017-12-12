# Unbridled joy only!

На самом деле задание состоит из двух частей: первое - техническое, и второе - творческое (отослать картинку). Здесь будет описана техническая часть. Итак, по заданию нам даны 900 пронумерованных фрагментов картинки, которую нам необходимо собрать. Для этого был написанс следующий скрипт на python с использованием модуля Pillow:
```python
from PIL import Image
from natsort import natsorted
import os

os.chdir('en')
images = map(Image.open, natsorted(os.listdir('.')))
images = [images[i:i+30] for i in range(0, len(images), 30)]
total_width = 43 * 30
total_height = 50 * 30
new_im = Image.new('RGB', (total_width, total_height))

y_offset = 0
for row in images:
    x_offset = 0
    for im in row:
        new_im.paste(im, (x_offset, y_offset))
        x_offset += im.size[0]
    y_offset += 50

new_im.save('../en.jpg')
```

Картинки располагаются в папке en. Размер был взят из быстрого анализа первых 30 фрагментов. Модуль natsorted использовался для естественной сортировки файлов-фрагментов. В итоге мы собрали картинку, на которой была надпись о том, что необходимо сделать фото команды и зафотошопить с темой Рика и Морти.

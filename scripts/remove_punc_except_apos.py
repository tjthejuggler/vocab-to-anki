import re
sentence="warhol's art used many types of media, including hand drawing, painting, printmaking, photography, silk screening, sculpture, film, and music."
print(re.sub(r"[^\w\d'\s]",'',sentence))


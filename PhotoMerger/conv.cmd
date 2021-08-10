SET input=output.jpg
SET /A width="identify -ping '%w' %input%"
convert %input% -region 3x100%+%width%+0 -blur 10x1000 blur1.jpg
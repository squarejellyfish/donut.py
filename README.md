# donut.c in Python
[🇹🇼 zh-tw](./README.md) &emsp; [🇺🇸 en](./README.en.md)  

![donut](https://i.imgur.com/6IbUZ43.gif)  
這是一個用Python寫的donut.c  
donut.c為Andy Sloane在2006年寫的一個原始碼形狀是甜甜圈、能夠在終端機呈現一個旋轉甜甜圈的程式  
原donut.c原始碼如下：
```c
             k;double sin()
         ,cos();main(){float A=
       0,B=0,i,j,z[1760];char b[
     1760];printf("\x1b[2J");for(;;
  ){memset(b,32,1760);memset(z,0,7040)
  ;for(j=0;6.28>j;j+=0.07)for(i=0;6.28
 >i;i+=0.02){float c=sin(i),d=cos(j),e=
 sin(A),f=sin(j),g=cos(A),h=d+2,D=1/(c*
 h*e+f*g+5),l=cos      (i),m=cos(B),n=s\
in(B),t=c*h*g-f*        e;int x=40+30*D*
(l*h*m-t*n),y=            12+15*D*(l*h*n
+t*m),o=x+80*y,          N=8*((f*e-c*d*g
 )*m-c*d*e-f*g-l        *d*n);if(22>y&&
 y>0&&x>0&&80>x&&D>z[o]){z[o]=D;;;b[o]=
 ".,-~:;=!*#$@"[N>0?N:0];}}/*#****!!-*/
  printf("\x1b[H");for(k=0;1761>k;k++)
   putchar(k%80?b[k]:10);A+=0.04;B+=
     0.02;}}/*****####*******!!=;:~
       ~::==!!!**********!!!==::-
         .,~~;;;========;;;:~-.
             ..,--------,*/
```
酷吧酷吧  
他在2011年寫了一篇文件解釋背後的原理，我就是照著這篇寫出donut.py的:  
https://www.a1k0n.net/2011/07/20/donut-math.html   
Maybe我之後會翻譯？  
# 下載：
先安裝numpy：
```
pip3 install numpy
```
然後複製我的donut.py文件後，在主控台打：
```
python3 donut.py
```
靜靜觀賞這美麗的甜甜圈吧
10 CLS 
12 DIM G(5)
13 DIM H(5)
15 FAST 
16 LET R=0 
17 LET Q$=""
18 LET F=1 
20 FOR I=0 TO 63 
30 PLOT I,0 
40 PLOT I,40 
50 NEXT I
60 FOR I=0 TO 40 
70 PLOT 0 ,I
80 PLOT 63 ,I
90 NEXT I
100 FOR I=1 TO 5 
110 LET X=RND*30 +1 
120 LET Y=RND*19 +2 
130 PRINT AT Y,X; ".";
132 LET G(I)=X*2 
134 LET H(I)=(21-Y)*2 
140 NEXT I
150 SLOW 
155 LET S=0
160 LET X=32
170 LET Y=10
175 LET V=1
180 LET K$=INKEY$
190 IF K$="O" THEN LET R=R+1 
200 IF K$="P" THEN LET R=R-1 
210 IF R<0 THEN LET R=3 
220 IF R>3 THEN LET R=0 
222 LET M=X
224 LET N=Y
230 IF R=0 THEN LET M=X+V
240 IF R=1 THEN LET N=Y+V
250 IF R=2 THEN LET M=X-V
260 IF R=3 THEN LET N=Y-V
270 IF M<0 THEN GOTO 900 
280 IF N<0 THEN GOTO 900 
290 IF M>62 THEN GOTO 900 
300 IF N>40 THEN GOTO 900 
320 LET X=M
330 LET Y=N
340 LET I=1 
350 IF G(I)-X<= 2 AND G(I)-X>= -2 AND H(I)-Y<= 2 AND H(I)-Y>= -2 THEN GOTO 500 
360 LET I=I+1 
370 IF I<6 THEN GOTO 350 
380 LET U=LEN Q$/2 
390 LET Q$=Q$+CHR$ X+CHR$ Y
400 IF (LEN Q$/2 )<= FTHEN GOTO 430 
410 UNPLOT CODE Q$(1 ),CODE Q$(2 )
420 LET Q$=Q$(3 TO )
430 LET W=1 
435 IF W>= LEN Q$-2 THEN GOTO 470 
440 IF Q$(W)=CHR$ X AND Q$(W+1)=CHR$ Y THEN GOTO 900 
450 LET W=W+2 
460 GOTO 435 
470 REM TESTE
490 PLOT X,Y
499 GOTO 180 
500 PRINT AT 21 -(H(I)/2 ),(G(I)/2 );" ";
505 PLOT X,Y
507 LET G(I)=RND*30+1 
510 LET H(I)=RND*19+2 
515 PRINT AT H(I),G(I);".";
516 LET G(I)=G(I)*2 
518 LET H(I)=(21-H(I))*2 
520 LET S=S+10 
525 IF F<= 99 THEN LET F=F+2 
530 PRINT AT 0 ,2 ;"SCORE:";S;
540 PRINT AT 22-(H(I)/2),(G(I)/2);" ";
545 PLOT X,Y
560 GOTO 380 
900 PRINT "FIM";
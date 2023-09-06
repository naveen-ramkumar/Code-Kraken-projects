#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>
#include <string.h>
struct coord
{
    char x;
    int y;
    int safe;
};
void grid(struct coord xy[][20],int shipno,int slen[])
{
    int run,run2,count,count1;
    printf("     ");
    for(run=1;run<=10;run++) printf("%c ",64+run);
    printf("\n     ");
    for(run=0;run<=9;run++) printf("- ");
    printf("\n");
    for(run=1;run<=10;run++)
    {
        for(run2=-1;run2<=10;run2++)
        {
            int isfound=0;
            if(run==10 && run2==-1) printf("%d ",run);
            if(run!=10 && run2==-1) printf("%d  ",run);
            if(run2==0) printf("| ");
            if(run2>=1)
            {
                for(count=0;count<shipno;count++)
                {
                    for(count1=0;count1<slen[count];count1++)
                    {
                        if(xy[count][count1].x-64==run2 && xy[count][count1].y==run)
                        {
                            if(xy[count][count1].safe==1) isfound=1;
                            else if(xy[count][count1].safe==0) isfound=-1;
                            break;
                        }
                    }
                    if(isfound==1 || isfound==-1) break;
                }
                if(isfound==1) printf("S ");
                else if(isfound==-1) printf("X ");
                else printf("* ");
            }
        }
        printf("\n");
    }
}
char linecheck(struct coord arr[],int l)
{
    int run,samex=1,samey=1;
    for(run=0;run<l-1;run++)
    {
        samex=samex&&(arr[run].x==arr[run+1].x);
        samey=samey&&(arr[run].y==arr[run+1].y);
    }
    if(samex==1) return 'v';
    else if(samey==1) return 'h';
    else return 'e';
}
void sort(struct coord arr[],int l)
{
    int run,run2,temp;
    if(linecheck(arr,l)=='v')
    {
        for(run=0;run<l-1;run++)
        {
            for(run2=run;run2<l;run2++)
            {
                if(arr[run].y>arr[run2].y)
                {
                    temp=arr[run].y;
                    arr[run].y=arr[run2].y;
                    arr[run2].y=temp;
                }
            }
        }
    }
    if(linecheck(arr,l)=='h')
    {
        for(run=0;run<l-1;run++)
        {
            for(run2=run;run2<l;run2++)
            {
                if(arr[run].x>arr[run2].x)
                {
                    temp=arr[run].x;
                    arr[run].x=arr[run2].x;
                    arr[run2].x=temp;
                }
            }
        }

    }
}
int issunk(struct coord arr[],int l);
int shoot(struct coord arr[][20],char guessx,int guessy,int ind[],int slen[])
{
    int run,run2,hit=0;
    for(run=0;run<5;run++)
    {
        for(run2=0;run2<slen[run];run2++)
        {
            if(arr[run][run2].x==guessx && arr[run][run2].y==guessy)
            {
                if(arr[run][run2].safe==1)
                {
                    arr[run][run2].safe=0;
                    hit=1;
                }
                else
                {
                    if(issunk(arr[run],slen[run])==1) hit=-2;
                    else hit=-1;
                }
                ind[0]=run;ind[1]=run2;
                break;

            }
        }
        if(hit==1 || hit==-1 || hit==-2) break;
    }
    return(hit);
}
int issunk(struct coord arr[],int l)
{
    int hits=0,run;
    for(run=0;run<l;run++)
    {
        if(arr[run].safe==0) hits+=1;
    }
    if(hits==l) return(1);
    else return(0);
}
main()
{
    int run,run2,c1,c2,c3,c4;
    char sname[5][20]={"CARRIER","BATTLESHIP","CRUISER","SUBMARINE","DESTROYER"};
    int slen[5]={5,4,3,3,2};
    struct coord pos[7][20]={{}};
    grid(pos,0,slen);
    for(run=0;run<=4;run++)
    {
        printf("\n.......................................................................................");
        printf("\n\nENTER THE COORDINATES OF %d SQUARE %s SHIP EX:A4,C10 ",slen[run],sname[run]);
        while(1)
        {
            fflush(stdin);
            for(run2=0;run2<slen[run];run2++)
            {
                scanf(" %1c%d",&pos[run][run2].x,&pos[run][run2].y);
                pos[run][run2].safe=1;
                if(pos[run][run2].x>=97 && pos[run][run2].x<=106) pos[run][run2].x-=32;
            }
            int isvalid=1;
            for(c1=0;c1<slen[run];c1++)
            {
                if((pos[run][c1].x<65 || pos[run][c1].x>74) || (pos[run][c1].y<1 || pos[run][c1].y>10))
                {
                    isvalid=0;break;
                }
            }
            if(isvalid==0) printf("\nPLEASE ENTER COORDINATES ONLY BETWEEN A-J FOR X AND 1-10 FOR Y\n");
            else
            {
                if(linecheck(pos[run],slen[run])=='e') printf("\nTHE SHIP COORDINATES HAVE TO FALL IN A STRAIGHT LINE. PLEASE ENTER AGAIN\n");
                else
                {
                    sort(pos[run],slen[run]);
                    int iscont=1;
                    if(linecheck(pos[run],slen[run])=='v')
                    {
                        for(c1=0;c1<slen[run]-1;c1++)
                        {
                            if((pos[run][c1+1].y)!=(pos[run][c1].y+1))
                            {
                                iscont=0;break;
                            }
                        }
                    }
                    if(linecheck(pos[run],slen[run])=='h')
                    {
                        for(c1=0;c1<slen[run]-1;c1++)
                        {
                            if((pos[run][c1+1].x)!=(pos[run][c1].x+1))
                            {
                                iscont=0;break;
                            }
                        }
                    }
                    if(iscont==0) printf("\nTHE SHIP COORDINATES SHOULD BE DISCRETE AND CONSECUTIVE. PLEASE ENTER AGAIN\n");
                    else
                    {
                        int isintersect=0;
                        for(c1=0;c1<slen[run];c1++)
                        {
                            for(c2=0;c2<run;c2++)
                            {
                                for(c3=0;c3<slen[c2];c3++)
                                {
                                    if((pos[run][c1].x==pos[c2][c3].x && pos[run][c1].y==pos[c2][c3].y) && c2!=run)
                                    {
                                        isintersect=1;break;
                                    }
                                }
                                if(isintersect==1) break;
                            }
                            if(isintersect==1) break;
                        }
                        if(isintersect==1) printf("\nTWO SHIPS ARE INTERSECTING OR OVERLAPPING. PLEASE ENTER AGAIN\n");
                        else break;
                    }
                }
            }
            printf("Enter the coordinates of %d square %s ship Ex:A4,C10 ",slen[run],sname[run]);
        }
        grid(pos,run+1,slen);
    }
    int score=0;
    while(1)
    {
        char input[5];
        int index[3],hit,sunk=0;
        printf("\n.........................................................................................");
        printf("\nWHEN YOU ARE READY, PRESS ENTER FOR THE COMPUTER TO SHOOT. TO END THE GAME, TYPE END\n");
        fflush(stdin);
        fgets(input,5,stdin);
        if(strcmp(input,"end\n")==0)
        {
            printf("\n\nTHANK YOU FOR PLAYING THE GAME. YOUR FINAL SCORE IS %d",score);
            break;
        }
        printf("\n\nCOMPUTER IS PLAYING.......");
        srand(time(0));
        char guessx=(rand()%10)+65;
        sleep(2);
        srand(time(0));
        int guessy=(rand()%10)+1;
        printf("\nCOMPUTER CHOOSES TO HIT AT %c%d",guessx,guessy);
        hit=shoot(pos,guessx,guessy,index,slen);
        if(hit==0)
        {
            printf("\n\nHOORAY! NONE OF YOUR SHIPS HAVE BEEN HIT. YOU GAIN 2 POINTS\n\n");
            score+=2;
        }
        else if(hit==-1) printf("\n\nTHIS PART OF YOUR %s SHIP IS ALREADY DAMAGED. NO POINTS\n\n",sname[index[0]]);
        else if(hit==-2) printf("\n\nTHIS IS PART OF YOUR %s SHIP, WHICH HAS ALREADY SUNK. NO POINTS\n\n",sname[index[0]]);
        else
        {
            printf("\n\nYOUR %s HAS BEEN HIT! YOU LOSE 5 POINTS\n\n",sname[index[0]]);
            score-=5;
            if(issunk(pos[index[0]],slen[index[0]])==1)
            {
                printf("\nYOUR %s HAS SUNK. YOU LOSE ADDITIONAL 5 POINTS\n\n",sname[index[0]]);
                score-=5;
            }
        }
        grid(pos,5,slen);
        for(run=0;run<5;run++)
        {
            if(issunk(pos[run],slen[run])==1) sunk+=1;
        }
        if(sunk==5)
        {
            printf("\n\nGAME OVER. ALL YOUR SHIPS HAVE SUNK. YOUR FINAL SCORE IS %d\n",score);
            break;
        }
        printf("\n\n\nYOUR SCORE IS %d\n\n",score);
        while(kbhit()) getch();
    }
}


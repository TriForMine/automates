motif (bla)+
    // déclarations en C
    int i = 0;
%%
{motif} i++;
\n ;
. ;
%%
int main (int argc, char *argv[]) {
    yylex();
    printf("%d\n", i);
    return 0;
}

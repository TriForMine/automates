    // déclarations en C
    int voyelles = 0;
    int min = 0;
    int maj = 0;
    int total = 0;
%%
[a|e|i|o|u|y] ++voyelles; REJECT;
[a-z] ++min; REJECT;
[A-Z] ++maj; REJECT;
[a-zA-Z] ++total;
\n ;
. ;
%%
int main (int argc, char *argv[]) {
    yylex();
    printf("Voyelles: %d\nMinuscules: %d\nMajuscules: %d\nTotal: %d\n", voyelles, min, maj, total);
    return 0;
}

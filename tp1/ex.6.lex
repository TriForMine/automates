    // déclarations en C
    int total = 0;
    int last_length = 0;
%%
[0-9]+  total += atoi(yytext);
[^(\ |\n)]+  if (strlen(yytext) > last_length) {last_length = strlen(yytext); printf("%s", yytext);};
. ;
%%
int main (int argc, char *argv[]) {
    yylex();
    printf("Somme: %d\n", total);
    return 0;
}

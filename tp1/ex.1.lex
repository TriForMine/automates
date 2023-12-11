mot     [A-Za-z]+
/*  déclarations en C (ligne débutant avec un espace au moins)  */
     #include <strings.h>
     char *motif = NULL;
     int i = 0;
%%
{mot}   if (strcmp(motif, yytext) == 0) i++;
\n       ;
.        ;
%%
int main (int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "usage: %s [a-zA-Z]+\n", argv[0]);
    exit(2);
  }
  motif = argv[1];
  yylex();
  printf("%d\n", i);
  return 0;
}

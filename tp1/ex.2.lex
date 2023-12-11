motif (to\ )?(am|are|is|was|were)+
%%
{motif}  printf("%s: To be !\n", yytext);
\n       ;
(.)+     printf("%s: Sorry, I can't regonize ...\n", yytext);
%%
int main (int argc, char *argv[]) {
  yylex();
  return 0;
}
